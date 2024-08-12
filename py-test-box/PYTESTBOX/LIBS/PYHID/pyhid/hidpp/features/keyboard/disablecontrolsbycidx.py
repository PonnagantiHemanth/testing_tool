#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.keyboard.disablecontrolsbycidx
:brief: HID++ 2.0 ``DisableControlsByCIDX`` command interface definition
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/03/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from enum import unique
from enum import IntEnum

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


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DisableControlsByCIDX(HidppMessage):
    """
    This feature provides the means to disable and enable any number of controls on a device.
    For gaming keyboards, the controls are only disabled when game mode is enabled.
    """
    FEATURE_ID = 0x4523
    MAX_FUNCTION_INDEX_V0 = 1
    MAX_FUNCTION_INDEX_V1 = 3

    DISABLE_KEYS_TABLE_LENGTH = 16

    @unique
    class GameMode(IntEnum):
        """
        Game Mode values
        """
        DISABLE = 0
        ENABLE = 1
    # end class GameMode

    @unique
    class GameModeLock(IntEnum):
        """
        Game Mode Lock values
        """
        DISABLE = 0
        ENABLE = 1
    # end class GameModeLock

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__

    class CidxBitmap(BitFieldContainerMixin):
        """
        Define ``CidxBitmap`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Cidx 7                        1
        Cidx 6                        1
        Cidx 5                        1
        Cidx 4                        1
        Cidx 3                        1
        Cidx 2                        1
        Cidx 1                        1
        Cidx 0                        1
        Cidx 15                       1
        Cidx 14                       1
        Cidx 13                       1
        Cidx 12                       1
        Cidx 11                       1
        Cidx 10                       1
        Cidx 9                        1
        Cidx 8                        1
        Cidx 23                       1
        Cidx 22                       1
        Cidx 21                       1
        Cidx 20                       1
        Cidx 19                       1
        Cidx 18                       1
        Cidx 17                       1
        Cidx 16                       1
        Cidx 31                       1
        Cidx 30                       1
        Cidx 29                       1
        Cidx 28                       1
        Cidx 27                       1
        Cidx 26                       1
        Cidx 25                       1
        Cidx 24                       1
        Cidx 39                       1
        Cidx 38                       1
        Cidx 37                       1
        Cidx 36                       1
        Cidx 35                       1
        Cidx 34                       1
        Cidx 33                       1
        Cidx 32                       1
        Cidx 47                       1
        Cidx 46                       1
        Cidx 45                       1
        Cidx 44                       1
        Cidx 43                       1
        Cidx 42                       1
        Cidx 41                       1
        Cidx 40                       1
        Cidx 55                       1
        Cidx 54                       1
        Cidx 53                       1
        Cidx 52                       1
        Cidx 51                       1
        Cidx 50                       1
        Cidx 49                       1
        Cidx 48                       1
        Cidx 63                       1
        Cidx 62                       1
        Cidx 61                       1
        Cidx 60                       1
        Cidx 59                       1
        Cidx 58                       1
        Cidx 57                       1
        Cidx 56                       1
        Cidx 71                       1
        Cidx 70                       1
        Cidx 69                       1
        Cidx 68                       1
        Cidx 67                       1
        Cidx 66                       1
        Cidx 65                       1
        Cidx 64                       1
        Cidx 79                       1
        Cidx 78                       1
        Cidx 77                       1
        Cidx 76                       1
        Cidx 75                       1
        Cidx 74                       1
        Cidx 73                       1
        Cidx 72                       1
        Cidx 87                       1
        Cidx 86                       1
        Cidx 85                       1
        Cidx 84                       1
        Cidx 83                       1
        Cidx 82                       1
        Cidx 81                       1
        Cidx 80                       1
        Cidx 95                       1
        Cidx 94                       1
        Cidx 93                       1
        Cidx 92                       1
        Cidx 91                       1
        Cidx 90                       1
        Cidx 89                       1
        Cidx 88                       1
        Cidx 103                      1
        Cidx 102                      1
        Cidx 101                      1
        Cidx 100                      1
        Cidx 99                       1
        Cidx 98                       1
        Cidx 97                       1
        Cidx 96                       1
        Cidx 111                      1
        Cidx 110                      1
        Cidx 109                      1
        Cidx 108                      1
        Cidx 107                      1
        Cidx 106                      1
        Cidx 105                      1
        Cidx 104                      1
        Cidx 119                      1
        Cidx 118                      1
        Cidx 117                      1
        Cidx 116                      1
        Cidx 115                      1
        Cidx 114                      1
        Cidx 113                      1
        Cidx 112                      1
        Cidx 127                      1
        Cidx 126                      1
        Cidx 125                      1
        Cidx 124                      1
        Cidx 123                      1
        Cidx 122                      1
        Cidx 121                      1
        Cidx 120                      1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            CIDX_7 = 0xFF
            CIDX_6 = CIDX_7 - 1
            CIDX_5 = CIDX_6 - 1
            CIDX_4 = CIDX_5 - 1
            CIDX_3 = CIDX_4 - 1
            CIDX_2 = CIDX_3 - 1
            CIDX_1 = CIDX_2 - 1
            CIDX_0 = CIDX_1 - 1
            CIDX_15 = CIDX_0 - 1
            CIDX_14 = CIDX_15 - 1
            CIDX_13 = CIDX_14 - 1
            CIDX_12 = CIDX_13 - 1
            CIDX_11 = CIDX_12 - 1
            CIDX_10 = CIDX_11 - 1
            CIDX_9 = CIDX_10 - 1
            CIDX_8 = CIDX_9 - 1
            CIDX_23 = CIDX_8 - 1
            CIDX_22 = CIDX_23 - 1
            CIDX_21 = CIDX_22 - 1
            CIDX_20 = CIDX_21 - 1
            CIDX_19 = CIDX_20 - 1
            CIDX_18 = CIDX_19 - 1
            CIDX_17 = CIDX_18 - 1
            CIDX_16 = CIDX_17 - 1
            CIDX_31 = CIDX_16 - 1
            CIDX_30 = CIDX_31 - 1
            CIDX_29 = CIDX_30 - 1
            CIDX_28 = CIDX_29 - 1
            CIDX_27 = CIDX_28 - 1
            CIDX_26 = CIDX_27 - 1
            CIDX_25 = CIDX_26 - 1
            CIDX_24 = CIDX_25 - 1
            CIDX_39 = CIDX_24 - 1
            CIDX_38 = CIDX_39 - 1
            CIDX_37 = CIDX_38 - 1
            CIDX_36 = CIDX_37 - 1
            CIDX_35 = CIDX_36 - 1
            CIDX_34 = CIDX_35 - 1
            CIDX_33 = CIDX_34 - 1
            CIDX_32 = CIDX_33 - 1
            CIDX_47 = CIDX_32 - 1
            CIDX_46 = CIDX_47 - 1
            CIDX_45 = CIDX_46 - 1
            CIDX_44 = CIDX_45 - 1
            CIDX_43 = CIDX_44 - 1
            CIDX_42 = CIDX_43 - 1
            CIDX_41 = CIDX_42 - 1
            CIDX_40 = CIDX_41 - 1
            CIDX_55 = CIDX_40 - 1
            CIDX_54 = CIDX_55 - 1
            CIDX_53 = CIDX_54 - 1
            CIDX_52 = CIDX_53 - 1
            CIDX_51 = CIDX_52 - 1
            CIDX_50 = CIDX_51 - 1
            CIDX_49 = CIDX_50 - 1
            CIDX_48 = CIDX_49 - 1
            CIDX_63 = CIDX_48 - 1
            CIDX_62 = CIDX_63 - 1
            CIDX_61 = CIDX_62 - 1
            CIDX_60 = CIDX_61 - 1
            CIDX_59 = CIDX_60 - 1
            CIDX_58 = CIDX_59 - 1
            CIDX_57 = CIDX_58 - 1
            CIDX_56 = CIDX_57 - 1
            CIDX_71 = CIDX_56 - 1
            CIDX_70 = CIDX_71 - 1
            CIDX_69 = CIDX_70 - 1
            CIDX_68 = CIDX_69 - 1
            CIDX_67 = CIDX_68 - 1
            CIDX_66 = CIDX_67 - 1
            CIDX_65 = CIDX_66 - 1
            CIDX_64 = CIDX_65 - 1
            CIDX_79 = CIDX_64 - 1
            CIDX_78 = CIDX_79 - 1
            CIDX_77 = CIDX_78 - 1
            CIDX_76 = CIDX_77 - 1
            CIDX_75 = CIDX_76 - 1
            CIDX_74 = CIDX_75 - 1
            CIDX_73 = CIDX_74 - 1
            CIDX_72 = CIDX_73 - 1
            CIDX_87 = CIDX_72 - 1
            CIDX_86 = CIDX_87 - 1
            CIDX_85 = CIDX_86 - 1
            CIDX_84 = CIDX_85 - 1
            CIDX_83 = CIDX_84 - 1
            CIDX_82 = CIDX_83 - 1
            CIDX_81 = CIDX_82 - 1
            CIDX_80 = CIDX_81 - 1
            CIDX_95 = CIDX_80 - 1
            CIDX_94 = CIDX_95 - 1
            CIDX_93 = CIDX_94 - 1
            CIDX_92 = CIDX_93 - 1
            CIDX_91 = CIDX_92 - 1
            CIDX_90 = CIDX_91 - 1
            CIDX_89 = CIDX_90 - 1
            CIDX_88 = CIDX_89 - 1
            CIDX_103 = CIDX_88 - 1
            CIDX_102 = CIDX_103 - 1
            CIDX_101 = CIDX_102 - 1
            CIDX_100 = CIDX_101 - 1
            CIDX_99 = CIDX_100 - 1
            CIDX_98 = CIDX_99 - 1
            CIDX_97 = CIDX_98 - 1
            CIDX_96 = CIDX_97 - 1
            CIDX_111 = CIDX_96 - 1
            CIDX_110 = CIDX_111 - 1
            CIDX_109 = CIDX_110 - 1
            CIDX_108 = CIDX_109 - 1
            CIDX_107 = CIDX_108 - 1
            CIDX_106 = CIDX_107 - 1
            CIDX_105 = CIDX_106 - 1
            CIDX_104 = CIDX_105 - 1
            CIDX_119 = CIDX_104 - 1
            CIDX_118 = CIDX_119 - 1
            CIDX_117 = CIDX_118 - 1
            CIDX_116 = CIDX_117 - 1
            CIDX_115 = CIDX_116 - 1
            CIDX_114 = CIDX_115 - 1
            CIDX_113 = CIDX_114 - 1
            CIDX_112 = CIDX_113 - 1
            CIDX_127 = CIDX_112 - 1
            CIDX_126 = CIDX_127 - 1
            CIDX_125 = CIDX_126 - 1
            CIDX_124 = CIDX_125 - 1
            CIDX_123 = CIDX_124 - 1
            CIDX_122 = CIDX_123 - 1
            CIDX_121 = CIDX_122 - 1
            CIDX_120 = CIDX_121 - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            CIDX_7 = 0x1
            CIDX_6 = 0x1
            CIDX_5 = 0x1
            CIDX_4 = 0x1
            CIDX_3 = 0x1
            CIDX_2 = 0x1
            CIDX_1 = 0x1
            CIDX_0 = 0x1
            CIDX_15 = 0x1
            CIDX_14 = 0x1
            CIDX_13 = 0x1
            CIDX_12 = 0x1
            CIDX_11 = 0x1
            CIDX_10 = 0x1
            CIDX_9 = 0x1
            CIDX_8 = 0x1
            CIDX_23 = 0x1
            CIDX_22 = 0x1
            CIDX_21 = 0x1
            CIDX_20 = 0x1
            CIDX_19 = 0x1
            CIDX_18 = 0x1
            CIDX_17 = 0x1
            CIDX_16 = 0x1
            CIDX_31 = 0x1
            CIDX_30 = 0x1
            CIDX_29 = 0x1
            CIDX_28 = 0x1
            CIDX_27 = 0x1
            CIDX_26 = 0x1
            CIDX_25 = 0x1
            CIDX_24 = 0x1
            CIDX_39 = 0x1
            CIDX_38 = 0x1
            CIDX_37 = 0x1
            CIDX_36 = 0x1
            CIDX_35 = 0x1
            CIDX_34 = 0x1
            CIDX_33 = 0x1
            CIDX_32 = 0x1
            CIDX_47 = 0x1
            CIDX_46 = 0x1
            CIDX_45 = 0x1
            CIDX_44 = 0x1
            CIDX_43 = 0x1
            CIDX_42 = 0x1
            CIDX_41 = 0x1
            CIDX_40 = 0x1
            CIDX_55 = 0x1
            CIDX_54 = 0x1
            CIDX_53 = 0x1
            CIDX_52 = 0x1
            CIDX_51 = 0x1
            CIDX_50 = 0x1
            CIDX_49 = 0x1
            CIDX_48 = 0x1
            CIDX_63 = 0x1
            CIDX_62 = 0x1
            CIDX_61 = 0x1
            CIDX_60 = 0x1
            CIDX_59 = 0x1
            CIDX_58 = 0x1
            CIDX_57 = 0x1
            CIDX_56 = 0x1
            CIDX_71 = 0x1
            CIDX_70 = 0x1
            CIDX_69 = 0x1
            CIDX_68 = 0x1
            CIDX_67 = 0x1
            CIDX_66 = 0x1
            CIDX_65 = 0x1
            CIDX_64 = 0x1
            CIDX_79 = 0x1
            CIDX_78 = 0x1
            CIDX_77 = 0x1
            CIDX_76 = 0x1
            CIDX_75 = 0x1
            CIDX_74 = 0x1
            CIDX_73 = 0x1
            CIDX_72 = 0x1
            CIDX_87 = 0x1
            CIDX_86 = 0x1
            CIDX_85 = 0x1
            CIDX_84 = 0x1
            CIDX_83 = 0x1
            CIDX_82 = 0x1
            CIDX_81 = 0x1
            CIDX_80 = 0x1
            CIDX_95 = 0x1
            CIDX_94 = 0x1
            CIDX_93 = 0x1
            CIDX_92 = 0x1
            CIDX_91 = 0x1
            CIDX_90 = 0x1
            CIDX_89 = 0x1
            CIDX_88 = 0x1
            CIDX_103 = 0x1
            CIDX_102 = 0x1
            CIDX_101 = 0x1
            CIDX_100 = 0x1
            CIDX_99 = 0x1
            CIDX_98 = 0x1
            CIDX_97 = 0x1
            CIDX_96 = 0x1
            CIDX_111 = 0x1
            CIDX_110 = 0x1
            CIDX_109 = 0x1
            CIDX_108 = 0x1
            CIDX_107 = 0x1
            CIDX_106 = 0x1
            CIDX_105 = 0x1
            CIDX_104 = 0x1
            CIDX_119 = 0x1
            CIDX_118 = 0x1
            CIDX_117 = 0x1
            CIDX_116 = 0x1
            CIDX_115 = 0x1
            CIDX_114 = 0x1
            CIDX_113 = 0x1
            CIDX_112 = 0x1
            CIDX_127 = 0x1
            CIDX_126 = 0x1
            CIDX_125 = 0x1
            CIDX_124 = 0x1
            CIDX_123 = 0x1
            CIDX_122 = 0x1
            CIDX_121 = 0x1
            CIDX_120 = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.CIDX_7, length=LEN.CIDX_7,
                     title="Cidx7", name="cidx_7",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_7) - 1),)),
            BitField(fid=FID.CIDX_6, length=LEN.CIDX_6,
                     title="Cidx6", name="cidx_6",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_6) - 1),)),
            BitField(fid=FID.CIDX_5, length=LEN.CIDX_5,
                     title="Cidx5", name="cidx_5",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_5) - 1),)),
            BitField(fid=FID.CIDX_4, length=LEN.CIDX_4,
                     title="Cidx4", name="cidx_4",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_4) - 1),)),
            BitField(fid=FID.CIDX_3, length=LEN.CIDX_3,
                     title="Cidx3", name="cidx_3",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_3) - 1),)),
            BitField(fid=FID.CIDX_2, length=LEN.CIDX_2,
                     title="Cidx2", name="cidx_2",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_2) - 1),)),
            BitField(fid=FID.CIDX_1, length=LEN.CIDX_1,
                     title="Cidx1", name="cidx_1",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_1) - 1),)),
            BitField(fid=FID.CIDX_0, length=LEN.CIDX_0,
                     title="Cidx0", name="cidx_0",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_0) - 1),)),
            BitField(fid=FID.CIDX_15, length=LEN.CIDX_15,
                     title="Cidx15", name="cidx_15",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_15) - 1),)),
            BitField(fid=FID.CIDX_14, length=LEN.CIDX_14,
                     title="Cidx14", name="cidx_14",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_14) - 1),)),
            BitField(fid=FID.CIDX_13, length=LEN.CIDX_13,
                     title="Cidx13", name="cidx_13",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_13) - 1),)),
            BitField(fid=FID.CIDX_12, length=LEN.CIDX_12,
                     title="Cidx12", name="cidx_12",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_12) - 1),)),
            BitField(fid=FID.CIDX_11, length=LEN.CIDX_11,
                     title="Cidx11", name="cidx_11",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_11) - 1),)),
            BitField(fid=FID.CIDX_10, length=LEN.CIDX_10,
                     title="Cidx10", name="cidx_10",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_10) - 1),)),
            BitField(fid=FID.CIDX_9, length=LEN.CIDX_9,
                     title="Cidx9", name="cidx_9",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_9) - 1),)),
            BitField(fid=FID.CIDX_8, length=LEN.CIDX_8,
                     title="Cidx8", name="cidx_8",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_8) - 1),)),
            BitField(fid=FID.CIDX_23, length=LEN.CIDX_23,
                     title="Cidx23", name="cidx_23",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_23) - 1),)),
            BitField(fid=FID.CIDX_22, length=LEN.CIDX_22,
                     title="Cidx22", name="cidx_22",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_22) - 1),)),
            BitField(fid=FID.CIDX_21, length=LEN.CIDX_21,
                     title="Cidx21", name="cidx_21",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_21) - 1),)),
            BitField(fid=FID.CIDX_20, length=LEN.CIDX_20,
                     title="Cidx20", name="cidx_20",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_20) - 1),)),
            BitField(fid=FID.CIDX_19, length=LEN.CIDX_19,
                     title="Cidx19", name="cidx_19",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_19) - 1),)),
            BitField(fid=FID.CIDX_18, length=LEN.CIDX_18,
                     title="Cidx18", name="cidx_18",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_18) - 1),)),
            BitField(fid=FID.CIDX_17, length=LEN.CIDX_17,
                     title="Cidx17", name="cidx_17",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_17) - 1),)),
            BitField(fid=FID.CIDX_16, length=LEN.CIDX_16,
                     title="Cidx16", name="cidx_16",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_16) - 1),)),
            BitField(fid=FID.CIDX_31, length=LEN.CIDX_31,
                     title="Cidx31", name="cidx_31",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_31) - 1),)),
            BitField(fid=FID.CIDX_30, length=LEN.CIDX_30,
                     title="Cidx30", name="cidx_30",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_30) - 1),)),
            BitField(fid=FID.CIDX_29, length=LEN.CIDX_29,
                     title="Cidx29", name="cidx_29",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_29) - 1),)),
            BitField(fid=FID.CIDX_28, length=LEN.CIDX_28,
                     title="Cidx28", name="cidx_28",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_28) - 1),)),
            BitField(fid=FID.CIDX_27, length=LEN.CIDX_27,
                     title="Cidx27", name="cidx_27",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_27) - 1),)),
            BitField(fid=FID.CIDX_26, length=LEN.CIDX_26,
                     title="Cidx26", name="cidx_26",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_26) - 1),)),
            BitField(fid=FID.CIDX_25, length=LEN.CIDX_25,
                     title="Cidx25", name="cidx_25",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_25) - 1),)),
            BitField(fid=FID.CIDX_24, length=LEN.CIDX_24,
                     title="Cidx24", name="cidx_24",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_24) - 1),)),
            BitField(fid=FID.CIDX_39, length=LEN.CIDX_39,
                     title="Cidx39", name="cidx_39",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_39) - 1),)),
            BitField(fid=FID.CIDX_38, length=LEN.CIDX_38,
                     title="Cidx38", name="cidx_38",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_38) - 1),)),
            BitField(fid=FID.CIDX_37, length=LEN.CIDX_37,
                     title="Cidx37", name="cidx_37",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_37) - 1),)),
            BitField(fid=FID.CIDX_36, length=LEN.CIDX_36,
                     title="Cidx36", name="cidx_36",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_36) - 1),)),
            BitField(fid=FID.CIDX_35, length=LEN.CIDX_35,
                     title="Cidx35", name="cidx_35",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_35) - 1),)),
            BitField(fid=FID.CIDX_34, length=LEN.CIDX_34,
                     title="Cidx34", name="cidx_34",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_34) - 1),)),
            BitField(fid=FID.CIDX_33, length=LEN.CIDX_33,
                     title="Cidx33", name="cidx_33",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_33) - 1),)),
            BitField(fid=FID.CIDX_32, length=LEN.CIDX_32,
                     title="Cidx32", name="cidx_32",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_32) - 1),)),
            BitField(fid=FID.CIDX_47, length=LEN.CIDX_47,
                     title="Cidx47", name="cidx_47",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_47) - 1),)),
            BitField(fid=FID.CIDX_46, length=LEN.CIDX_46,
                     title="Cidx46", name="cidx_46",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_46) - 1),)),
            BitField(fid=FID.CIDX_45, length=LEN.CIDX_45,
                     title="Cidx45", name="cidx_45",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_45) - 1),)),
            BitField(fid=FID.CIDX_44, length=LEN.CIDX_44,
                     title="Cidx44", name="cidx_44",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_44) - 1),)),
            BitField(fid=FID.CIDX_43, length=LEN.CIDX_43,
                     title="Cidx43", name="cidx_43",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_43) - 1),)),
            BitField(fid=FID.CIDX_42, length=LEN.CIDX_42,
                     title="Cidx42", name="cidx_42",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_42) - 1),)),
            BitField(fid=FID.CIDX_41, length=LEN.CIDX_41,
                     title="Cidx41", name="cidx_41",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_41) - 1),)),
            BitField(fid=FID.CIDX_40, length=LEN.CIDX_40,
                     title="Cidx40", name="cidx_40",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_40) - 1),)),
            BitField(fid=FID.CIDX_55, length=LEN.CIDX_55,
                     title="Cidx55", name="cidx_55",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_55) - 1),)),
            BitField(fid=FID.CIDX_54, length=LEN.CIDX_54,
                     title="Cidx54", name="cidx_54",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_54) - 1),)),
            BitField(fid=FID.CIDX_53, length=LEN.CIDX_53,
                     title="Cidx53", name="cidx_53",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_53) - 1),)),
            BitField(fid=FID.CIDX_52, length=LEN.CIDX_52,
                     title="Cidx52", name="cidx_52",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_52) - 1),)),
            BitField(fid=FID.CIDX_51, length=LEN.CIDX_51,
                     title="Cidx51", name="cidx_51",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_51) - 1),)),
            BitField(fid=FID.CIDX_50, length=LEN.CIDX_50,
                     title="Cidx50", name="cidx_50",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_50) - 1),)),
            BitField(fid=FID.CIDX_49, length=LEN.CIDX_49,
                     title="Cidx49", name="cidx_49",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_49) - 1),)),
            BitField(fid=FID.CIDX_48, length=LEN.CIDX_48,
                     title="Cidx48", name="cidx_48",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_48) - 1),)),
            BitField(fid=FID.CIDX_63, length=LEN.CIDX_63,
                     title="Cidx63", name="cidx_63",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_63) - 1),)),
            BitField(fid=FID.CIDX_62, length=LEN.CIDX_62,
                     title="Cidx62", name="cidx_62",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_62) - 1),)),
            BitField(fid=FID.CIDX_61, length=LEN.CIDX_61,
                     title="Cidx61", name="cidx_61",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_61) - 1),)),
            BitField(fid=FID.CIDX_60, length=LEN.CIDX_60,
                     title="Cidx60", name="cidx_60",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_60) - 1),)),
            BitField(fid=FID.CIDX_59, length=LEN.CIDX_59,
                     title="Cidx59", name="cidx_59",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_59) - 1),)),
            BitField(fid=FID.CIDX_58, length=LEN.CIDX_58,
                     title="Cidx58", name="cidx_58",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_58) - 1),)),
            BitField(fid=FID.CIDX_57, length=LEN.CIDX_57,
                     title="Cidx57", name="cidx_57",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_57) - 1),)),
            BitField(fid=FID.CIDX_56, length=LEN.CIDX_56,
                     title="Cidx56", name="cidx_56",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_56) - 1),)),
            BitField(fid=FID.CIDX_71, length=LEN.CIDX_71,
                     title="Cidx71", name="cidx_71",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_71) - 1),)),
            BitField(fid=FID.CIDX_70, length=LEN.CIDX_70,
                     title="Cidx70", name="cidx_70",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_70) - 1),)),
            BitField(fid=FID.CIDX_69, length=LEN.CIDX_69,
                     title="Cidx69", name="cidx_69",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_69) - 1),)),
            BitField(fid=FID.CIDX_68, length=LEN.CIDX_68,
                     title="Cidx68", name="cidx_68",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_68) - 1),)),
            BitField(fid=FID.CIDX_67, length=LEN.CIDX_67,
                     title="Cidx67", name="cidx_67",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_67) - 1),)),
            BitField(fid=FID.CIDX_66, length=LEN.CIDX_66,
                     title="Cidx66", name="cidx_66",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_66) - 1),)),
            BitField(fid=FID.CIDX_65, length=LEN.CIDX_65,
                     title="Cidx65", name="cidx_65",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_65) - 1),)),
            BitField(fid=FID.CIDX_64, length=LEN.CIDX_64,
                     title="Cidx64", name="cidx_64",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_64) - 1),)),
            BitField(fid=FID.CIDX_79, length=LEN.CIDX_79,
                     title="Cidx79", name="cidx_79",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_79) - 1),)),
            BitField(fid=FID.CIDX_78, length=LEN.CIDX_78,
                     title="Cidx78", name="cidx_78",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_78) - 1),)),
            BitField(fid=FID.CIDX_77, length=LEN.CIDX_77,
                     title="Cidx77", name="cidx_77",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_77) - 1),)),
            BitField(fid=FID.CIDX_76, length=LEN.CIDX_76,
                     title="Cidx76", name="cidx_76",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_76) - 1),)),
            BitField(fid=FID.CIDX_75, length=LEN.CIDX_75,
                     title="Cidx75", name="cidx_75",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_75) - 1),)),
            BitField(fid=FID.CIDX_74, length=LEN.CIDX_74,
                     title="Cidx74", name="cidx_74",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_74) - 1),)),
            BitField(fid=FID.CIDX_73, length=LEN.CIDX_73,
                     title="Cidx73", name="cidx_73",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_73) - 1),)),
            BitField(fid=FID.CIDX_72, length=LEN.CIDX_72,
                     title="Cidx72", name="cidx_72",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_72) - 1),)),
            BitField(fid=FID.CIDX_87, length=LEN.CIDX_87,
                     title="Cidx87", name="cidx_87",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_87) - 1),)),
            BitField(fid=FID.CIDX_86, length=LEN.CIDX_86,
                     title="Cidx86", name="cidx_86",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_86) - 1),)),
            BitField(fid=FID.CIDX_85, length=LEN.CIDX_85,
                     title="Cidx85", name="cidx_85",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_85) - 1),)),
            BitField(fid=FID.CIDX_84, length=LEN.CIDX_84,
                     title="Cidx84", name="cidx_84",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_84) - 1),)),
            BitField(fid=FID.CIDX_83, length=LEN.CIDX_83,
                     title="Cidx83", name="cidx_83",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_83) - 1),)),
            BitField(fid=FID.CIDX_82, length=LEN.CIDX_82,
                     title="Cidx82", name="cidx_82",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_82) - 1),)),
            BitField(fid=FID.CIDX_81, length=LEN.CIDX_81,
                     title="Cidx81", name="cidx_81",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_81) - 1),)),
            BitField(fid=FID.CIDX_80, length=LEN.CIDX_80,
                     title="Cidx80", name="cidx_80",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_80) - 1),)),
            BitField(fid=FID.CIDX_95, length=LEN.CIDX_95,
                     title="Cidx95", name="cidx_95",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_95) - 1),)),
            BitField(fid=FID.CIDX_94, length=LEN.CIDX_94,
                     title="Cidx94", name="cidx_94",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_94) - 1),)),
            BitField(fid=FID.CIDX_93, length=LEN.CIDX_93,
                     title="Cidx93", name="cidx_93",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_93) - 1),)),
            BitField(fid=FID.CIDX_92, length=LEN.CIDX_92,
                     title="Cidx92", name="cidx_92",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_92) - 1),)),
            BitField(fid=FID.CIDX_91, length=LEN.CIDX_91,
                     title="Cidx91", name="cidx_91",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_91) - 1),)),
            BitField(fid=FID.CIDX_90, length=LEN.CIDX_90,
                     title="Cidx90", name="cidx_90",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_90) - 1),)),
            BitField(fid=FID.CIDX_89, length=LEN.CIDX_89,
                     title="Cidx89", name="cidx_89",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_89) - 1),)),
            BitField(fid=FID.CIDX_88, length=LEN.CIDX_88,
                     title="Cidx88", name="cidx_88",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_88) - 1),)),
            BitField(fid=FID.CIDX_103, length=LEN.CIDX_103,
                     title="Cidx103", name="cidx_103",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_103) - 1),)),
            BitField(fid=FID.CIDX_102, length=LEN.CIDX_102,
                     title="Cidx102", name="cidx_102",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_102) - 1),)),
            BitField(fid=FID.CIDX_101, length=LEN.CIDX_101,
                     title="Cidx101", name="cidx_101",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_101) - 1),)),
            BitField(fid=FID.CIDX_100, length=LEN.CIDX_100,
                     title="Cidx100", name="cidx_100",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_100) - 1),)),
            BitField(fid=FID.CIDX_99, length=LEN.CIDX_99,
                     title="Cidx99", name="cidx_99",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_99) - 1),)),
            BitField(fid=FID.CIDX_98, length=LEN.CIDX_98,
                     title="Cidx98", name="cidx_98",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_98) - 1),)),
            BitField(fid=FID.CIDX_97, length=LEN.CIDX_97,
                     title="Cidx97", name="cidx_97",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_97) - 1),)),
            BitField(fid=FID.CIDX_96, length=LEN.CIDX_96,
                     title="Cidx96", name="cidx_96",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_96) - 1),)),
            BitField(fid=FID.CIDX_111, length=LEN.CIDX_111,
                     title="Cidx111", name="cidx_111",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_111) - 1),)),
            BitField(fid=FID.CIDX_110, length=LEN.CIDX_110,
                     title="Cidx110", name="cidx_110",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_110) - 1),)),
            BitField(fid=FID.CIDX_109, length=LEN.CIDX_109,
                     title="Cidx109", name="cidx_109",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_109) - 1),)),
            BitField(fid=FID.CIDX_108, length=LEN.CIDX_108,
                     title="Cidx108", name="cidx_108",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_108) - 1),)),
            BitField(fid=FID.CIDX_107, length=LEN.CIDX_107,
                     title="Cidx107", name="cidx_107",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_107) - 1),)),
            BitField(fid=FID.CIDX_106, length=LEN.CIDX_106,
                     title="Cidx106", name="cidx_106",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_106) - 1),)),
            BitField(fid=FID.CIDX_105, length=LEN.CIDX_105,
                     title="Cidx105", name="cidx_105",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_105) - 1),)),
            BitField(fid=FID.CIDX_104, length=LEN.CIDX_104,
                     title="Cidx104", name="cidx_104",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_104) - 1),)),
            BitField(fid=FID.CIDX_119, length=LEN.CIDX_119,
                     title="Cidx119", name="cidx_119",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_119) - 1),)),
            BitField(fid=FID.CIDX_118, length=LEN.CIDX_118,
                     title="Cidx118", name="cidx_118",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_118) - 1),)),
            BitField(fid=FID.CIDX_117, length=LEN.CIDX_117,
                     title="Cidx117", name="cidx_117",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_117) - 1),)),
            BitField(fid=FID.CIDX_116, length=LEN.CIDX_116,
                     title="Cidx116", name="cidx_116",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_116) - 1),)),
            BitField(fid=FID.CIDX_115, length=LEN.CIDX_115,
                     title="Cidx115", name="cidx_115",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_115) - 1),)),
            BitField(fid=FID.CIDX_114, length=LEN.CIDX_114,
                     title="Cidx114", name="cidx_114",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_114) - 1),)),
            BitField(fid=FID.CIDX_113, length=LEN.CIDX_113,
                     title="Cidx113", name="cidx_113",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_113) - 1),)),
            BitField(fid=FID.CIDX_112, length=LEN.CIDX_112,
                     title="Cidx112", name="cidx_112",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_112) - 1),)),
            BitField(fid=FID.CIDX_127, length=LEN.CIDX_127,
                     title="Cidx127", name="cidx_127",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_127) - 1),)),
            BitField(fid=FID.CIDX_126, length=LEN.CIDX_126,
                     title="Cidx126", name="cidx_126",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_126) - 1),)),
            BitField(fid=FID.CIDX_125, length=LEN.CIDX_125,
                     title="Cidx125", name="cidx_125",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_125) - 1),)),
            BitField(fid=FID.CIDX_124, length=LEN.CIDX_124,
                     title="Cidx124", name="cidx_124",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_124) - 1),)),
            BitField(fid=FID.CIDX_123, length=LEN.CIDX_123,
                     title="Cidx123", name="cidx_123",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_123) - 1),)),
            BitField(fid=FID.CIDX_122, length=LEN.CIDX_122,
                     title="Cidx122", name="cidx_122",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_122) - 1),)),
            BitField(fid=FID.CIDX_121, length=LEN.CIDX_121,
                     title="Cidx121", name="cidx_121",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_121) - 1),)),
            BitField(fid=FID.CIDX_120, length=LEN.CIDX_120,
                     title="Cidx120", name="cidx_120",
                     checks=(CheckInt(0, pow(2, LEN.CIDX_120) - 1),)),
        )
    # end class CidxBitmap

    class GameModeFullState(BitFieldContainerMixin):
        """
        Define ``GameModeFullState`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      4
        Lock Supported                1
        Supported                     1
        Locked                        1
        Enabled                       1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            LOCK_SUPPORTED = RESERVED - 1
            SUPPORTED = LOCK_SUPPORTED - 1
            LOCKED = SUPPORTED - 1
            ENABLED = LOCKED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x4
            LOCK_SUPPORTED = 0x1
            SUPPORTED = 0x1
            LOCKED = 0x1
            ENABLED = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),
            BitField(fid=FID.LOCK_SUPPORTED, length=LEN.LOCK_SUPPORTED,
                     title="LockSupported", name="lock_supported",
                     checks=(CheckInt(0, pow(2, LEN.LOCK_SUPPORTED) - 1),)),
            BitField(fid=FID.SUPPORTED, length=LEN.SUPPORTED,
                     title="Supported", name="supported",
                     checks=(CheckInt(0, pow(2, LEN.SUPPORTED) - 1),)),
            BitField(fid=FID.LOCKED, length=LEN.LOCKED,
                     title="Locked", name="locked",
                     checks=(CheckInt(0, pow(2, LEN.LOCKED) - 1),)),
            BitField(fid=FID.ENABLED, length=LEN.ENABLED,
                     title="Enabled", name="enabled",
                     checks=(CheckInt(0, pow(2, LEN.ENABLED) - 1),)),
        )
    # end class GameModeFullState

    class SetMask(BitFieldContainerMixin):
        """
        Define ``SetMask`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      6
        poweron game mode lock        1
        poweron game mode             1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            POWERON_GAME_MODE_LOCK = RESERVED - 1
            POWERON_GAME_MODE = POWERON_GAME_MODE_LOCK - 1

        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x6
            POWERON_GAME_MODE_LOCK = 0x1
            POWERON_GAME_MODE = 0x1

        # end class LENNone

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),)),
            BitField(fid=FID.POWERON_GAME_MODE_LOCK, length=LEN.POWERON_GAME_MODE_LOCK,
                     title="PoweronGameModeLock", name="poweron_game_mode_lock",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.POWERON_GAME_MODE_LOCK) - 1),)),
            BitField(fid=FID.POWERON_GAME_MODE, length=LEN.POWERON_GAME_MODE,
                     title="PoweronGameMode", name="poweron_game_mode",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.POWERON_GAME_MODE) - 1),)),
        )
    # end class SetMask

    class SetValue(SetMask):
        """
        See ``SetMask`` information
        """
        pass
    # end class SetValue

    class GetValue(SetMask):
        """
        See ``SetMask`` information
        """
        pass
    # end class GetValue

    class SupportedPowerOnParams(BitFieldContainerMixin):
        """
        Define ``SupportedPowerOnParams`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      6
        poweron game mode lock        1
        poweron game mode             1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            POWERON_GAME_MODE_LOCK = RESERVED - 1
            POWERON_GAME_MODE = POWERON_GAME_MODE_LOCK - 1

        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x6
            POWERON_GAME_MODE_LOCK = 0x1
            POWERON_GAME_MODE = 0x1

        # end class LENNone

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),)),
            BitField(fid=FID.POWERON_GAME_MODE_LOCK, length=LEN.POWERON_GAME_MODE_LOCK,
                     title="PoweronGameModeLock", name="poweron_game_mode_lock",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.POWERON_GAME_MODE_LOCK) - 1),)),
            BitField(fid=FID.POWERON_GAME_MODE, length=LEN.POWERON_GAME_MODE,
                     title="PoweronGameMode", name="poweron_game_mode",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.POWERON_GAME_MODE) - 1),)),
        )
    # end class SupportedPowerOnParams

    class GameModeState(BitFieldContainerMixin):
        """
        Define ``GameModeState`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      6
        Locked                        1
        Enabled                       1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            LOCKED = RESERVED - 1
            ENABLED = LOCKED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x6
            LOCKED = 0x1
            ENABLED = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),)),
            BitField(fid=FID.LOCKED, length=LEN.LOCKED,
                     title="Locked", name="locked",
                     checks=(CheckInt(0, pow(2, LEN.LOCKED) - 1),)),
            BitField(fid=FID.ENABLED, length=LEN.ENABLED,
                     title="Enabled", name="enabled",
                     checks=(CheckInt(0, pow(2, LEN.ENABLED) - 1),)),
        )
    # end class GameModeState
# end class DisableControlsByCIDX


class DisableControlsByCIDXModel(FeatureModel):
    """
    Define ``DisableControlsByCIDX`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        SET_DISABLED_CONTROLS = 0
        GET_GAME_MODE = 1
        GET_SET_POWER_ON_PARAMS = 2
        GET_CAPABILITIES = 3

        # Event index
        GAME_MODE = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``DisableControlsByCIDX`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.SET_DISABLED_CONTROLS: {
                    "request": SetDisabledControls,
                    "response": SetDisabledControlsResponse
                },
                cls.INDEX.GET_GAME_MODE: {
                    "request": GetGameMode,
                    "response": GetGameModeResponse
                }
            },
            "events": {
                cls.INDEX.GAME_MODE: {"report": GameModeEvent}
            }
        }

        function_map_v1 = {
            "functions": {
                cls.INDEX.SET_DISABLED_CONTROLS: {
                    "request": SetDisabledControls,
                    "response": SetDisabledControlsResponse
                },
                cls.INDEX.GET_GAME_MODE: {
                    "request": GetGameMode,
                    "response": GetGameModeResponse
                },
                cls.INDEX.GET_SET_POWER_ON_PARAMS: {
                    "request": GetSetPowerOnParams,
                    "response": GetSetPowerOnParamsResponse
                },
                cls.INDEX.GET_CAPABILITIES: {
                    "request": GetCapabilities,
                    "response": GetCapabilitiesResponse
                }
            },
            "events": {
                cls.INDEX.GAME_MODE: {"report": GameModeEvent}
            }
        }

        return {
            "feature_base": DisableControlsByCIDX,
            "versions": {
                DisableControlsByCIDXV0.VERSION: {
                    "main_cls": DisableControlsByCIDXV0,
                    "api": function_map_v0
                },
                DisableControlsByCIDXV1.VERSION: {
                    "main_cls": DisableControlsByCIDXV1,
                    "api": function_map_v1
                }
            }
        }
    # end def _get_data_model
# end class DisableControlsByCIDXModel


class DisableControlsByCIDXFactory(FeatureFactory):
    """
    Get ``DisableControlsByCIDX`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``DisableControlsByCIDX`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``DisableControlsByCIDXInterface``
        """
        return DisableControlsByCIDXModel.get_main_cls(version)()
    # end def create
# end class DisableControlsByCIDXFactory


class DisableControlsByCIDXInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``DisableControlsByCIDX``
    """

    def __init__(self):
        # Requests
        self.set_disabled_controls_cls = None
        self.get_game_mode_cls = None
        self.get_set_power_on_params_cls = None
        self.get_capabilities_cls = None

        # Responses
        self.set_disabled_controls_response_cls = None
        self.get_game_mode_response_cls = None
        self.get_set_power_on_params_response_cls = None
        self.get_capabilities_response_cls = None

        # Events
        self.game_mode_event_cls = None
    # end def __init__
# end class DisableControlsByCIDXInterface


class DisableControlsByCIDXV0(DisableControlsByCIDXInterface):
    """
    Define ``DisableControlsByCIDXV0`` feature

    This feature provides model and unit specific information for version 0

    [0] SetDisabledControls(CidxBitmap) -> None

    [1] GetGameMode() -> GameModeFullState

    [Event 0] GameModeEvent -> GameModeState
    """
    VERSION = 0

    def __init__(self):
        # See ``DisableControlsByCIDX.__init__``
        super().__init__()
        index = DisableControlsByCIDXModel.INDEX

        # Requests
        self.set_disabled_controls_cls = DisableControlsByCIDXModel.get_request_cls(
            self.VERSION, index.SET_DISABLED_CONTROLS)
        self.get_game_mode_cls = DisableControlsByCIDXModel.get_request_cls(
            self.VERSION, index.GET_GAME_MODE)

        # Responses
        self.set_disabled_controls_response_cls = DisableControlsByCIDXModel.get_response_cls(
            self.VERSION, index.SET_DISABLED_CONTROLS)
        self.get_game_mode_response_cls = DisableControlsByCIDXModel.get_response_cls(
            self.VERSION, index.GET_GAME_MODE)

        # Events
        self.game_mode_event_cls = DisableControlsByCIDXModel.get_report_cls(
            self.VERSION, index.GAME_MODE)
    # end def __init__

    def get_max_function_index(self):
        # See ``DisableControlsByCIDXInterface.get_max_function_index``
        return DisableControlsByCIDXModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class DisableControlsByCIDXV0


class DisableControlsByCIDXV1(DisableControlsByCIDXV0):
    """
    Define ``DisableControlsByCIDXV1`` feature

    This feature provides model and unit specific information for version 1

    [0] setDisabledControls(cidxBitmap) -> None

    [1] getGameMode() -> gameModeFullState

    [2] getSetPowerOnParams(setMask, setValue) -> getValue

    [3] getCapabilities() -> supportedPowerOnParams

    [Event 0] GameModeEvent -> gameModeState
    """
    VERSION = 1

    def __init__(self):
        # See ``DisableControlsByCIDXV0.__init__``
        super().__init__()
        index = DisableControlsByCIDXModel.INDEX

        # Requests
        self.get_set_power_on_params_cls = DisableControlsByCIDXModel.get_request_cls(
            self.VERSION, index.GET_SET_POWER_ON_PARAMS)
        self.get_capabilities_cls = DisableControlsByCIDXModel.get_request_cls(
            self.VERSION, index.GET_CAPABILITIES)

        # Responses
        self.get_set_power_on_params_response_cls = DisableControlsByCIDXModel.get_response_cls(
            self.VERSION, index.GET_SET_POWER_ON_PARAMS)
        self.get_capabilities_response_cls = DisableControlsByCIDXModel.get_response_cls(
            self.VERSION, index.GET_CAPABILITIES)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``DisableControlsByCIDXInterface.get_max_function_index``
        return DisableControlsByCIDXModel.get_base_cls().MAX_FUNCTION_INDEX_V1
    # end def get_max_function_index
# end class DisableControlsByCIDXV1


class ShortEmptyPacketDataFormat(DisableControlsByCIDX):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetGameMode

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(DisableControlsByCIDX.FID):
        # See ``DisableControlsByCIDX.FID``
        PADDING = DisableControlsByCIDX.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(DisableControlsByCIDX.LEN):
        # See ``DisableControlsByCIDX.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = DisableControlsByCIDX.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DisableControlsByCIDX.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(DisableControlsByCIDX):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetDisabledControlsResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(DisableControlsByCIDX.FID):
        # See ``DisableControlsByCIDX.FID``
        PADDING = DisableControlsByCIDX.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(DisableControlsByCIDX.LEN):
        # See ``DisableControlsByCIDX.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = DisableControlsByCIDX.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DisableControlsByCIDX.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class SetDisabledControls(DisableControlsByCIDX):
    """
    Define ``SetDisabledControls`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Cidx Bitmap                   128
    ============================  ==========
    """

    class FID(DisableControlsByCIDX.FID):
        # See ``DisableControlsByCIDX.FID``
        CIDX_BITMAP = DisableControlsByCIDX.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(DisableControlsByCIDX.LEN):
        # See ``DisableControlsByCIDX.LEN``
        CIDX_BITMAP = 0x80
    # end class LEN

    FIELDS = DisableControlsByCIDX.FIELDS + (
        BitField(fid=FID.CIDX_BITMAP, length=LEN.CIDX_BITMAP,
                 title="CidxBitmap", name="cidx_bitmap",
                 checks=(CheckHexList(LEN.CIDX_BITMAP // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CIDX_BITMAP) - 1),)),
    )

    def __init__(self, device_index, feature_index, cidx_7, cidx_6, cidx_5, cidx_4, cidx_3, cidx_2, cidx_1, cidx_0,
                 cidx_15, cidx_14, cidx_13, cidx_12, cidx_11, cidx_10, cidx_9, cidx_8, cidx_23, cidx_22, cidx_21,
                 cidx_20, cidx_19, cidx_18, cidx_17, cidx_16, cidx_31, cidx_30, cidx_29, cidx_28, cidx_27, cidx_26,
                 cidx_25, cidx_24, cidx_39, cidx_38, cidx_37, cidx_36, cidx_35, cidx_34, cidx_33, cidx_32, cidx_47,
                 cidx_46, cidx_45, cidx_44, cidx_43, cidx_42, cidx_41, cidx_40, cidx_55, cidx_54, cidx_53, cidx_52,
                 cidx_51, cidx_50, cidx_49, cidx_48, cidx_63, cidx_62, cidx_61, cidx_60, cidx_59, cidx_58, cidx_57,
                 cidx_56, cidx_71, cidx_70, cidx_69, cidx_68, cidx_67, cidx_66, cidx_65, cidx_64, cidx_79, cidx_78,
                 cidx_77, cidx_76, cidx_75, cidx_74, cidx_73, cidx_72, cidx_87, cidx_86, cidx_85, cidx_84, cidx_83,
                 cidx_82, cidx_81, cidx_80, cidx_95, cidx_94, cidx_93, cidx_92, cidx_91, cidx_90, cidx_89, cidx_88,
                 cidx_103, cidx_102, cidx_101, cidx_100, cidx_99, cidx_98, cidx_97, cidx_96, cidx_111, cidx_110,
                 cidx_109, cidx_108, cidx_107, cidx_106, cidx_105, cidx_104, cidx_119, cidx_118, cidx_117, cidx_116,
                 cidx_115, cidx_114, cidx_113, cidx_112, cidx_127, cidx_126, cidx_125, cidx_124, cidx_123, cidx_122,
                 cidx_121, cidx_120, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param cidx_7: Cidx 7
        :type cidx_7: ``int | HexList``
        :param cidx_6: Cidx 6
        :type cidx_6: ``int | HexList``
        :param cidx_5: Cidx 5
        :type cidx_5: ``int | HexList``
        :param cidx_4: Cidx 4
        :type cidx_4: ``int | HexList``
        :param cidx_3: Cidx 3
        :type cidx_3: ``int | HexList``
        :param cidx_2: Cidx 2
        :type cidx_2: ``int | HexList``
        :param cidx_1: Cidx 1
        :type cidx_1: ``int | HexList``
        :param cidx_0: Cidx 0
        :type cidx_0: ``int | HexList``
        :param cidx_15: Cidx 15
        :type cidx_15: ``int | HexList``
        :param cidx_14: Cidx 14
        :type cidx_14: ``int | HexList``
        :param cidx_13: Cidx 13
        :type cidx_13: ``int | HexList``
        :param cidx_12: Cidx 12
        :type cidx_12: ``int | HexList``
        :param cidx_11: Cidx 11
        :type cidx_11: ``int | HexList``
        :param cidx_10: Cidx 10
        :type cidx_10: ``int | HexList``
        :param cidx_9: Cidx 9
        :type cidx_9: ``int | HexList``
        :param cidx_8: Cidx 8
        :type cidx_8: ``int | HexList``
        :param cidx_23: Cidx 23
        :type cidx_23: ``int | HexList``
        :param cidx_22: Cidx 22
        :type cidx_22: ``int | HexList``
        :param cidx_21: Cidx 21
        :type cidx_21: ``int | HexList``
        :param cidx_20: Cidx 20
        :type cidx_20: ``int | HexList``
        :param cidx_19: Cidx 19
        :type cidx_19: ``int | HexList``
        :param cidx_18: Cidx 18
        :type cidx_18: ``int | HexList``
        :param cidx_17: Cidx 17
        :type cidx_17: ``int | HexList``
        :param cidx_16: Cidx 16
        :type cidx_16: ``int | HexList``
        :param cidx_31: Cidx 31
        :type cidx_31: ``int | HexList``
        :param cidx_30: Cidx 30
        :type cidx_30: ``int | HexList``
        :param cidx_29: Cidx 29
        :type cidx_29: ``int | HexList``
        :param cidx_28: Cidx 28
        :type cidx_28: ``int | HexList``
        :param cidx_27: Cidx 27
        :type cidx_27: ``int | HexList``
        :param cidx_26: Cidx 26
        :type cidx_26: ``int | HexList``
        :param cidx_25: Cidx 25
        :type cidx_25: ``int | HexList``
        :param cidx_24: Cidx 24
        :type cidx_24: ``int | HexList``
        :param cidx_39: Cidx 39
        :type cidx_39: ``int | HexList``
        :param cidx_38: Cidx 38
        :type cidx_38: ``int | HexList``
        :param cidx_37: Cidx 37
        :type cidx_37: ``int | HexList``
        :param cidx_36: Cidx 36
        :type cidx_36: ``int | HexList``
        :param cidx_35: Cidx 35
        :type cidx_35: ``int | HexList``
        :param cidx_34: Cidx 34
        :type cidx_34: ``int | HexList``
        :param cidx_33: Cidx 33
        :type cidx_33: ``int | HexList``
        :param cidx_32: Cidx 32
        :type cidx_32: ``int | HexList``
        :param cidx_47: Cidx 47
        :type cidx_47: ``int | HexList``
        :param cidx_46: Cidx 46
        :type cidx_46: ``int | HexList``
        :param cidx_45: Cidx 45
        :type cidx_45: ``int | HexList``
        :param cidx_44: Cidx 44
        :type cidx_44: ``int | HexList``
        :param cidx_43: Cidx 43
        :type cidx_43: ``int | HexList``
        :param cidx_42: Cidx 42
        :type cidx_42: ``int | HexList``
        :param cidx_41: Cidx 41
        :type cidx_41: ``int | HexList``
        :param cidx_40: Cidx 40
        :type cidx_40: ``int | HexList``
        :param cidx_55: Cidx 55
        :type cidx_55: ``int | HexList``
        :param cidx_54: Cidx 54
        :type cidx_54: ``int | HexList``
        :param cidx_53: Cidx 53
        :type cidx_53: ``int | HexList``
        :param cidx_52: Cidx 52
        :type cidx_52: ``int | HexList``
        :param cidx_51: Cidx 51
        :type cidx_51: ``int | HexList``
        :param cidx_50: Cidx 50
        :type cidx_50: ``int | HexList``
        :param cidx_49: Cidx 49
        :type cidx_49: ``int | HexList``
        :param cidx_48: Cidx 48
        :type cidx_48: ``int | HexList``
        :param cidx_63: Cidx 63
        :type cidx_63: ``int | HexList``
        :param cidx_62: Cidx 62
        :type cidx_62: ``int | HexList``
        :param cidx_61: Cidx 61
        :type cidx_61: ``int | HexList``
        :param cidx_60: Cidx 60
        :type cidx_60: ``int | HexList``
        :param cidx_59: Cidx 59
        :type cidx_59: ``int | HexList``
        :param cidx_58: Cidx 58
        :type cidx_58: ``int | HexList``
        :param cidx_57: Cidx 57
        :type cidx_57: ``int | HexList``
        :param cidx_56: Cidx 56
        :type cidx_56: ``int | HexList``
        :param cidx_71: Cidx 71
        :type cidx_71: ``int | HexList``
        :param cidx_70: Cidx 70
        :type cidx_70: ``int | HexList``
        :param cidx_69: Cidx 69
        :type cidx_69: ``int | HexList``
        :param cidx_68: Cidx 68
        :type cidx_68: ``int | HexList``
        :param cidx_67: Cidx 67
        :type cidx_67: ``int | HexList``
        :param cidx_66: Cidx 66
        :type cidx_66: ``int | HexList``
        :param cidx_65: Cidx 65
        :type cidx_65: ``int | HexList``
        :param cidx_64: Cidx 64
        :type cidx_64: ``int | HexList``
        :param cidx_79: Cidx 79
        :type cidx_79: ``int | HexList``
        :param cidx_78: Cidx 78
        :type cidx_78: ``int | HexList``
        :param cidx_77: Cidx 77
        :type cidx_77: ``int | HexList``
        :param cidx_76: Cidx 76
        :type cidx_76: ``int | HexList``
        :param cidx_75: Cidx 75
        :type cidx_75: ``int | HexList``
        :param cidx_74: Cidx 74
        :type cidx_74: ``int | HexList``
        :param cidx_73: Cidx 73
        :type cidx_73: ``int | HexList``
        :param cidx_72: Cidx 72
        :type cidx_72: ``int | HexList``
        :param cidx_87: Cidx 87
        :type cidx_87: ``int | HexList``
        :param cidx_86: Cidx 86
        :type cidx_86: ``int | HexList``
        :param cidx_85: Cidx 85
        :type cidx_85: ``int | HexList``
        :param cidx_84: Cidx 84
        :type cidx_84: ``int | HexList``
        :param cidx_83: Cidx 83
        :type cidx_83: ``int | HexList``
        :param cidx_82: Cidx 82
        :type cidx_82: ``int | HexList``
        :param cidx_81: Cidx 81
        :type cidx_81: ``int | HexList``
        :param cidx_80: Cidx 80
        :type cidx_80: ``int | HexList``
        :param cidx_95: Cidx 95
        :type cidx_95: ``int | HexList``
        :param cidx_94: Cidx 94
        :type cidx_94: ``int | HexList``
        :param cidx_93: Cidx 93
        :type cidx_93: ``int | HexList``
        :param cidx_92: Cidx 92
        :type cidx_92: ``int | HexList``
        :param cidx_91: Cidx 91
        :type cidx_91: ``int | HexList``
        :param cidx_90: Cidx 90
        :type cidx_90: ``int | HexList``
        :param cidx_89: Cidx 89
        :type cidx_89: ``int | HexList``
        :param cidx_88: Cidx 88
        :type cidx_88: ``int | HexList``
        :param cidx_103: Cidx 103
        :type cidx_103: ``int | HexList``
        :param cidx_102: Cidx 102
        :type cidx_102: ``int | HexList``
        :param cidx_101: Cidx 101
        :type cidx_101: ``int | HexList``
        :param cidx_100: Cidx 100
        :type cidx_100: ``int | HexList``
        :param cidx_99: Cidx 99
        :type cidx_99: ``int | HexList``
        :param cidx_98: Cidx 98
        :type cidx_98: ``int | HexList``
        :param cidx_97: Cidx 97
        :type cidx_97: ``int | HexList``
        :param cidx_96: Cidx 96
        :type cidx_96: ``int | HexList``
        :param cidx_111: Cidx 111
        :type cidx_111: ``int | HexList``
        :param cidx_110: Cidx 110
        :type cidx_110: ``int | HexList``
        :param cidx_109: Cidx 109
        :type cidx_109: ``int | HexList``
        :param cidx_108: Cidx 108
        :type cidx_108: ``int | HexList``
        :param cidx_107: Cidx 107
        :type cidx_107: ``int | HexList``
        :param cidx_106: Cidx 106
        :type cidx_106: ``int | HexList``
        :param cidx_105: Cidx 105
        :type cidx_105: ``int | HexList``
        :param cidx_104: Cidx 104
        :type cidx_104: ``int | HexList``
        :param cidx_119: Cidx 119
        :type cidx_119: ``int | HexList``
        :param cidx_118: Cidx 118
        :type cidx_118: ``int | HexList``
        :param cidx_117: Cidx 117
        :type cidx_117: ``int | HexList``
        :param cidx_116: Cidx 116
        :type cidx_116: ``int | HexList``
        :param cidx_115: Cidx 115
        :type cidx_115: ``int | HexList``
        :param cidx_114: Cidx 114
        :type cidx_114: ``int | HexList``
        :param cidx_113: Cidx 113
        :type cidx_113: ``int | HexList``
        :param cidx_112: Cidx 112
        :type cidx_112: ``int | HexList``
        :param cidx_127: Cidx 127
        :type cidx_127: ``int | HexList``
        :param cidx_126: Cidx 126
        :type cidx_126: ``int | HexList``
        :param cidx_125: Cidx 125
        :type cidx_125: ``int | HexList``
        :param cidx_124: Cidx 124
        :type cidx_124: ``int | HexList``
        :param cidx_123: Cidx 123
        :type cidx_123: ``int | HexList``
        :param cidx_122: Cidx 122
        :type cidx_122: ``int | HexList``
        :param cidx_121: Cidx 121
        :type cidx_121: ``int | HexList``
        :param cidx_120: Cidx 120
        :type cidx_120: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetDisabledControlsResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.cidx_bitmap = self.CidxBitmap(cidx_7=cidx_7,
                                           cidx_6=cidx_6,
                                           cidx_5=cidx_5,
                                           cidx_4=cidx_4,
                                           cidx_3=cidx_3,
                                           cidx_2=cidx_2,
                                           cidx_1=cidx_1,
                                           cidx_0=cidx_0,
                                           cidx_15=cidx_15,
                                           cidx_14=cidx_14,
                                           cidx_13=cidx_13,
                                           cidx_12=cidx_12,
                                           cidx_11=cidx_11,
                                           cidx_10=cidx_10,
                                           cidx_9=cidx_9,
                                           cidx_8=cidx_8,
                                           cidx_23=cidx_23,
                                           cidx_22=cidx_22,
                                           cidx_21=cidx_21,
                                           cidx_20=cidx_20,
                                           cidx_19=cidx_19,
                                           cidx_18=cidx_18,
                                           cidx_17=cidx_17,
                                           cidx_16=cidx_16,
                                           cidx_31=cidx_31,
                                           cidx_30=cidx_30,
                                           cidx_29=cidx_29,
                                           cidx_28=cidx_28,
                                           cidx_27=cidx_27,
                                           cidx_26=cidx_26,
                                           cidx_25=cidx_25,
                                           cidx_24=cidx_24,
                                           cidx_39=cidx_39,
                                           cidx_38=cidx_38,
                                           cidx_37=cidx_37,
                                           cidx_36=cidx_36,
                                           cidx_35=cidx_35,
                                           cidx_34=cidx_34,
                                           cidx_33=cidx_33,
                                           cidx_32=cidx_32,
                                           cidx_47=cidx_47,
                                           cidx_46=cidx_46,
                                           cidx_45=cidx_45,
                                           cidx_44=cidx_44,
                                           cidx_43=cidx_43,
                                           cidx_42=cidx_42,
                                           cidx_41=cidx_41,
                                           cidx_40=cidx_40,
                                           cidx_55=cidx_55,
                                           cidx_54=cidx_54,
                                           cidx_53=cidx_53,
                                           cidx_52=cidx_52,
                                           cidx_51=cidx_51,
                                           cidx_50=cidx_50,
                                           cidx_49=cidx_49,
                                           cidx_48=cidx_48,
                                           cidx_63=cidx_63,
                                           cidx_62=cidx_62,
                                           cidx_61=cidx_61,
                                           cidx_60=cidx_60,
                                           cidx_59=cidx_59,
                                           cidx_58=cidx_58,
                                           cidx_57=cidx_57,
                                           cidx_56=cidx_56,
                                           cidx_71=cidx_71,
                                           cidx_70=cidx_70,
                                           cidx_69=cidx_69,
                                           cidx_68=cidx_68,
                                           cidx_67=cidx_67,
                                           cidx_66=cidx_66,
                                           cidx_65=cidx_65,
                                           cidx_64=cidx_64,
                                           cidx_79=cidx_79,
                                           cidx_78=cidx_78,
                                           cidx_77=cidx_77,
                                           cidx_76=cidx_76,
                                           cidx_75=cidx_75,
                                           cidx_74=cidx_74,
                                           cidx_73=cidx_73,
                                           cidx_72=cidx_72,
                                           cidx_87=cidx_87,
                                           cidx_86=cidx_86,
                                           cidx_85=cidx_85,
                                           cidx_84=cidx_84,
                                           cidx_83=cidx_83,
                                           cidx_82=cidx_82,
                                           cidx_81=cidx_81,
                                           cidx_80=cidx_80,
                                           cidx_95=cidx_95,
                                           cidx_94=cidx_94,
                                           cidx_93=cidx_93,
                                           cidx_92=cidx_92,
                                           cidx_91=cidx_91,
                                           cidx_90=cidx_90,
                                           cidx_89=cidx_89,
                                           cidx_88=cidx_88,
                                           cidx_103=cidx_103,
                                           cidx_102=cidx_102,
                                           cidx_101=cidx_101,
                                           cidx_100=cidx_100,
                                           cidx_99=cidx_99,
                                           cidx_98=cidx_98,
                                           cidx_97=cidx_97,
                                           cidx_96=cidx_96,
                                           cidx_111=cidx_111,
                                           cidx_110=cidx_110,
                                           cidx_109=cidx_109,
                                           cidx_108=cidx_108,
                                           cidx_107=cidx_107,
                                           cidx_106=cidx_106,
                                           cidx_105=cidx_105,
                                           cidx_104=cidx_104,
                                           cidx_119=cidx_119,
                                           cidx_118=cidx_118,
                                           cidx_117=cidx_117,
                                           cidx_116=cidx_116,
                                           cidx_115=cidx_115,
                                           cidx_114=cidx_114,
                                           cidx_113=cidx_113,
                                           cidx_112=cidx_112,
                                           cidx_127=cidx_127,
                                           cidx_126=cidx_126,
                                           cidx_125=cidx_125,
                                           cidx_124=cidx_124,
                                           cidx_123=cidx_123,
                                           cidx_122=cidx_122,
                                           cidx_121=cidx_121,
                                           cidx_120=cidx_120)
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``SetDisabledControls``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.cidx_bitmap = cls.CidxBitmap.fromHexList(
            inner_field_container_mixin.cidx_bitmap)
        return inner_field_container_mixin
    # end def fromHexList
# end class SetDisabledControls


class SetDisabledControlsResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetDisabledControlsResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetDisabledControls,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetDisabledControlsResponse


class GetGameMode(ShortEmptyPacketDataFormat):
    """
    Define ``GetGameMode`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetGameModeResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetGameMode


class GetGameModeResponse(DisableControlsByCIDX):
    """
    Define ``GetGameModeResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Game Mode Full State          8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetGameMode,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 1

    class FID(DisableControlsByCIDX.FID):
        # See ``DisableControlsByCIDX.FID``
        GAME_MODE_FULL_STATE = DisableControlsByCIDX.FID.SOFTWARE_ID - 1
        PADDING = GAME_MODE_FULL_STATE - 1
    # end class FID

    class LEN(DisableControlsByCIDX.LEN):
        # See ``DisableControlsByCIDX.LEN``
        GAME_MODE_FULL_STATE = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = DisableControlsByCIDX.FIELDS + (
        BitField(fid=FID.GAME_MODE_FULL_STATE, length=LEN.GAME_MODE_FULL_STATE,
                 title="GameModeFullState", name="game_mode_full_state",
                 checks=(CheckHexList(LEN.GAME_MODE_FULL_STATE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DisableControlsByCIDX.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, lock_supported, supported, locked, enabled, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param lock_supported: Lock Supported
        :type lock_supported: ``int | HexList``
        :param supported: Supported
        :type supported: ``int | HexList``
        :param locked: Locked
        :type locked: ``int | HexList``
        :param enabled: Enabled
        :type enabled: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.game_mode_full_state = self.GameModeFullState(lock_supported=lock_supported,
                                                           supported=supported,
                                                           locked=locked,
                                                           enabled=enabled)
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``GetGameModeResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.game_mode_full_state = cls.GameModeFullState.fromHexList(
            inner_field_container_mixin.game_mode_full_state)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetGameModeResponse


class GetSetPowerOnParams(DisableControlsByCIDX):
    """
    Define ``GetSetPowerOnParams`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Set Mask                      8
    Set Value                     8
    Padding                       8
    ============================  ==========
    """

    class FID(DisableControlsByCIDX.FID):
        # See ``DisableControlsByCIDX.FID``
        SET_MASK = DisableControlsByCIDX.FID.SOFTWARE_ID - 1
        SET_VALUE = SET_MASK - 1
        PADDING = SET_VALUE - 1
    # end class FID

    class LEN(DisableControlsByCIDX.LEN):
        # See ``DisableControlsByCIDX.LEN``
        SET_MASK = 0x8
        SET_VALUE = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = DisableControlsByCIDX.FIELDS + (
        BitField(fid=FID.SET_MASK, length=LEN.SET_MASK,
                 title="SetMask", name="set_mask",
                 checks=(CheckHexList(LEN.SET_MASK // 8), CheckByte(),)),
        BitField(fid=FID.SET_VALUE, length=LEN.SET_VALUE,
                 title="SetValue", name="set_value",
                 checks=(CheckHexList(LEN.SET_VALUE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DisableControlsByCIDX.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, poweron_game_mode_lock_valid, poweron_game_mode_valid,
                 poweron_game_mode_lock, poweron_game_mode, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param poweron_game_mode_lock_valid: poweron game mode lock valid
        :type poweron_game_mode_lock_valid: ``int | HexList``
        :param poweron_game_mode_valid: poweron game mode valid
        :type poweron_game_mode_valid: ``int | HexList``
        :param poweron_game_mode_lock: poweron game mode lock
        :type poweron_game_mode_lock: ``int | HexList``
        :param poweron_game_mode: poweron game mode
        :type poweron_game_mode: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetSetPowerOnParamsResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.set_mask = self.SetMask(reserved=0,
                                     poweron_game_mode_lock=poweron_game_mode_lock_valid,
                                     poweron_game_mode=poweron_game_mode_valid)
        self.set_value = self.SetValue(reserved=0,
                                       poweron_game_mode_lock=poweron_game_mode_lock,
                                       poweron_game_mode=poweron_game_mode)
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
        inner_field_container_mixin.set_mask = cls.SetMask.fromHexList(
            inner_field_container_mixin.set_mask)
        inner_field_container_mixin.set_value = cls.SetValue.fromHexList(
            inner_field_container_mixin.set_value)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetSetPowerOnParams


class GetSetPowerOnParamsResponse(DisableControlsByCIDX):
    """
    Define ``GetSetPowerOnParamsResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Get Value                     8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetSetPowerOnParams,)
    VERSION = (1,)
    FUNCTION_INDEX = 2

    class FID(DisableControlsByCIDX.FID):
        # See ``DisableControlsByCIDX.FID``
        GET_VALUE = DisableControlsByCIDX.FID.SOFTWARE_ID - 1
        PADDING = GET_VALUE - 1
    # end class FID

    class LEN(DisableControlsByCIDX.LEN):
        # See ``DisableControlsByCIDX.LEN``
        GET_VALUE = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = DisableControlsByCIDX.FIELDS + (
        BitField(fid=FID.GET_VALUE, length=LEN.GET_VALUE,
                 title="GetValue", name="get_value",
                 checks=(CheckHexList(LEN.GET_VALUE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DisableControlsByCIDX.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, poweron_game_mode_lock, poweron_game_mode, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param poweron_game_mode_lock: poweron game mode lock
        :type poweron_game_mode_lock: ``int | HexList``
        :param poweron_game_mode: poweron game mode
        :type poweron_game_mode: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.get_value = self.GetValue(poweron_game_mode_lock=poweron_game_mode_lock,
                                       poweron_game_mode=poweron_game_mode)
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
        inner_field_container_mixin.get_value = cls.GetValue.fromHexList(
            inner_field_container_mixin.get_value)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetSetPowerOnParamsResponse


class GetCapabilities(ShortEmptyPacketDataFormat):
    """
    Define ``GetCapabilities`` implementation class
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
                         function_index=GetCapabilitiesResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetCapabilities


class GetCapabilitiesResponse(DisableControlsByCIDX):
    """
    Define ``GetCapabilitiesResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Supported Power On Params     8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilities,)
    VERSION = (1,)
    FUNCTION_INDEX = 3

    class FID(DisableControlsByCIDX.FID):
        # See ``DisableControlsByCIDX.FID``
        SUPPORTED_POWER_ON_PARAMS = DisableControlsByCIDX.FID.SOFTWARE_ID - 1
        PADDING = SUPPORTED_POWER_ON_PARAMS - 1
    # end class FID

    class LEN(DisableControlsByCIDX.LEN):
        # See ``DisableControlsByCIDX.LEN``
        SUPPORTED_POWER_ON_PARAMS = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = DisableControlsByCIDX.FIELDS + (
        BitField(fid=FID.SUPPORTED_POWER_ON_PARAMS, length=LEN.SUPPORTED_POWER_ON_PARAMS,
                 title="SupportedPowerOnParams", name="supported_power_on_params",
                 checks=(CheckHexList(LEN.SUPPORTED_POWER_ON_PARAMS // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DisableControlsByCIDX.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, poweron_game_mode_lock, poweron_game_mode, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param poweron_game_mode_lock: poweron game mode lock
        :type poweron_game_mode_lock: ``int | HexList``
        :param poweron_game_mode: poweron game mode
        :type poweron_game_mode: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.supported_power_on_params = self.SupportedPowerOnParams(poweron_game_mode_lock=poweron_game_mode_lock,
                                                                     poweron_game_mode=poweron_game_mode)
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
        :rtype: ``GetCapabilitiesResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.supported_power_on_params = cls.SupportedPowerOnParams.fromHexList(
            inner_field_container_mixin.supported_power_on_params)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetCapabilitiesResponse


class GameModeEvent(DisableControlsByCIDX):
    """
    Define ``GameModeEvent`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Game Mode State               8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1,)
    FUNCTION_INDEX = 0

    class FID(DisableControlsByCIDX.FID):
        # See ``DisableControlsByCIDX.FID``
        GAME_MODE_STATE = DisableControlsByCIDX.FID.SOFTWARE_ID - 1
        PADDING = GAME_MODE_STATE - 1
    # end class FID

    class LEN(DisableControlsByCIDX.LEN):
        # See ``DisableControlsByCIDX.LEN``
        GAME_MODE_STATE = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = DisableControlsByCIDX.FIELDS + (
        BitField(fid=FID.GAME_MODE_STATE, length=LEN.GAME_MODE_STATE,
                 title="GameModeState", name="game_mode_state",
                 checks=(CheckHexList(LEN.GAME_MODE_STATE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DisableControlsByCIDX.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, locked, enabled, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param locked: Locked
        :type locked: ``int | HexList``
        :param enabled: Enabled
        :type enabled: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.game_mode_state = self.GameModeState(locked=locked,
                                                  enabled=enabled)
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``GameModeEvent``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.game_mode_state = cls.GameModeState.fromHexList(
            inner_field_container_mixin.game_mode_state)
        return inner_field_container_mixin
    # end def fromHexList
# end class GameModeEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
