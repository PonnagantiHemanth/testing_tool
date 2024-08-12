#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.common.fullkeycustomization
:brief: HID++ 2.0 ``FullKeyCustomization`` command interface definition
:author: Masan Xu <mxu11@logitech.com>
:date: 2023/03/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from enum import IntEnum
from enum import unique

from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FullKeyCustomization(HidppMessage):
    """
    This feature allows the host software to control & monitor full key customization (FKC).
    """
    FEATURE_ID = 0x1B05
    MAX_FUNCTION_INDEX_V0 = 3
    MAX_FUNCTION_INDEX_V1 = 4
    TOGGLE_HOTKEYS_CNT = 8  # Count of FKC toggle hotkeys

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__

    @unique
    class TriggerBitField(IntEnum):
        """
        This bitmap contains the trigger modifier keys. All the modifiers have to be pressed to trigger. These
        correspond to logical modifiers and include all the standard modifiers (leftCtrl to rightGui).

        The bitmap also contains the SingleKeyMatch flag, which dictates the type of trigger matching to apply.

        https://docs.google.com/spreadsheets/d/1-EmO2L0k_nDq4fASdaM3T6Ktn7V5P36NULwHgRpbVVg/view#gid=1017032508&range=A21
        """
        SINGLE_KEY_MATCH = 0x8000
        R_GUI = 0x0080
        R_ALT = 0x0040
        R_SHIFT = 0x0020
        R_CTRL = 0x0010
        L_GUI = 0x0008
        L_ALT = 0x0004
        L_SHIFT = 0x0002
        L_CTRL = 0x0001
    # end class TriggerBitField

    @unique
    class ActionBitField(IntEnum):
        """
        This bitmap contains the target action modifier keys.
        These correspond to standard HID modifiers (leftCtrl to rightGui)

        This bitmap also contains the bit "NotifySW":
        Meaning:
        0: Do not notify software
        1: Notify software for all presses and releases of this trigger key.

        UpdateModifiers:
        0: No change to (FKC internal) logical modifier states
        1: The FKC logical modifiers are updated based on the values in the Action bitmap (using OR-type logic).
           Thus they affect future trigger matching

        https://docs.google.com/spreadsheets/d/1-EmO2L0k_nDq4fASdaM3T6Ktn7V5P36NULwHgRpbVVg/view#gid=1017032508&range=A41
        """
        NOTIFY_SW = 0x8000
        UPDATE_MODIFIERS = 0x4000
        R_GUI = 0x0080
        R_ALT = 0x0040
        R_SHIFT = 0x0020
        R_CTRL = 0x0010
        L_GUI = 0x0008
        L_ALT = 0x0004
        L_SHIFT = 0x0002
        L_CTRL = 0x0001
    # end class ActionBitField

    @unique
    class PowerOnFKCRequest(IntEnum):
        """
        Inform the device if the poweron_fkc_enable value should be set or not
        """
        GET = 0
        SET = 1
    # end class PowerOnFKCRequest

    @unique
    class FKCStateRequest(IntEnum):
        """
        Inform the device if the fkc_enabled value should be set or not
        """
        GET = 0
        SET = 1
    # end class FKCStateRequest

    @unique
    class ToggleKeysRequest(IntEnum):
        """
        Inform the device if the toggle_keys_enabled value should be set or not
        """
        GET = 0
        SET = 1
    # end class ToggleKeysRequest

    @unique
    class SWConfigurationCookieRequest(IntEnum):
        """
        Inform the device if the sw_configuration_cookie value should be set or not
        """
        GET = 0
        SET = 1
    # end class SWConfigurationCookieRequest

    @unique
    class FKCStatus(IntEnum):
        """
        The enabled state of current of FKC status
        """
        DISABLE = 0
        ENABLE = 1
    # end class FKCStatus

    @unique
    class PowerOnFKCStatus(IntEnum):
        """
        The enabled state of current power-on FKC status
        """
        DISABLE = 0
        ENABLE = 1
    # end class PowerOnFKCStatus

    @unique
    class ToggleKeyStatus(IntEnum):
        """
        The enabled state of current toggle keys
        """
        DISABLE = 0
        ENABLE = 1
    # end class ToggleKeyStatus

    @unique
    class EnableDisableStatus(IntEnum):
        """
        Indicates if the enabling/disabling of FKC failed or not
        """
        SUCCESS = 0
        FAIL = 1
    # end class EnableDisableStatus

    @unique
    class KeyState(IntEnum):
        """
        Indicates the key is released or pressed for 0x1b05 trigger list/bitmap event
        """
        RELEASED = 0
        PRESSED = 1
    # end class KeyState

    class SetPowerOnFkcState(BitFieldContainerMixin):
        """
        Define ``SetPowerOnFkcState`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      7
        Set Power On Fkc Enable       1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            SET_POWER_ON_FKC_ENABLE = RESERVED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x7
            SET_POWER_ON_FKC_ENABLE = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            SET_POWER_ON_FKC_ENABLE = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.SET_POWER_ON_FKC_ENABLE, length=LEN.SET_POWER_ON_FKC_ENABLE,
                     title="SetPowerOnFkcEnable", name="set_power_on_fkc_enable",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.SET_POWER_ON_FKC_ENABLE) - 1),),
                     default_value=DEFAULT.SET_POWER_ON_FKC_ENABLE),
        )
    # end class SetPowerOnFkcState

    class PowerOnFkcState(BitFieldContainerMixin):
        """
        Define ``PowerOnFkcState`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      7
        Power On Fkc Enable           1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            POWER_ON_FKC_ENABLE = RESERVED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x7
            POWER_ON_FKC_ENABLE = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            POWER_ON_FKC_ENABLE = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.POWER_ON_FKC_ENABLE, length=LEN.POWER_ON_FKC_ENABLE,
                     title="PowerOnFkcEnable", name="power_on_fkc_enable",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.POWER_ON_FKC_ENABLE) - 1),),
                     default_value=DEFAULT.POWER_ON_FKC_ENABLE),
        )
    # end class PowerOnFkcState

    class SetGetFkcState(BitFieldContainerMixin):
        """
        Define ``SetGetFkcState`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      6
        Set Toggle Keys Enabled       1
        Set Fkc Enabled               1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            SET_TOGGLE_KEYS_ENABLED = RESERVED - 1
            SET_FKC_ENABLED = SET_TOGGLE_KEYS_ENABLED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x6
            SET_TOGGLE_KEYS_ENABLED = 0x1
            SET_FKC_ENABLED = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            SET_TOGGLE_KEYS_ENABLED = 0x0
            SET_FKC_ENABLED = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.SET_TOGGLE_KEYS_ENABLED, length=LEN.SET_TOGGLE_KEYS_ENABLED,
                     title="SetToggleKeysEnabled", name="set_toggle_keys_enabled",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.SET_TOGGLE_KEYS_ENABLED) - 1),),
                     default_value=DEFAULT.SET_TOGGLE_KEYS_ENABLED),
            BitField(fid=FID.SET_FKC_ENABLED, length=LEN.SET_FKC_ENABLED,
                     title="SetFkcEnabled", name="set_fkc_enabled",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.SET_FKC_ENABLED) - 1),),
                     default_value=DEFAULT.SET_FKC_ENABLED),
        )
    # end class SetGetFkcState

    class FkcState(BitFieldContainerMixin):
        """
        Define ``FkcState`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      7
        Fkc Enabled                   1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            FKC_ENABLED = RESERVED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x7
            FKC_ENABLED = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            FKC_ENABLED = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.FKC_ENABLED, length=LEN.FKC_ENABLED,
                     title="FkcEnabled", name="fkc_enabled",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_ENABLED) - 1),),
                     default_value=DEFAULT.FKC_ENABLED),
        )
    # end class FkcState

    class ToggleKeysState(BitFieldContainerMixin):
        """
        Define ``ToggleKeysState`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Toggle Key 7 Enabled          1
        Toggle Key 6 Enabled          1
        Toggle Key 5 Enabled          1
        Toggle Key 4 Enabled          1
        Toggle Key 3 Enabled          1
        Toggle Key 2 Enabled          1
        Toggle Key 1 Enabled          1
        Toggle Key 0 Enabled          1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            TOGGLE_KEY_7_ENABLED = 0xFF
            TOGGLE_KEY_6_ENABLED = TOGGLE_KEY_7_ENABLED - 1
            TOGGLE_KEY_5_ENABLED = TOGGLE_KEY_6_ENABLED - 1
            TOGGLE_KEY_4_ENABLED = TOGGLE_KEY_5_ENABLED - 1
            TOGGLE_KEY_3_ENABLED = TOGGLE_KEY_4_ENABLED - 1
            TOGGLE_KEY_2_ENABLED = TOGGLE_KEY_3_ENABLED - 1
            TOGGLE_KEY_1_ENABLED = TOGGLE_KEY_2_ENABLED - 1
            TOGGLE_KEY_0_ENABLED = TOGGLE_KEY_1_ENABLED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            TOGGLE_KEY_7_ENABLED = 0x1
            TOGGLE_KEY_6_ENABLED = 0x1
            TOGGLE_KEY_5_ENABLED = 0x1
            TOGGLE_KEY_4_ENABLED = 0x1
            TOGGLE_KEY_3_ENABLED = 0x1
            TOGGLE_KEY_2_ENABLED = 0x1
            TOGGLE_KEY_1_ENABLED = 0x1
            TOGGLE_KEY_0_ENABLED = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            TOGGLE_KEY_7_ENABLED = 0x0
            TOGGLE_KEY_6_ENABLED = 0x0
            TOGGLE_KEY_5_ENABLED = 0x0
            TOGGLE_KEY_4_ENABLED = 0x0
            TOGGLE_KEY_3_ENABLED = 0x0
            TOGGLE_KEY_2_ENABLED = 0x0
            TOGGLE_KEY_1_ENABLED = 0x0
            TOGGLE_KEY_0_ENABLED = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.TOGGLE_KEY_7_ENABLED, length=LEN.TOGGLE_KEY_7_ENABLED,
                     title="ToggleKey7Enabled", name="toggle_key_7_enabled",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.TOGGLE_KEY_7_ENABLED) - 1),),
                     default_value=DEFAULT.TOGGLE_KEY_7_ENABLED),
            BitField(fid=FID.TOGGLE_KEY_6_ENABLED, length=LEN.TOGGLE_KEY_6_ENABLED,
                     title="ToggleKey6Enabled", name="toggle_key_6_enabled",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.TOGGLE_KEY_6_ENABLED) - 1),),
                     default_value=DEFAULT.TOGGLE_KEY_6_ENABLED),
            BitField(fid=FID.TOGGLE_KEY_5_ENABLED, length=LEN.TOGGLE_KEY_5_ENABLED,
                     title="ToggleKey5Enabled", name="toggle_key_5_enabled",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.TOGGLE_KEY_5_ENABLED) - 1),),
                     default_value=DEFAULT.TOGGLE_KEY_5_ENABLED),
            BitField(fid=FID.TOGGLE_KEY_4_ENABLED, length=LEN.TOGGLE_KEY_4_ENABLED,
                     title="ToggleKey4Enabled", name="toggle_key_4_enabled",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.TOGGLE_KEY_4_ENABLED) - 1),),
                     default_value=DEFAULT.TOGGLE_KEY_4_ENABLED),
            BitField(fid=FID.TOGGLE_KEY_3_ENABLED, length=LEN.TOGGLE_KEY_3_ENABLED,
                     title="ToggleKey3Enabled", name="toggle_key_3_enabled",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.TOGGLE_KEY_3_ENABLED) - 1),),
                     default_value=DEFAULT.TOGGLE_KEY_3_ENABLED),
            BitField(fid=FID.TOGGLE_KEY_2_ENABLED, length=LEN.TOGGLE_KEY_2_ENABLED,
                     title="ToggleKey2Enabled", name="toggle_key_2_enabled",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.TOGGLE_KEY_2_ENABLED) - 1),),
                     default_value=DEFAULT.TOGGLE_KEY_2_ENABLED),
            BitField(fid=FID.TOGGLE_KEY_1_ENABLED, length=LEN.TOGGLE_KEY_1_ENABLED,
                     title="ToggleKey1Enabled", name="toggle_key_1_enabled",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.TOGGLE_KEY_1_ENABLED) - 1),),
                     default_value=DEFAULT.TOGGLE_KEY_1_ENABLED),
            BitField(fid=FID.TOGGLE_KEY_0_ENABLED, length=LEN.TOGGLE_KEY_0_ENABLED,
                     title="ToggleKey0Enabled", name="toggle_key_0_enabled",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.TOGGLE_KEY_0_ENABLED) - 1),),
                     default_value=DEFAULT.TOGGLE_KEY_0_ENABLED),
        )
    # end class ToggleKeysState

    class KeyTriggerBitmap(BitFieldContainerMixin):
        """
        Define ``KeyTriggerBitmap`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Fkc Idx 7                     1
        Fkc Idx 6                     1
        Fkc Idx 5                     1
        Fkc Idx 4                     1
        Fkc Idx 3                     1
        Fkc Idx 2                     1
        Fkc Idx 1                     1
        Fkc Idx 0                     1
        Fkc Idx 15                    1
        Fkc Idx 14                    1
        Fkc Idx 13                    1
        Fkc Idx 12                    1
        Fkc Idx 11                    1
        Fkc Idx 10                    1
        Fkc Idx 9                     1
        Fkc Idx 8                     1
        Fkc Idx 23                    1
        Fkc Idx 22                    1
        Fkc Idx 21                    1
        Fkc Idx 20                    1
        Fkc Idx 19                    1
        Fkc Idx 18                    1
        Fkc Idx 17                    1
        Fkc Idx 16                    1
        Fkc Idx 31                    1
        Fkc Idx 30                    1
        Fkc Idx 29                    1
        Fkc Idx 28                    1
        Fkc Idx 27                    1
        Fkc Idx 26                    1
        Fkc Idx 25                    1
        Fkc Idx 24                    1
        Fkc Idx 39                    1
        Fkc Idx 38                    1
        Fkc Idx 37                    1
        Fkc Idx 36                    1
        Fkc Idx 35                    1
        Fkc Idx 34                    1
        Fkc Idx 33                    1
        Fkc Idx 32                    1
        Fkc Idx 47                    1
        Fkc Idx 46                    1
        Fkc Idx 45                    1
        Fkc Idx 44                    1
        Fkc Idx 43                    1
        Fkc Idx 42                    1
        Fkc Idx 41                    1
        Fkc Idx 40                    1
        Fkc Idx 55                    1
        Fkc Idx 54                    1
        Fkc Idx 53                    1
        Fkc Idx 52                    1
        Fkc Idx 51                    1
        Fkc Idx 50                    1
        Fkc Idx 49                    1
        Fkc Idx 48                    1
        Fkc Idx 63                    1
        Fkc Idx 62                    1
        Fkc Idx 61                    1
        Fkc Idx 60                    1
        Fkc Idx 59                    1
        Fkc Idx 58                    1
        Fkc Idx 57                    1
        Fkc Idx 56                    1
        Fkc Idx 71                    1
        Fkc Idx 70                    1
        Fkc Idx 69                    1
        Fkc Idx 68                    1
        Fkc Idx 67                    1
        Fkc Idx 66                    1
        Fkc Idx 65                    1
        Fkc Idx 64                    1
        Fkc Idx 79                    1
        Fkc Idx 78                    1
        Fkc Idx 77                    1
        Fkc Idx 76                    1
        Fkc Idx 75                    1
        Fkc Idx 74                    1
        Fkc Idx 73                    1
        Fkc Idx 72                    1
        Fkc Idx 87                    1
        Fkc Idx 86                    1
        Fkc Idx 85                    1
        Fkc Idx 84                    1
        Fkc Idx 83                    1
        Fkc Idx 82                    1
        Fkc Idx 81                    1
        Fkc Idx 80                    1
        Fkc Idx 95                    1
        Fkc Idx 94                    1
        Fkc Idx 93                    1
        Fkc Idx 92                    1
        Fkc Idx 91                    1
        Fkc Idx 90                    1
        Fkc Idx 89                    1
        Fkc Idx 88                    1
        Fkc Idx 103                   1
        Fkc Idx 102                   1
        Fkc Idx 101                   1
        Fkc Idx 100                   1
        Fkc Idx 99                    1
        Fkc Idx 98                    1
        Fkc Idx 97                    1
        Fkc Idx 96                    1
        Fkc Idx 111                   1
        Fkc Idx 110                   1
        Fkc Idx 109                   1
        Fkc Idx 108                   1
        Fkc Idx 107                   1
        Fkc Idx 106                   1
        Fkc Idx 105                   1
        Fkc Idx 104                   1
        Fkc Idx 119                   1
        Fkc Idx 118                   1
        Fkc Idx 117                   1
        Fkc Idx 116                   1
        Fkc Idx 115                   1
        Fkc Idx 114                   1
        Fkc Idx 113                   1
        Fkc Idx 112                   1
        Fkc Idx 127                   1
        Fkc Idx 126                   1
        Fkc Idx 125                   1
        Fkc Idx 124                   1
        Fkc Idx 123                   1
        Fkc Idx 122                   1
        Fkc Idx 121                   1
        Fkc Idx 120                   1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            FKC_IDX_7 = 0xFF
            FKC_IDX_6 = FKC_IDX_7 - 1
            FKC_IDX_5 = FKC_IDX_6 - 1
            FKC_IDX_4 = FKC_IDX_5 - 1
            FKC_IDX_3 = FKC_IDX_4 - 1
            FKC_IDX_2 = FKC_IDX_3 - 1
            FKC_IDX_1 = FKC_IDX_2 - 1
            FKC_IDX_0 = FKC_IDX_1 - 1
            FKC_IDX_15 = FKC_IDX_0 - 1
            FKC_IDX_14 = FKC_IDX_15 - 1
            FKC_IDX_13 = FKC_IDX_14 - 1
            FKC_IDX_12 = FKC_IDX_13 - 1
            FKC_IDX_11 = FKC_IDX_12 - 1
            FKC_IDX_10 = FKC_IDX_11 - 1
            FKC_IDX_9 = FKC_IDX_10 - 1
            FKC_IDX_8 = FKC_IDX_9 - 1
            FKC_IDX_23 = FKC_IDX_8 - 1
            FKC_IDX_22 = FKC_IDX_23 - 1
            FKC_IDX_21 = FKC_IDX_22 - 1
            FKC_IDX_20 = FKC_IDX_21 - 1
            FKC_IDX_19 = FKC_IDX_20 - 1
            FKC_IDX_18 = FKC_IDX_19 - 1
            FKC_IDX_17 = FKC_IDX_18 - 1
            FKC_IDX_16 = FKC_IDX_17 - 1
            FKC_IDX_31 = FKC_IDX_16 - 1
            FKC_IDX_30 = FKC_IDX_31 - 1
            FKC_IDX_29 = FKC_IDX_30 - 1
            FKC_IDX_28 = FKC_IDX_29 - 1
            FKC_IDX_27 = FKC_IDX_28 - 1
            FKC_IDX_26 = FKC_IDX_27 - 1
            FKC_IDX_25 = FKC_IDX_26 - 1
            FKC_IDX_24 = FKC_IDX_25 - 1
            FKC_IDX_39 = FKC_IDX_24 - 1
            FKC_IDX_38 = FKC_IDX_39 - 1
            FKC_IDX_37 = FKC_IDX_38 - 1
            FKC_IDX_36 = FKC_IDX_37 - 1
            FKC_IDX_35 = FKC_IDX_36 - 1
            FKC_IDX_34 = FKC_IDX_35 - 1
            FKC_IDX_33 = FKC_IDX_34 - 1
            FKC_IDX_32 = FKC_IDX_33 - 1
            FKC_IDX_47 = FKC_IDX_32 - 1
            FKC_IDX_46 = FKC_IDX_47 - 1
            FKC_IDX_45 = FKC_IDX_46 - 1
            FKC_IDX_44 = FKC_IDX_45 - 1
            FKC_IDX_43 = FKC_IDX_44 - 1
            FKC_IDX_42 = FKC_IDX_43 - 1
            FKC_IDX_41 = FKC_IDX_42 - 1
            FKC_IDX_40 = FKC_IDX_41 - 1
            FKC_IDX_55 = FKC_IDX_40 - 1
            FKC_IDX_54 = FKC_IDX_55 - 1
            FKC_IDX_53 = FKC_IDX_54 - 1
            FKC_IDX_52 = FKC_IDX_53 - 1
            FKC_IDX_51 = FKC_IDX_52 - 1
            FKC_IDX_50 = FKC_IDX_51 - 1
            FKC_IDX_49 = FKC_IDX_50 - 1
            FKC_IDX_48 = FKC_IDX_49 - 1
            FKC_IDX_63 = FKC_IDX_48 - 1
            FKC_IDX_62 = FKC_IDX_63 - 1
            FKC_IDX_61 = FKC_IDX_62 - 1
            FKC_IDX_60 = FKC_IDX_61 - 1
            FKC_IDX_59 = FKC_IDX_60 - 1
            FKC_IDX_58 = FKC_IDX_59 - 1
            FKC_IDX_57 = FKC_IDX_58 - 1
            FKC_IDX_56 = FKC_IDX_57 - 1
            FKC_IDX_71 = FKC_IDX_56 - 1
            FKC_IDX_70 = FKC_IDX_71 - 1
            FKC_IDX_69 = FKC_IDX_70 - 1
            FKC_IDX_68 = FKC_IDX_69 - 1
            FKC_IDX_67 = FKC_IDX_68 - 1
            FKC_IDX_66 = FKC_IDX_67 - 1
            FKC_IDX_65 = FKC_IDX_66 - 1
            FKC_IDX_64 = FKC_IDX_65 - 1
            FKC_IDX_79 = FKC_IDX_64 - 1
            FKC_IDX_78 = FKC_IDX_79 - 1
            FKC_IDX_77 = FKC_IDX_78 - 1
            FKC_IDX_76 = FKC_IDX_77 - 1
            FKC_IDX_75 = FKC_IDX_76 - 1
            FKC_IDX_74 = FKC_IDX_75 - 1
            FKC_IDX_73 = FKC_IDX_74 - 1
            FKC_IDX_72 = FKC_IDX_73 - 1
            FKC_IDX_87 = FKC_IDX_72 - 1
            FKC_IDX_86 = FKC_IDX_87 - 1
            FKC_IDX_85 = FKC_IDX_86 - 1
            FKC_IDX_84 = FKC_IDX_85 - 1
            FKC_IDX_83 = FKC_IDX_84 - 1
            FKC_IDX_82 = FKC_IDX_83 - 1
            FKC_IDX_81 = FKC_IDX_82 - 1
            FKC_IDX_80 = FKC_IDX_81 - 1
            FKC_IDX_95 = FKC_IDX_80 - 1
            FKC_IDX_94 = FKC_IDX_95 - 1
            FKC_IDX_93 = FKC_IDX_94 - 1
            FKC_IDX_92 = FKC_IDX_93 - 1
            FKC_IDX_91 = FKC_IDX_92 - 1
            FKC_IDX_90 = FKC_IDX_91 - 1
            FKC_IDX_89 = FKC_IDX_90 - 1
            FKC_IDX_88 = FKC_IDX_89 - 1
            FKC_IDX_103 = FKC_IDX_88 - 1
            FKC_IDX_102 = FKC_IDX_103 - 1
            FKC_IDX_101 = FKC_IDX_102 - 1
            FKC_IDX_100 = FKC_IDX_101 - 1
            FKC_IDX_99 = FKC_IDX_100 - 1
            FKC_IDX_98 = FKC_IDX_99 - 1
            FKC_IDX_97 = FKC_IDX_98 - 1
            FKC_IDX_96 = FKC_IDX_97 - 1
            FKC_IDX_111 = FKC_IDX_96 - 1
            FKC_IDX_110 = FKC_IDX_111 - 1
            FKC_IDX_109 = FKC_IDX_110 - 1
            FKC_IDX_108 = FKC_IDX_109 - 1
            FKC_IDX_107 = FKC_IDX_108 - 1
            FKC_IDX_106 = FKC_IDX_107 - 1
            FKC_IDX_105 = FKC_IDX_106 - 1
            FKC_IDX_104 = FKC_IDX_105 - 1
            FKC_IDX_119 = FKC_IDX_104 - 1
            FKC_IDX_118 = FKC_IDX_119 - 1
            FKC_IDX_117 = FKC_IDX_118 - 1
            FKC_IDX_116 = FKC_IDX_117 - 1
            FKC_IDX_115 = FKC_IDX_116 - 1
            FKC_IDX_114 = FKC_IDX_115 - 1
            FKC_IDX_113 = FKC_IDX_114 - 1
            FKC_IDX_112 = FKC_IDX_113 - 1
            FKC_IDX_127 = FKC_IDX_112 - 1
            FKC_IDX_126 = FKC_IDX_127 - 1
            FKC_IDX_125 = FKC_IDX_126 - 1
            FKC_IDX_124 = FKC_IDX_125 - 1
            FKC_IDX_123 = FKC_IDX_124 - 1
            FKC_IDX_122 = FKC_IDX_123 - 1
            FKC_IDX_121 = FKC_IDX_122 - 1
            FKC_IDX_120 = FKC_IDX_121 - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            FKC_IDX_7 = 0x1
            FKC_IDX_6 = 0x1
            FKC_IDX_5 = 0x1
            FKC_IDX_4 = 0x1
            FKC_IDX_3 = 0x1
            FKC_IDX_2 = 0x1
            FKC_IDX_1 = 0x1
            FKC_IDX_0 = 0x1
            FKC_IDX_15 = 0x1
            FKC_IDX_14 = 0x1
            FKC_IDX_13 = 0x1
            FKC_IDX_12 = 0x1
            FKC_IDX_11 = 0x1
            FKC_IDX_10 = 0x1
            FKC_IDX_9 = 0x1
            FKC_IDX_8 = 0x1
            FKC_IDX_23 = 0x1
            FKC_IDX_22 = 0x1
            FKC_IDX_21 = 0x1
            FKC_IDX_20 = 0x1
            FKC_IDX_19 = 0x1
            FKC_IDX_18 = 0x1
            FKC_IDX_17 = 0x1
            FKC_IDX_16 = 0x1
            FKC_IDX_31 = 0x1
            FKC_IDX_30 = 0x1
            FKC_IDX_29 = 0x1
            FKC_IDX_28 = 0x1
            FKC_IDX_27 = 0x1
            FKC_IDX_26 = 0x1
            FKC_IDX_25 = 0x1
            FKC_IDX_24 = 0x1
            FKC_IDX_39 = 0x1
            FKC_IDX_38 = 0x1
            FKC_IDX_37 = 0x1
            FKC_IDX_36 = 0x1
            FKC_IDX_35 = 0x1
            FKC_IDX_34 = 0x1
            FKC_IDX_33 = 0x1
            FKC_IDX_32 = 0x1
            FKC_IDX_47 = 0x1
            FKC_IDX_46 = 0x1
            FKC_IDX_45 = 0x1
            FKC_IDX_44 = 0x1
            FKC_IDX_43 = 0x1
            FKC_IDX_42 = 0x1
            FKC_IDX_41 = 0x1
            FKC_IDX_40 = 0x1
            FKC_IDX_55 = 0x1
            FKC_IDX_54 = 0x1
            FKC_IDX_53 = 0x1
            FKC_IDX_52 = 0x1
            FKC_IDX_51 = 0x1
            FKC_IDX_50 = 0x1
            FKC_IDX_49 = 0x1
            FKC_IDX_48 = 0x1
            FKC_IDX_63 = 0x1
            FKC_IDX_62 = 0x1
            FKC_IDX_61 = 0x1
            FKC_IDX_60 = 0x1
            FKC_IDX_59 = 0x1
            FKC_IDX_58 = 0x1
            FKC_IDX_57 = 0x1
            FKC_IDX_56 = 0x1
            FKC_IDX_71 = 0x1
            FKC_IDX_70 = 0x1
            FKC_IDX_69 = 0x1
            FKC_IDX_68 = 0x1
            FKC_IDX_67 = 0x1
            FKC_IDX_66 = 0x1
            FKC_IDX_65 = 0x1
            FKC_IDX_64 = 0x1
            FKC_IDX_79 = 0x1
            FKC_IDX_78 = 0x1
            FKC_IDX_77 = 0x1
            FKC_IDX_76 = 0x1
            FKC_IDX_75 = 0x1
            FKC_IDX_74 = 0x1
            FKC_IDX_73 = 0x1
            FKC_IDX_72 = 0x1
            FKC_IDX_87 = 0x1
            FKC_IDX_86 = 0x1
            FKC_IDX_85 = 0x1
            FKC_IDX_84 = 0x1
            FKC_IDX_83 = 0x1
            FKC_IDX_82 = 0x1
            FKC_IDX_81 = 0x1
            FKC_IDX_80 = 0x1
            FKC_IDX_95 = 0x1
            FKC_IDX_94 = 0x1
            FKC_IDX_93 = 0x1
            FKC_IDX_92 = 0x1
            FKC_IDX_91 = 0x1
            FKC_IDX_90 = 0x1
            FKC_IDX_89 = 0x1
            FKC_IDX_88 = 0x1
            FKC_IDX_103 = 0x1
            FKC_IDX_102 = 0x1
            FKC_IDX_101 = 0x1
            FKC_IDX_100 = 0x1
            FKC_IDX_99 = 0x1
            FKC_IDX_98 = 0x1
            FKC_IDX_97 = 0x1
            FKC_IDX_96 = 0x1
            FKC_IDX_111 = 0x1
            FKC_IDX_110 = 0x1
            FKC_IDX_109 = 0x1
            FKC_IDX_108 = 0x1
            FKC_IDX_107 = 0x1
            FKC_IDX_106 = 0x1
            FKC_IDX_105 = 0x1
            FKC_IDX_104 = 0x1
            FKC_IDX_119 = 0x1
            FKC_IDX_118 = 0x1
            FKC_IDX_117 = 0x1
            FKC_IDX_116 = 0x1
            FKC_IDX_115 = 0x1
            FKC_IDX_114 = 0x1
            FKC_IDX_113 = 0x1
            FKC_IDX_112 = 0x1
            FKC_IDX_127 = 0x1
            FKC_IDX_126 = 0x1
            FKC_IDX_125 = 0x1
            FKC_IDX_124 = 0x1
            FKC_IDX_123 = 0x1
            FKC_IDX_122 = 0x1
            FKC_IDX_121 = 0x1
            FKC_IDX_120 = 0x1
        # end class LEN

        FIELDS = (
            BitField(fid=FID.FKC_IDX_7, length=LEN.FKC_IDX_7,
                     title="FkcIdx7", name="fkc_idx_7",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_7) - 1),)),
            BitField(fid=FID.FKC_IDX_6, length=LEN.FKC_IDX_6,
                     title="FkcIdx6", name="fkc_idx_6",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_6) - 1),)),
            BitField(fid=FID.FKC_IDX_5, length=LEN.FKC_IDX_5,
                     title="FkcIdx5", name="fkc_idx_5",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_5) - 1),)),
            BitField(fid=FID.FKC_IDX_4, length=LEN.FKC_IDX_4,
                     title="FkcIdx4", name="fkc_idx_4",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_4) - 1),)),
            BitField(fid=FID.FKC_IDX_3, length=LEN.FKC_IDX_3,
                     title="FkcIdx3", name="fkc_idx_3",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_3) - 1),)),
            BitField(fid=FID.FKC_IDX_2, length=LEN.FKC_IDX_2,
                     title="FkcIdx2", name="fkc_idx_2",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_2) - 1),)),
            BitField(fid=FID.FKC_IDX_1, length=LEN.FKC_IDX_1,
                     title="FkcIdx1", name="fkc_idx_1",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_1) - 1),)),
            BitField(fid=FID.FKC_IDX_0, length=LEN.FKC_IDX_0,
                     title="FkcIdx0", name="fkc_idx_0",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_0) - 1),)),
            BitField(fid=FID.FKC_IDX_15, length=LEN.FKC_IDX_15,
                     title="FkcIdx15", name="fkc_idx_15",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_15) - 1),)),
            BitField(fid=FID.FKC_IDX_14, length=LEN.FKC_IDX_14,
                     title="FkcIdx14", name="fkc_idx_14",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_14) - 1),)),
            BitField(fid=FID.FKC_IDX_13, length=LEN.FKC_IDX_13,
                     title="FkcIdx13", name="fkc_idx_13",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_13) - 1),)),
            BitField(fid=FID.FKC_IDX_12, length=LEN.FKC_IDX_12,
                     title="FkcIdx12", name="fkc_idx_12",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_12) - 1),)),
            BitField(fid=FID.FKC_IDX_11, length=LEN.FKC_IDX_11,
                     title="FkcIdx11", name="fkc_idx_11",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_11) - 1),)),
            BitField(fid=FID.FKC_IDX_10, length=LEN.FKC_IDX_10,
                     title="FkcIdx10", name="fkc_idx_10",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_10) - 1),)),
            BitField(fid=FID.FKC_IDX_9, length=LEN.FKC_IDX_9,
                     title="FkcIdx9", name="fkc_idx_9",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_9) - 1),)),
            BitField(fid=FID.FKC_IDX_8, length=LEN.FKC_IDX_8,
                     title="FkcIdx8", name="fkc_idx_8",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_8) - 1),)),
            BitField(fid=FID.FKC_IDX_23, length=LEN.FKC_IDX_23,
                     title="FkcIdx23", name="fkc_idx_23",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_23) - 1),)),
            BitField(fid=FID.FKC_IDX_22, length=LEN.FKC_IDX_22,
                     title="FkcIdx22", name="fkc_idx_22",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_22) - 1),)),
            BitField(fid=FID.FKC_IDX_21, length=LEN.FKC_IDX_21,
                     title="FkcIdx21", name="fkc_idx_21",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_21) - 1),)),
            BitField(fid=FID.FKC_IDX_20, length=LEN.FKC_IDX_20,
                     title="FkcIdx20", name="fkc_idx_20",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_20) - 1),)),
            BitField(fid=FID.FKC_IDX_19, length=LEN.FKC_IDX_19,
                     title="FkcIdx19", name="fkc_idx_19",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_19) - 1),)),
            BitField(fid=FID.FKC_IDX_18, length=LEN.FKC_IDX_18,
                     title="FkcIdx18", name="fkc_idx_18",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_18) - 1),)),
            BitField(fid=FID.FKC_IDX_17, length=LEN.FKC_IDX_17,
                     title="FkcIdx17", name="fkc_idx_17",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_17) - 1),)),
            BitField(fid=FID.FKC_IDX_16, length=LEN.FKC_IDX_16,
                     title="FkcIdx16", name="fkc_idx_16",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_16) - 1),)),
            BitField(fid=FID.FKC_IDX_31, length=LEN.FKC_IDX_31,
                     title="FkcIdx31", name="fkc_idx_31",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_31) - 1),)),
            BitField(fid=FID.FKC_IDX_30, length=LEN.FKC_IDX_30,
                     title="FkcIdx30", name="fkc_idx_30",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_30) - 1),)),
            BitField(fid=FID.FKC_IDX_29, length=LEN.FKC_IDX_29,
                     title="FkcIdx29", name="fkc_idx_29",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_29) - 1),)),
            BitField(fid=FID.FKC_IDX_28, length=LEN.FKC_IDX_28,
                     title="FkcIdx28", name="fkc_idx_28",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_28) - 1),)),
            BitField(fid=FID.FKC_IDX_27, length=LEN.FKC_IDX_27,
                     title="FkcIdx27", name="fkc_idx_27",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_27) - 1),)),
            BitField(fid=FID.FKC_IDX_26, length=LEN.FKC_IDX_26,
                     title="FkcIdx26", name="fkc_idx_26",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_26) - 1),)),
            BitField(fid=FID.FKC_IDX_25, length=LEN.FKC_IDX_25,
                     title="FkcIdx25", name="fkc_idx_25",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_25) - 1),)),
            BitField(fid=FID.FKC_IDX_24, length=LEN.FKC_IDX_24,
                     title="FkcIdx24", name="fkc_idx_24",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_24) - 1),)),
            BitField(fid=FID.FKC_IDX_39, length=LEN.FKC_IDX_39,
                     title="FkcIdx39", name="fkc_idx_39",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_39) - 1),)),
            BitField(fid=FID.FKC_IDX_38, length=LEN.FKC_IDX_38,
                     title="FkcIdx38", name="fkc_idx_38",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_38) - 1),)),
            BitField(fid=FID.FKC_IDX_37, length=LEN.FKC_IDX_37,
                     title="FkcIdx37", name="fkc_idx_37",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_37) - 1),)),
            BitField(fid=FID.FKC_IDX_36, length=LEN.FKC_IDX_36,
                     title="FkcIdx36", name="fkc_idx_36",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_36) - 1),)),
            BitField(fid=FID.FKC_IDX_35, length=LEN.FKC_IDX_35,
                     title="FkcIdx35", name="fkc_idx_35",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_35) - 1),)),
            BitField(fid=FID.FKC_IDX_34, length=LEN.FKC_IDX_34,
                     title="FkcIdx34", name="fkc_idx_34",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_34) - 1),)),
            BitField(fid=FID.FKC_IDX_33, length=LEN.FKC_IDX_33,
                     title="FkcIdx33", name="fkc_idx_33",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_33) - 1),)),
            BitField(fid=FID.FKC_IDX_32, length=LEN.FKC_IDX_32,
                     title="FkcIdx32", name="fkc_idx_32",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_32) - 1),)),
            BitField(fid=FID.FKC_IDX_47, length=LEN.FKC_IDX_47,
                     title="FkcIdx47", name="fkc_idx_47",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_47) - 1),)),
            BitField(fid=FID.FKC_IDX_46, length=LEN.FKC_IDX_46,
                     title="FkcIdx46", name="fkc_idx_46",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_46) - 1),)),
            BitField(fid=FID.FKC_IDX_45, length=LEN.FKC_IDX_45,
                     title="FkcIdx45", name="fkc_idx_45",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_45) - 1),)),
            BitField(fid=FID.FKC_IDX_44, length=LEN.FKC_IDX_44,
                     title="FkcIdx44", name="fkc_idx_44",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_44) - 1),)),
            BitField(fid=FID.FKC_IDX_43, length=LEN.FKC_IDX_43,
                     title="FkcIdx43", name="fkc_idx_43",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_43) - 1),)),
            BitField(fid=FID.FKC_IDX_42, length=LEN.FKC_IDX_42,
                     title="FkcIdx42", name="fkc_idx_42",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_42) - 1),)),
            BitField(fid=FID.FKC_IDX_41, length=LEN.FKC_IDX_41,
                     title="FkcIdx41", name="fkc_idx_41",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_41) - 1),)),
            BitField(fid=FID.FKC_IDX_40, length=LEN.FKC_IDX_40,
                     title="FkcIdx40", name="fkc_idx_40",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_40) - 1),)),
            BitField(fid=FID.FKC_IDX_55, length=LEN.FKC_IDX_55,
                     title="FkcIdx55", name="fkc_idx_55",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_55) - 1),)),
            BitField(fid=FID.FKC_IDX_54, length=LEN.FKC_IDX_54,
                     title="FkcIdx54", name="fkc_idx_54",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_54) - 1),)),
            BitField(fid=FID.FKC_IDX_53, length=LEN.FKC_IDX_53,
                     title="FkcIdx53", name="fkc_idx_53",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_53) - 1),)),
            BitField(fid=FID.FKC_IDX_52, length=LEN.FKC_IDX_52,
                     title="FkcIdx52", name="fkc_idx_52",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_52) - 1),)),
            BitField(fid=FID.FKC_IDX_51, length=LEN.FKC_IDX_51,
                     title="FkcIdx51", name="fkc_idx_51",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_51) - 1),)),
            BitField(fid=FID.FKC_IDX_50, length=LEN.FKC_IDX_50,
                     title="FkcIdx50", name="fkc_idx_50",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_50) - 1),)),
            BitField(fid=FID.FKC_IDX_49, length=LEN.FKC_IDX_49,
                     title="FkcIdx49", name="fkc_idx_49",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_49) - 1),)),
            BitField(fid=FID.FKC_IDX_48, length=LEN.FKC_IDX_48,
                     title="FkcIdx48", name="fkc_idx_48",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_48) - 1),)),
            BitField(fid=FID.FKC_IDX_63, length=LEN.FKC_IDX_63,
                     title="FkcIdx63", name="fkc_idx_63",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_63) - 1),)),
            BitField(fid=FID.FKC_IDX_62, length=LEN.FKC_IDX_62,
                     title="FkcIdx62", name="fkc_idx_62",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_62) - 1),)),
            BitField(fid=FID.FKC_IDX_61, length=LEN.FKC_IDX_61,
                     title="FkcIdx61", name="fkc_idx_61",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_61) - 1),)),
            BitField(fid=FID.FKC_IDX_60, length=LEN.FKC_IDX_60,
                     title="FkcIdx60", name="fkc_idx_60",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_60) - 1),)),
            BitField(fid=FID.FKC_IDX_59, length=LEN.FKC_IDX_59,
                     title="FkcIdx59", name="fkc_idx_59",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_59) - 1),)),
            BitField(fid=FID.FKC_IDX_58, length=LEN.FKC_IDX_58,
                     title="FkcIdx58", name="fkc_idx_58",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_58) - 1),)),
            BitField(fid=FID.FKC_IDX_57, length=LEN.FKC_IDX_57,
                     title="FkcIdx57", name="fkc_idx_57",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_57) - 1),)),
            BitField(fid=FID.FKC_IDX_56, length=LEN.FKC_IDX_56,
                     title="FkcIdx56", name="fkc_idx_56",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_56) - 1),)),
            BitField(fid=FID.FKC_IDX_71, length=LEN.FKC_IDX_71,
                     title="FkcIdx71", name="fkc_idx_71",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_71) - 1),)),
            BitField(fid=FID.FKC_IDX_70, length=LEN.FKC_IDX_70,
                     title="FkcIdx70", name="fkc_idx_70",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_70) - 1),)),
            BitField(fid=FID.FKC_IDX_69, length=LEN.FKC_IDX_69,
                     title="FkcIdx69", name="fkc_idx_69",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_69) - 1),)),
            BitField(fid=FID.FKC_IDX_68, length=LEN.FKC_IDX_68,
                     title="FkcIdx68", name="fkc_idx_68",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_68) - 1),)),
            BitField(fid=FID.FKC_IDX_67, length=LEN.FKC_IDX_67,
                     title="FkcIdx67", name="fkc_idx_67",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_67) - 1),)),
            BitField(fid=FID.FKC_IDX_66, length=LEN.FKC_IDX_66,
                     title="FkcIdx66", name="fkc_idx_66",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_66) - 1),)),
            BitField(fid=FID.FKC_IDX_65, length=LEN.FKC_IDX_65,
                     title="FkcIdx65", name="fkc_idx_65",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_65) - 1),)),
            BitField(fid=FID.FKC_IDX_64, length=LEN.FKC_IDX_64,
                     title="FkcIdx64", name="fkc_idx_64",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_64) - 1),)),
            BitField(fid=FID.FKC_IDX_79, length=LEN.FKC_IDX_79,
                     title="FkcIdx79", name="fkc_idx_79",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_79) - 1),)),
            BitField(fid=FID.FKC_IDX_78, length=LEN.FKC_IDX_78,
                     title="FkcIdx78", name="fkc_idx_78",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_78) - 1),)),
            BitField(fid=FID.FKC_IDX_77, length=LEN.FKC_IDX_77,
                     title="FkcIdx77", name="fkc_idx_77",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_77) - 1),)),
            BitField(fid=FID.FKC_IDX_76, length=LEN.FKC_IDX_76,
                     title="FkcIdx76", name="fkc_idx_76",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_76) - 1),)),
            BitField(fid=FID.FKC_IDX_75, length=LEN.FKC_IDX_75,
                     title="FkcIdx75", name="fkc_idx_75",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_75) - 1),)),
            BitField(fid=FID.FKC_IDX_74, length=LEN.FKC_IDX_74,
                     title="FkcIdx74", name="fkc_idx_74",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_74) - 1),)),
            BitField(fid=FID.FKC_IDX_73, length=LEN.FKC_IDX_73,
                     title="FkcIdx73", name="fkc_idx_73",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_73) - 1),)),
            BitField(fid=FID.FKC_IDX_72, length=LEN.FKC_IDX_72,
                     title="FkcIdx72", name="fkc_idx_72",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_72) - 1),)),
            BitField(fid=FID.FKC_IDX_87, length=LEN.FKC_IDX_87,
                     title="FkcIdx87", name="fkc_idx_87",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_87) - 1),)),
            BitField(fid=FID.FKC_IDX_86, length=LEN.FKC_IDX_86,
                     title="FkcIdx86", name="fkc_idx_86",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_86) - 1),)),
            BitField(fid=FID.FKC_IDX_85, length=LEN.FKC_IDX_85,
                     title="FkcIdx85", name="fkc_idx_85",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_85) - 1),)),
            BitField(fid=FID.FKC_IDX_84, length=LEN.FKC_IDX_84,
                     title="FkcIdx84", name="fkc_idx_84",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_84) - 1),)),
            BitField(fid=FID.FKC_IDX_83, length=LEN.FKC_IDX_83,
                     title="FkcIdx83", name="fkc_idx_83",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_83) - 1),)),
            BitField(fid=FID.FKC_IDX_82, length=LEN.FKC_IDX_82,
                     title="FkcIdx82", name="fkc_idx_82",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_82) - 1),)),
            BitField(fid=FID.FKC_IDX_81, length=LEN.FKC_IDX_81,
                     title="FkcIdx81", name="fkc_idx_81",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_81) - 1),)),
            BitField(fid=FID.FKC_IDX_80, length=LEN.FKC_IDX_80,
                     title="FkcIdx80", name="fkc_idx_80",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_80) - 1),)),
            BitField(fid=FID.FKC_IDX_95, length=LEN.FKC_IDX_95,
                     title="FkcIdx95", name="fkc_idx_95",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_95) - 1),)),
            BitField(fid=FID.FKC_IDX_94, length=LEN.FKC_IDX_94,
                     title="FkcIdx94", name="fkc_idx_94",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_94) - 1),)),
            BitField(fid=FID.FKC_IDX_93, length=LEN.FKC_IDX_93,
                     title="FkcIdx93", name="fkc_idx_93",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_93) - 1),)),
            BitField(fid=FID.FKC_IDX_92, length=LEN.FKC_IDX_92,
                     title="FkcIdx92", name="fkc_idx_92",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_92) - 1),)),
            BitField(fid=FID.FKC_IDX_91, length=LEN.FKC_IDX_91,
                     title="FkcIdx91", name="fkc_idx_91",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_91) - 1),)),
            BitField(fid=FID.FKC_IDX_90, length=LEN.FKC_IDX_90,
                     title="FkcIdx90", name="fkc_idx_90",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_90) - 1),)),
            BitField(fid=FID.FKC_IDX_89, length=LEN.FKC_IDX_89,
                     title="FkcIdx89", name="fkc_idx_89",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_89) - 1),)),
            BitField(fid=FID.FKC_IDX_88, length=LEN.FKC_IDX_88,
                     title="FkcIdx88", name="fkc_idx_88",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_88) - 1),)),
            BitField(fid=FID.FKC_IDX_103, length=LEN.FKC_IDX_103,
                     title="FkcIdx103", name="fkc_idx_103",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_103) - 1),)),
            BitField(fid=FID.FKC_IDX_102, length=LEN.FKC_IDX_102,
                     title="FkcIdx102", name="fkc_idx_102",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_102) - 1),)),
            BitField(fid=FID.FKC_IDX_101, length=LEN.FKC_IDX_101,
                     title="FkcIdx101", name="fkc_idx_101",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_101) - 1),)),
            BitField(fid=FID.FKC_IDX_100, length=LEN.FKC_IDX_100,
                     title="FkcIdx100", name="fkc_idx_100",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_100) - 1),)),
            BitField(fid=FID.FKC_IDX_99, length=LEN.FKC_IDX_99,
                     title="FkcIdx99", name="fkc_idx_99",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_99) - 1),)),
            BitField(fid=FID.FKC_IDX_98, length=LEN.FKC_IDX_98,
                     title="FkcIdx98", name="fkc_idx_98",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_98) - 1),)),
            BitField(fid=FID.FKC_IDX_97, length=LEN.FKC_IDX_97,
                     title="FkcIdx97", name="fkc_idx_97",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_97) - 1),)),
            BitField(fid=FID.FKC_IDX_96, length=LEN.FKC_IDX_96,
                     title="FkcIdx96", name="fkc_idx_96",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_96) - 1),)),
            BitField(fid=FID.FKC_IDX_111, length=LEN.FKC_IDX_111,
                     title="FkcIdx111", name="fkc_idx_111",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_111) - 1),)),
            BitField(fid=FID.FKC_IDX_110, length=LEN.FKC_IDX_110,
                     title="FkcIdx110", name="fkc_idx_110",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_110) - 1),)),
            BitField(fid=FID.FKC_IDX_109, length=LEN.FKC_IDX_109,
                     title="FkcIdx109", name="fkc_idx_109",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_109) - 1),)),
            BitField(fid=FID.FKC_IDX_108, length=LEN.FKC_IDX_108,
                     title="FkcIdx108", name="fkc_idx_108",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_108) - 1),)),
            BitField(fid=FID.FKC_IDX_107, length=LEN.FKC_IDX_107,
                     title="FkcIdx107", name="fkc_idx_107",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_107) - 1),)),
            BitField(fid=FID.FKC_IDX_106, length=LEN.FKC_IDX_106,
                     title="FkcIdx106", name="fkc_idx_106",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_106) - 1),)),
            BitField(fid=FID.FKC_IDX_105, length=LEN.FKC_IDX_105,
                     title="FkcIdx105", name="fkc_idx_105",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_105) - 1),)),
            BitField(fid=FID.FKC_IDX_104, length=LEN.FKC_IDX_104,
                     title="FkcIdx104", name="fkc_idx_104",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_104) - 1),)),
            BitField(fid=FID.FKC_IDX_119, length=LEN.FKC_IDX_119,
                     title="FkcIdx119", name="fkc_idx_119",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_119) - 1),)),
            BitField(fid=FID.FKC_IDX_118, length=LEN.FKC_IDX_118,
                     title="FkcIdx118", name="fkc_idx_118",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_118) - 1),)),
            BitField(fid=FID.FKC_IDX_117, length=LEN.FKC_IDX_117,
                     title="FkcIdx117", name="fkc_idx_117",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_117) - 1),)),
            BitField(fid=FID.FKC_IDX_116, length=LEN.FKC_IDX_116,
                     title="FkcIdx116", name="fkc_idx_116",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_116) - 1),)),
            BitField(fid=FID.FKC_IDX_115, length=LEN.FKC_IDX_115,
                     title="FkcIdx115", name="fkc_idx_115",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_115) - 1),)),
            BitField(fid=FID.FKC_IDX_114, length=LEN.FKC_IDX_114,
                     title="FkcIdx114", name="fkc_idx_114",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_114) - 1),)),
            BitField(fid=FID.FKC_IDX_113, length=LEN.FKC_IDX_113,
                     title="FkcIdx113", name="fkc_idx_113",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_113) - 1),)),
            BitField(fid=FID.FKC_IDX_112, length=LEN.FKC_IDX_112,
                     title="FkcIdx112", name="fkc_idx_112",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_112) - 1),)),
            BitField(fid=FID.FKC_IDX_127, length=LEN.FKC_IDX_127,
                     title="FkcIdx127", name="fkc_idx_127",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_127) - 1),)),
            BitField(fid=FID.FKC_IDX_126, length=LEN.FKC_IDX_126,
                     title="FkcIdx126", name="fkc_idx_126",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_126) - 1),)),
            BitField(fid=FID.FKC_IDX_125, length=LEN.FKC_IDX_125,
                     title="FkcIdx125", name="fkc_idx_125",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_125) - 1),)),
            BitField(fid=FID.FKC_IDX_124, length=LEN.FKC_IDX_124,
                     title="FkcIdx124", name="fkc_idx_124",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_124) - 1),)),
            BitField(fid=FID.FKC_IDX_123, length=LEN.FKC_IDX_123,
                     title="FkcIdx123", name="fkc_idx_123",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_123) - 1),)),
            BitField(fid=FID.FKC_IDX_122, length=LEN.FKC_IDX_122,
                     title="FkcIdx122", name="fkc_idx_122",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_122) - 1),)),
            BitField(fid=FID.FKC_IDX_121, length=LEN.FKC_IDX_121,
                     title="FkcIdx121", name="fkc_idx_121",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_121) - 1),)),
            BitField(fid=FID.FKC_IDX_120, length=LEN.FKC_IDX_120,
                     title="FkcIdx120", name="fkc_idx_120",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FKC_IDX_120) - 1),)),
        )
    # end class KeyTriggerBitmap

    class FkcFailureEnabledState(BitFieldContainerMixin):
        """
        Define ``FkcFailureEnabledState`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      6
        Failure                       1
        Enabled                       1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            FAILURE = RESERVED - 1
            ENABLED = FAILURE - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x6
            FAILURE = 0x1
            ENABLED = 0x1
        # end class

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),)),
            BitField(fid=FID.FAILURE, length=LEN.FAILURE,
                     title="Failure", name="failure",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FAILURE) - 1),)),
            BitField(fid=FID.ENABLED, length=LEN.ENABLED,
                     title="Enabled", name="enabled",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.ENABLED) - 1),)),
        )
    # end class FkcFailureEnabledState
# end class FullKeyCustomization


class FullKeyCustomizationModel(FeatureModel):
    """
    Define ``FullKeyCustomization`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_CAPABILITIES = 0
        GET_SET_POWER_ON_PARAMS = 1
        GET_TOGGLE_KEY_LIST = 2
        GET_SET_ENABLED = 3
        GET_SET_SW_CONFIGURATION_COOKIE = 4

        # Event index
        BASE_LAYER_TRIGGER_AS_LIST = 0
        BASE_LAYER_TRIGGER_AS_BITMAP = 1
        FN_LAYER_TRIGGER_AS_LIST = 2
        FN_LAYER_TRIGGER_AS_BITMAP = 3
        GSHIFT_LAYER_TRIGGER_AS_LIST = 4
        GSHIFT_LAYER_TRIGGER_AS_BITMAP = 5
        ENABLE_DISABLE = 6
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``FullKeyCustomization`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_CAPABILITIES: {
                    "request": GetCapabilitiesV0ToV1,
                    "response": GetCapabilitiesResponseV0
                },
                cls.INDEX.GET_SET_POWER_ON_PARAMS: {
                    "request": GetSetPowerOnParams,
                    "response": GetSetPowerOnParamsResponse
                },
                cls.INDEX.GET_TOGGLE_KEY_LIST: {
                    "request": GetToggleKeyList,
                    "response": GetToggleKeyListResponse
                },
                cls.INDEX.GET_SET_ENABLED: {
                    "request": GetSetEnabled,
                    "response": GetSetEnabledResponse
                }
            },
            "events": {
                cls.INDEX.BASE_LAYER_TRIGGER_AS_LIST: {"report": BaseLayerTriggerAsListEvent},
                cls.INDEX.BASE_LAYER_TRIGGER_AS_BITMAP: {"report": BaseLayerTriggerAsBitmapEvent},
                cls.INDEX.FN_LAYER_TRIGGER_AS_LIST: {"report": FNLayerTriggerAsListEvent},
                cls.INDEX.FN_LAYER_TRIGGER_AS_BITMAP: {"report": FNLayerTriggerAsBitmapEvent},
                cls.INDEX.GSHIFT_LAYER_TRIGGER_AS_LIST: {"report": GShiftLayerTriggerAsListEvent},
                cls.INDEX.GSHIFT_LAYER_TRIGGER_AS_BITMAP: {"report": GShiftLayerTriggerAsBitmapEvent},
                cls.INDEX.ENABLE_DISABLE: {"report": EnableDisableEvent}
            }
        }

        function_map_v1 = {
            "functions": {
                cls.INDEX.GET_CAPABILITIES: {
                    "request": GetCapabilitiesV0ToV1,
                    "response": GetCapabilitiesResponseV1
                },
                cls.INDEX.GET_SET_POWER_ON_PARAMS: {
                    "request": GetSetPowerOnParams,
                    "response": GetSetPowerOnParamsResponse
                },
                cls.INDEX.GET_TOGGLE_KEY_LIST: {
                    "request": GetToggleKeyList,
                    "response": GetToggleKeyListResponse
                },
                cls.INDEX.GET_SET_ENABLED: {
                    "request": GetSetEnabled,
                    "response": GetSetEnabledResponse
                },
                cls.INDEX.GET_SET_SW_CONFIGURATION_COOKIE: {
                    "request": GetSetSWConfigurationCookieV1,
                    "response": GetSetSWConfigurationCookieResponseV1
                }
            },
            "events": {
                cls.INDEX.BASE_LAYER_TRIGGER_AS_LIST: {"report": BaseLayerTriggerAsListEvent},
                cls.INDEX.BASE_LAYER_TRIGGER_AS_BITMAP: {"report": BaseLayerTriggerAsBitmapEvent},
                cls.INDEX.FN_LAYER_TRIGGER_AS_LIST: {"report": FNLayerTriggerAsListEvent},
                cls.INDEX.FN_LAYER_TRIGGER_AS_BITMAP: {"report": FNLayerTriggerAsBitmapEvent},
                cls.INDEX.GSHIFT_LAYER_TRIGGER_AS_LIST: {"report": GShiftLayerTriggerAsListEvent},
                cls.INDEX.GSHIFT_LAYER_TRIGGER_AS_BITMAP: {"report": GShiftLayerTriggerAsBitmapEvent},
                cls.INDEX.ENABLE_DISABLE: {"report": EnableDisableEvent}
            }
        }

        return {
            "feature_base": FullKeyCustomization,
            "versions": {
                FullKeyCustomizationV0.VERSION: {
                    "main_cls": FullKeyCustomizationV0,
                    "api": function_map_v0
                },
                FullKeyCustomizationV1.VERSION: {
                    "main_cls": FullKeyCustomizationV1,
                    "api": function_map_v1
                }
            }
        }
    # end def _get_data_model
# end class FullKeyCustomizationModel


class FullKeyCustomizationFactory(FeatureFactory):
    """
    Get ``FullKeyCustomization`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``FullKeyCustomization`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``FullKeyCustomizationInterface``
        """
        return FullKeyCustomizationModel.get_main_cls(version)()
    # end def create
# end class FullKeyCustomizationFactory


class FullKeyCustomizationInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``FullKeyCustomization``
    """

    def __init__(self):
        # Requests
        self.get_capabilities_cls = None
        self.get_set_power_on_params_cls = None
        self.get_toggle_key_list_cls = None
        self.get_set_enabled_cls = None
        self.get_set_sw_configuration_cookie_cls = None

        # Responses
        self.get_capabilities_response_cls = None
        self.get_set_power_on_params_response_cls = None
        self.get_toggle_key_list_response_cls = None
        self.get_set_enabled_response_cls = None
        self.get_set_sw_configuration_cookie_response_cls = None

        # Events
        self.base_layer_trigger_as_list_event_cls = None
        self.base_layer_trigger_as_bitmap_event_cls = None
        self.fn_layer_trigger_as_list_event_cls = None
        self.fn_layer_trigger_as_bitmap_event_cls = None
        self.gshift_layer_trigger_as_list_event_cls = None
        self.gshift_layer_trigger_as_bitmap_event_cls = None
        self.enable_disable_event_cls = None
    # end def __init__
# end class FullKeyCustomizationInterface


class FullKeyCustomizationV0(FullKeyCustomizationInterface):
    """
    Define ``FullKeyCustomizationV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getCapabilities() -> fkcConfigFileVer, macroDefFileVer, fkcConfigFileMaxsize, macroDefFileMaxsize,
    fkcConfigMaxTriggers

    [1] getSetPowerOnParams(setPowerOnFkcState, powerOnFkcState) -> powerOnFkcState

    [2] getToggleKeyList() -> ToggleKey0Cidx, ToggleKey1Cidx, ToggleKey2Cidx, ToggleKey3Cidx, ToggleKey4Cidx,
    ToggleKey5Cidx, ToggleKey6Cidx, ToggleKey7Cidx

    [3] getSetEnabled(setGetFkcState, fkcState, toggleKeysState) -> fkcState, toggleKeysState

    [Event 0] BaseLayerTriggerAsListEvent -> keyTrigger0, keyTrigger1, keyTrigger2, keyTrigger3, keyTrigger4,
    keyTrigger5, keyTrigger6, keyTrigger7, keyTrigger8, keyTrigger9, keyTrigger10, keyTrigger11, keyTrigger12,
    keyTrigger13, keyTrigger14, keyTrigger15

    [Event 1] BaseLayerTriggerAsBitmapEvent -> keyTriggerBitmap

    [Event 2] FNLayerTriggerAsListEvent -> keyTrigger0, keyTrigger1, keyTrigger2, keyTrigger3, keyTrigger4,
    keyTrigger5, keyTrigger6, keyTrigger7, keyTrigger8, keyTrigger9, keyTrigger10, keyTrigger11, keyTrigger12,
    keyTrigger13, keyTrigger14, keyTrigger15

    [Event 3] FNLayerTriggerAsBitmapEvent -> keyTriggerBitmap

    [Event 4] GShiftLayerTriggerAsListEvent -> keyTrigger0, keyTrigger1, keyTrigger2, keyTrigger3, keyTrigger4,
    keyTrigger5, keyTrigger6, keyTrigger7, keyTrigger8, keyTrigger9, keyTrigger10, keyTrigger11, keyTrigger12,
    keyTrigger13, keyTrigger14, keyTrigger15

    [Event 5] GShiftLayerTriggerAsBitmapEvent -> keyTriggerBitmap

    [Event 6] EnableDisableEvent -> fkcFailureEnabledState
    """
    VERSION = 0

    def __init__(self):
        # See ``FullKeyCustomization.__init__``
        super().__init__()
        index = FullKeyCustomizationModel.INDEX

        # Requests
        self.get_capabilities_cls = FullKeyCustomizationModel.get_request_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_set_power_on_params_cls = FullKeyCustomizationModel.get_request_cls(
            self.VERSION, index.GET_SET_POWER_ON_PARAMS)
        self.get_toggle_key_list_cls = FullKeyCustomizationModel.get_request_cls(
            self.VERSION, index.GET_TOGGLE_KEY_LIST)
        self.get_set_enabled_cls = FullKeyCustomizationModel.get_request_cls(
            self.VERSION, index.GET_SET_ENABLED)

        # Responses
        self.get_capabilities_response_cls = FullKeyCustomizationModel.get_response_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_set_power_on_params_response_cls = FullKeyCustomizationModel.get_response_cls(
            self.VERSION, index.GET_SET_POWER_ON_PARAMS)
        self.get_toggle_key_list_response_cls = FullKeyCustomizationModel.get_response_cls(
            self.VERSION, index.GET_TOGGLE_KEY_LIST)
        self.get_set_enabled_response_cls = FullKeyCustomizationModel.get_response_cls(
            self.VERSION, index.GET_SET_ENABLED)

        # Events
        self.base_layer_trigger_as_list_event_cls = FullKeyCustomizationModel.get_report_cls(
            self.VERSION, index.BASE_LAYER_TRIGGER_AS_LIST)
        self.base_layer_trigger_as_bitmap_event_cls = FullKeyCustomizationModel.get_report_cls(
            self.VERSION, index.BASE_LAYER_TRIGGER_AS_BITMAP)
        self.fn_layer_trigger_as_list_event_cls = FullKeyCustomizationModel.get_report_cls(
            self.VERSION, index.FN_LAYER_TRIGGER_AS_LIST)
        self.fn_layer_trigger_as_bitmap_event_cls = FullKeyCustomizationModel.get_report_cls(
            self.VERSION, index.FN_LAYER_TRIGGER_AS_BITMAP)
        self.gshift_layer_trigger_as_list_event_cls = FullKeyCustomizationModel.get_report_cls(
            self.VERSION, index.GSHIFT_LAYER_TRIGGER_AS_LIST)
        self.gshift_layer_trigger_as_bitmap_event_cls = FullKeyCustomizationModel.get_report_cls(
            self.VERSION, index.GSHIFT_LAYER_TRIGGER_AS_BITMAP)
        self.enable_disable_event_cls = FullKeyCustomizationModel.get_report_cls(
            self.VERSION, index.ENABLE_DISABLE)
    # end def __init__

    def get_max_function_index(self):
        # See ``FullKeyCustomizationInterface.get_max_function_index``
        return FullKeyCustomizationModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class FullKeyCustomizationV0


class FullKeyCustomizationV1(FullKeyCustomizationV0):
    """
    Define ``FullKeyCustomizationV1`` feature

    This feature provides model and unit specific information for version 1

    [0] getCapabilities() -> fkcConfigFileVer, macroDefFileVer, fkcConfigFileMaxsize, macroDefFileMaxsize,
    fkcConfigMaxTriggers, swConfigCapabilities

    [4] getSetSWConfigurationCookie(setSwConfigurationCookie, swConfigurationCookie) -> swConfigurationCookie
    """
    VERSION = 1

    def __init__(self):
        # See ``FullKeyCustomization.__init__``
        super().__init__()
        index = FullKeyCustomizationModel.INDEX

        # Requests
        self.get_set_sw_configuration_cookie_cls = FullKeyCustomizationModel.get_request_cls(
            self.VERSION, index.GET_SET_SW_CONFIGURATION_COOKIE)

        # Responses
        self.get_set_sw_configuration_cookie_response_cls = FullKeyCustomizationModel.get_response_cls(
            self.VERSION, index.GET_SET_SW_CONFIGURATION_COOKIE)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``FullKeyCustomizationInterface.get_max_function_index``
        return FullKeyCustomizationModel.get_base_cls().MAX_FUNCTION_INDEX_V1
    # end def get_max_function_index
# end class FullKeyCustomizationV1


class ShortEmptyPacketDataFormat(FullKeyCustomization):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetCapabilities
        - GetToggleKeyList

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(FullKeyCustomization.FID):
        # See ``FullKeyCustomization.FID``
        PADDING = FullKeyCustomization.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(FullKeyCustomization.LEN):
        # See ``FullKeyCustomization.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = FullKeyCustomization.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=FullKeyCustomization.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class KeyTriggerAsList(FullKeyCustomization):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - BaseLayerTriggerAsListEvent
        - FNLayerTriggerAsListEvent
        - GShiftLayerTriggerAsListEvent

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Key Trigger 0                 8
    Key Trigger 1                 8
    Key Trigger 2                 8
    Key Trigger 3                 8
    Key Trigger 4                 8
    Key Trigger 5                 8
    Key Trigger 6                 8
    Key Trigger 7                 8
    Key Trigger 8                 8
    Key Trigger 9                 8
    Key Trigger 10                8
    Key Trigger 11                8
    Key Trigger 12                8
    Key Trigger 13                8
    Key Trigger 14                8
    Key Trigger 15                8
    ============================  ==========
    """

    class FID(FullKeyCustomization.FID):
        # See ``FullKeyCustomization.FID``
        KEY_TRIGGER_0 = FullKeyCustomization.FID.SOFTWARE_ID - 1
        KEY_TRIGGER_1 = KEY_TRIGGER_0 - 1
        KEY_TRIGGER_2 = KEY_TRIGGER_1 - 1
        KEY_TRIGGER_3 = KEY_TRIGGER_2 - 1
        KEY_TRIGGER_4 = KEY_TRIGGER_3 - 1
        KEY_TRIGGER_5 = KEY_TRIGGER_4 - 1
        KEY_TRIGGER_6 = KEY_TRIGGER_5 - 1
        KEY_TRIGGER_7 = KEY_TRIGGER_6 - 1
        KEY_TRIGGER_8 = KEY_TRIGGER_7 - 1
        KEY_TRIGGER_9 = KEY_TRIGGER_8 - 1
        KEY_TRIGGER_10 = KEY_TRIGGER_9 - 1
        KEY_TRIGGER_11 = KEY_TRIGGER_10 - 1
        KEY_TRIGGER_12 = KEY_TRIGGER_11 - 1
        KEY_TRIGGER_13 = KEY_TRIGGER_12 - 1
        KEY_TRIGGER_14 = KEY_TRIGGER_13 - 1
        KEY_TRIGGER_15 = KEY_TRIGGER_14 - 1
    # end class FID

    class LEN(FullKeyCustomization.LEN):
        # See ``FullKeyCustomization.LEN``
        KEY_TRIGGER_0 = 0x8
        KEY_TRIGGER_1 = 0x8
        KEY_TRIGGER_2 = 0x8
        KEY_TRIGGER_3 = 0x8
        KEY_TRIGGER_4 = 0x8
        KEY_TRIGGER_5 = 0x8
        KEY_TRIGGER_6 = 0x8
        KEY_TRIGGER_7 = 0x8
        KEY_TRIGGER_8 = 0x8
        KEY_TRIGGER_9 = 0x8
        KEY_TRIGGER_10 = 0x8
        KEY_TRIGGER_11 = 0x8
        KEY_TRIGGER_12 = 0x8
        KEY_TRIGGER_13 = 0x8
        KEY_TRIGGER_14 = 0x8
        KEY_TRIGGER_15 = 0x8
    # end class LEN

    FIELDS = FullKeyCustomization.FIELDS + (
        BitField(fid=FID.KEY_TRIGGER_0, length=LEN.KEY_TRIGGER_0,
                 title="KeyTrigger0", name="key_trigger_0",
                 checks=(CheckHexList(LEN.KEY_TRIGGER_0 // 8), CheckByte(),)),
        BitField(fid=FID.KEY_TRIGGER_1, length=LEN.KEY_TRIGGER_1,
                 title="KeyTrigger1", name="key_trigger_1",
                 checks=(CheckHexList(LEN.KEY_TRIGGER_1 // 8), CheckByte(),)),
        BitField(fid=FID.KEY_TRIGGER_2, length=LEN.KEY_TRIGGER_2,
                 title="KeyTrigger2", name="key_trigger_2",
                 checks=(CheckHexList(LEN.KEY_TRIGGER_2 // 8), CheckByte(),)),
        BitField(fid=FID.KEY_TRIGGER_3, length=LEN.KEY_TRIGGER_3,
                 title="KeyTrigger3", name="key_trigger_3",
                 checks=(CheckHexList(LEN.KEY_TRIGGER_3 // 8), CheckByte(),)),
        BitField(fid=FID.KEY_TRIGGER_4, length=LEN.KEY_TRIGGER_4,
                 title="KeyTrigger4", name="key_trigger_4",
                 checks=(CheckHexList(LEN.KEY_TRIGGER_4 // 8), CheckByte(),)),
        BitField(fid=FID.KEY_TRIGGER_5, length=LEN.KEY_TRIGGER_5,
                 title="KeyTrigger5", name="key_trigger_5",
                 checks=(CheckHexList(LEN.KEY_TRIGGER_5 // 8), CheckByte(),)),
        BitField(fid=FID.KEY_TRIGGER_6, length=LEN.KEY_TRIGGER_6,
                 title="KeyTrigger6", name="key_trigger_6",
                 checks=(CheckHexList(LEN.KEY_TRIGGER_6 // 8), CheckByte(),)),
        BitField(fid=FID.KEY_TRIGGER_7, length=LEN.KEY_TRIGGER_7,
                 title="KeyTrigger7", name="key_trigger_7",
                 checks=(CheckHexList(LEN.KEY_TRIGGER_7 // 8), CheckByte(),)),
        BitField(fid=FID.KEY_TRIGGER_8, length=LEN.KEY_TRIGGER_8,
                 title="KeyTrigger8", name="key_trigger_8",
                 checks=(CheckHexList(LEN.KEY_TRIGGER_8 // 8), CheckByte(),)),
        BitField(fid=FID.KEY_TRIGGER_9, length=LEN.KEY_TRIGGER_9,
                 title="KeyTrigger9", name="key_trigger_9",
                 checks=(CheckHexList(LEN.KEY_TRIGGER_9 // 8), CheckByte(),)),
        BitField(fid=FID.KEY_TRIGGER_10, length=LEN.KEY_TRIGGER_10,
                 title="KeyTrigger10", name="key_trigger_10",
                 checks=(CheckHexList(LEN.KEY_TRIGGER_10 // 8), CheckByte(),)),
        BitField(fid=FID.KEY_TRIGGER_11, length=LEN.KEY_TRIGGER_11,
                 title="KeyTrigger11", name="key_trigger_11",
                 checks=(CheckHexList(LEN.KEY_TRIGGER_11 // 8), CheckByte(),)),
        BitField(fid=FID.KEY_TRIGGER_12, length=LEN.KEY_TRIGGER_12,
                 title="KeyTrigger12", name="key_trigger_12",
                 checks=(CheckHexList(LEN.KEY_TRIGGER_12 // 8), CheckByte(),)),
        BitField(fid=FID.KEY_TRIGGER_13, length=LEN.KEY_TRIGGER_13,
                 title="KeyTrigger13", name="key_trigger_13",
                 checks=(CheckHexList(LEN.KEY_TRIGGER_13 // 8), CheckByte(),)),
        BitField(fid=FID.KEY_TRIGGER_14, length=LEN.KEY_TRIGGER_14,
                 title="KeyTrigger14", name="key_trigger_14",
                 checks=(CheckHexList(LEN.KEY_TRIGGER_14 // 8), CheckByte(),)),
        BitField(fid=FID.KEY_TRIGGER_15, length=LEN.KEY_TRIGGER_15,
                 title="KeyTrigger15", name="key_trigger_15",
                 checks=(CheckHexList(LEN.KEY_TRIGGER_15 // 8), CheckByte(),)),
    )
# end class KeyTriggerAsList


class KeyTriggerAsBitmap(FullKeyCustomization):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - BaseLayerTriggerAsBitmapEvent
        - FNLayerTriggerAsBitmapEvent
        - GShiftLayerTriggerAsBitmapEvent

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Key Trigger Bitmap            128
    ============================  ==========
    """

    class FID(FullKeyCustomization.FID):
        # See ``FullKeyCustomization.FID``
        KEY_TRIGGER_BITMAP = FullKeyCustomization.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(FullKeyCustomization.LEN):
        # See ``FullKeyCustomization.LEN``
        KEY_TRIGGER_BITMAP = 0x80
    # end class LEN

    FIELDS = FullKeyCustomization.FIELDS + (
        BitField(fid=FID.KEY_TRIGGER_BITMAP, length=LEN.KEY_TRIGGER_BITMAP,
                 title="KeyTriggerBitmap", name="key_trigger_bitmap",
                 checks=(CheckHexList(LEN.KEY_TRIGGER_BITMAP // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.KEY_TRIGGER_BITMAP) - 1),)),
    )
# end class KeyTriggerAsBitmap


class GetCapabilitiesV0ToV1(ShortEmptyPacketDataFormat):
    """
    Define ``GetCapabilitiesV0ToV1`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetCapabilitiesResponseV0.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetCapabilitiesV0ToV1


class GetSetPowerOnParams(FullKeyCustomization):
    """
    Define ``GetSetPowerOnParams`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Set Power On Fkc State        8
    Power On Fkc State            8
    Padding                       8
    ============================  ==========
    """

    class FID(FullKeyCustomization.FID):
        # See ``FullKeyCustomization.FID``
        SET_POWER_ON_FKC_STATE = FullKeyCustomization.FID.SOFTWARE_ID - 1
        POWER_ON_FKC_STATE = SET_POWER_ON_FKC_STATE - 1
        PADDING = POWER_ON_FKC_STATE - 1
    # end class FID

    class LEN(FullKeyCustomization.LEN):
        # See ``FullKeyCustomization.LEN``
        SET_POWER_ON_FKC_STATE = 0x8
        POWER_ON_FKC_STATE = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = FullKeyCustomization.FIELDS + (
        BitField(fid=FID.SET_POWER_ON_FKC_STATE, length=LEN.SET_POWER_ON_FKC_STATE,
                 title="SetPowerOnFkcState", name="set_power_on_fkc_state",
                 checks=(CheckHexList(LEN.SET_POWER_ON_FKC_STATE // 8), CheckByte(),)),
        BitField(fid=FID.POWER_ON_FKC_STATE, length=LEN.POWER_ON_FKC_STATE,
                 title="PowerOnFkcState", name="power_on_fkc_state",
                 checks=(CheckHexList(LEN.POWER_ON_FKC_STATE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=FullKeyCustomization.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, set_power_on_fkc_enable, power_on_fkc_enable, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param set_power_on_fkc_enable: Set Power On Fkc Enable
        :type set_power_on_fkc_enable: ``int | HexList``
        :param power_on_fkc_enable: Power On Fkc Enable
        :type power_on_fkc_enable: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetSetPowerOnParamsResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.set_power_on_fkc_state = self.SetPowerOnFkcState(set_power_on_fkc_enable=set_power_on_fkc_enable)
        self.power_on_fkc_state = self.PowerOnFkcState(power_on_fkc_enable=power_on_fkc_enable)
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GetSetPowerOnParams``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.set_power_on_fkc_state = cls.SetPowerOnFkcState.fromHexList(
            inner_field_container_mixin.set_power_on_fkc_state)
        inner_field_container_mixin.power_on_fkc_state = cls.PowerOnFkcState.fromHexList(
            inner_field_container_mixin.power_on_fkc_state)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetSetPowerOnParams


class GetToggleKeyList(ShortEmptyPacketDataFormat):
    """
    Define ``GetToggleKeyList`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetToggleKeyListResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetToggleKeyList


class GetSetEnabled(FullKeyCustomization):
    """
    Define ``GetSetEnabled`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Set Get Fkc State             8
    Fkc State                     8
    Toggle Keys State             8
    ============================  ==========
    """

    class FID(FullKeyCustomization.FID):
        # See ``FullKeyCustomization.FID``
        SET_GET_FKC_STATE = FullKeyCustomization.FID.SOFTWARE_ID - 1
        FKC_STATE = SET_GET_FKC_STATE - 1
        TOGGLE_KEYS_STATE = FKC_STATE - 1
    # end class FID

    class LEN(FullKeyCustomization.LEN):
        # See ``FullKeyCustomization.LEN``
        SET_GET_FKC_STATE = 0x8
        FKC_STATE = 0x8
        TOGGLE_KEYS_STATE = 0x8
    # end class LEN

    FIELDS = FullKeyCustomization.FIELDS + (
        BitField(fid=FID.SET_GET_FKC_STATE, length=LEN.SET_GET_FKC_STATE,
                 title="SetGetFkcState", name="set_get_fkc_state",
                 checks=(CheckHexList(LEN.SET_GET_FKC_STATE // 8), CheckByte(),)),
        BitField(fid=FID.FKC_STATE, length=LEN.FKC_STATE,
                 title="FkcState", name="fkc_state",
                 checks=(CheckHexList(LEN.FKC_STATE // 8), CheckByte(),)),
        BitField(fid=FID.TOGGLE_KEYS_STATE, length=LEN.TOGGLE_KEYS_STATE,
                 title="ToggleKeysState", name="toggle_keys_state",
                 checks=(CheckHexList(LEN.TOGGLE_KEYS_STATE // 8), CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, set_toggle_keys_enabled, set_fkc_enabled, fkc_enabled,
                 toggle_key_7_enabled, toggle_key_6_enabled, toggle_key_5_enabled, toggle_key_4_enabled,
                 toggle_key_3_enabled, toggle_key_2_enabled, toggle_key_1_enabled, toggle_key_0_enabled, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param set_toggle_keys_enabled: Set Toggle Keys Enabled
        :type set_toggle_keys_enabled: ``int | HexList``
        :param set_fkc_enabled: Set Fkc Enabled
        :type set_fkc_enabled: ``int | HexList``
        :param fkc_enabled: Fkc Enabled
        :type fkc_enabled: ``int | HexList``
        :param toggle_key_7_enabled: Toggle Key 7 Enabled
        :type toggle_key_7_enabled: ``int | HexList``
        :param toggle_key_6_enabled: Toggle Key 6 Enabled
        :type toggle_key_6_enabled: ``int | HexList``
        :param toggle_key_5_enabled: Toggle Key 5 Enabled
        :type toggle_key_5_enabled: ``int | HexList``
        :param toggle_key_4_enabled: Toggle Key 4 Enabled
        :type toggle_key_4_enabled: ``int | HexList``
        :param toggle_key_3_enabled: Toggle Key 3 Enabled
        :type toggle_key_3_enabled: ``int | HexList``
        :param toggle_key_2_enabled: Toggle Key 2 Enabled
        :type toggle_key_2_enabled: ``int | HexList``
        :param toggle_key_1_enabled: Toggle Key 1 Enabled
        :type toggle_key_1_enabled: ``int | HexList``
        :param toggle_key_0_enabled: Toggle Key 0 Enabled
        :type toggle_key_0_enabled: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetSetEnabledResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.set_get_fkc_state = self.SetGetFkcState(set_toggle_keys_enabled=set_toggle_keys_enabled,
                                                     set_fkc_enabled=set_fkc_enabled)
        self.fkc_state = self.FkcState(fkc_enabled=fkc_enabled)
        self.toggle_keys_state = self.ToggleKeysState(toggle_key_7_enabled=toggle_key_7_enabled,
                                                      toggle_key_6_enabled=toggle_key_6_enabled,
                                                      toggle_key_5_enabled=toggle_key_5_enabled,
                                                      toggle_key_4_enabled=toggle_key_4_enabled,
                                                      toggle_key_3_enabled=toggle_key_3_enabled,
                                                      toggle_key_2_enabled=toggle_key_2_enabled,
                                                      toggle_key_1_enabled=toggle_key_1_enabled,
                                                      toggle_key_0_enabled=toggle_key_0_enabled)
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GetSetEnabled``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.set_get_fkc_state = cls.SetGetFkcState.fromHexList(
            inner_field_container_mixin.set_get_fkc_state)
        inner_field_container_mixin.fkc_state = cls.FkcState.fromHexList(
            inner_field_container_mixin.fkc_state)
        inner_field_container_mixin.toggle_keys_state = cls.ToggleKeysState.fromHexList(
            inner_field_container_mixin.toggle_keys_state)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetSetEnabled


class GetSetSWConfigurationCookieV1(FullKeyCustomization):
    """
    Define ``GetSetSWConfigurationCookieV1`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      7
    Set Sw Configuration Cookie   1
    Sw Configuration Cookie       8
    Padding                       8
    ============================  ==========
    """

    class FID(FullKeyCustomization.FID):
        # See ``FullKeyCustomization.FID``
        RESERVED = FullKeyCustomization.FID.SOFTWARE_ID - 1
        SET_SW_CONFIGURATION_COOKIE = RESERVED - 1
        SW_CONFIGURATION_COOKIE = SET_SW_CONFIGURATION_COOKIE - 1
        PADDING = SW_CONFIGURATION_COOKIE - 1
    # end class FID

    class LEN(FullKeyCustomization.LEN):
        # See ``FullKeyCustomization.LEN``
        RESERVED = 0x7
        SET_SW_CONFIGURATION_COOKIE = 0x1
        SW_CONFIGURATION_COOKIE = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = FullKeyCustomization.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=FullKeyCustomization.DEFAULT.RESERVED),
        BitField(fid=FID.SET_SW_CONFIGURATION_COOKIE, length=LEN.SET_SW_CONFIGURATION_COOKIE,
                 title="SetSwConfigurationCookie", name="set_sw_configuration_cookie",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.SET_SW_CONFIGURATION_COOKIE) - 1),)),
        BitField(fid=FID.SW_CONFIGURATION_COOKIE, length=LEN.SW_CONFIGURATION_COOKIE,
                 title="SwConfigurationCookie", name="sw_configuration_cookie",
                 checks=(CheckHexList(LEN.SW_CONFIGURATION_COOKIE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=FullKeyCustomization.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, set_sw_configuration_cookie, sw_configuration_cookie, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param set_sw_configuration_cookie: Set Sw Configuration Cookie
        :type set_sw_configuration_cookie: ``int | HexList``
        :param sw_configuration_cookie: Sw Configuration Cookie
        :type sw_configuration_cookie: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetSetSWConfigurationCookieResponseV1.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.set_sw_configuration_cookie = set_sw_configuration_cookie
        self.sw_configuration_cookie = HexList(Numeral(sw_configuration_cookie, self.LEN.SW_CONFIGURATION_COOKIE // 8))
    # end def __init__
# end class GetSetSWConfigurationCookieV1


class GetCapabilitiesResponseV0(FullKeyCustomization):
    """
    Define ``GetCapabilitiesResponseV0`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Fkc Config File Ver           8
    Macro Def File Ver            8
    Fkc Config File Maxsize       16
    Macro Def File Maxsize        16
    Fkc Config Max Triggers       8
    Padding                       72
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilitiesV0ToV1,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(FullKeyCustomization.FID):
        # See ``FullKeyCustomization.FID``
        FKC_CONFIG_FILE_VER = FullKeyCustomization.FID.SOFTWARE_ID - 1
        MACRO_DEF_FILE_VER = FKC_CONFIG_FILE_VER - 1
        FKC_CONFIG_FILE_MAXSIZE = MACRO_DEF_FILE_VER - 1
        MACRO_DEF_FILE_MAXSIZE = FKC_CONFIG_FILE_MAXSIZE - 1
        FKC_CONFIG_MAX_TRIGGERS = MACRO_DEF_FILE_MAXSIZE - 1
        PADDING = FKC_CONFIG_MAX_TRIGGERS - 1
    # end class FID

    class LEN(FullKeyCustomization.LEN):
        # See ``FullKeyCustomization.LEN``
        FKC_CONFIG_FILE_VER = 0x8
        MACRO_DEF_FILE_VER = 0x8
        FKC_CONFIG_FILE_MAXSIZE = 0x10
        MACRO_DEF_FILE_MAXSIZE = 0x10
        FKC_CONFIG_MAX_TRIGGERS = 0x8
        PADDING = 0x48
    # end class LEN

    FIELDS = FullKeyCustomization.FIELDS + (
        BitField(fid=FID.FKC_CONFIG_FILE_VER, length=LEN.FKC_CONFIG_FILE_VER,
                 title="FkcConfigFileVer", name="fkc_config_file_ver",
                 checks=(CheckHexList(LEN.FKC_CONFIG_FILE_VER // 8), CheckByte(),)),
        BitField(fid=FID.MACRO_DEF_FILE_VER, length=LEN.MACRO_DEF_FILE_VER,
                 title="MacroDefFileVer", name="macro_def_file_ver",
                 checks=(CheckHexList(LEN.MACRO_DEF_FILE_VER // 8), CheckByte(),)),
        BitField(fid=FID.FKC_CONFIG_FILE_MAXSIZE, length=LEN.FKC_CONFIG_FILE_MAXSIZE,
                 title="FkcConfigFileMaxsize", name="fkc_config_file_maxsize",
                 checks=(CheckHexList(LEN.FKC_CONFIG_FILE_MAXSIZE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FKC_CONFIG_FILE_MAXSIZE) - 1),)),
        BitField(fid=FID.MACRO_DEF_FILE_MAXSIZE, length=LEN.MACRO_DEF_FILE_MAXSIZE,
                 title="MacroDefFileMaxsize", name="macro_def_file_maxsize",
                 checks=(CheckHexList(LEN.MACRO_DEF_FILE_MAXSIZE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.MACRO_DEF_FILE_MAXSIZE) - 1),)),
        BitField(fid=FID.FKC_CONFIG_MAX_TRIGGERS, length=LEN.FKC_CONFIG_MAX_TRIGGERS,
                 title="FkcConfigMaxTriggers", name="fkc_config_max_triggers",
                 checks=(CheckHexList(LEN.FKC_CONFIG_MAX_TRIGGERS // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=FullKeyCustomization.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, fkc_config_file_ver, macro_def_file_ver, fkc_config_file_maxsize,
                 macro_def_file_maxsize, fkc_config_max_triggers, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param fkc_config_file_ver: Fkc Config File Ver
        :type fkc_config_file_ver: ``int | HexList``
        :param macro_def_file_ver: Macro Def File Ver
        :type macro_def_file_ver: ``int | HexList``
        :param fkc_config_file_maxsize: Fkc Config File Maxsize
        :type fkc_config_file_maxsize: ``int | HexList``
        :param macro_def_file_maxsize: Macro Def File Maxsize
        :type macro_def_file_maxsize: ``int | HexList``
        :param fkc_config_max_triggers: Fkc Config Max Triggers
        :type fkc_config_max_triggers: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.fkc_config_file_ver = HexList(Numeral(fkc_config_file_ver, self.LEN.FKC_CONFIG_FILE_VER // 8))
        self.macro_def_file_ver = HexList(Numeral(macro_def_file_ver, self.LEN.MACRO_DEF_FILE_VER // 8))
        self.fkc_config_file_maxsize = HexList(Numeral(fkc_config_file_maxsize, self.LEN.FKC_CONFIG_FILE_MAXSIZE // 8))
        self.macro_def_file_maxsize = HexList(Numeral(macro_def_file_maxsize, self.LEN.MACRO_DEF_FILE_MAXSIZE // 8))
        self.fkc_config_max_triggers = HexList(Numeral(fkc_config_max_triggers, self.LEN.FKC_CONFIG_MAX_TRIGGERS // 8))
    # end def __init__
# end class GetCapabilitiesResponseV0


class GetCapabilitiesResponseV1(GetCapabilitiesResponseV0):
    """
    Define ``GetCapabilitiesResponseV1`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Fkc Config File Ver           8
    Macro Def File Ver            8
    Fkc Config File Maxsize       16
    Macro Def File Maxsize        16
    Fkc Config Max Triggers       8
    Reserved                      7
    SW Config Capabilities        1
    Padding                       64
    ============================  ==========
    """
    VERSION = (1,)

    class FID(GetCapabilitiesResponseV0.FID):
        # See ``GetCapabilitiesResponseV0.FID``
        RESERVED = GetCapabilitiesResponseV0.FID.FKC_CONFIG_MAX_TRIGGERS - 1
        SW_CONFIG_CAPABILITIES = RESERVED - 1
        PADDING = SW_CONFIG_CAPABILITIES - 1
    # end class FID

    class LEN(GetCapabilitiesResponseV0.LEN):
        # See ``FullKeyCustomization.LEN``
        RESERVED = 0x7
        SW_CONFIG_CAPABILITIES = 0x1
        PADDING = 0x40
    # end class LEN

    FIELDS = GetCapabilitiesResponseV0.FIELDS[:-1] + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=FullKeyCustomization.DEFAULT.RESERVED),
        BitField(fid=FID.SW_CONFIG_CAPABILITIES, length=LEN.SW_CONFIG_CAPABILITIES,
                 title="SwConfigCapabilities", name="sw_config_capabilities",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.SW_CONFIG_CAPABILITIES) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=FullKeyCustomization.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, fkc_config_file_ver, macro_def_file_ver, fkc_config_file_maxsize,
                 macro_def_file_maxsize, fkc_config_max_triggers, sw_config_capabilities, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param fkc_config_file_ver: Fkc Config File Ver
        :type fkc_config_file_ver: ``int | HexList``
        :param macro_def_file_ver: Macro Def File Ver
        :type macro_def_file_ver: ``int | HexList``
        :param fkc_config_file_maxsize: Fkc Config File Maxsize
        :type fkc_config_file_maxsize: ``int | HexList``
        :param macro_def_file_maxsize: Macro Def File Maxsize
        :type macro_def_file_maxsize: ``int | HexList``
        :param fkc_config_max_triggers: Fkc Config Max Triggers
        :type fkc_config_max_triggers: ``int | HexList``
        :param sw_config_capabilities: SW Config Capabilities
        :type sw_config_capabilities: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         fkc_config_file_ver=HexList(Numeral(fkc_config_file_ver, self.LEN.FKC_CONFIG_FILE_VER // 8)),
                         macro_def_file_ver=HexList(Numeral(macro_def_file_ver, self.LEN.MACRO_DEF_FILE_VER // 8)),
                         fkc_config_file_maxsize=HexList(
                             Numeral(fkc_config_file_maxsize, self.LEN.FKC_CONFIG_FILE_MAXSIZE // 8)),
                         macro_def_file_maxsize=HexList(
                             Numeral(macro_def_file_maxsize, self.LEN.MACRO_DEF_FILE_MAXSIZE // 8)),
                         fkc_config_max_triggers=HexList(
                             Numeral(fkc_config_max_triggers, self.LEN.FKC_CONFIG_MAX_TRIGGERS // 8)),
                         **kwargs)
        self.sw_config_capabilities = sw_config_capabilities
    # end def __init__
# end class GetCapabilitiesResponseV1


class GetSetPowerOnParamsResponse(FullKeyCustomization):
    """
    Define ``GetSetPowerOnParamsResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Power On Fkc State            8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetSetPowerOnParams,)
    VERSION = (0, 1)
    FUNCTION_INDEX = 1

    class FID(FullKeyCustomization.FID):
        # See ``FullKeyCustomization.FID``
        POWER_ON_FKC_STATE = FullKeyCustomization.FID.SOFTWARE_ID - 1
        PADDING = POWER_ON_FKC_STATE - 1
    # end class FID

    class LEN(FullKeyCustomization.LEN):
        # See ``FullKeyCustomization.LEN``
        POWER_ON_FKC_STATE = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = FullKeyCustomization.FIELDS + (
        BitField(fid=FID.POWER_ON_FKC_STATE, length=LEN.POWER_ON_FKC_STATE,
                 title="PowerOnFkcState", name="power_on_fkc_state",
                 checks=(CheckHexList(LEN.POWER_ON_FKC_STATE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=FullKeyCustomization.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, power_on_fkc_enable, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param power_on_fkc_enable: Power On Fkc Enable
        :type power_on_fkc_enable: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.power_on_fkc_state = self.PowerOnFkcState(power_on_fkc_enable=power_on_fkc_enable)
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GetSetPowerOnParamsResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.power_on_fkc_state = cls.PowerOnFkcState.fromHexList(
            inner_field_container_mixin.power_on_fkc_state)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetSetPowerOnParamsResponse


class GetToggleKeyListResponse(FullKeyCustomization):
    """
    Define ``GetToggleKeyListResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Toggle Key 0 Cidx              16
    Toggle Key 1 Cidx              16
    Toggle Key 2 Cidx              16
    Toggle Key 3 Cidx              16
    Toggle Key 4 Cidx              16
    Toggle Key 5 Cidx              16
    Toggle Key 6 Cidx              16
    Toggle Key 7 Cidx              16
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetToggleKeyList,)
    VERSION = (0, 1)
    FUNCTION_INDEX = 2

    class FID(FullKeyCustomization.FID):
        # See ``FullKeyCustomization.FID``
        TOGGLE_KEY_0_CIDX = FullKeyCustomization.FID.SOFTWARE_ID - 1
        TOGGLE_KEY_1_CIDX = TOGGLE_KEY_0_CIDX - 1
        TOGGLE_KEY_2_CIDX = TOGGLE_KEY_1_CIDX - 1
        TOGGLE_KEY_3_CIDX = TOGGLE_KEY_2_CIDX - 1
        TOGGLE_KEY_4_CIDX = TOGGLE_KEY_3_CIDX - 1
        TOGGLE_KEY_5_CIDX = TOGGLE_KEY_4_CIDX - 1
        TOGGLE_KEY_6_CIDX = TOGGLE_KEY_5_CIDX - 1
        TOGGLE_KEY_7_CIDX = TOGGLE_KEY_6_CIDX - 1
    # end class FID

    class LEN(FullKeyCustomization.LEN):
        # See ``FullKeyCustomization.LEN``
        TOGGLE_KEY_0_CIDX = 0x10
        TOGGLE_KEY_1_CIDX = 0x10
        TOGGLE_KEY_2_CIDX = 0x10
        TOGGLE_KEY_3_CIDX = 0x10
        TOGGLE_KEY_4_CIDX = 0x10
        TOGGLE_KEY_5_CIDX = 0x10
        TOGGLE_KEY_6_CIDX = 0x10
        TOGGLE_KEY_7_CIDX = 0x10
    # end class LEN

    FIELDS = FullKeyCustomization.FIELDS + (
        BitField(fid=FID.TOGGLE_KEY_0_CIDX, length=LEN.TOGGLE_KEY_0_CIDX,
                 title="ToggleKey0Cidx", name="toggle_key_0_cidx",
                 checks=(CheckHexList(LEN.TOGGLE_KEY_0_CIDX // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TOGGLE_KEY_0_CIDX) - 1),)),
        BitField(fid=FID.TOGGLE_KEY_1_CIDX, length=LEN.TOGGLE_KEY_1_CIDX,
                 title="ToggleKey1Cidx", name="toggle_key_1_cidx",
                 checks=(CheckHexList(LEN.TOGGLE_KEY_1_CIDX // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TOGGLE_KEY_1_CIDX) - 1),)),
        BitField(fid=FID.TOGGLE_KEY_2_CIDX, length=LEN.TOGGLE_KEY_2_CIDX,
                 title="ToggleKey2Cidx", name="toggle_key_2_cidx",
                 checks=(CheckHexList(LEN.TOGGLE_KEY_2_CIDX // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TOGGLE_KEY_2_CIDX) - 1),)),
        BitField(fid=FID.TOGGLE_KEY_3_CIDX, length=LEN.TOGGLE_KEY_3_CIDX,
                 title="ToggleKey3Cidx", name="toggle_key_3_cidx",
                 checks=(CheckHexList(LEN.TOGGLE_KEY_3_CIDX // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TOGGLE_KEY_3_CIDX) - 1),)),
        BitField(fid=FID.TOGGLE_KEY_4_CIDX, length=LEN.TOGGLE_KEY_4_CIDX,
                 title="ToggleKey4Cidx", name="toggle_key_4_cidx",
                 checks=(CheckHexList(LEN.TOGGLE_KEY_4_CIDX // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TOGGLE_KEY_4_CIDX) - 1),)),
        BitField(fid=FID.TOGGLE_KEY_5_CIDX, length=LEN.TOGGLE_KEY_5_CIDX,
                 title="ToggleKey5Cidx", name="toggle_key_5_cidx",
                 checks=(CheckHexList(LEN.TOGGLE_KEY_5_CIDX // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TOGGLE_KEY_5_CIDX) - 1),)),
        BitField(fid=FID.TOGGLE_KEY_6_CIDX, length=LEN.TOGGLE_KEY_6_CIDX,
                 title="ToggleKey6Cidx", name="toggle_key_6_cidx",
                 checks=(CheckHexList(LEN.TOGGLE_KEY_6_CIDX // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TOGGLE_KEY_6_CIDX) - 1),)),
        BitField(fid=FID.TOGGLE_KEY_7_CIDX, length=LEN.TOGGLE_KEY_7_CIDX,
                 title="ToggleKey7Cidx", name="toggle_key_7_cidx",
                 checks=(CheckHexList(LEN.TOGGLE_KEY_7_CIDX // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TOGGLE_KEY_7_CIDX) - 1),)),
    )

    def __init__(self, device_index, feature_index, toggle_key_0_cidx, toggle_key_1_cidx, toggle_key_2_cidx,
                 toggle_key_3_cidx, toggle_key_4_cidx, toggle_key_5_cidx, toggle_key_6_cidx, toggle_key_7_cidx,
                 **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param toggle_key_0_cidx: Toggle Key 0 Cidx
        :type toggle_key_0_cidx: ``HexList``
        :param toggle_key_1_cidx: Toggle Key 1 Cidx
        :type toggle_key_1_cidx: ``HexList``
        :param toggle_key_2_cidx: Toggle Key 2 Cidx
        :type toggle_key_2_cidx: ``HexList``
        :param toggle_key_3_cidx: Toggle Key 3 Cidx
        :type toggle_key_3_cidx: ``HexList``
        :param toggle_key_4_cidx: Toggle Key 4 Cidx
        :type toggle_key_4_cidx: ``HexList``
        :param toggle_key_5_cidx: Toggle Key 5 Cidx
        :type toggle_key_5_cidx: ``HexList``
        :param toggle_key_6_cidx: Toggle Key 6 Cidx
        :type toggle_key_6_cidx: ``HexList``
        :param toggle_key_7_cidx: Toggle Key 7 Cidx
        :type toggle_key_7_cidx: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        toggle_key_0_cidx_copy = HexList(toggle_key_0_cidx.copy())
        toggle_key_0_cidx_copy.addPadding(self.LEN.TOGGLE_KEY_0_CIDX // 8)
        self.toggle_key_0_cidx = toggle_key_0_cidx_copy

        toggle_key_1_cidx_copy = HexList(toggle_key_1_cidx.copy())
        toggle_key_1_cidx_copy.addPadding(self.LEN.TOGGLE_KEY_1_CIDX // 8)
        self.toggle_key_1_cidx = toggle_key_1_cidx_copy

        toggle_key_2_cidx_copy = HexList(toggle_key_2_cidx.copy())
        toggle_key_2_cidx_copy.addPadding(self.LEN.TOGGLE_KEY_2_CIDX // 8)
        self.toggle_key_2_cidx = toggle_key_2_cidx_copy

        toggle_key_3_cidx_copy = HexList(toggle_key_3_cidx.copy())
        toggle_key_3_cidx_copy.addPadding(self.LEN.TOGGLE_KEY_3_CIDX // 8)
        self.toggle_key_3_cidx = toggle_key_3_cidx_copy

        toggle_key_4_cidx_copy = HexList(toggle_key_4_cidx.copy())
        toggle_key_4_cidx_copy.addPadding(self.LEN.TOGGLE_KEY_4_CIDX // 8)
        self.toggle_key_4_cidx = toggle_key_4_cidx_copy

        toggle_key_5_cidx_copy = HexList(toggle_key_5_cidx.copy())
        toggle_key_5_cidx_copy.addPadding(self.LEN.TOGGLE_KEY_5_CIDX // 8)
        self.toggle_key_5_cidx = toggle_key_5_cidx_copy

        toggle_key_6_cidx_copy = HexList(toggle_key_6_cidx.copy())
        toggle_key_6_cidx_copy.addPadding(self.LEN.TOGGLE_KEY_6_CIDX // 8)
        self.toggle_key_6_cidx = toggle_key_6_cidx_copy

        toggle_key_7_cidx_copy = HexList(toggle_key_7_cidx.copy())
        toggle_key_7_cidx_copy.addPadding(self.LEN.TOGGLE_KEY_7_CIDX // 8)
        self.toggle_key_7_cidx = toggle_key_7_cidx_copy
    # end def __init__
# end class GetToggleKeyListResponse


class GetSetEnabledResponse(FullKeyCustomization):
    """
    Define ``GetSetEnabledResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Fkc State                     8
    Toggle Keys State             8
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetSetEnabled,)
    VERSION = (0, 1)
    FUNCTION_INDEX = 3

    class FID(FullKeyCustomization.FID):
        # See ``FullKeyCustomization.FID``
        FKC_STATE = FullKeyCustomization.FID.SOFTWARE_ID - 1
        TOGGLE_KEYS_STATE = FKC_STATE - 1
        PADDING = TOGGLE_KEYS_STATE - 1
    # end class FID

    class LEN(FullKeyCustomization.LEN):
        # See ``FullKeyCustomization.LEN``
        FKC_STATE = 0x8
        TOGGLE_KEYS_STATE = 0x8
        PADDING = 0x70
    # end class LEN

    FIELDS = FullKeyCustomization.FIELDS + (
        BitField(fid=FID.FKC_STATE, length=LEN.FKC_STATE,
                 title="FkcState", name="fkc_state",
                 checks=(CheckHexList(LEN.FKC_STATE // 8), CheckByte(),)),
        BitField(fid=FID.TOGGLE_KEYS_STATE, length=LEN.TOGGLE_KEYS_STATE,
                 title="ToggleKeysState", name="toggle_keys_state",
                 checks=(CheckHexList(LEN.TOGGLE_KEYS_STATE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=FullKeyCustomization.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, fkc_enabled, toggle_key_7_enabled, toggle_key_6_enabled,
                 toggle_key_5_enabled, toggle_key_4_enabled, toggle_key_3_enabled, toggle_key_2_enabled,
                 toggle_key_1_enabled, toggle_key_0_enabled, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param fkc_enabled: Fkc Enabled
        :type fkc_enabled: ``int | HexList``
        :param toggle_key_7_enabled: Toggle Key 7 Enabled
        :type toggle_key_7_enabled: ``int | HexList``
        :param toggle_key_6_enabled: Toggle Key 6 Enabled
        :type toggle_key_6_enabled: ``int | HexList``
        :param toggle_key_5_enabled: Toggle Key 5 Enabled
        :type toggle_key_5_enabled: ``int | HexList``
        :param toggle_key_4_enabled: Toggle Key 4 Enabled
        :type toggle_key_4_enabled: ``int | HexList``
        :param toggle_key_3_enabled: Toggle Key 3 Enabled
        :type toggle_key_3_enabled: ``int | HexList``
        :param toggle_key_2_enabled: Toggle Key 2 Enabled
        :type toggle_key_2_enabled: ``int | HexList``
        :param toggle_key_1_enabled: Toggle Key 1 Enabled
        :type toggle_key_1_enabled: ``int | HexList``
        :param toggle_key_0_enabled: Toggle Key 0 Enabled
        :type toggle_key_0_enabled: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.fkc_state = self.FkcState(fkc_enabled=fkc_enabled)
        self.toggle_keys_state = self.ToggleKeysState(toggle_key_7_enabled=toggle_key_7_enabled,
                                                      toggle_key_6_enabled=toggle_key_6_enabled,
                                                      toggle_key_5_enabled=toggle_key_5_enabled,
                                                      toggle_key_4_enabled=toggle_key_4_enabled,
                                                      toggle_key_3_enabled=toggle_key_3_enabled,
                                                      toggle_key_2_enabled=toggle_key_2_enabled,
                                                      toggle_key_1_enabled=toggle_key_1_enabled,
                                                      toggle_key_0_enabled=toggle_key_0_enabled)
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GetSetEnabledResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.fkc_state = cls.FkcState.fromHexList(
            inner_field_container_mixin.fkc_state)
        inner_field_container_mixin.toggle_keys_state = cls.ToggleKeysState.fromHexList(
            inner_field_container_mixin.toggle_keys_state)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetSetEnabledResponse


class GetSetSWConfigurationCookieResponseV1(FullKeyCustomization):
    """
    Define ``GetSetSWConfigurationCookieResponseV1`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Sw Configuration Cookie       8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetSetSWConfigurationCookieV1,)
    VERSION = (1,)
    FUNCTION_INDEX = 4

    class FID(FullKeyCustomization.FID):
        # See ``FullKeyCustomization.FID``
        SW_CONFIGURATION_COOKIE = FullKeyCustomization.FID.SOFTWARE_ID - 1
        PADDING = SW_CONFIGURATION_COOKIE - 1
    # end class FID

    class LEN(FullKeyCustomization.LEN):
        # See ``FullKeyCustomization.LEN``
        SW_CONFIGURATION_COOKIE = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = FullKeyCustomization.FIELDS + (
        BitField(fid=FID.SW_CONFIGURATION_COOKIE, length=LEN.SW_CONFIGURATION_COOKIE,
                 title="SwConfigurationCookie", name="sw_configuration_cookie",
                 checks=(CheckHexList(LEN.SW_CONFIGURATION_COOKIE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=FullKeyCustomization.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, sw_configuration_cookie, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param sw_configuration_cookie: Sw Configuration Cookie
        :type sw_configuration_cookie: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sw_configuration_cookie = HexList(Numeral(sw_configuration_cookie, self.LEN.SW_CONFIGURATION_COOKIE // 8))
    # end def __init__
# end class GetSetSWConfigurationCookieResponseV1


class BaseLayerTriggerAsListEvent(KeyTriggerAsList):
    """
    Define ``BaseLayerTriggerAsListEvent`` implementation class
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1)
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, key_trigger_0, key_trigger_1, key_trigger_2, key_trigger_3,
                 key_trigger_4, key_trigger_5, key_trigger_6, key_trigger_7, key_trigger_8, key_trigger_9,
                 key_trigger_10, key_trigger_11, key_trigger_12, key_trigger_13, key_trigger_14, key_trigger_15,
                 **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param key_trigger_0: Key Trigger 0
        :type key_trigger_0: ``int | HexList``
        :param key_trigger_1: Key Trigger 1
        :type key_trigger_1: ``int | HexList``
        :param key_trigger_2: Key Trigger 2
        :type key_trigger_2: ``int | HexList``
        :param key_trigger_3: Key Trigger 3
        :type key_trigger_3: ``int | HexList``
        :param key_trigger_4: Key Trigger 4
        :type key_trigger_4: ``int | HexList``
        :param key_trigger_5: Key Trigger 5
        :type key_trigger_5: ``int | HexList``
        :param key_trigger_6: Key Trigger 6
        :type key_trigger_6: ``int | HexList``
        :param key_trigger_7: Key Trigger 7
        :type key_trigger_7: ``int | HexList``
        :param key_trigger_8: Key Trigger 8
        :type key_trigger_8: ``int | HexList``
        :param key_trigger_9: Key Trigger 9
        :type key_trigger_9: ``int | HexList``
        :param key_trigger_10: Key Trigger 10
        :type key_trigger_10: ``int | HexList``
        :param key_trigger_11: Key Trigger 11
        :type key_trigger_11: ``int | HexList``
        :param key_trigger_12: Key Trigger 12
        :type key_trigger_12: ``int | HexList``
        :param key_trigger_13: Key Trigger 13
        :type key_trigger_13: ``int | HexList``
        :param key_trigger_14: Key Trigger 14
        :type key_trigger_14: ``int | HexList``
        :param key_trigger_15: Key Trigger 15
        :type key_trigger_15: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.key_trigger_0 = HexList(Numeral(key_trigger_0, self.LEN.KEY_TRIGGER_0 // 8))
        self.key_trigger_1 = HexList(Numeral(key_trigger_1, self.LEN.KEY_TRIGGER_1 // 8))
        self.key_trigger_2 = HexList(Numeral(key_trigger_2, self.LEN.KEY_TRIGGER_2 // 8))
        self.key_trigger_3 = HexList(Numeral(key_trigger_3, self.LEN.KEY_TRIGGER_3 // 8))
        self.key_trigger_4 = HexList(Numeral(key_trigger_4, self.LEN.KEY_TRIGGER_4 // 8))
        self.key_trigger_5 = HexList(Numeral(key_trigger_5, self.LEN.KEY_TRIGGER_5 // 8))
        self.key_trigger_6 = HexList(Numeral(key_trigger_6, self.LEN.KEY_TRIGGER_6 // 8))
        self.key_trigger_7 = HexList(Numeral(key_trigger_7, self.LEN.KEY_TRIGGER_7 // 8))
        self.key_trigger_8 = HexList(Numeral(key_trigger_8, self.LEN.KEY_TRIGGER_8 // 8))
        self.key_trigger_9 = HexList(Numeral(key_trigger_9, self.LEN.KEY_TRIGGER_9 // 8))
        self.key_trigger_10 = HexList(Numeral(key_trigger_10, self.LEN.KEY_TRIGGER_10 // 8))
        self.key_trigger_11 = HexList(Numeral(key_trigger_11, self.LEN.KEY_TRIGGER_11 // 8))
        self.key_trigger_12 = HexList(Numeral(key_trigger_12, self.LEN.KEY_TRIGGER_12 // 8))
        self.key_trigger_13 = HexList(Numeral(key_trigger_13, self.LEN.KEY_TRIGGER_13 // 8))
        self.key_trigger_14 = HexList(Numeral(key_trigger_14, self.LEN.KEY_TRIGGER_14 // 8))
        self.key_trigger_15 = HexList(Numeral(key_trigger_15, self.LEN.KEY_TRIGGER_15 // 8))
    # end def __init__
# end class BaseLayerTriggerAsListEvent


class BaseLayerTriggerAsBitmapEvent(KeyTriggerAsBitmap):
    """
    Define ``BaseLayerTriggerAsBitmapEvent`` implementation class
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, fkc_idx_7=False, fkc_idx_6=False, fkc_idx_5=False, fkc_idx_4=False,
                 fkc_idx_3=False, fkc_idx_2=False, fkc_idx_1=False, fkc_idx_0=False, fkc_idx_15=False,
                 fkc_idx_14=False, fkc_idx_13=False, fkc_idx_12=False, fkc_idx_11=False, fkc_idx_10=False,
                 fkc_idx_9=False, fkc_idx_8=False, fkc_idx_23=False, fkc_idx_22=False, fkc_idx_21=False,
                 fkc_idx_20=False, fkc_idx_19=False, fkc_idx_18=False, fkc_idx_17=False, fkc_idx_16=False,
                 fkc_idx_31=False, fkc_idx_30=False, fkc_idx_29=False, fkc_idx_28=False, fkc_idx_27=False,
                 fkc_idx_26=False, fkc_idx_25=False, fkc_idx_24=False, fkc_idx_39=False, fkc_idx_38=False,
                 fkc_idx_37=False, fkc_idx_36=False, fkc_idx_35=False, fkc_idx_34=False, fkc_idx_33=False,
                 fkc_idx_32=False, fkc_idx_47=False, fkc_idx_46=False, fkc_idx_45=False, fkc_idx_44=False,
                 fkc_idx_43=False, fkc_idx_42=False, fkc_idx_41=False, fkc_idx_40=False, fkc_idx_55=False,
                 fkc_idx_54=False, fkc_idx_53=False, fkc_idx_52=False, fkc_idx_51=False, fkc_idx_50=False,
                 fkc_idx_49=False, fkc_idx_48=False, fkc_idx_63=False, fkc_idx_62=False, fkc_idx_61=False,
                 fkc_idx_60=False, fkc_idx_59=False, fkc_idx_58=False, fkc_idx_57=False, fkc_idx_56=False,
                 fkc_idx_71=False, fkc_idx_70=False, fkc_idx_69=False, fkc_idx_68=False, fkc_idx_67=False,
                 fkc_idx_66=False, fkc_idx_65=False, fkc_idx_64=False, fkc_idx_79=False, fkc_idx_78=False,
                 fkc_idx_77=False, fkc_idx_76=False, fkc_idx_75=False, fkc_idx_74=False, fkc_idx_73=False,
                 fkc_idx_72=False, fkc_idx_87=False, fkc_idx_86=False, fkc_idx_85=False, fkc_idx_84=False,
                 fkc_idx_83=False, fkc_idx_82=False, fkc_idx_81=False, fkc_idx_80=False, fkc_idx_95=False,
                 fkc_idx_94=False, fkc_idx_93=False, fkc_idx_92=False, fkc_idx_91=False, fkc_idx_90=False,
                 fkc_idx_89=False, fkc_idx_88=False, fkc_idx_103=False, fkc_idx_102=False, fkc_idx_101=False,
                 fkc_idx_100=False, fkc_idx_99=False, fkc_idx_98=False, fkc_idx_97=False, fkc_idx_96=False,
                 fkc_idx_111=False, fkc_idx_110=False, fkc_idx_109=False, fkc_idx_108=False, fkc_idx_107=False,
                 fkc_idx_106=False, fkc_idx_105=False, fkc_idx_104=False, fkc_idx_119=False, fkc_idx_118=False,
                 fkc_idx_117=False, fkc_idx_116=False, fkc_idx_115=False, fkc_idx_114=False, fkc_idx_113=False,
                 fkc_idx_112=False, fkc_idx_127=False, fkc_idx_126=False, fkc_idx_125=False, fkc_idx_124=False,
                 fkc_idx_123=False, fkc_idx_122=False, fkc_idx_121=False, fkc_idx_120=False, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param fkc_idx_7: Fkc Idx 7 - OPTIONAL
        :type fkc_idx_7: ``int | HexList``
        :param fkc_idx_6: Fkc Idx 6 - OPTIONAL
        :type fkc_idx_6: ``int | HexList``
        :param fkc_idx_5: Fkc Idx 5 - OPTIONAL
        :type fkc_idx_5: ``int | HexList``
        :param fkc_idx_4: Fkc Idx 4 - OPTIONAL
        :type fkc_idx_4: ``int | HexList``
        :param fkc_idx_3: Fkc Idx 3 - OPTIONAL
        :type fkc_idx_3: ``int | HexList``
        :param fkc_idx_2: Fkc Idx 2 - OPTIONAL
        :type fkc_idx_2: ``int | HexList``
        :param fkc_idx_1: Fkc Idx 1 - OPTIONAL
        :type fkc_idx_1: ``int | HexList``
        :param fkc_idx_0: Fkc Idx 0 - OPTIONAL
        :type fkc_idx_0: ``int | HexList``
        :param fkc_idx_15: Fkc Idx 15 - OPTIONAL
        :type fkc_idx_15: ``int | HexList``
        :param fkc_idx_14: Fkc Idx 14 - OPTIONAL
        :type fkc_idx_14: ``int | HexList``
        :param fkc_idx_13: Fkc Idx 13 - OPTIONAL
        :type fkc_idx_13: ``int | HexList``
        :param fkc_idx_12: Fkc Idx 12 - OPTIONAL
        :type fkc_idx_12: ``int | HexList``
        :param fkc_idx_11: Fkc Idx 11 - OPTIONAL
        :type fkc_idx_11: ``int | HexList``
        :param fkc_idx_10: Fkc Idx 10 - OPTIONAL
        :type fkc_idx_10: ``int | HexList``
        :param fkc_idx_9: Fkc Idx 9 - OPTIONAL
        :type fkc_idx_9: ``int | HexList``
        :param fkc_idx_8: Fkc Idx 8 - OPTIONAL
        :type fkc_idx_8: ``int | HexList``
        :param fkc_idx_23: Fkc Idx 23 - OPTIONAL
        :type fkc_idx_23: ``int | HexList``
        :param fkc_idx_22: Fkc Idx 22 - OPTIONAL
        :type fkc_idx_22: ``int | HexList``
        :param fkc_idx_21: Fkc Idx 21 - OPTIONAL
        :type fkc_idx_21: ``int | HexList``
        :param fkc_idx_20: Fkc Idx 20 - OPTIONAL
        :type fkc_idx_20: ``int | HexList``
        :param fkc_idx_19: Fkc Idx 19 - OPTIONAL
        :type fkc_idx_19: ``int | HexList``
        :param fkc_idx_18: Fkc Idx 18 - OPTIONAL
        :type fkc_idx_18: ``int | HexList``
        :param fkc_idx_17: Fkc Idx 17 - OPTIONAL
        :type fkc_idx_17: ``int | HexList``
        :param fkc_idx_16: Fkc Idx 16 - OPTIONAL
        :type fkc_idx_16: ``int | HexList``
        :param fkc_idx_31: Fkc Idx 31 - OPTIONAL
        :type fkc_idx_31: ``int | HexList``
        :param fkc_idx_30: Fkc Idx 30 - OPTIONAL
        :type fkc_idx_30: ``int | HexList``
        :param fkc_idx_29: Fkc Idx 29 - OPTIONAL
        :type fkc_idx_29: ``int | HexList``
        :param fkc_idx_28: Fkc Idx 28 - OPTIONAL
        :type fkc_idx_28: ``int | HexList``
        :param fkc_idx_27: Fkc Idx 27 - OPTIONAL
        :type fkc_idx_27: ``int | HexList``
        :param fkc_idx_26: Fkc Idx 26 - OPTIONAL
        :type fkc_idx_26: ``int | HexList``
        :param fkc_idx_25: Fkc Idx 25 - OPTIONAL
        :type fkc_idx_25: ``int | HexList``
        :param fkc_idx_24: Fkc Idx 24 - OPTIONAL
        :type fkc_idx_24: ``int | HexList``
        :param fkc_idx_39: Fkc Idx 39 - OPTIONAL
        :type fkc_idx_39: ``int | HexList``
        :param fkc_idx_38: Fkc Idx 38 - OPTIONAL
        :type fkc_idx_38: ``int | HexList``
        :param fkc_idx_37: Fkc Idx 37 - OPTIONAL
        :type fkc_idx_37: ``int | HexList``
        :param fkc_idx_36: Fkc Idx 36 - OPTIONAL
        :type fkc_idx_36: ``int | HexList``
        :param fkc_idx_35: Fkc Idx 35 - OPTIONAL
        :type fkc_idx_35: ``int | HexList``
        :param fkc_idx_34: Fkc Idx 34 - OPTIONAL
        :type fkc_idx_34: ``int | HexList``
        :param fkc_idx_33: Fkc Idx 33 - OPTIONAL
        :type fkc_idx_33: ``int | HexList``
        :param fkc_idx_32: Fkc Idx 32 - OPTIONAL
        :type fkc_idx_32: ``int | HexList``
        :param fkc_idx_47: Fkc Idx 47 - OPTIONAL
        :type fkc_idx_47: ``int | HexList``
        :param fkc_idx_46: Fkc Idx 46 - OPTIONAL
        :type fkc_idx_46: ``int | HexList``
        :param fkc_idx_45: Fkc Idx 45 - OPTIONAL
        :type fkc_idx_45: ``int | HexList``
        :param fkc_idx_44: Fkc Idx 44 - OPTIONAL
        :type fkc_idx_44: ``int | HexList``
        :param fkc_idx_43: Fkc Idx 43 - OPTIONAL
        :type fkc_idx_43: ``int | HexList``
        :param fkc_idx_42: Fkc Idx 42 - OPTIONAL
        :type fkc_idx_42: ``int | HexList``
        :param fkc_idx_41: Fkc Idx 41 - OPTIONAL
        :type fkc_idx_41: ``int | HexList``
        :param fkc_idx_40: Fkc Idx 40 - OPTIONAL
        :type fkc_idx_40: ``int | HexList``
        :param fkc_idx_55: Fkc Idx 55 - OPTIONAL
        :type fkc_idx_55: ``int | HexList``
        :param fkc_idx_54: Fkc Idx 54 - OPTIONAL
        :type fkc_idx_54: ``int | HexList``
        :param fkc_idx_53: Fkc Idx 53 - OPTIONAL
        :type fkc_idx_53: ``int | HexList``
        :param fkc_idx_52: Fkc Idx 52 - OPTIONAL
        :type fkc_idx_52: ``int | HexList``
        :param fkc_idx_51: Fkc Idx 51 - OPTIONAL
        :type fkc_idx_51: ``int | HexList``
        :param fkc_idx_50: Fkc Idx 50 - OPTIONAL
        :type fkc_idx_50: ``int | HexList``
        :param fkc_idx_49: Fkc Idx 49 - OPTIONAL
        :type fkc_idx_49: ``int | HexList``
        :param fkc_idx_48: Fkc Idx 48 - OPTIONAL
        :type fkc_idx_48: ``int | HexList``
        :param fkc_idx_63: Fkc Idx 63 - OPTIONAL
        :type fkc_idx_63: ``int | HexList``
        :param fkc_idx_62: Fkc Idx 62 - OPTIONAL
        :type fkc_idx_62: ``int | HexList``
        :param fkc_idx_61: Fkc Idx 61 - OPTIONAL
        :type fkc_idx_61: ``int | HexList``
        :param fkc_idx_60: Fkc Idx 60 - OPTIONAL
        :type fkc_idx_60: ``int | HexList``
        :param fkc_idx_59: Fkc Idx 59 - OPTIONAL
        :type fkc_idx_59: ``int | HexList``
        :param fkc_idx_58: Fkc Idx 58 - OPTIONAL
        :type fkc_idx_58: ``int | HexList``
        :param fkc_idx_57: Fkc Idx 57 - OPTIONAL
        :type fkc_idx_57: ``int | HexList``
        :param fkc_idx_56: Fkc Idx 56 - OPTIONAL
        :type fkc_idx_56: ``int | HexList``
        :param fkc_idx_71: Fkc Idx 71 - OPTIONAL
        :type fkc_idx_71: ``int | HexList``
        :param fkc_idx_70: Fkc Idx 70 - OPTIONAL
        :type fkc_idx_70: ``int | HexList``
        :param fkc_idx_69: Fkc Idx 69 - OPTIONAL
        :type fkc_idx_69: ``int | HexList``
        :param fkc_idx_68: Fkc Idx 68 - OPTIONAL
        :type fkc_idx_68: ``int | HexList``
        :param fkc_idx_67: Fkc Idx 67 - OPTIONAL
        :type fkc_idx_67: ``int | HexList``
        :param fkc_idx_66: Fkc Idx 66 - OPTIONAL
        :type fkc_idx_66: ``int | HexList``
        :param fkc_idx_65: Fkc Idx 65 - OPTIONAL
        :type fkc_idx_65: ``int | HexList``
        :param fkc_idx_64: Fkc Idx 64 - OPTIONAL
        :type fkc_idx_64: ``int | HexList``
        :param fkc_idx_79: Fkc Idx 79 - OPTIONAL
        :type fkc_idx_79: ``int | HexList``
        :param fkc_idx_78: Fkc Idx 78 - OPTIONAL
        :type fkc_idx_78: ``int | HexList``
        :param fkc_idx_77: Fkc Idx 77 - OPTIONAL
        :type fkc_idx_77: ``int | HexList``
        :param fkc_idx_76: Fkc Idx 76 - OPTIONAL
        :type fkc_idx_76: ``int | HexList``
        :param fkc_idx_75: Fkc Idx 75 - OPTIONAL
        :type fkc_idx_75: ``int | HexList``
        :param fkc_idx_74: Fkc Idx 74 - OPTIONAL
        :type fkc_idx_74: ``int | HexList``
        :param fkc_idx_73: Fkc Idx 73 - OPTIONAL
        :type fkc_idx_73: ``int | HexList``
        :param fkc_idx_72: Fkc Idx 72 - OPTIONAL
        :type fkc_idx_72: ``int | HexList``
        :param fkc_idx_87: Fkc Idx 87 - OPTIONAL
        :type fkc_idx_87: ``int | HexList``
        :param fkc_idx_86: Fkc Idx 86 - OPTIONAL
        :type fkc_idx_86: ``int | HexList``
        :param fkc_idx_85: Fkc Idx 85 - OPTIONAL
        :type fkc_idx_85: ``int | HexList``
        :param fkc_idx_84: Fkc Idx 84 - OPTIONAL
        :type fkc_idx_84: ``int | HexList``
        :param fkc_idx_83: Fkc Idx 83 - OPTIONAL
        :type fkc_idx_83: ``int | HexList``
        :param fkc_idx_82: Fkc Idx 82 - OPTIONAL
        :type fkc_idx_82: ``int | HexList``
        :param fkc_idx_81: Fkc Idx 81 - OPTIONAL
        :type fkc_idx_81: ``int | HexList``
        :param fkc_idx_80: Fkc Idx 80 - OPTIONAL
        :type fkc_idx_80: ``int | HexList``
        :param fkc_idx_95: Fkc Idx 95 - OPTIONAL
        :type fkc_idx_95: ``int | HexList``
        :param fkc_idx_94: Fkc Idx 94 - OPTIONAL
        :type fkc_idx_94: ``int | HexList``
        :param fkc_idx_93: Fkc Idx 93 - OPTIONAL
        :type fkc_idx_93: ``int | HexList``
        :param fkc_idx_92: Fkc Idx 92 - OPTIONAL
        :type fkc_idx_92: ``int | HexList``
        :param fkc_idx_91: Fkc Idx 91 - OPTIONAL
        :type fkc_idx_91: ``int | HexList``
        :param fkc_idx_90: Fkc Idx 90 - OPTIONAL
        :type fkc_idx_90: ``int | HexList``
        :param fkc_idx_89: Fkc Idx 89 - OPTIONAL
        :type fkc_idx_89: ``int | HexList``
        :param fkc_idx_88: Fkc Idx 88 - OPTIONAL
        :type fkc_idx_88: ``int | HexList``
        :param fkc_idx_103: Fkc Idx 103 - OPTIONAL
        :type fkc_idx_103: ``int | HexList``
        :param fkc_idx_102: Fkc Idx 102 - OPTIONAL
        :type fkc_idx_102: ``int | HexList``
        :param fkc_idx_101: Fkc Idx 101 - OPTIONAL
        :type fkc_idx_101: ``int | HexList``
        :param fkc_idx_100: Fkc Idx 100 - OPTIONAL
        :type fkc_idx_100: ``int | HexList``
        :param fkc_idx_99: Fkc Idx 99 - OPTIONAL
        :type fkc_idx_99: ``int | HexList``
        :param fkc_idx_98: Fkc Idx 98 - OPTIONAL
        :type fkc_idx_98: ``int | HexList``
        :param fkc_idx_97: Fkc Idx 97 - OPTIONAL
        :type fkc_idx_97: ``int | HexList``
        :param fkc_idx_96: Fkc Idx 96 - OPTIONAL
        :type fkc_idx_96: ``int | HexList``
        :param fkc_idx_111: Fkc Idx 111 - OPTIONAL
        :type fkc_idx_111: ``int | HexList``
        :param fkc_idx_110: Fkc Idx 110 - OPTIONAL
        :type fkc_idx_110: ``int | HexList``
        :param fkc_idx_109: Fkc Idx 109 - OPTIONAL
        :type fkc_idx_109: ``int | HexList``
        :param fkc_idx_108: Fkc Idx 108 - OPTIONAL
        :type fkc_idx_108: ``int | HexList``
        :param fkc_idx_107: Fkc Idx 107 - OPTIONAL
        :type fkc_idx_107: ``int | HexList``
        :param fkc_idx_106: Fkc Idx 106 - OPTIONAL
        :type fkc_idx_106: ``int | HexList``
        :param fkc_idx_105: Fkc Idx 105 - OPTIONAL
        :type fkc_idx_105: ``int | HexList``
        :param fkc_idx_104: Fkc Idx 104 - OPTIONAL
        :type fkc_idx_104: ``int | HexList``
        :param fkc_idx_119: Fkc Idx 119 - OPTIONAL
        :type fkc_idx_119: ``int | HexList``
        :param fkc_idx_118: Fkc Idx 118 - OPTIONAL
        :type fkc_idx_118: ``int | HexList``
        :param fkc_idx_117: Fkc Idx 117 - OPTIONAL
        :type fkc_idx_117: ``int | HexList``
        :param fkc_idx_116: Fkc Idx 116 - OPTIONAL
        :type fkc_idx_116: ``int | HexList``
        :param fkc_idx_115: Fkc Idx 115 - OPTIONAL
        :type fkc_idx_115: ``int | HexList``
        :param fkc_idx_114: Fkc Idx 114 - OPTIONAL
        :type fkc_idx_114: ``int | HexList``
        :param fkc_idx_113: Fkc Idx 113 - OPTIONAL
        :type fkc_idx_113: ``int | HexList``
        :param fkc_idx_112: Fkc Idx 112 - OPTIONAL
        :type fkc_idx_112: ``int | HexList``
        :param fkc_idx_127: Fkc Idx 127 - OPTIONAL
        :type fkc_idx_127: ``int | HexList``
        :param fkc_idx_126: Fkc Idx 126 - OPTIONAL
        :type fkc_idx_126: ``int | HexList``
        :param fkc_idx_125: Fkc Idx 125 - OPTIONAL
        :type fkc_idx_125: ``int | HexList``
        :param fkc_idx_124: Fkc Idx 124 - OPTIONAL
        :type fkc_idx_124: ``int | HexList``
        :param fkc_idx_123: Fkc Idx 123 - OPTIONAL
        :type fkc_idx_123: ``int | HexList``
        :param fkc_idx_122: Fkc Idx 122 - OPTIONAL
        :type fkc_idx_122: ``int | HexList``
        :param fkc_idx_121: Fkc Idx 121 - OPTIONAL
        :type fkc_idx_121: ``int | HexList``
        :param fkc_idx_120: Fkc Idx 120 - OPTIONAL
        :type fkc_idx_120: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.key_trigger_bitmap = self.KeyTriggerBitmap(fkc_idx_7=fkc_idx_7, fkc_idx_6=fkc_idx_6,
                                                        fkc_idx_5=fkc_idx_5, fkc_idx_4=fkc_idx_4,
                                                        fkc_idx_3=fkc_idx_3, fkc_idx_2=fkc_idx_2,
                                                        fkc_idx_1=fkc_idx_1, fkc_idx_0=fkc_idx_0,
                                                        fkc_idx_15=fkc_idx_15, fkc_idx_14=fkc_idx_14,
                                                        fkc_idx_13=fkc_idx_13, fkc_idx_12=fkc_idx_12,
                                                        fkc_idx_11=fkc_idx_11, fkc_idx_10=fkc_idx_10,
                                                        fkc_idx_9=fkc_idx_9, fkc_idx_8=fkc_idx_8,
                                                        fkc_idx_23=fkc_idx_23, fkc_idx_22=fkc_idx_22,
                                                        fkc_idx_21=fkc_idx_21, fkc_idx_20=fkc_idx_20,
                                                        fkc_idx_19=fkc_idx_19, fkc_idx_18=fkc_idx_18,
                                                        fkc_idx_17=fkc_idx_17, fkc_idx_16=fkc_idx_16,
                                                        fkc_idx_31=fkc_idx_31, fkc_idx_30=fkc_idx_30,
                                                        fkc_idx_29=fkc_idx_29, fkc_idx_28=fkc_idx_28,
                                                        fkc_idx_27=fkc_idx_27, fkc_idx_26=fkc_idx_26,
                                                        fkc_idx_25=fkc_idx_25, fkc_idx_24=fkc_idx_24,
                                                        fkc_idx_39=fkc_idx_39, fkc_idx_38=fkc_idx_38,
                                                        fkc_idx_37=fkc_idx_37, fkc_idx_36=fkc_idx_36,
                                                        fkc_idx_35=fkc_idx_35, fkc_idx_34=fkc_idx_34,
                                                        fkc_idx_33=fkc_idx_33, fkc_idx_32=fkc_idx_32,
                                                        fkc_idx_47=fkc_idx_47, fkc_idx_46=fkc_idx_46,
                                                        fkc_idx_45=fkc_idx_45, fkc_idx_44=fkc_idx_44,
                                                        fkc_idx_43=fkc_idx_43, fkc_idx_42=fkc_idx_42,
                                                        fkc_idx_41=fkc_idx_41, fkc_idx_40=fkc_idx_40,
                                                        fkc_idx_55=fkc_idx_55, fkc_idx_54=fkc_idx_54,
                                                        fkc_idx_53=fkc_idx_53, fkc_idx_52=fkc_idx_52,
                                                        fkc_idx_51=fkc_idx_51, fkc_idx_50=fkc_idx_50,
                                                        fkc_idx_49=fkc_idx_49, fkc_idx_48=fkc_idx_48,
                                                        fkc_idx_63=fkc_idx_63, fkc_idx_62=fkc_idx_62,
                                                        fkc_idx_61=fkc_idx_61, fkc_idx_60=fkc_idx_60,
                                                        fkc_idx_59=fkc_idx_59, fkc_idx_58=fkc_idx_58,
                                                        fkc_idx_57=fkc_idx_57, fkc_idx_56=fkc_idx_56,
                                                        fkc_idx_71=fkc_idx_71, fkc_idx_70=fkc_idx_70,
                                                        fkc_idx_69=fkc_idx_69, fkc_idx_68=fkc_idx_68,
                                                        fkc_idx_67=fkc_idx_67, fkc_idx_66=fkc_idx_66,
                                                        fkc_idx_65=fkc_idx_65, fkc_idx_64=fkc_idx_64,
                                                        fkc_idx_79=fkc_idx_79, fkc_idx_78=fkc_idx_78,
                                                        fkc_idx_77=fkc_idx_77, fkc_idx_76=fkc_idx_76,
                                                        fkc_idx_75=fkc_idx_75, fkc_idx_74=fkc_idx_74,
                                                        fkc_idx_73=fkc_idx_73, fkc_idx_72=fkc_idx_72,
                                                        fkc_idx_87=fkc_idx_87, fkc_idx_86=fkc_idx_86,
                                                        fkc_idx_85=fkc_idx_85, fkc_idx_84=fkc_idx_84,
                                                        fkc_idx_83=fkc_idx_83, fkc_idx_82=fkc_idx_82,
                                                        fkc_idx_81=fkc_idx_81, fkc_idx_80=fkc_idx_80,
                                                        fkc_idx_95=fkc_idx_95, fkc_idx_94=fkc_idx_94,
                                                        fkc_idx_93=fkc_idx_93, fkc_idx_92=fkc_idx_92,
                                                        fkc_idx_91=fkc_idx_91, fkc_idx_90=fkc_idx_90,
                                                        fkc_idx_89=fkc_idx_89, fkc_idx_88=fkc_idx_88,
                                                        fkc_idx_103=fkc_idx_103, fkc_idx_102=fkc_idx_102,
                                                        fkc_idx_101=fkc_idx_101, fkc_idx_100=fkc_idx_100,
                                                        fkc_idx_99=fkc_idx_99, fkc_idx_98=fkc_idx_98,
                                                        fkc_idx_97=fkc_idx_97, fkc_idx_96=fkc_idx_96,
                                                        fkc_idx_111=fkc_idx_111, fkc_idx_110=fkc_idx_110,
                                                        fkc_idx_109=fkc_idx_109, fkc_idx_108=fkc_idx_108,
                                                        fkc_idx_107=fkc_idx_107, fkc_idx_106=fkc_idx_106,
                                                        fkc_idx_105=fkc_idx_105, fkc_idx_104=fkc_idx_104,
                                                        fkc_idx_119=fkc_idx_119, fkc_idx_118=fkc_idx_118,
                                                        fkc_idx_117=fkc_idx_117, fkc_idx_116=fkc_idx_116,
                                                        fkc_idx_115=fkc_idx_115, fkc_idx_114=fkc_idx_114,
                                                        fkc_idx_113=fkc_idx_113, fkc_idx_112=fkc_idx_112,
                                                        fkc_idx_127=fkc_idx_127, fkc_idx_126=fkc_idx_126,
                                                        fkc_idx_125=fkc_idx_125, fkc_idx_124=fkc_idx_124,
                                                        fkc_idx_123=fkc_idx_123, fkc_idx_122=fkc_idx_122,
                                                        fkc_idx_121=fkc_idx_121, fkc_idx_120=fkc_idx_120)
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``BaseLayerTriggerAsBitmapEvent``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.key_trigger_bitmap = cls.KeyTriggerBitmap.fromHexList(
            inner_field_container_mixin.key_trigger_bitmap)
        return inner_field_container_mixin
    # end def fromHexList
# end class BaseLayerTriggerAsBitmapEvent


class FNLayerTriggerAsListEvent(KeyTriggerAsList):
    """
    Define ``FNLayerTriggerAsListEvent`` implementation class
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1)
    FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, key_trigger_0, key_trigger_1, key_trigger_2, key_trigger_3,
                 key_trigger_4, key_trigger_5, key_trigger_6, key_trigger_7, key_trigger_8, key_trigger_9,
                 key_trigger_10, key_trigger_11, key_trigger_12, key_trigger_13, key_trigger_14, key_trigger_15,
                 **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param key_trigger_0: Key Trigger 0
        :type key_trigger_0: ``int | HexList``
        :param key_trigger_1: Key Trigger 1
        :type key_trigger_1: ``int | HexList``
        :param key_trigger_2: Key Trigger 2
        :type key_trigger_2: ``int | HexList``
        :param key_trigger_3: Key Trigger 3
        :type key_trigger_3: ``int | HexList``
        :param key_trigger_4: Key Trigger 4
        :type key_trigger_4: ``int | HexList``
        :param key_trigger_5: Key Trigger 5
        :type key_trigger_5: ``int | HexList``
        :param key_trigger_6: Key Trigger 6
        :type key_trigger_6: ``int | HexList``
        :param key_trigger_7: Key Trigger 7
        :type key_trigger_7: ``int | HexList``
        :param key_trigger_8: Key Trigger 8
        :type key_trigger_8: ``int | HexList``
        :param key_trigger_9: Key Trigger 9
        :type key_trigger_9: ``int | HexList``
        :param key_trigger_10: Key Trigger 10
        :type key_trigger_10: ``int | HexList``
        :param key_trigger_11: Key Trigger 11
        :type key_trigger_11: ``int | HexList``
        :param key_trigger_12: Key Trigger 12
        :type key_trigger_12: ``int | HexList``
        :param key_trigger_13: Key Trigger 13
        :type key_trigger_13: ``int | HexList``
        :param key_trigger_14: Key Trigger 14
        :type key_trigger_14: ``int | HexList``
        :param key_trigger_15: Key Trigger 15
        :type key_trigger_15: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.key_trigger_0 = HexList(Numeral(key_trigger_0, self.LEN.KEY_TRIGGER_0 // 8))
        self.key_trigger_1 = HexList(Numeral(key_trigger_1, self.LEN.KEY_TRIGGER_1 // 8))
        self.key_trigger_2 = HexList(Numeral(key_trigger_2, self.LEN.KEY_TRIGGER_2 // 8))
        self.key_trigger_3 = HexList(Numeral(key_trigger_3, self.LEN.KEY_TRIGGER_3 // 8))
        self.key_trigger_4 = HexList(Numeral(key_trigger_4, self.LEN.KEY_TRIGGER_4 // 8))
        self.key_trigger_5 = HexList(Numeral(key_trigger_5, self.LEN.KEY_TRIGGER_5 // 8))
        self.key_trigger_6 = HexList(Numeral(key_trigger_6, self.LEN.KEY_TRIGGER_6 // 8))
        self.key_trigger_7 = HexList(Numeral(key_trigger_7, self.LEN.KEY_TRIGGER_7 // 8))
        self.key_trigger_8 = HexList(Numeral(key_trigger_8, self.LEN.KEY_TRIGGER_8 // 8))
        self.key_trigger_9 = HexList(Numeral(key_trigger_9, self.LEN.KEY_TRIGGER_9 // 8))
        self.key_trigger_10 = HexList(Numeral(key_trigger_10, self.LEN.KEY_TRIGGER_10 // 8))
        self.key_trigger_11 = HexList(Numeral(key_trigger_11, self.LEN.KEY_TRIGGER_11 // 8))
        self.key_trigger_12 = HexList(Numeral(key_trigger_12, self.LEN.KEY_TRIGGER_12 // 8))
        self.key_trigger_13 = HexList(Numeral(key_trigger_13, self.LEN.KEY_TRIGGER_13 // 8))
        self.key_trigger_14 = HexList(Numeral(key_trigger_14, self.LEN.KEY_TRIGGER_14 // 8))
        self.key_trigger_15 = HexList(Numeral(key_trigger_15, self.LEN.KEY_TRIGGER_15 // 8))
    # end def __init__
# end class FNLayerTriggerAsListEvent


class FNLayerTriggerAsBitmapEvent(KeyTriggerAsBitmap):
    """
    Define ``FNLayerTriggerAsBitmapEvent`` implementation class
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, fkc_idx_7=False, fkc_idx_6=False, fkc_idx_5=False, fkc_idx_4=False,
                 fkc_idx_3=False, fkc_idx_2=False, fkc_idx_1=False, fkc_idx_0=False, fkc_idx_15=False,
                 fkc_idx_14=False, fkc_idx_13=False, fkc_idx_12=False, fkc_idx_11=False, fkc_idx_10=False,
                 fkc_idx_9=False, fkc_idx_8=False, fkc_idx_23=False, fkc_idx_22=False, fkc_idx_21=False,
                 fkc_idx_20=False, fkc_idx_19=False, fkc_idx_18=False, fkc_idx_17=False, fkc_idx_16=False,
                 fkc_idx_31=False, fkc_idx_30=False, fkc_idx_29=False, fkc_idx_28=False, fkc_idx_27=False,
                 fkc_idx_26=False, fkc_idx_25=False, fkc_idx_24=False, fkc_idx_39=False, fkc_idx_38=False,
                 fkc_idx_37=False, fkc_idx_36=False, fkc_idx_35=False, fkc_idx_34=False, fkc_idx_33=False,
                 fkc_idx_32=False, fkc_idx_47=False, fkc_idx_46=False, fkc_idx_45=False, fkc_idx_44=False,
                 fkc_idx_43=False, fkc_idx_42=False, fkc_idx_41=False, fkc_idx_40=False, fkc_idx_55=False,
                 fkc_idx_54=False, fkc_idx_53=False, fkc_idx_52=False, fkc_idx_51=False, fkc_idx_50=False,
                 fkc_idx_49=False, fkc_idx_48=False, fkc_idx_63=False, fkc_idx_62=False, fkc_idx_61=False,
                 fkc_idx_60=False, fkc_idx_59=False, fkc_idx_58=False, fkc_idx_57=False, fkc_idx_56=False,
                 fkc_idx_71=False, fkc_idx_70=False, fkc_idx_69=False, fkc_idx_68=False, fkc_idx_67=False,
                 fkc_idx_66=False, fkc_idx_65=False, fkc_idx_64=False, fkc_idx_79=False, fkc_idx_78=False,
                 fkc_idx_77=False, fkc_idx_76=False, fkc_idx_75=False, fkc_idx_74=False, fkc_idx_73=False,
                 fkc_idx_72=False, fkc_idx_87=False, fkc_idx_86=False, fkc_idx_85=False, fkc_idx_84=False,
                 fkc_idx_83=False, fkc_idx_82=False, fkc_idx_81=False, fkc_idx_80=False, fkc_idx_95=False,
                 fkc_idx_94=False, fkc_idx_93=False, fkc_idx_92=False, fkc_idx_91=False, fkc_idx_90=False,
                 fkc_idx_89=False, fkc_idx_88=False, fkc_idx_103=False, fkc_idx_102=False, fkc_idx_101=False,
                 fkc_idx_100=False, fkc_idx_99=False, fkc_idx_98=False, fkc_idx_97=False, fkc_idx_96=False,
                 fkc_idx_111=False, fkc_idx_110=False, fkc_idx_109=False, fkc_idx_108=False, fkc_idx_107=False,
                 fkc_idx_106=False, fkc_idx_105=False, fkc_idx_104=False, fkc_idx_119=False, fkc_idx_118=False,
                 fkc_idx_117=False, fkc_idx_116=False, fkc_idx_115=False, fkc_idx_114=False, fkc_idx_113=False,
                 fkc_idx_112=False, fkc_idx_127=False, fkc_idx_126=False, fkc_idx_125=False, fkc_idx_124=False,
                 fkc_idx_123=False, fkc_idx_122=False, fkc_idx_121=False, fkc_idx_120=False, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param fkc_idx_7: Fkc Idx 7 - OPTIONAL
        :type fkc_idx_7: ``int | HexList``
        :param fkc_idx_6: Fkc Idx 6 - OPTIONAL
        :type fkc_idx_6: ``int | HexList``
        :param fkc_idx_5: Fkc Idx 5 - OPTIONAL
        :type fkc_idx_5: ``int | HexList``
        :param fkc_idx_4: Fkc Idx 4 - OPTIONAL
        :type fkc_idx_4: ``int | HexList``
        :param fkc_idx_3: Fkc Idx 3 - OPTIONAL
        :type fkc_idx_3: ``int | HexList``
        :param fkc_idx_2: Fkc Idx 2 - OPTIONAL
        :type fkc_idx_2: ``int | HexList``
        :param fkc_idx_1: Fkc Idx 1 - OPTIONAL
        :type fkc_idx_1: ``int | HexList``
        :param fkc_idx_0: Fkc Idx 0 - OPTIONAL
        :type fkc_idx_0: ``int | HexList``
        :param fkc_idx_15: Fkc Idx 15 - OPTIONAL
        :type fkc_idx_15: ``int | HexList``
        :param fkc_idx_14: Fkc Idx 14 - OPTIONAL
        :type fkc_idx_14: ``int | HexList``
        :param fkc_idx_13: Fkc Idx 13 - OPTIONAL
        :type fkc_idx_13: ``int | HexList``
        :param fkc_idx_12: Fkc Idx 12 - OPTIONAL
        :type fkc_idx_12: ``int | HexList``
        :param fkc_idx_11: Fkc Idx 11 - OPTIONAL
        :type fkc_idx_11: ``int | HexList``
        :param fkc_idx_10: Fkc Idx 10 - OPTIONAL
        :type fkc_idx_10: ``int | HexList``
        :param fkc_idx_9: Fkc Idx 9 - OPTIONAL
        :type fkc_idx_9: ``int | HexList``
        :param fkc_idx_8: Fkc Idx 8 - OPTIONAL
        :type fkc_idx_8: ``int | HexList``
        :param fkc_idx_23: Fkc Idx 23 - OPTIONAL
        :type fkc_idx_23: ``int | HexList``
        :param fkc_idx_22: Fkc Idx 22 - OPTIONAL
        :type fkc_idx_22: ``int | HexList``
        :param fkc_idx_21: Fkc Idx 21 - OPTIONAL
        :type fkc_idx_21: ``int | HexList``
        :param fkc_idx_20: Fkc Idx 20 - OPTIONAL
        :type fkc_idx_20: ``int | HexList``
        :param fkc_idx_19: Fkc Idx 19 - OPTIONAL
        :type fkc_idx_19: ``int | HexList``
        :param fkc_idx_18: Fkc Idx 18 - OPTIONAL
        :type fkc_idx_18: ``int | HexList``
        :param fkc_idx_17: Fkc Idx 17 - OPTIONAL
        :type fkc_idx_17: ``int | HexList``
        :param fkc_idx_16: Fkc Idx 16 - OPTIONAL
        :type fkc_idx_16: ``int | HexList``
        :param fkc_idx_31: Fkc Idx 31 - OPTIONAL
        :type fkc_idx_31: ``int | HexList``
        :param fkc_idx_30: Fkc Idx 30 - OPTIONAL
        :type fkc_idx_30: ``int | HexList``
        :param fkc_idx_29: Fkc Idx 29 - OPTIONAL
        :type fkc_idx_29: ``int | HexList``
        :param fkc_idx_28: Fkc Idx 28 - OPTIONAL
        :type fkc_idx_28: ``int | HexList``
        :param fkc_idx_27: Fkc Idx 27 - OPTIONAL
        :type fkc_idx_27: ``int | HexList``
        :param fkc_idx_26: Fkc Idx 26 - OPTIONAL
        :type fkc_idx_26: ``int | HexList``
        :param fkc_idx_25: Fkc Idx 25 - OPTIONAL
        :type fkc_idx_25: ``int | HexList``
        :param fkc_idx_24: Fkc Idx 24 - OPTIONAL
        :type fkc_idx_24: ``int | HexList``
        :param fkc_idx_39: Fkc Idx 39 - OPTIONAL
        :type fkc_idx_39: ``int | HexList``
        :param fkc_idx_38: Fkc Idx 38 - OPTIONAL
        :type fkc_idx_38: ``int | HexList``
        :param fkc_idx_37: Fkc Idx 37 - OPTIONAL
        :type fkc_idx_37: ``int | HexList``
        :param fkc_idx_36: Fkc Idx 36 - OPTIONAL
        :type fkc_idx_36: ``int | HexList``
        :param fkc_idx_35: Fkc Idx 35 - OPTIONAL
        :type fkc_idx_35: ``int | HexList``
        :param fkc_idx_34: Fkc Idx 34 - OPTIONAL
        :type fkc_idx_34: ``int | HexList``
        :param fkc_idx_33: Fkc Idx 33 - OPTIONAL
        :type fkc_idx_33: ``int | HexList``
        :param fkc_idx_32: Fkc Idx 32 - OPTIONAL
        :type fkc_idx_32: ``int | HexList``
        :param fkc_idx_47: Fkc Idx 47 - OPTIONAL
        :type fkc_idx_47: ``int | HexList``
        :param fkc_idx_46: Fkc Idx 46 - OPTIONAL
        :type fkc_idx_46: ``int | HexList``
        :param fkc_idx_45: Fkc Idx 45 - OPTIONAL
        :type fkc_idx_45: ``int | HexList``
        :param fkc_idx_44: Fkc Idx 44 - OPTIONAL
        :type fkc_idx_44: ``int | HexList``
        :param fkc_idx_43: Fkc Idx 43 - OPTIONAL
        :type fkc_idx_43: ``int | HexList``
        :param fkc_idx_42: Fkc Idx 42 - OPTIONAL
        :type fkc_idx_42: ``int | HexList``
        :param fkc_idx_41: Fkc Idx 41 - OPTIONAL
        :type fkc_idx_41: ``int | HexList``
        :param fkc_idx_40: Fkc Idx 40 - OPTIONAL
        :type fkc_idx_40: ``int | HexList``
        :param fkc_idx_55: Fkc Idx 55 - OPTIONAL
        :type fkc_idx_55: ``int | HexList``
        :param fkc_idx_54: Fkc Idx 54 - OPTIONAL
        :type fkc_idx_54: ``int | HexList``
        :param fkc_idx_53: Fkc Idx 53 - OPTIONAL
        :type fkc_idx_53: ``int | HexList``
        :param fkc_idx_52: Fkc Idx 52 - OPTIONAL
        :type fkc_idx_52: ``int | HexList``
        :param fkc_idx_51: Fkc Idx 51 - OPTIONAL
        :type fkc_idx_51: ``int | HexList``
        :param fkc_idx_50: Fkc Idx 50 - OPTIONAL
        :type fkc_idx_50: ``int | HexList``
        :param fkc_idx_49: Fkc Idx 49 - OPTIONAL
        :type fkc_idx_49: ``int | HexList``
        :param fkc_idx_48: Fkc Idx 48 - OPTIONAL
        :type fkc_idx_48: ``int | HexList``
        :param fkc_idx_63: Fkc Idx 63 - OPTIONAL
        :type fkc_idx_63: ``int | HexList``
        :param fkc_idx_62: Fkc Idx 62 - OPTIONAL
        :type fkc_idx_62: ``int | HexList``
        :param fkc_idx_61: Fkc Idx 61 - OPTIONAL
        :type fkc_idx_61: ``int | HexList``
        :param fkc_idx_60: Fkc Idx 60 - OPTIONAL
        :type fkc_idx_60: ``int | HexList``
        :param fkc_idx_59: Fkc Idx 59 - OPTIONAL
        :type fkc_idx_59: ``int | HexList``
        :param fkc_idx_58: Fkc Idx 58 - OPTIONAL
        :type fkc_idx_58: ``int | HexList``
        :param fkc_idx_57: Fkc Idx 57 - OPTIONAL
        :type fkc_idx_57: ``int | HexList``
        :param fkc_idx_56: Fkc Idx 56 - OPTIONAL
        :type fkc_idx_56: ``int | HexList``
        :param fkc_idx_71: Fkc Idx 71 - OPTIONAL
        :type fkc_idx_71: ``int | HexList``
        :param fkc_idx_70: Fkc Idx 70 - OPTIONAL
        :type fkc_idx_70: ``int | HexList``
        :param fkc_idx_69: Fkc Idx 69 - OPTIONAL
        :type fkc_idx_69: ``int | HexList``
        :param fkc_idx_68: Fkc Idx 68 - OPTIONAL
        :type fkc_idx_68: ``int | HexList``
        :param fkc_idx_67: Fkc Idx 67 - OPTIONAL
        :type fkc_idx_67: ``int | HexList``
        :param fkc_idx_66: Fkc Idx 66 - OPTIONAL
        :type fkc_idx_66: ``int | HexList``
        :param fkc_idx_65: Fkc Idx 65 - OPTIONAL
        :type fkc_idx_65: ``int | HexList``
        :param fkc_idx_64: Fkc Idx 64 - OPTIONAL
        :type fkc_idx_64: ``int | HexList``
        :param fkc_idx_79: Fkc Idx 79 - OPTIONAL
        :type fkc_idx_79: ``int | HexList``
        :param fkc_idx_78: Fkc Idx 78 - OPTIONAL
        :type fkc_idx_78: ``int | HexList``
        :param fkc_idx_77: Fkc Idx 77 - OPTIONAL
        :type fkc_idx_77: ``int | HexList``
        :param fkc_idx_76: Fkc Idx 76 - OPTIONAL
        :type fkc_idx_76: ``int | HexList``
        :param fkc_idx_75: Fkc Idx 75 - OPTIONAL
        :type fkc_idx_75: ``int | HexList``
        :param fkc_idx_74: Fkc Idx 74 - OPTIONAL
        :type fkc_idx_74: ``int | HexList``
        :param fkc_idx_73: Fkc Idx 73 - OPTIONAL
        :type fkc_idx_73: ``int | HexList``
        :param fkc_idx_72: Fkc Idx 72 - OPTIONAL
        :type fkc_idx_72: ``int | HexList``
        :param fkc_idx_87: Fkc Idx 87 - OPTIONAL
        :type fkc_idx_87: ``int | HexList``
        :param fkc_idx_86: Fkc Idx 86 - OPTIONAL
        :type fkc_idx_86: ``int | HexList``
        :param fkc_idx_85: Fkc Idx 85 - OPTIONAL
        :type fkc_idx_85: ``int | HexList``
        :param fkc_idx_84: Fkc Idx 84 - OPTIONAL
        :type fkc_idx_84: ``int | HexList``
        :param fkc_idx_83: Fkc Idx 83 - OPTIONAL
        :type fkc_idx_83: ``int | HexList``
        :param fkc_idx_82: Fkc Idx 82 - OPTIONAL
        :type fkc_idx_82: ``int | HexList``
        :param fkc_idx_81: Fkc Idx 81 - OPTIONAL
        :type fkc_idx_81: ``int | HexList``
        :param fkc_idx_80: Fkc Idx 80 - OPTIONAL
        :type fkc_idx_80: ``int | HexList``
        :param fkc_idx_95: Fkc Idx 95 - OPTIONAL
        :type fkc_idx_95: ``int | HexList``
        :param fkc_idx_94: Fkc Idx 94 - OPTIONAL
        :type fkc_idx_94: ``int | HexList``
        :param fkc_idx_93: Fkc Idx 93 - OPTIONAL
        :type fkc_idx_93: ``int | HexList``
        :param fkc_idx_92: Fkc Idx 92 - OPTIONAL
        :type fkc_idx_92: ``int | HexList``
        :param fkc_idx_91: Fkc Idx 91 - OPTIONAL
        :type fkc_idx_91: ``int | HexList``
        :param fkc_idx_90: Fkc Idx 90 - OPTIONAL
        :type fkc_idx_90: ``int | HexList``
        :param fkc_idx_89: Fkc Idx 89 - OPTIONAL
        :type fkc_idx_89: ``int | HexList``
        :param fkc_idx_88: Fkc Idx 88 - OPTIONAL
        :type fkc_idx_88: ``int | HexList``
        :param fkc_idx_103: Fkc Idx 103 - OPTIONAL
        :type fkc_idx_103: ``int | HexList``
        :param fkc_idx_102: Fkc Idx 102 - OPTIONAL
        :type fkc_idx_102: ``int | HexList``
        :param fkc_idx_101: Fkc Idx 101 - OPTIONAL
        :type fkc_idx_101: ``int | HexList``
        :param fkc_idx_100: Fkc Idx 100 - OPTIONAL
        :type fkc_idx_100: ``int | HexList``
        :param fkc_idx_99: Fkc Idx 99 - OPTIONAL
        :type fkc_idx_99: ``int | HexList``
        :param fkc_idx_98: Fkc Idx 98 - OPTIONAL
        :type fkc_idx_98: ``int | HexList``
        :param fkc_idx_97: Fkc Idx 97 - OPTIONAL
        :type fkc_idx_97: ``int | HexList``
        :param fkc_idx_96: Fkc Idx 96 - OPTIONAL
        :type fkc_idx_96: ``int | HexList``
        :param fkc_idx_111: Fkc Idx 111 - OPTIONAL
        :type fkc_idx_111: ``int | HexList``
        :param fkc_idx_110: Fkc Idx 110 - OPTIONAL
        :type fkc_idx_110: ``int | HexList``
        :param fkc_idx_109: Fkc Idx 109 - OPTIONAL
        :type fkc_idx_109: ``int | HexList``
        :param fkc_idx_108: Fkc Idx 108 - OPTIONAL
        :type fkc_idx_108: ``int | HexList``
        :param fkc_idx_107: Fkc Idx 107 - OPTIONAL
        :type fkc_idx_107: ``int | HexList``
        :param fkc_idx_106: Fkc Idx 106 - OPTIONAL
        :type fkc_idx_106: ``int | HexList``
        :param fkc_idx_105: Fkc Idx 105 - OPTIONAL
        :type fkc_idx_105: ``int | HexList``
        :param fkc_idx_104: Fkc Idx 104 - OPTIONAL
        :type fkc_idx_104: ``int | HexList``
        :param fkc_idx_119: Fkc Idx 119 - OPTIONAL
        :type fkc_idx_119: ``int | HexList``
        :param fkc_idx_118: Fkc Idx 118 - OPTIONAL
        :type fkc_idx_118: ``int | HexList``
        :param fkc_idx_117: Fkc Idx 117 - OPTIONAL
        :type fkc_idx_117: ``int | HexList``
        :param fkc_idx_116: Fkc Idx 116 - OPTIONAL
        :type fkc_idx_116: ``int | HexList``
        :param fkc_idx_115: Fkc Idx 115 - OPTIONAL
        :type fkc_idx_115: ``int | HexList``
        :param fkc_idx_114: Fkc Idx 114 - OPTIONAL
        :type fkc_idx_114: ``int | HexList``
        :param fkc_idx_113: Fkc Idx 113 - OPTIONAL
        :type fkc_idx_113: ``int | HexList``
        :param fkc_idx_112: Fkc Idx 112 - OPTIONAL
        :type fkc_idx_112: ``int | HexList``
        :param fkc_idx_127: Fkc Idx 127 - OPTIONAL
        :type fkc_idx_127: ``int | HexList``
        :param fkc_idx_126: Fkc Idx 126 - OPTIONAL
        :type fkc_idx_126: ``int | HexList``
        :param fkc_idx_125: Fkc Idx 125 - OPTIONAL
        :type fkc_idx_125: ``int | HexList``
        :param fkc_idx_124: Fkc Idx 124 - OPTIONAL
        :type fkc_idx_124: ``int | HexList``
        :param fkc_idx_123: Fkc Idx 123 - OPTIONAL
        :type fkc_idx_123: ``int | HexList``
        :param fkc_idx_122: Fkc Idx 122 - OPTIONAL
        :type fkc_idx_122: ``int | HexList``
        :param fkc_idx_121: Fkc Idx 121 - OPTIONAL
        :type fkc_idx_121: ``int | HexList``
        :param fkc_idx_120: Fkc Idx 120 - OPTIONAL
        :type fkc_idx_120: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.key_trigger_bitmap = self.KeyTriggerBitmap(fkc_idx_7=fkc_idx_7, fkc_idx_6=fkc_idx_6,
                                                        fkc_idx_5=fkc_idx_5, fkc_idx_4=fkc_idx_4,
                                                        fkc_idx_3=fkc_idx_3, fkc_idx_2=fkc_idx_2,
                                                        fkc_idx_1=fkc_idx_1, fkc_idx_0=fkc_idx_0,
                                                        fkc_idx_15=fkc_idx_15, fkc_idx_14=fkc_idx_14,
                                                        fkc_idx_13=fkc_idx_13, fkc_idx_12=fkc_idx_12,
                                                        fkc_idx_11=fkc_idx_11, fkc_idx_10=fkc_idx_10,
                                                        fkc_idx_9=fkc_idx_9, fkc_idx_8=fkc_idx_8,
                                                        fkc_idx_23=fkc_idx_23, fkc_idx_22=fkc_idx_22,
                                                        fkc_idx_21=fkc_idx_21, fkc_idx_20=fkc_idx_20,
                                                        fkc_idx_19=fkc_idx_19, fkc_idx_18=fkc_idx_18,
                                                        fkc_idx_17=fkc_idx_17, fkc_idx_16=fkc_idx_16,
                                                        fkc_idx_31=fkc_idx_31, fkc_idx_30=fkc_idx_30,
                                                        fkc_idx_29=fkc_idx_29, fkc_idx_28=fkc_idx_28,
                                                        fkc_idx_27=fkc_idx_27, fkc_idx_26=fkc_idx_26,
                                                        fkc_idx_25=fkc_idx_25, fkc_idx_24=fkc_idx_24,
                                                        fkc_idx_39=fkc_idx_39, fkc_idx_38=fkc_idx_38,
                                                        fkc_idx_37=fkc_idx_37, fkc_idx_36=fkc_idx_36,
                                                        fkc_idx_35=fkc_idx_35, fkc_idx_34=fkc_idx_34,
                                                        fkc_idx_33=fkc_idx_33, fkc_idx_32=fkc_idx_32,
                                                        fkc_idx_47=fkc_idx_47, fkc_idx_46=fkc_idx_46,
                                                        fkc_idx_45=fkc_idx_45, fkc_idx_44=fkc_idx_44,
                                                        fkc_idx_43=fkc_idx_43, fkc_idx_42=fkc_idx_42,
                                                        fkc_idx_41=fkc_idx_41, fkc_idx_40=fkc_idx_40,
                                                        fkc_idx_55=fkc_idx_55, fkc_idx_54=fkc_idx_54,
                                                        fkc_idx_53=fkc_idx_53, fkc_idx_52=fkc_idx_52,
                                                        fkc_idx_51=fkc_idx_51, fkc_idx_50=fkc_idx_50,
                                                        fkc_idx_49=fkc_idx_49, fkc_idx_48=fkc_idx_48,
                                                        fkc_idx_63=fkc_idx_63, fkc_idx_62=fkc_idx_62,
                                                        fkc_idx_61=fkc_idx_61, fkc_idx_60=fkc_idx_60,
                                                        fkc_idx_59=fkc_idx_59, fkc_idx_58=fkc_idx_58,
                                                        fkc_idx_57=fkc_idx_57, fkc_idx_56=fkc_idx_56,
                                                        fkc_idx_71=fkc_idx_71, fkc_idx_70=fkc_idx_70,
                                                        fkc_idx_69=fkc_idx_69, fkc_idx_68=fkc_idx_68,
                                                        fkc_idx_67=fkc_idx_67, fkc_idx_66=fkc_idx_66,
                                                        fkc_idx_65=fkc_idx_65, fkc_idx_64=fkc_idx_64,
                                                        fkc_idx_79=fkc_idx_79, fkc_idx_78=fkc_idx_78,
                                                        fkc_idx_77=fkc_idx_77, fkc_idx_76=fkc_idx_76,
                                                        fkc_idx_75=fkc_idx_75, fkc_idx_74=fkc_idx_74,
                                                        fkc_idx_73=fkc_idx_73, fkc_idx_72=fkc_idx_72,
                                                        fkc_idx_87=fkc_idx_87, fkc_idx_86=fkc_idx_86,
                                                        fkc_idx_85=fkc_idx_85, fkc_idx_84=fkc_idx_84,
                                                        fkc_idx_83=fkc_idx_83, fkc_idx_82=fkc_idx_82,
                                                        fkc_idx_81=fkc_idx_81, fkc_idx_80=fkc_idx_80,
                                                        fkc_idx_95=fkc_idx_95, fkc_idx_94=fkc_idx_94,
                                                        fkc_idx_93=fkc_idx_93, fkc_idx_92=fkc_idx_92,
                                                        fkc_idx_91=fkc_idx_91, fkc_idx_90=fkc_idx_90,
                                                        fkc_idx_89=fkc_idx_89, fkc_idx_88=fkc_idx_88,
                                                        fkc_idx_103=fkc_idx_103, fkc_idx_102=fkc_idx_102,
                                                        fkc_idx_101=fkc_idx_101, fkc_idx_100=fkc_idx_100,
                                                        fkc_idx_99=fkc_idx_99, fkc_idx_98=fkc_idx_98,
                                                        fkc_idx_97=fkc_idx_97, fkc_idx_96=fkc_idx_96,
                                                        fkc_idx_111=fkc_idx_111, fkc_idx_110=fkc_idx_110,
                                                        fkc_idx_109=fkc_idx_109, fkc_idx_108=fkc_idx_108,
                                                        fkc_idx_107=fkc_idx_107, fkc_idx_106=fkc_idx_106,
                                                        fkc_idx_105=fkc_idx_105, fkc_idx_104=fkc_idx_104,
                                                        fkc_idx_119=fkc_idx_119, fkc_idx_118=fkc_idx_118,
                                                        fkc_idx_117=fkc_idx_117, fkc_idx_116=fkc_idx_116,
                                                        fkc_idx_115=fkc_idx_115, fkc_idx_114=fkc_idx_114,
                                                        fkc_idx_113=fkc_idx_113, fkc_idx_112=fkc_idx_112,
                                                        fkc_idx_127=fkc_idx_127, fkc_idx_126=fkc_idx_126,
                                                        fkc_idx_125=fkc_idx_125, fkc_idx_124=fkc_idx_124,
                                                        fkc_idx_123=fkc_idx_123, fkc_idx_122=fkc_idx_122,
                                                        fkc_idx_121=fkc_idx_121, fkc_idx_120=fkc_idx_120)
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``FNLayerTriggerAsBitmapEvent``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.key_trigger_bitmap = cls.KeyTriggerBitmap.fromHexList(
            inner_field_container_mixin.key_trigger_bitmap)
        return inner_field_container_mixin
    # end def fromHexList
# end class FNLayerTriggerAsBitmapEvent


class GShiftLayerTriggerAsListEvent(KeyTriggerAsList):
    """
    Define ``GShiftLayerTriggerAsListEvent`` implementation class
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1)
    FUNCTION_INDEX = 4

    def __init__(self, device_index, feature_index, key_trigger_0, key_trigger_1, key_trigger_2, key_trigger_3,
                 key_trigger_4, key_trigger_5, key_trigger_6, key_trigger_7, key_trigger_8, key_trigger_9,
                 key_trigger_10, key_trigger_11, key_trigger_12, key_trigger_13, key_trigger_14, key_trigger_15,
                 **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param key_trigger_0: Key Trigger 0
        :type key_trigger_0: ``int | HexList``
        :param key_trigger_1: Key Trigger 1
        :type key_trigger_1: ``int | HexList``
        :param key_trigger_2: Key Trigger 2
        :type key_trigger_2: ``int | HexList``
        :param key_trigger_3: Key Trigger 3
        :type key_trigger_3: ``int | HexList``
        :param key_trigger_4: Key Trigger 4
        :type key_trigger_4: ``int | HexList``
        :param key_trigger_5: Key Trigger 5
        :type key_trigger_5: ``int | HexList``
        :param key_trigger_6: Key Trigger 6
        :type key_trigger_6: ``int | HexList``
        :param key_trigger_7: Key Trigger 7
        :type key_trigger_7: ``int | HexList``
        :param key_trigger_8: Key Trigger 8
        :type key_trigger_8: ``int | HexList``
        :param key_trigger_9: Key Trigger 9
        :type key_trigger_9: ``int | HexList``
        :param key_trigger_10: Key Trigger 10
        :type key_trigger_10: ``int | HexList``
        :param key_trigger_11: Key Trigger 11
        :type key_trigger_11: ``int | HexList``
        :param key_trigger_12: Key Trigger 12
        :type key_trigger_12: ``int | HexList``
        :param key_trigger_13: Key Trigger 13
        :type key_trigger_13: ``int | HexList``
        :param key_trigger_14: Key Trigger 14
        :type key_trigger_14: ``int | HexList``
        :param key_trigger_15: Key Trigger 15
        :type key_trigger_15: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.key_trigger_0 = HexList(Numeral(key_trigger_0, self.LEN.KEY_TRIGGER_0 // 8))
        self.key_trigger_1 = HexList(Numeral(key_trigger_1, self.LEN.KEY_TRIGGER_1 // 8))
        self.key_trigger_2 = HexList(Numeral(key_trigger_2, self.LEN.KEY_TRIGGER_2 // 8))
        self.key_trigger_3 = HexList(Numeral(key_trigger_3, self.LEN.KEY_TRIGGER_3 // 8))
        self.key_trigger_4 = HexList(Numeral(key_trigger_4, self.LEN.KEY_TRIGGER_4 // 8))
        self.key_trigger_5 = HexList(Numeral(key_trigger_5, self.LEN.KEY_TRIGGER_5 // 8))
        self.key_trigger_6 = HexList(Numeral(key_trigger_6, self.LEN.KEY_TRIGGER_6 // 8))
        self.key_trigger_7 = HexList(Numeral(key_trigger_7, self.LEN.KEY_TRIGGER_7 // 8))
        self.key_trigger_8 = HexList(Numeral(key_trigger_8, self.LEN.KEY_TRIGGER_8 // 8))
        self.key_trigger_9 = HexList(Numeral(key_trigger_9, self.LEN.KEY_TRIGGER_9 // 8))
        self.key_trigger_10 = HexList(Numeral(key_trigger_10, self.LEN.KEY_TRIGGER_10 // 8))
        self.key_trigger_11 = HexList(Numeral(key_trigger_11, self.LEN.KEY_TRIGGER_11 // 8))
        self.key_trigger_12 = HexList(Numeral(key_trigger_12, self.LEN.KEY_TRIGGER_12 // 8))
        self.key_trigger_13 = HexList(Numeral(key_trigger_13, self.LEN.KEY_TRIGGER_13 // 8))
        self.key_trigger_14 = HexList(Numeral(key_trigger_14, self.LEN.KEY_TRIGGER_14 // 8))
        self.key_trigger_15 = HexList(Numeral(key_trigger_15, self.LEN.KEY_TRIGGER_15 // 8))
    # end def __init__
# end class GShiftLayerTriggerAsListEvent


class GShiftLayerTriggerAsBitmapEvent(KeyTriggerAsBitmap):
    """
    Define ``GShiftLayerTriggerAsBitmapEvent`` implementation class
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1)
    FUNCTION_INDEX = 5

    def __init__(self, device_index, feature_index, fkc_idx_7=False, fkc_idx_6=False, fkc_idx_5=False, fkc_idx_4=False,
                 fkc_idx_3=False, fkc_idx_2=False, fkc_idx_1=False, fkc_idx_0=False, fkc_idx_15=False,
                 fkc_idx_14=False, fkc_idx_13=False, fkc_idx_12=False, fkc_idx_11=False, fkc_idx_10=False,
                 fkc_idx_9=False, fkc_idx_8=False, fkc_idx_23=False, fkc_idx_22=False, fkc_idx_21=False,
                 fkc_idx_20=False, fkc_idx_19=False, fkc_idx_18=False, fkc_idx_17=False, fkc_idx_16=False,
                 fkc_idx_31=False, fkc_idx_30=False, fkc_idx_29=False, fkc_idx_28=False, fkc_idx_27=False,
                 fkc_idx_26=False, fkc_idx_25=False, fkc_idx_24=False, fkc_idx_39=False, fkc_idx_38=False,
                 fkc_idx_37=False, fkc_idx_36=False, fkc_idx_35=False, fkc_idx_34=False, fkc_idx_33=False,
                 fkc_idx_32=False, fkc_idx_47=False, fkc_idx_46=False, fkc_idx_45=False, fkc_idx_44=False,
                 fkc_idx_43=False, fkc_idx_42=False, fkc_idx_41=False, fkc_idx_40=False, fkc_idx_55=False,
                 fkc_idx_54=False, fkc_idx_53=False, fkc_idx_52=False, fkc_idx_51=False, fkc_idx_50=False,
                 fkc_idx_49=False, fkc_idx_48=False, fkc_idx_63=False, fkc_idx_62=False, fkc_idx_61=False,
                 fkc_idx_60=False, fkc_idx_59=False, fkc_idx_58=False, fkc_idx_57=False, fkc_idx_56=False,
                 fkc_idx_71=False, fkc_idx_70=False, fkc_idx_69=False, fkc_idx_68=False, fkc_idx_67=False,
                 fkc_idx_66=False, fkc_idx_65=False, fkc_idx_64=False, fkc_idx_79=False, fkc_idx_78=False,
                 fkc_idx_77=False, fkc_idx_76=False, fkc_idx_75=False, fkc_idx_74=False, fkc_idx_73=False,
                 fkc_idx_72=False, fkc_idx_87=False, fkc_idx_86=False, fkc_idx_85=False, fkc_idx_84=False,
                 fkc_idx_83=False, fkc_idx_82=False, fkc_idx_81=False, fkc_idx_80=False, fkc_idx_95=False,
                 fkc_idx_94=False, fkc_idx_93=False, fkc_idx_92=False, fkc_idx_91=False, fkc_idx_90=False,
                 fkc_idx_89=False, fkc_idx_88=False, fkc_idx_103=False, fkc_idx_102=False, fkc_idx_101=False,
                 fkc_idx_100=False, fkc_idx_99=False, fkc_idx_98=False, fkc_idx_97=False, fkc_idx_96=False,
                 fkc_idx_111=False, fkc_idx_110=False, fkc_idx_109=False, fkc_idx_108=False, fkc_idx_107=False,
                 fkc_idx_106=False, fkc_idx_105=False, fkc_idx_104=False, fkc_idx_119=False, fkc_idx_118=False,
                 fkc_idx_117=False, fkc_idx_116=False, fkc_idx_115=False, fkc_idx_114=False, fkc_idx_113=False,
                 fkc_idx_112=False, fkc_idx_127=False, fkc_idx_126=False, fkc_idx_125=False, fkc_idx_124=False,
                 fkc_idx_123=False, fkc_idx_122=False, fkc_idx_121=False, fkc_idx_120=False, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param fkc_idx_7: Fkc Idx 7 - OPTIONAL
        :type fkc_idx_7: ``int | HexList``
        :param fkc_idx_6: Fkc Idx 6 - OPTIONAL
        :type fkc_idx_6: ``int | HexList``
        :param fkc_idx_5: Fkc Idx 5 - OPTIONAL
        :type fkc_idx_5: ``int | HexList``
        :param fkc_idx_4: Fkc Idx 4 - OPTIONAL
        :type fkc_idx_4: ``int | HexList``
        :param fkc_idx_3: Fkc Idx 3 - OPTIONAL
        :type fkc_idx_3: ``int | HexList``
        :param fkc_idx_2: Fkc Idx 2 - OPTIONAL
        :type fkc_idx_2: ``int | HexList``
        :param fkc_idx_1: Fkc Idx 1 - OPTIONAL
        :type fkc_idx_1: ``int | HexList``
        :param fkc_idx_0: Fkc Idx 0 - OPTIONAL
        :type fkc_idx_0: ``int | HexList``
        :param fkc_idx_15: Fkc Idx 15 - OPTIONAL
        :type fkc_idx_15: ``int | HexList``
        :param fkc_idx_14: Fkc Idx 14 - OPTIONAL
        :type fkc_idx_14: ``int | HexList``
        :param fkc_idx_13: Fkc Idx 13 - OPTIONAL
        :type fkc_idx_13: ``int | HexList``
        :param fkc_idx_12: Fkc Idx 12 - OPTIONAL
        :type fkc_idx_12: ``int | HexList``
        :param fkc_idx_11: Fkc Idx 11 - OPTIONAL
        :type fkc_idx_11: ``int | HexList``
        :param fkc_idx_10: Fkc Idx 10 - OPTIONAL
        :type fkc_idx_10: ``int | HexList``
        :param fkc_idx_9: Fkc Idx 9 - OPTIONAL
        :type fkc_idx_9: ``int | HexList``
        :param fkc_idx_8: Fkc Idx 8 - OPTIONAL
        :type fkc_idx_8: ``int | HexList``
        :param fkc_idx_23: Fkc Idx 23 - OPTIONAL
        :type fkc_idx_23: ``int | HexList``
        :param fkc_idx_22: Fkc Idx 22 - OPTIONAL
        :type fkc_idx_22: ``int | HexList``
        :param fkc_idx_21: Fkc Idx 21 - OPTIONAL
        :type fkc_idx_21: ``int | HexList``
        :param fkc_idx_20: Fkc Idx 20 - OPTIONAL
        :type fkc_idx_20: ``int | HexList``
        :param fkc_idx_19: Fkc Idx 19 - OPTIONAL
        :type fkc_idx_19: ``int | HexList``
        :param fkc_idx_18: Fkc Idx 18 - OPTIONAL
        :type fkc_idx_18: ``int | HexList``
        :param fkc_idx_17: Fkc Idx 17 - OPTIONAL
        :type fkc_idx_17: ``int | HexList``
        :param fkc_idx_16: Fkc Idx 16 - OPTIONAL
        :type fkc_idx_16: ``int | HexList``
        :param fkc_idx_31: Fkc Idx 31 - OPTIONAL
        :type fkc_idx_31: ``int | HexList``
        :param fkc_idx_30: Fkc Idx 30 - OPTIONAL
        :type fkc_idx_30: ``int | HexList``
        :param fkc_idx_29: Fkc Idx 29 - OPTIONAL
        :type fkc_idx_29: ``int | HexList``
        :param fkc_idx_28: Fkc Idx 28 - OPTIONAL
        :type fkc_idx_28: ``int | HexList``
        :param fkc_idx_27: Fkc Idx 27 - OPTIONAL
        :type fkc_idx_27: ``int | HexList``
        :param fkc_idx_26: Fkc Idx 26 - OPTIONAL
        :type fkc_idx_26: ``int | HexList``
        :param fkc_idx_25: Fkc Idx 25 - OPTIONAL
        :type fkc_idx_25: ``int | HexList``
        :param fkc_idx_24: Fkc Idx 24 - OPTIONAL
        :type fkc_idx_24: ``int | HexList``
        :param fkc_idx_39: Fkc Idx 39 - OPTIONAL
        :type fkc_idx_39: ``int | HexList``
        :param fkc_idx_38: Fkc Idx 38 - OPTIONAL
        :type fkc_idx_38: ``int | HexList``
        :param fkc_idx_37: Fkc Idx 37 - OPTIONAL
        :type fkc_idx_37: ``int | HexList``
        :param fkc_idx_36: Fkc Idx 36 - OPTIONAL
        :type fkc_idx_36: ``int | HexList``
        :param fkc_idx_35: Fkc Idx 35 - OPTIONAL
        :type fkc_idx_35: ``int | HexList``
        :param fkc_idx_34: Fkc Idx 34 - OPTIONAL
        :type fkc_idx_34: ``int | HexList``
        :param fkc_idx_33: Fkc Idx 33 - OPTIONAL
        :type fkc_idx_33: ``int | HexList``
        :param fkc_idx_32: Fkc Idx 32 - OPTIONAL
        :type fkc_idx_32: ``int | HexList``
        :param fkc_idx_47: Fkc Idx 47 - OPTIONAL
        :type fkc_idx_47: ``int | HexList``
        :param fkc_idx_46: Fkc Idx 46 - OPTIONAL
        :type fkc_idx_46: ``int | HexList``
        :param fkc_idx_45: Fkc Idx 45 - OPTIONAL
        :type fkc_idx_45: ``int | HexList``
        :param fkc_idx_44: Fkc Idx 44 - OPTIONAL
        :type fkc_idx_44: ``int | HexList``
        :param fkc_idx_43: Fkc Idx 43 - OPTIONAL
        :type fkc_idx_43: ``int | HexList``
        :param fkc_idx_42: Fkc Idx 42 - OPTIONAL
        :type fkc_idx_42: ``int | HexList``
        :param fkc_idx_41: Fkc Idx 41 - OPTIONAL
        :type fkc_idx_41: ``int | HexList``
        :param fkc_idx_40: Fkc Idx 40 - OPTIONAL
        :type fkc_idx_40: ``int | HexList``
        :param fkc_idx_55: Fkc Idx 55 - OPTIONAL
        :type fkc_idx_55: ``int | HexList``
        :param fkc_idx_54: Fkc Idx 54 - OPTIONAL
        :type fkc_idx_54: ``int | HexList``
        :param fkc_idx_53: Fkc Idx 53 - OPTIONAL
        :type fkc_idx_53: ``int | HexList``
        :param fkc_idx_52: Fkc Idx 52 - OPTIONAL
        :type fkc_idx_52: ``int | HexList``
        :param fkc_idx_51: Fkc Idx 51 - OPTIONAL
        :type fkc_idx_51: ``int | HexList``
        :param fkc_idx_50: Fkc Idx 50 - OPTIONAL
        :type fkc_idx_50: ``int | HexList``
        :param fkc_idx_49: Fkc Idx 49 - OPTIONAL
        :type fkc_idx_49: ``int | HexList``
        :param fkc_idx_48: Fkc Idx 48 - OPTIONAL
        :type fkc_idx_48: ``int | HexList``
        :param fkc_idx_63: Fkc Idx 63 - OPTIONAL
        :type fkc_idx_63: ``int | HexList``
        :param fkc_idx_62: Fkc Idx 62 - OPTIONAL
        :type fkc_idx_62: ``int | HexList``
        :param fkc_idx_61: Fkc Idx 61 - OPTIONAL
        :type fkc_idx_61: ``int | HexList``
        :param fkc_idx_60: Fkc Idx 60 - OPTIONAL
        :type fkc_idx_60: ``int | HexList``
        :param fkc_idx_59: Fkc Idx 59 - OPTIONAL
        :type fkc_idx_59: ``int | HexList``
        :param fkc_idx_58: Fkc Idx 58 - OPTIONAL
        :type fkc_idx_58: ``int | HexList``
        :param fkc_idx_57: Fkc Idx 57 - OPTIONAL
        :type fkc_idx_57: ``int | HexList``
        :param fkc_idx_56: Fkc Idx 56 - OPTIONAL
        :type fkc_idx_56: ``int | HexList``
        :param fkc_idx_71: Fkc Idx 71 - OPTIONAL
        :type fkc_idx_71: ``int | HexList``
        :param fkc_idx_70: Fkc Idx 70 - OPTIONAL
        :type fkc_idx_70: ``int | HexList``
        :param fkc_idx_69: Fkc Idx 69 - OPTIONAL
        :type fkc_idx_69: ``int | HexList``
        :param fkc_idx_68: Fkc Idx 68 - OPTIONAL
        :type fkc_idx_68: ``int | HexList``
        :param fkc_idx_67: Fkc Idx 67 - OPTIONAL
        :type fkc_idx_67: ``int | HexList``
        :param fkc_idx_66: Fkc Idx 66 - OPTIONAL
        :type fkc_idx_66: ``int | HexList``
        :param fkc_idx_65: Fkc Idx 65 - OPTIONAL
        :type fkc_idx_65: ``int | HexList``
        :param fkc_idx_64: Fkc Idx 64 - OPTIONAL
        :type fkc_idx_64: ``int | HexList``
        :param fkc_idx_79: Fkc Idx 79 - OPTIONAL
        :type fkc_idx_79: ``int | HexList``
        :param fkc_idx_78: Fkc Idx 78 - OPTIONAL
        :type fkc_idx_78: ``int | HexList``
        :param fkc_idx_77: Fkc Idx 77 - OPTIONAL
        :type fkc_idx_77: ``int | HexList``
        :param fkc_idx_76: Fkc Idx 76 - OPTIONAL
        :type fkc_idx_76: ``int | HexList``
        :param fkc_idx_75: Fkc Idx 75 - OPTIONAL
        :type fkc_idx_75: ``int | HexList``
        :param fkc_idx_74: Fkc Idx 74 - OPTIONAL
        :type fkc_idx_74: ``int | HexList``
        :param fkc_idx_73: Fkc Idx 73 - OPTIONAL
        :type fkc_idx_73: ``int | HexList``
        :param fkc_idx_72: Fkc Idx 72 - OPTIONAL
        :type fkc_idx_72: ``int | HexList``
        :param fkc_idx_87: Fkc Idx 87 - OPTIONAL
        :type fkc_idx_87: ``int | HexList``
        :param fkc_idx_86: Fkc Idx 86 - OPTIONAL
        :type fkc_idx_86: ``int | HexList``
        :param fkc_idx_85: Fkc Idx 85 - OPTIONAL
        :type fkc_idx_85: ``int | HexList``
        :param fkc_idx_84: Fkc Idx 84 - OPTIONAL
        :type fkc_idx_84: ``int | HexList``
        :param fkc_idx_83: Fkc Idx 83 - OPTIONAL
        :type fkc_idx_83: ``int | HexList``
        :param fkc_idx_82: Fkc Idx 82 - OPTIONAL
        :type fkc_idx_82: ``int | HexList``
        :param fkc_idx_81: Fkc Idx 81 - OPTIONAL
        :type fkc_idx_81: ``int | HexList``
        :param fkc_idx_80: Fkc Idx 80 - OPTIONAL
        :type fkc_idx_80: ``int | HexList``
        :param fkc_idx_95: Fkc Idx 95 - OPTIONAL
        :type fkc_idx_95: ``int | HexList``
        :param fkc_idx_94: Fkc Idx 94 - OPTIONAL
        :type fkc_idx_94: ``int | HexList``
        :param fkc_idx_93: Fkc Idx 93 - OPTIONAL
        :type fkc_idx_93: ``int | HexList``
        :param fkc_idx_92: Fkc Idx 92 - OPTIONAL
        :type fkc_idx_92: ``int | HexList``
        :param fkc_idx_91: Fkc Idx 91 - OPTIONAL
        :type fkc_idx_91: ``int | HexList``
        :param fkc_idx_90: Fkc Idx 90 - OPTIONAL
        :type fkc_idx_90: ``int | HexList``
        :param fkc_idx_89: Fkc Idx 89 - OPTIONAL
        :type fkc_idx_89: ``int | HexList``
        :param fkc_idx_88: Fkc Idx 88 - OPTIONAL
        :type fkc_idx_88: ``int | HexList``
        :param fkc_idx_103: Fkc Idx 103 - OPTIONAL
        :type fkc_idx_103: ``int | HexList``
        :param fkc_idx_102: Fkc Idx 102 - OPTIONAL
        :type fkc_idx_102: ``int | HexList``
        :param fkc_idx_101: Fkc Idx 101 - OPTIONAL
        :type fkc_idx_101: ``int | HexList``
        :param fkc_idx_100: Fkc Idx 100 - OPTIONAL
        :type fkc_idx_100: ``int | HexList``
        :param fkc_idx_99: Fkc Idx 99 - OPTIONAL
        :type fkc_idx_99: ``int | HexList``
        :param fkc_idx_98: Fkc Idx 98 - OPTIONAL
        :type fkc_idx_98: ``int | HexList``
        :param fkc_idx_97: Fkc Idx 97 - OPTIONAL
        :type fkc_idx_97: ``int | HexList``
        :param fkc_idx_96: Fkc Idx 96 - OPTIONAL
        :type fkc_idx_96: ``int | HexList``
        :param fkc_idx_111: Fkc Idx 111 - OPTIONAL
        :type fkc_idx_111: ``int | HexList``
        :param fkc_idx_110: Fkc Idx 110 - OPTIONAL
        :type fkc_idx_110: ``int | HexList``
        :param fkc_idx_109: Fkc Idx 109 - OPTIONAL
        :type fkc_idx_109: ``int | HexList``
        :param fkc_idx_108: Fkc Idx 108 - OPTIONAL
        :type fkc_idx_108: ``int | HexList``
        :param fkc_idx_107: Fkc Idx 107 - OPTIONAL
        :type fkc_idx_107: ``int | HexList``
        :param fkc_idx_106: Fkc Idx 106 - OPTIONAL
        :type fkc_idx_106: ``int | HexList``
        :param fkc_idx_105: Fkc Idx 105 - OPTIONAL
        :type fkc_idx_105: ``int | HexList``
        :param fkc_idx_104: Fkc Idx 104 - OPTIONAL
        :type fkc_idx_104: ``int | HexList``
        :param fkc_idx_119: Fkc Idx 119 - OPTIONAL
        :type fkc_idx_119: ``int | HexList``
        :param fkc_idx_118: Fkc Idx 118 - OPTIONAL
        :type fkc_idx_118: ``int | HexList``
        :param fkc_idx_117: Fkc Idx 117 - OPTIONAL
        :type fkc_idx_117: ``int | HexList``
        :param fkc_idx_116: Fkc Idx 116 - OPTIONAL
        :type fkc_idx_116: ``int | HexList``
        :param fkc_idx_115: Fkc Idx 115 - OPTIONAL
        :type fkc_idx_115: ``int | HexList``
        :param fkc_idx_114: Fkc Idx 114 - OPTIONAL
        :type fkc_idx_114: ``int | HexList``
        :param fkc_idx_113: Fkc Idx 113 - OPTIONAL
        :type fkc_idx_113: ``int | HexList``
        :param fkc_idx_112: Fkc Idx 112 - OPTIONAL
        :type fkc_idx_112: ``int | HexList``
        :param fkc_idx_127: Fkc Idx 127 - OPTIONAL
        :type fkc_idx_127: ``int | HexList``
        :param fkc_idx_126: Fkc Idx 126 - OPTIONAL
        :type fkc_idx_126: ``int | HexList``
        :param fkc_idx_125: Fkc Idx 125 - OPTIONAL
        :type fkc_idx_125: ``int | HexList``
        :param fkc_idx_124: Fkc Idx 124 - OPTIONAL
        :type fkc_idx_124: ``int | HexList``
        :param fkc_idx_123: Fkc Idx 123 - OPTIONAL
        :type fkc_idx_123: ``int | HexList``
        :param fkc_idx_122: Fkc Idx 122 - OPTIONAL
        :type fkc_idx_122: ``int | HexList``
        :param fkc_idx_121: Fkc Idx 121 - OPTIONAL
        :type fkc_idx_121: ``int | HexList``
        :param fkc_idx_120: Fkc Idx 120 - OPTIONAL
        :type fkc_idx_120: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.key_trigger_bitmap = self.KeyTriggerBitmap(fkc_idx_7=fkc_idx_7, fkc_idx_6=fkc_idx_6,
                                                        fkc_idx_5=fkc_idx_5, fkc_idx_4=fkc_idx_4,
                                                        fkc_idx_3=fkc_idx_3, fkc_idx_2=fkc_idx_2,
                                                        fkc_idx_1=fkc_idx_1, fkc_idx_0=fkc_idx_0,
                                                        fkc_idx_15=fkc_idx_15, fkc_idx_14=fkc_idx_14,
                                                        fkc_idx_13=fkc_idx_13, fkc_idx_12=fkc_idx_12,
                                                        fkc_idx_11=fkc_idx_11, fkc_idx_10=fkc_idx_10,
                                                        fkc_idx_9=fkc_idx_9, fkc_idx_8=fkc_idx_8,
                                                        fkc_idx_23=fkc_idx_23, fkc_idx_22=fkc_idx_22,
                                                        fkc_idx_21=fkc_idx_21, fkc_idx_20=fkc_idx_20,
                                                        fkc_idx_19=fkc_idx_19, fkc_idx_18=fkc_idx_18,
                                                        fkc_idx_17=fkc_idx_17, fkc_idx_16=fkc_idx_16,
                                                        fkc_idx_31=fkc_idx_31, fkc_idx_30=fkc_idx_30,
                                                        fkc_idx_29=fkc_idx_29, fkc_idx_28=fkc_idx_28,
                                                        fkc_idx_27=fkc_idx_27, fkc_idx_26=fkc_idx_26,
                                                        fkc_idx_25=fkc_idx_25, fkc_idx_24=fkc_idx_24,
                                                        fkc_idx_39=fkc_idx_39, fkc_idx_38=fkc_idx_38,
                                                        fkc_idx_37=fkc_idx_37, fkc_idx_36=fkc_idx_36,
                                                        fkc_idx_35=fkc_idx_35, fkc_idx_34=fkc_idx_34,
                                                        fkc_idx_33=fkc_idx_33, fkc_idx_32=fkc_idx_32,
                                                        fkc_idx_47=fkc_idx_47, fkc_idx_46=fkc_idx_46,
                                                        fkc_idx_45=fkc_idx_45, fkc_idx_44=fkc_idx_44,
                                                        fkc_idx_43=fkc_idx_43, fkc_idx_42=fkc_idx_42,
                                                        fkc_idx_41=fkc_idx_41, fkc_idx_40=fkc_idx_40,
                                                        fkc_idx_55=fkc_idx_55, fkc_idx_54=fkc_idx_54,
                                                        fkc_idx_53=fkc_idx_53, fkc_idx_52=fkc_idx_52,
                                                        fkc_idx_51=fkc_idx_51, fkc_idx_50=fkc_idx_50,
                                                        fkc_idx_49=fkc_idx_49, fkc_idx_48=fkc_idx_48,
                                                        fkc_idx_63=fkc_idx_63, fkc_idx_62=fkc_idx_62,
                                                        fkc_idx_61=fkc_idx_61, fkc_idx_60=fkc_idx_60,
                                                        fkc_idx_59=fkc_idx_59, fkc_idx_58=fkc_idx_58,
                                                        fkc_idx_57=fkc_idx_57, fkc_idx_56=fkc_idx_56,
                                                        fkc_idx_71=fkc_idx_71, fkc_idx_70=fkc_idx_70,
                                                        fkc_idx_69=fkc_idx_69, fkc_idx_68=fkc_idx_68,
                                                        fkc_idx_67=fkc_idx_67, fkc_idx_66=fkc_idx_66,
                                                        fkc_idx_65=fkc_idx_65, fkc_idx_64=fkc_idx_64,
                                                        fkc_idx_79=fkc_idx_79, fkc_idx_78=fkc_idx_78,
                                                        fkc_idx_77=fkc_idx_77, fkc_idx_76=fkc_idx_76,
                                                        fkc_idx_75=fkc_idx_75, fkc_idx_74=fkc_idx_74,
                                                        fkc_idx_73=fkc_idx_73, fkc_idx_72=fkc_idx_72,
                                                        fkc_idx_87=fkc_idx_87, fkc_idx_86=fkc_idx_86,
                                                        fkc_idx_85=fkc_idx_85, fkc_idx_84=fkc_idx_84,
                                                        fkc_idx_83=fkc_idx_83, fkc_idx_82=fkc_idx_82,
                                                        fkc_idx_81=fkc_idx_81, fkc_idx_80=fkc_idx_80,
                                                        fkc_idx_95=fkc_idx_95, fkc_idx_94=fkc_idx_94,
                                                        fkc_idx_93=fkc_idx_93, fkc_idx_92=fkc_idx_92,
                                                        fkc_idx_91=fkc_idx_91, fkc_idx_90=fkc_idx_90,
                                                        fkc_idx_89=fkc_idx_89, fkc_idx_88=fkc_idx_88,
                                                        fkc_idx_103=fkc_idx_103, fkc_idx_102=fkc_idx_102,
                                                        fkc_idx_101=fkc_idx_101, fkc_idx_100=fkc_idx_100,
                                                        fkc_idx_99=fkc_idx_99, fkc_idx_98=fkc_idx_98,
                                                        fkc_idx_97=fkc_idx_97, fkc_idx_96=fkc_idx_96,
                                                        fkc_idx_111=fkc_idx_111, fkc_idx_110=fkc_idx_110,
                                                        fkc_idx_109=fkc_idx_109, fkc_idx_108=fkc_idx_108,
                                                        fkc_idx_107=fkc_idx_107, fkc_idx_106=fkc_idx_106,
                                                        fkc_idx_105=fkc_idx_105, fkc_idx_104=fkc_idx_104,
                                                        fkc_idx_119=fkc_idx_119, fkc_idx_118=fkc_idx_118,
                                                        fkc_idx_117=fkc_idx_117, fkc_idx_116=fkc_idx_116,
                                                        fkc_idx_115=fkc_idx_115, fkc_idx_114=fkc_idx_114,
                                                        fkc_idx_113=fkc_idx_113, fkc_idx_112=fkc_idx_112,
                                                        fkc_idx_127=fkc_idx_127, fkc_idx_126=fkc_idx_126,
                                                        fkc_idx_125=fkc_idx_125, fkc_idx_124=fkc_idx_124,
                                                        fkc_idx_123=fkc_idx_123, fkc_idx_122=fkc_idx_122,
                                                        fkc_idx_121=fkc_idx_121, fkc_idx_120=fkc_idx_120)
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GShiftLayerTriggerAsBitmapEvent``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.key_trigger_bitmap = cls.KeyTriggerBitmap.fromHexList(
            inner_field_container_mixin.key_trigger_bitmap)
        return inner_field_container_mixin
    # end def fromHexList
# end class GShiftLayerTriggerAsBitmapEvent


class EnableDisableEvent(FullKeyCustomization):
    """
    Define ``EnableDisableEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Fkc Failure Enabled State     8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1)
    FUNCTION_INDEX = 6

    class FID(FullKeyCustomization.FID):
        # See ``FullKeyCustomization.FID``
        FKC_FAILURE_ENABLED_STATE = FullKeyCustomization.FID.SOFTWARE_ID - 1
        PADDING = FKC_FAILURE_ENABLED_STATE - 1
    # end class FID

    class LEN(FullKeyCustomization.LEN):
        # See ``FullKeyCustomization.LEN``
        FKC_FAILURE_ENABLED_STATE = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = FullKeyCustomization.FIELDS + (
        BitField(fid=FID.FKC_FAILURE_ENABLED_STATE, length=LEN.FKC_FAILURE_ENABLED_STATE,
                 title="FkcFailureEnabledState", name="fkc_failure_enabled_state",
                 checks=(CheckHexList(LEN.FKC_FAILURE_ENABLED_STATE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=FullKeyCustomization.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, failure, enabled, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param failure: Failure
        :type failure: ``int | HexList``
        :param enabled: Enabled
        :type enabled: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.fkc_failure_enabled_state = self.FkcFailureEnabledState(failure=failure,
                                                                     enabled=enabled)
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``EnableDisableEvent``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.fkc_failure_enabled_state = cls.FkcFailureEnabledState.fromHexList(
            inner_field_container_mixin.fkc_failure_enabled_state)
        return inner_field_container_mixin
    # end def fromHexList
# end class EnableDisableEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
