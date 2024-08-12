#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pylibrary.mcu.profileformat
:brief: Profile format data classes
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/11/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import time
import warnings
from enum import IntEnum
from enum import unique

from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hid.usbhidusagetable import ConsumerHidUsage
from pyhid.hid.usbhidusagetable import STANDARD_KEYS
from pyhid.hiddata import HidData
from pyhid.hiddata import OS
from pyhid.hidpp.hidppmessage import HidppMessage
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ProfileDirectory:
    """
    Profile Directory data class
    """

    END_OF_PROFILE = 0xFFFF

    class Item(BitFieldContainerMixin):
        """
        Directory Item class definition
        """

        class FID:
            """
            Field Identifiers
            """
            SECTOR_ID = 0xFF
            ENABLED = SECTOR_ID - 1
            RESERVED = ENABLED - 1
        # end class FID

        class LEN:
            """
            Field Lengths in bits
            """
            SECTOR_ID = 0x10
            ENABLED = 0x08
            RESERVED = 0x08
        # end class LEN

        FIELDS = (
            BitField(
                fid=FID.SECTOR_ID,
                length=LEN.SECTOR_ID,
                title='SectorId',
                name='sector_id',
                checks=(CheckHexList(LEN.SECTOR_ID // 8), CheckInt(),), ),
            BitField(
                fid=FID.ENABLED,
                length=LEN.ENABLED,
                title='Enabled',
                name='enabled',
                checks=(CheckHexList(LEN.ENABLED // 8), CheckByte(),), ),
            BitField(
                fid=FID.RESERVED,
                length=LEN.RESERVED,
                title='Reserved',
                name='reserved',
                checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                default_value=HidppMessage.DEFAULT.RESERVED),
        )
    # end class Item
# end class ProfileDirectory


class ProfileFieldName:
    """
    Define common fields name be used in profile
    """
    BUTTON = 'button_fields'
    G_SHIFT_BUTTON = 'g_shift_button_fields'
# end def class ProfileFieldName


class ProfileCommonHeader(BitFieldContainerMixin):
    """
    This class provides the common part of ``ProfileCommonFormatV1ToV3`` and ``ProfileCommonFormatV4ToV5``
    18 first bytes of Profile Format defined here:
    https://sites.google.com/a/logitech.com/hyjal/product-design-phase/design-analysis/fw-pfe/fw-----sw-interface/profiles-profiles-directory-format
    """

    class FID:
        """
        Field Identifiers
        """
        REPORT_RATE = 0xFF
        DEFAULT_DPI_INDEX = REPORT_RATE - 1
        SHIFT_DPI_INDEX = DEFAULT_DPI_INDEX - 1
        DPI_0_TO_4 = SHIFT_DPI_INDEX - 1
        LED_COLOR_RED = DPI_0_TO_4 - 1
        LED_COLOR_GREEN = LED_COLOR_RED - 1
        LED_COLOR_BLUE = LED_COLOR_GREEN - 1
        POWER_MODE = LED_COLOR_BLUE - 1
        ANGLE_SNAPPING = POWER_MODE - 1
    # end class FID

    class LEN:
        """
        Field Lengths in bits
        """
        REPORT_RATE = 0x08
        DEFAULT_DPI_INDEX = 0x08
        SHIFT_DPI_INDEX = 0x08
        DPI_0_TO_4 = 0x50
        LED_COLOR_RED = 0x08
        LED_COLOR_GREEN = 0x08
        LED_COLOR_BLUE = 0x08
        POWER_MODE = 0x08
        ANGLE_SNAPPING = 0x08
    # end class LEN

    FIELDS = (
        BitField(
            fid=FID.REPORT_RATE,
            length=LEN.REPORT_RATE,
            title='ReportRate',
            name='report_rate',
            checks=(CheckHexList(LEN.REPORT_RATE // 8), CheckByte(),),),
        BitField(
            fid=FID.DEFAULT_DPI_INDEX,
            length=LEN.DEFAULT_DPI_INDEX,
            title='DefaultDpiIndex',
            name='default_dpi_index',
            checks=(CheckHexList(LEN.DEFAULT_DPI_INDEX // 8), CheckByte(),),),
        BitField(
            fid=FID.SHIFT_DPI_INDEX,
            length=LEN.SHIFT_DPI_INDEX,
            title='ShiftDpiIndex',
            name='shift_dpi_index',
            checks=(CheckHexList(LEN.SHIFT_DPI_INDEX // 8), CheckByte(),),),
        BitField(
            fid=FID.DPI_0_TO_4,
            length=LEN.DPI_0_TO_4,
            title='Dpi_0_To_4',
            name='dpi_0_to_4',
            checks=(CheckHexList(LEN.DPI_0_TO_4 // 8), CheckByte(),),),
        BitField(
            fid=FID.LED_COLOR_RED,
            length=LEN.LED_COLOR_RED,
            title='LedColorRed',
            name='led_color_red',
            checks=(CheckHexList(LEN.LED_COLOR_RED // 8), CheckByte(),),),
        BitField(
            fid=FID.LED_COLOR_GREEN,
            length=LEN.LED_COLOR_GREEN,
            title='LedColorGreen',
            name='led_color_green',
            checks=(CheckHexList(LEN.LED_COLOR_GREEN // 8), CheckByte(),),),
        BitField(
            fid=FID.LED_COLOR_BLUE,
            length=LEN.LED_COLOR_BLUE,
            title='LedColorBlue',
            name='led_color_blue',
            checks=(CheckHexList(LEN.LED_COLOR_BLUE // 8), CheckByte(),), ),
        BitField(
            fid=FID.POWER_MODE,
            length=LEN.POWER_MODE,
            title='PowerMode',
            name='power_mode',
            checks=(CheckHexList(LEN.POWER_MODE // 8), CheckByte(),),),
        BitField(
            fid=FID.ANGLE_SNAPPING,
            length=LEN.ANGLE_SNAPPING,
            title='AngleSnapping',
            name='angle_snapping',
            checks=(CheckHexList(LEN.ANGLE_SNAPPING // 8), CheckByte(),),),
    )

    def __init__(self, report_rate, resolution_index, shift_resolution_index, dpi_0_to_4, led_color_red,
                 led_color_green, led_color_blue, power_mode, angle_snapping, **kwargs):
        """
        :param report_rate: Report rate
        :type report_rate: ``int`` ot ``HexList``
        :param resolution_index: Resolution index
        :type resolution_index: ``int`` ot ``HexList``
        :param shift_resolution_index: Shift resolution index
        :type shift_resolution_index: ``int`` ot ``HexList``
        :param dpi_0_to_4: Resolution 0 to 4
        :type dpi_0_to_4: ``int`` ot ``HexList``
        :param led_color_red: Led color red
        :type led_color_red: ``int`` ot ``HexList``
        :param led_color_green: Led color green
        :type led_color_green: ``int`` ot ``HexList``
        :param led_color_green: Led color green
        :type led_color_green: ``int`` ot ``HexList``
        :param led_color_blue: Led color blue
        :type led_color_blue: ``int`` ot ``HexList``
        :param power_mode: Power_mode
        :type power_mode: ``int`` ot ``HexList``
        :param angle_snapping: Angle_ napping
        :type angle_snapping: ``int`` ot ``HexList``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(**kwargs)

        # Parameters initialization
        self.report_rate = report_rate
        self.resolution_index = resolution_index
        self.shift_resolution_index = shift_resolution_index
        self.dpi_0_to_4 = dpi_0_to_4
        self.led_color_red = led_color_red
        self.led_color_green = led_color_green
        self.led_color_blue = led_color_blue
        self.power_mode = power_mode
        self.angle_snapping = angle_snapping
    # end def __init__
# end class ProfileCommonHeader


class ProfileCommonFormatV1ToV3(ProfileCommonHeader):
    """
    This class provides the common part of ``ProfileFormatV1`` and ``ProfileFormatV2ToV3``
    """

    class FID(ProfileCommonHeader.FID):
        # See ``ProfileCommonHeader.FID``
        RESERVED_14 = ProfileCommonHeader.FID.ANGLE_SNAPPING - 1
        BTN_0_TO_15 = RESERVED_14 - 1
        G_SHIFT_BTN_0_TO_15 = BTN_0_TO_15 - 1
        PROFILE_NAME_0_TO_23 = G_SHIFT_BTN_0_TO_15 - 1
    # end class FID

    class LEN(ProfileCommonHeader.LEN):
        # See ``ProfileCommonHeader.LEN``
        RESERVED_14 = 0x70
        BTN_0_TO_15 = 0x200
        G_SHIFT_BTN_0_TO_15 = 0x200
        PROFILE_NAME_0_TO_23 = 0x180
    # end class LEN

    FIELDS = ProfileCommonHeader.FIELDS + (
        BitField(
            fid=FID.RESERVED_14,
            length=LEN.RESERVED_14,
            title='Reserved_14',
            name='reserved_14',
            checks=(CheckHexList(LEN.RESERVED_14 // 8), CheckByte(),),),
        BitField(
            fid=FID.BTN_0_TO_15,
            length=LEN.BTN_0_TO_15,
            title='Btn_0_To_15',
            name='btn_0_to_15',
            aliases=('button_fields',),
            checks=(CheckHexList(LEN.BTN_0_TO_15 // 8), CheckByte(),),),
        BitField(
            fid=FID.G_SHIFT_BTN_0_TO_15,
            length=LEN.G_SHIFT_BTN_0_TO_15,
            title='GShiftBtn_0_To_15',
            name='g_shift_btn_0_to_15',
            aliases=('g_shift_button_fields',),
            checks=(CheckHexList(LEN.G_SHIFT_BTN_0_TO_15 // 8), CheckByte(),),),
        BitField(
            fid=FID.PROFILE_NAME_0_TO_23,
            length=LEN.PROFILE_NAME_0_TO_23,
            title='ProfileName_0_To_23',
            name='profile_name_0_to_23',
            checks=(CheckHexList(LEN.PROFILE_NAME_0_TO_23 // 8), CheckByte(),),),
    )
# end class ProfileCommonFormatV1ToV3


class ProfileCommonFormatV4ToV5(ProfileCommonHeader):
    """
    This class provides the common part of ``ProfileFormatV4`` and ``ProfileFormatV5``
    """

    class FID(ProfileCommonHeader.FID):
        # See ``ProfileCommonHeader.FID``
        WRITE_COUNTER = ProfileCommonHeader.FID.ANGLE_SNAPPING - 1
        RESERVED_8 = WRITE_COUNTER - 1
        POWER_SAVE_TIMEOUT = RESERVED_8 - 1
        POWER_OFF_TIMEOUT = POWER_SAVE_TIMEOUT - 1
        BTN_0_TO_15 = POWER_OFF_TIMEOUT - 1
        G_SHIFT_BTN_0_TO_15 = BTN_0_TO_15 - 1
        PROFILE_NAME_0_TO_23 = G_SHIFT_BTN_0_TO_15 - 1
    # end class FID

    class LEN(ProfileCommonHeader.LEN):
        # See ``ProfileCommonHeader.LEN``
        WRITE_COUNTER = 0x10
        RESERVED_8 = 0x40
        POWER_SAVE_TIMEOUT = 0x10
        POWER_OFF_TIMEOUT = 0x10
        BTN_0_TO_15 = 0x200
        G_SHIFT_BTN_0_TO_15 = 0x200
        PROFILE_NAME_0_TO_23 = 0x180
    # end class LEN

    FIELDS = ProfileCommonHeader.FIELDS + (
        BitField(
            fid=FID.WRITE_COUNTER,
            length=LEN.WRITE_COUNTER,
            title='WriteCounter',
            name='write_counter',
            checks=(CheckHexList(LEN.WRITE_COUNTER // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.WRITE_COUNTER) - 1),),),
        BitField(
            fid=FID.RESERVED_8,
            length=LEN.RESERVED_8,
            title='Reserved_8',
            name='reserved_8',
            checks=(CheckHexList(LEN.RESERVED_8 // 8), CheckByte(),), ),
        BitField(
            fid=FID.POWER_SAVE_TIMEOUT,
            length=LEN.POWER_SAVE_TIMEOUT,
            title='PwrSaveTimeout',
            name='pwr_save_timeout',
            checks=(CheckHexList(LEN.POWER_SAVE_TIMEOUT // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.POWER_SAVE_TIMEOUT) - 1),), ),
        BitField(
            fid=FID.POWER_OFF_TIMEOUT,
            length=LEN.POWER_OFF_TIMEOUT,
            title='PwrOffTimeout',
            name='pwr_off_timeout',
            checks=(CheckHexList(LEN.POWER_OFF_TIMEOUT // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.POWER_OFF_TIMEOUT) - 1),), ),
        BitField(
            fid=FID.BTN_0_TO_15,
            length=LEN.BTN_0_TO_15,
            title='Btn_0_To_15',
            name='btn_0_to_15',
            aliases=('button_fields',),
            checks=(CheckHexList(LEN.BTN_0_TO_15 // 8), CheckByte(),),),
        BitField(
            fid=FID.G_SHIFT_BTN_0_TO_15,
            length=LEN.G_SHIFT_BTN_0_TO_15,
            title='GShiftBtn_0_To_15',
            name='g_shift_btn_0_to_15',
            aliases=('g_shift_button_fields',),
            checks=(CheckHexList(LEN.G_SHIFT_BTN_0_TO_15 // 8), CheckByte(),),),
        BitField(
            fid=FID.PROFILE_NAME_0_TO_23,
            length=LEN.PROFILE_NAME_0_TO_23,
            title='ProfileName_0_To_23',
            name='profile_name_0_to_23',
            checks=(CheckHexList(LEN.PROFILE_NAME_0_TO_23 // 8), CheckByte(),),),
    )

    def __init__(self, report_rate, resolution_index, shift_resolution_index, res_0, res_1, res_2, res_3, res_4,
                 led_color_red, led_color_green, led_color_blue, power_mode, angle_snapping, write_counter,
                 pwr_save_timeout, pwr_off_timeout, btn_0_to_15, g_shift_btn_0_to_15, profile_name_0_to_23, **kwargs):
        """
        :param report_rate: Report rate
        :type report_rate: ``int`` ot ``HexList``
        :param resolution_index: Resolution index
        :type resolution_index: ``int`` ot ``HexList``
        :param shift_resolution_index: Shift resolution index
        :type shift_resolution_index: ``int`` ot ``HexList``
        :param res_0: Resolution 0
        :type res_0: ``int`` ot ``HexList``
        :param res_1: Resolution 1
        :type res_1: ``int`` ot ``HexList``
        :param res_2: Resolution 2
        :type res_2: ``int`` ot ``HexList``
        :param res_3: Resolution 3
        :type res_3: ``int`` ot ``HexList``
        :param res_4: Resolution 4
        :type res_4: ``int`` ot ``HexList``
        :param led_color_red: Led color red
        :type led_color_red: ``int`` ot ``HexList``
        :param led_color_green: Led color green
        :type led_color_green: ``int`` ot ``HexList``
        :param led_color_green: Led color green
        :type led_color_green: ``int`` ot ``HexList``
        :param led_color_blue: Led color blue
        :type led_color_blue: ``int`` ot ``HexList``
        :param power_mode: Power_mode
        :type power_mode: ``int`` ot ``HexList``
        :param angle_snapping: Angle snapping
        :type angle_snapping: ``int`` ot ``HexList``
        :param write_counter: Write counter
        :type write_counter: ``int`` ot ``HexList``
        :param pwr_save_timeout: Power save timeout
        :type pwr_save_timeout: ``int`` ot ``HexList``
        :param pwr_off_timeout: Power off timeout
        :type pwr_off_timeout: ``int`` ot ``HexList``
        :param btn_0_to_15: Button 0 to 15
        :type btn_0_to_15: ``int`` ot ``HexList``
        :param g_shift_btn_0_to_15: G-Shift Button 0 to 15
        :type g_shift_btn_0_to_15: ``int`` ot ``HexList``
        :param profile_name_0_to_23: Profile name 0 to 23
        :type profile_name_0_to_23: ``int`` ot ``HexList``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(report_rate, resolution_index, shift_resolution_index,
                         HexList(Numeral(res_0, byteCount=2)) + HexList(Numeral(res_1, byteCount=2)) +
                         HexList(Numeral(res_2, byteCount=2)) + HexList(Numeral(res_3, byteCount=2)) +
                         HexList(Numeral(res_4, byteCount=2)), led_color_red, led_color_green, led_color_blue,
                         power_mode, angle_snapping, **kwargs)

        # Parameters initialization
        self.write_counter = write_counter
        self.pwr_save_timeout = pwr_save_timeout
        self.pwr_off_timeout = pwr_off_timeout
        self.btn_0_to_15 = btn_0_to_15
        self.g_shift_btn_0_to_15 = g_shift_btn_0_to_15
        self.profile_name_0_to_23 = profile_name_0_to_23
    # end def __init__

    @property
    def power_save_timeout(self):
        """
        Convert to big endian
        """
        return self.pwr_save_timeout[::-1]
    # end getter def power_save_timeout

    @power_save_timeout.setter
    def power_save_timeout(self, value):
        """
        Convert value to little endian
        """
        self.pwr_save_timeout = HexList(Numeral(value[::-1]))
    # end setter def power_save_timeout

    @property
    def power_off_timeout(self):
        """
        Convert to big endian
        """
        return self.pwr_off_timeout[::-1]
    # end getter def power_off_timeout

    @power_off_timeout.setter
    def power_off_timeout(self, value):
        """
        Convert value to little endian
        """
        self.pwr_off_timeout = HexList(Numeral(value[::-1]))
    # end setter def power_off_timeout
# end class ProfileCommonFormatV4ToV5


class ProfileFormatV1(ProfileCommonFormatV1ToV3):
    """
    Profile Format V1
    https://sites.google.com/a/logitech.com/hyjal/product-design-phase/design-analysis/fw-pfe/fw-----sw-interface/profiles-profiles-directory-format
    """
    ID = 1

    class FID(ProfileCommonFormatV1ToV3.FID):
        # See ``ProfileCommonFormatV1ToV3.FID``
        RESERVED_45 = ProfileCommonFormatV1ToV3.FID.PROFILE_NAME_0_TO_23 - 1
        CRC = RESERVED_45 - 1
    # end class FID

    class LEN(ProfileCommonFormatV1ToV3.LEN):
        # See ``ProfileCommonFormatV1ToV3.LEN``
        RESERVED_45 = 0x168
        CRC = 0x10
    # end class LEN

    FIELDS = ProfileCommonFormatV1ToV3.FIELDS + (
        BitField(
            fid=FID.RESERVED_45,
            length=LEN.RESERVED_45,
            title='Reserved_45',
            name='reserved_45',
            checks=(CheckHexList(LEN.RESERVED_45 // 8), CheckByte(),),),
        BitField(
            fid=FID.CRC,
            length=LEN.CRC,
            title='Crc',
            name='crc',
            checks=(CheckHexList(LEN.CRC // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.CRC) - 1),)),
    )
# end class ProfileFormatV1


class ProfileFormatV2ToV3(ProfileCommonFormatV1ToV3):
    """
    This class provides the common part of ``ProfileFormatV2`` and ``ProfileFormatV3``
    """

    class FID(ProfileCommonFormatV1ToV3.FID):
        # See ``ProfileCommonFormatV1ToV3.FID``
        LOGO_EFFECT = ProfileCommonFormatV1ToV3.FID.PROFILE_NAME_0_TO_23 - 1
        SIDE_EFFECT = LOGO_EFFECT - 1
        RESERVED_23 = SIDE_EFFECT - 1
        CRC = RESERVED_23 - 1
    # end class FID

    class LEN(ProfileCommonFormatV1ToV3.LEN):
        # See ``ProfileCommonFormatV1ToV3.LEN``
        LOGO_EFFECT = 0x58
        SIDE_EFFECT = 0x58
        RESERVED_23 = 0xB8
        CRC = 0x10
    # end class LEN

    FIELDS = ProfileCommonFormatV1ToV3.FIELDS + (
        BitField(
            fid=FID.LOGO_EFFECT,
            length=LEN.LOGO_EFFECT,
            title='LogoEffect',
            name='logo_effect',
            checks=(CheckHexList(LEN.LOGO_EFFECT // 8), CheckByte(),),),
        BitField(
            fid=FID.SIDE_EFFECT,
            length=LEN.SIDE_EFFECT,
            title='SideEffect',
            name='side_effect',
            checks=(CheckHexList(LEN.SIDE_EFFECT // 8), CheckByte(),),),
        BitField(
            fid=FID.RESERVED_23,
            length=LEN.RESERVED_23,
            title='Reserved_23',
            name='reserved_23',
            checks=(CheckHexList(LEN.RESERVED_23 // 8), CheckByte(),),),
        BitField(
            fid=FID.CRC,
            length=LEN.CRC,
            title='Crc',
            name='crc',
            checks=(CheckHexList(LEN.CRC // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.CRC) - 1),)),
    )
# end class ProfileFormatV2ToV3


class ProfileFormatV2(ProfileFormatV2ToV3):
    """
    Profile Format
    V2
    https://sites.google.com/a/logitech.com/logan/product-design-phase/6---fw---sw-design/fws-specifications/profile-mapping-extension
    """
    ID = 2
# end class ProfileFormatV2


class ProfileFormatV3(ProfileFormatV2ToV3):
    """
    Profile Format
    V3
    https://docs.google.com/document/d/1zOprRFR6lj-NyVbOWwdgagEIsnE3dSMT58tr9pNSSIU/edit?usp=sharing
    """
    ID = 3
# end class ProfileFormatV3


class ProfileFormatV4(ProfileCommonFormatV4ToV5):
    """
    Profile Format V4
    https://docs.google.com/document/d/1Xkh0JiA6CkMnYoA9g28qj7wJzs-k7eP3NFuZKDenAXE/edit?usp=sharing
    """
    ID = 4

    class FID(ProfileCommonFormatV4ToV5.FID):
        # See ``ProfileCommonFormatV4ToV5.FID``
        LOGO_ACTIVE_EFFECT = ProfileCommonFormatV4ToV5.FID.PROFILE_NAME_0_TO_23 - 1
        SIDE_ACTIVE_EFFECT = LOGO_ACTIVE_EFFECT - 1
        LOGO_PASSIVE_EFFECT = SIDE_ACTIVE_EFFECT - 1
        SIDE_PASSIVE_EFFECT = LOGO_PASSIVE_EFFECT - 1
        RESERVED_1 = SIDE_PASSIVE_EFFECT - 1
        CRC = RESERVED_1 - 1
    # end class FID

    class LEN(ProfileCommonFormatV4ToV5.LEN):
        # See ``ProfileCommonFormatV4ToV5.LEN``
        LOGO_ACTIVE_EFFECT = 0x58
        SIDE_ACTIVE_EFFECT = 0x58
        LOGO_PASSIVE_EFFECT = 0x58
        SIDE_PASSIVE_EFFECT = 0x58
        RESERVED_1 = 0x08
        CRC = 0x10
    # end class LEN

    FIELDS = ProfileCommonFormatV4ToV5.FIELDS + (
        BitField(
            fid=FID.LOGO_ACTIVE_EFFECT,
            length=LEN.LOGO_ACTIVE_EFFECT,
            title='LogoActiveEffect',
            name='logo_active_effect',
            checks=(CheckHexList(LEN.LOGO_ACTIVE_EFFECT // 8), CheckByte(),),),
        BitField(
            fid=FID.SIDE_ACTIVE_EFFECT,
            length=LEN.SIDE_ACTIVE_EFFECT,
            title='SideActiveEffect',
            name='side_active_effect',
            checks=(CheckHexList(LEN.SIDE_ACTIVE_EFFECT // 8), CheckByte(),),),
        BitField(
            fid=FID.LOGO_PASSIVE_EFFECT,
            length=LEN.LOGO_PASSIVE_EFFECT,
            title='LogoPassiveEffect',
            name='logo_passive_effect',
            checks=(CheckHexList(LEN.LOGO_PASSIVE_EFFECT // 8), CheckByte(),),),
        BitField(
            fid=FID.SIDE_PASSIVE_EFFECT,
            length=LEN.SIDE_PASSIVE_EFFECT,
            title='SidePassiveEffect',
            name='side_passive_effect',
            checks=(CheckHexList(LEN.SIDE_PASSIVE_EFFECT // 8), CheckByte(),),),
        BitField(
            fid=FID.RESERVED_1,
            length=LEN.RESERVED_1,
            title='Reserved_1',
            name='reserved_1',
            checks=(CheckHexList(LEN.RESERVED_1 // 8), CheckByte(),),),
        BitField(
            fid=FID.CRC,
            length=LEN.CRC,
            title='Crc',
            name='crc',
            checks=(CheckHexList(LEN.CRC // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.CRC) - 1),)),
    )
# end class ProfileFormatV4


class ProfileFormatV5(ProfileCommonFormatV4ToV5):
    """
    Profile Format V5
    https://docs.google.com/document/d/1A5SdvwAL9QSSGj9IxKa2n_en3-27flrdt2cY0OQsLgs/edit?usp=sharing
    """
    ID = 5

    class FID(ProfileCommonFormatV4ToV5.FID):
        # See ``ProfileCommonFormatV4ToV5.FID``
        CLUSTER_0_ACTIVE_EFFECT = ProfileCommonFormatV4ToV5.FID.PROFILE_NAME_0_TO_23 - 1
        CLUSTER_1_ACTIVE_EFFECT = CLUSTER_0_ACTIVE_EFFECT - 1
        CLUSTER_0_PASSIVE_EFFECT = CLUSTER_1_ACTIVE_EFFECT - 1
        CLUSTER_1_PASSIVE_EFFECT = CLUSTER_0_PASSIVE_EFFECT - 1
        LIGHTNING_FLAG = CLUSTER_1_PASSIVE_EFFECT - 1
        CRC = LIGHTNING_FLAG - 1
    # end class FID

    class LEN(ProfileCommonFormatV4ToV5.LEN):
        # See ``ProfileCommonFormatV4ToV5.LEN``
        CLUSTER_0_ACTIVE_EFFECT = 0x58
        CLUSTER_1_ACTIVE_EFFECT = 0x58
        CLUSTER_0_PASSIVE_EFFECT = 0x58
        CLUSTER_1_PASSIVE_EFFECT = 0x58
        LIGHTNING_FLAG = 0x08
        CRC = 0x10
    # end class LEN

    FIELDS = ProfileCommonFormatV4ToV5.FIELDS + (
        BitField(
            fid=FID.CLUSTER_0_ACTIVE_EFFECT,
            length=LEN.CLUSTER_0_ACTIVE_EFFECT,
            title='Cluster_0_ActiveEffect',
            name='cluster_0_active_effect',
            checks=(CheckHexList(LEN.CLUSTER_0_ACTIVE_EFFECT // 8), CheckByte(),),),
        BitField(
            fid=FID.CLUSTER_1_ACTIVE_EFFECT,
            length=LEN.CLUSTER_1_ACTIVE_EFFECT,
            title='Cluster_1_ActiveEffect',
            name='cluster_1_active_effect',
            checks=(CheckHexList(LEN.CLUSTER_1_ACTIVE_EFFECT // 8), CheckByte(),),),
        BitField(
            fid=FID.CLUSTER_0_PASSIVE_EFFECT,
            length=LEN.CLUSTER_0_PASSIVE_EFFECT,
            title='Cluster_0_PassiveEffect',
            name='cluster_0_passive_effect',
            checks=(CheckHexList(LEN.CLUSTER_0_PASSIVE_EFFECT // 8), CheckByte(),),),
        BitField(
            fid=FID.CLUSTER_1_PASSIVE_EFFECT,
            length=LEN.CLUSTER_1_PASSIVE_EFFECT,
            title='Cluster_1_PassiveEffect',
            name='cluster_1_passive_effect',
            checks=(CheckHexList(LEN.CLUSTER_1_PASSIVE_EFFECT // 8), CheckByte(),),),
        BitField(
            fid=FID.LIGHTNING_FLAG,
            length=LEN.LIGHTNING_FLAG,
            title='LightningFlag',
            name='lightning_flag',
            checks=(CheckHexList(LEN.LIGHTNING_FLAG // 8), CheckByte(),), ),
        BitField(
            fid=FID.CRC,
            length=LEN.CRC,
            title='Crc',
            name='crc',
            checks=(CheckHexList(LEN.CRC // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.CRC) - 1),)),
    )
# end class ProfileFormatV5


class ProfileFormatV6(BitFieldContainerMixin):
    """
    Profile Format V6
    https://docs.google.com/spreadsheets/d/1LWfjsa7q5J77t9ENdWjwLZJhpY-83Wt8Uv6i5MtS7yg/edit?usp=sharing
    """
    ID = 6

    class FID:
        """
        Field Identifiers
        """
        REPORT_RATE_WIRELESS = 0xFF
        REPORT_RATE_WIRED = REPORT_RATE_WIRELESS - 1
        DEFAULT_DPI_INDEX = REPORT_RATE_WIRED - 1
        SHIFT_DPI_INDEX = DEFAULT_DPI_INDEX - 1
        DPI_XY_0_TO_4 = SHIFT_DPI_INDEX - 1
        DPI_DELTA_X = DPI_XY_0_TO_4 - 1
        DPI_DELTA_Y = DPI_DELTA_X - 1
        POWER_MODE = DPI_DELTA_Y - 1
        ANGLE_SNAPPING = POWER_MODE - 1
        WRITE_COUNTER = ANGLE_SNAPPING - 1
        RESERVED_7 = WRITE_COUNTER - 1
        POWER_SAVE_TIMEOUT = RESERVED_7 - 1
        POWER_OFF_TIMEOUT = POWER_SAVE_TIMEOUT - 1
        BTN_0_TO_11 = POWER_OFF_TIMEOUT - 1
        RESERVED_16 = BTN_0_TO_11 - 1
        G_SHIFT_BTN_0_TO_11 = RESERVED_16 - 1
        PROFILE_NAME_0_TO_23 = G_SHIFT_BTN_0_TO_11 - 1
        CLUSTER_0_ACTIVE_EFFECT = PROFILE_NAME_0_TO_23 - 1
        CLUSTER_1_ACTIVE_EFFECT = CLUSTER_0_ACTIVE_EFFECT - 1
        CLUSTER_0_PASSIVE_EFFECT = CLUSTER_1_ACTIVE_EFFECT - 1
        CLUSTER_1_PASSIVE_EFFECT = CLUSTER_0_PASSIVE_EFFECT - 1
        LIGHTNING_FLAG = CLUSTER_1_PASSIVE_EFFECT - 1
        CRC = LIGHTNING_FLAG - 1
    # end class FID

    class LEN:
        """
        Field Lengths in bits
        """
        REPORT_RATE_WIRELESS = 0x08
        REPORT_RATE_WIRED = 0x08
        DEFAULT_DPI_INDEX = 0x08
        SHIFT_DPI_INDEX = 0x08
        DPI_XY_0_TO_4 = 0xC8
        DPI_DELTA_X = 0x10
        DPI_DELTA_Y = 0x10
        POWER_MODE = 0x08
        ANGLE_SNAPPING = 0x08
        WRITE_COUNTER = 0x10
        RESERVED_7 = 0x38
        POWER_SAVE_TIMEOUT = 0x10
        POWER_OFF_TIMEOUT = 0x10
        BTN_0_TO_11 = 0x180
        RESERVED_16 = 0x80
        G_SHIFT_BTN_0_TO_11 = 0x180
        PROFILE_NAME_0_TO_23 = 0x180
        CLUSTER_0_ACTIVE_EFFECT = 0x58
        CLUSTER_1_ACTIVE_EFFECT = 0x58
        CLUSTER_0_PASSIVE_EFFECT = 0x58
        CLUSTER_1_PASSIVE_EFFECT = 0x58
        LIGHTNING_FLAG = 0x08
        CRC = 0x10
    # end class LEN

    FIELDS = (
        BitField(
            fid=FID.REPORT_RATE_WIRELESS,
            length=LEN.REPORT_RATE_WIRELESS,
            title='ReportRateWireless',
            name='report_rate_wireless',
            checks=(CheckHexList(LEN.REPORT_RATE_WIRELESS // 8), CheckByte(),), ),
        BitField(
            fid=FID.REPORT_RATE_WIRED,
            length=LEN.REPORT_RATE_WIRED,
            title='ReportRateWired',
            name='report_rate_wired',
            checks=(CheckHexList(LEN.REPORT_RATE_WIRED // 8), CheckByte(),), ),
        BitField(
            fid=FID.DEFAULT_DPI_INDEX,
            length=LEN.DEFAULT_DPI_INDEX,
            title='DefaultDpiIndex',
            name='default_dpi_index',
            checks=(CheckHexList(LEN.DEFAULT_DPI_INDEX // 8), CheckByte(),), ),
        BitField(
            fid=FID.SHIFT_DPI_INDEX,
            length=LEN.SHIFT_DPI_INDEX,
            title='ShiftDpiIndex',
            name='shift_dpi_index',
            checks=(CheckHexList(LEN.SHIFT_DPI_INDEX // 8), CheckByte(),), ),
        BitField(
            fid=FID.DPI_XY_0_TO_4,
            length=LEN.DPI_XY_0_TO_4,
            title='DpiXY_0_To_4',
            name='dpi_xy_0_to_4',
            checks=(CheckHexList(LEN.DPI_XY_0_TO_4 // 8), CheckByte(),),),
        BitField(
            fid=FID.DPI_DELTA_X,
            length=LEN.DPI_DELTA_X,
            title='DpiDeltaX',
            name='dpi_delta_x',
            checks=(CheckHexList(LEN.DPI_DELTA_X // 8), CheckByte(),), ),
        BitField(
            fid=FID.DPI_DELTA_Y,
            length=LEN.DPI_DELTA_Y,
            title='DpiDeltaY',
            name='dpi_delta_y',
            checks=(CheckHexList(LEN.DPI_DELTA_Y // 8), CheckByte(),), ),
        BitField(
            fid=FID.POWER_MODE,
            length=LEN.POWER_MODE,
            title='PowerMode',
            name='power_mode',
            checks=(CheckHexList(LEN.POWER_MODE // 8), CheckByte(),), ),
        BitField(
            fid=FID.ANGLE_SNAPPING,
            length=LEN.ANGLE_SNAPPING,
            title='AngleSnapping',
            name='angle_snapping',
            checks=(CheckHexList(LEN.ANGLE_SNAPPING // 8), CheckByte(),), ),
        BitField(
            fid=FID.WRITE_COUNTER,
            length=LEN.WRITE_COUNTER,
            title='WriteCounter',
            name='write_counter',
            checks=(CheckHexList(LEN.WRITE_COUNTER // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.WRITE_COUNTER) - 1),), ),
        BitField(
            fid=FID.RESERVED_7,
            length=LEN.RESERVED_7,
            title='Reserved_7',
            name='reserved_7',
            checks=(CheckHexList(LEN.RESERVED_7 // 8), CheckByte(),), ),
        BitField(
            fid=FID.POWER_SAVE_TIMEOUT,
            length=LEN.POWER_SAVE_TIMEOUT,
            title='PwrSaveTimeout',
            name='pwr_save_timeout',
            checks=(CheckHexList(LEN.POWER_SAVE_TIMEOUT // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.POWER_SAVE_TIMEOUT) - 1),), ),
        BitField(
            fid=FID.POWER_OFF_TIMEOUT,
            length=LEN.POWER_OFF_TIMEOUT,
            title='PwrOffTimeout',
            name='pwr_off_timeout',
            checks=(CheckHexList(LEN.POWER_OFF_TIMEOUT // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.POWER_OFF_TIMEOUT) - 1),), ),
        BitField(
            fid=FID.BTN_0_TO_11,
            length=LEN.BTN_0_TO_11,
            title='Btn_0_To_11',
            name='btn_0_to_11',
            aliases=('button_fields',),
            checks=(CheckHexList(LEN.BTN_0_TO_11 // 8), CheckByte(),), ),
        BitField(
            fid=FID.RESERVED_16,
            length=LEN.RESERVED_16,
            title='Reserved_16',
            name='reserved_16',
            checks=(CheckHexList(LEN.RESERVED_16 // 8), CheckByte(),), ),
        BitField(
            fid=FID.G_SHIFT_BTN_0_TO_11,
            length=LEN.G_SHIFT_BTN_0_TO_11,
            title='GShiftBtn_0_To_11',
            name='g_shift_btn_0_to_11',
            aliases=('g_shift_button_fields',),
            checks=(CheckHexList(LEN.G_SHIFT_BTN_0_TO_11 // 8), CheckByte(),), ),
        BitField(
            fid=FID.PROFILE_NAME_0_TO_23,
            length=LEN.PROFILE_NAME_0_TO_23,
            title='ProfileName_0_To_23',
            name='profile_name_0_to_23',
            checks=(CheckHexList(LEN.PROFILE_NAME_0_TO_23 // 8), CheckByte(),), ),
        BitField(
            fid=FID.CLUSTER_0_ACTIVE_EFFECT,
            length=LEN.CLUSTER_0_ACTIVE_EFFECT,
            title='Cluster_0_ActiveEffect',
            name='cluster_0_active_effect',
            checks=(CheckHexList(LEN.CLUSTER_0_ACTIVE_EFFECT // 8), CheckByte(),),),
        BitField(
            fid=FID.CLUSTER_1_ACTIVE_EFFECT,
            length=LEN.CLUSTER_1_ACTIVE_EFFECT,
            title='Cluster_1_ActiveEffect',
            name='cluster_1_active_effect',
            checks=(CheckHexList(LEN.CLUSTER_1_ACTIVE_EFFECT // 8), CheckByte(),),),
        BitField(
            fid=FID.CLUSTER_0_PASSIVE_EFFECT,
            length=LEN.CLUSTER_0_PASSIVE_EFFECT,
            title='Cluster_0_PassiveEffect',
            name='cluster_0_passive_effect',
            checks=(CheckHexList(LEN.CLUSTER_0_PASSIVE_EFFECT // 8), CheckByte(),),),
        BitField(
            fid=FID.CLUSTER_1_PASSIVE_EFFECT,
            length=LEN.CLUSTER_1_PASSIVE_EFFECT,
            title='Cluster_1_PassiveEffect',
            name='cluster_1_passive_effect',
            checks=(CheckHexList(LEN.CLUSTER_1_PASSIVE_EFFECT // 8), CheckByte(),),),
        BitField(
            fid=FID.LIGHTNING_FLAG,
            length=LEN.LIGHTNING_FLAG,
            title='LightningFlag',
            name='lightning_flag',
            checks=(CheckHexList(LEN.LIGHTNING_FLAG // 8), CheckByte(),), ),
        BitField(
            fid=FID.CRC,
            length=LEN.CRC,
            title='Crc',
            name='crc',
            checks=(CheckHexList(LEN.CRC // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.CRC) - 1),)),
    )

    @property
    def power_save_timeout(self):
        """
        Convert to big endian
        """
        return self.pwr_save_timeout[::-1]
    # end getter def power_save_timeout

    @power_save_timeout.setter
    def power_save_timeout(self, value):
        """
        Convert value to little endian
        """
        self.pwr_save_timeout = HexList(Numeral(value[::-1]))
    # end setter def power_save_timeout

    @property
    def power_off_timeout(self):
        """
        Convert to big endian
        """
        return self.pwr_off_timeout[::-1]
    # end getter def power_off_timeout

    @power_off_timeout.setter
    def power_off_timeout(self, value):
        """
        Convert value to little endian
        """
        self.pwr_off_timeout = HexList(Numeral(value[::-1]))
    # end setter def power_off_timeout
# end class ProfileFormatV6


class DpiResolutions:

    NORMAL_LENGTH = 10
    LONG_LENGTH = 25

    class Resolution:
        """
        Resolution data class
        """
        def __init__(self, dpi):
            """
            :param dpi: The DPI
            :type dpi: ``int`` or ``HexList``
            """
            self.dpi = to_int(dpi)
        # end def __init__

        def __hexlist__(self):
            """
            Convert the profile resolution settings to its ``HexList`` representation

            :return: HexList representation of the profile resolution settings
            :rtype: ``HexList``
            """
            # Convert to little endian
            return HexList(self.dpi.to_bytes(2, 'little'))
        # end def __hexlist__

        def __str__(self):
            return str(self.dpi)
        # end def __str__

        def __repr__(self):
            return self.__str__()
        # end def __repr__
    # end def Resolution

    class ResolutionXY:
        """
        Resolution XY data class
        """
        def __init__(self, dpi_x, dpi_y, lod):
            """
            :param dpi_x: X axis DPI
            :type dpi_x: ``int``
            :param dpi_y: Y axis DPI
            :type dpi_y: ``int``
            :param lod: Lift of distance
            :type lod: ``int``
            """
            self._dpi_x = DpiResolutions.Resolution(dpi_x)
            self._dpi_y = DpiResolutions.Resolution(dpi_y)
            self._lod = lod
        # end def __init__

        @property
        def dpi_x(self):
            return self._dpi_x
        # end def dpi_x

        @dpi_x.setter
        def dpi_x(self, value):
            self._dpi_x = value
        # end def dpi_x

        @property
        def dpi_y(self):
            return self._dpi_y
        # end def dpi_y

        @dpi_y.setter
        def dpi_y(self, value):
            self._dpi_y = value
        # end def dpi_y

        @property
        def lod(self):
            return self._lod
        # end def lod

        @lod.setter
        def lod(self, value):
            self._lod = value
        # end def lod

        def __hexlist__(self):
            """
            Convert the profile resolution settings to its ``HexList`` representation

            :return: HexList representation of the profile resolution settings
            :rtype: ``HexList``
            """
            return HexList(self._dpi_x) + HexList(self._dpi_y) + HexList(self._lod)
        # end def __hexlist_

        def __str__(self):
            return f'[{self._dpi_x}, {self._dpi_y}, {self._lod}]'
        # end def __str__

        def __repr__(self):
            return self.__str__()
        # end def __repr__
    # end class ResolutionXY

    def __init__(self, dpi_resolutions):
        """
        :param dpi_resolutions: The settings of profile resolutions
        :type dpi_resolutions: ``list[Resolution]``
        """
        self.dpi_resolutions = dpi_resolutions
    # end def __init__

    @property
    def count(self):
        """
        The number of profile resolutions

        :return: Profile resolution count
        :rtype: ``int``
        """
        return len(self.dpi_resolutions)
    # end getter def count

    @property
    def kind(self):
        """
        The kind of resolution

        :return: Profile resolution data type
        :rtype: ``Resolution`` or ``ResolutionXY``

        :raise: ``ValueError`` if got an unknown resolution length
        """
        if len(HexList(self)) == self.NORMAL_LENGTH:
            return self.Resolution
        elif len(HexList(self)) == self.LONG_LENGTH:
            return self.ResolutionXY
        else:
            raise ValueError(f'Unknown resolution length: {len(HexList(self)) }')
        # end if
    # end getter def kind

    @classmethod
    def from_dpi_list(cls, dpi_list):
        """
        Instantiate ``ProfileResolution`` by profile raw data

        :param dpi_list: The DPI list
        :type dpi_list: ``list[int]`` or ``list[list[int]]``

        :return: ProfileResolutions object
        :rtype: ``DpiResolutions``
        """
        normal_resolution_type = True if isinstance(dpi_list[0], int) else False
        resolutions = []
        for dpi in dpi_list:
            if normal_resolution_type:
                resolutions.append(cls.Resolution(dpi))
            else:
                if isinstance(dpi, list):
                    # dpi[idx]: Meaning
                    #      0  : X
                    #      1  : Y
                    #      2  : LOD
                    resolutions.append(cls.ResolutionXY(dpi[0], dpi[1], dpi[2]))
                # end if
            # end if
        # end for
        return DpiResolutions(resolutions)
    # end def from_dpi_list

    @classmethod
    def from_hex_list(cls, dpi_raw_data):
        """
        Instantiate ``ProfileResolution`` by profile raw data

        :param dpi_raw_data: Profile DPI resolutions raw data list
        :type dpi_raw_data: ``HexList``

        :return: ProfileResolutions object
        :rtype: ``DpiResolutions``
        """
        dpi_list = []
        if len(dpi_raw_data) == cls.NORMAL_LENGTH:
            for n in range(0, len(dpi_raw_data), 2):
                # Convert to big endian
                dpi = dpi_raw_data[n: n + 2][::-1]
                dpi_list.append(cls.Resolution(dpi))
            # end for
        elif len(dpi_raw_data) == cls.LONG_LENGTH:
            for n in range(0, len(dpi_raw_data), 5):
                # Convert to big endian
                dpi_x = dpi_raw_data[n: n + 2][::-1]
                dpi_y = dpi_raw_data[n + 2: n + 4][::-1]
                lod = dpi_raw_data[n + 4]
                dpi_list.append(cls.ResolutionXY(dpi_x, dpi_y, lod))
            # end for
        # end if
        return DpiResolutions(dpi_list)
    # end def from_hex_list

    def __hexlist__(self):
        """
        Convert ``DpiResolutions`` to its ``HexList`` representation

        :return: DpiResolutions data in ``HexList``
        :rtype: ``HexList``
        """
        dpi_raw_settings = HexList()
        for dpi_resolution in self.dpi_resolutions:
            dpi_raw_settings += HexList(dpi_resolution)
        # end for
        return dpi_raw_settings
    # end def __hexlist__

    def __str__(self):
        presentation = ''
        for dpi_resolution in self.dpi_resolutions:
            presentation += str(dpi_resolution)
            if isinstance(dpi_resolution, self.Resolution):
                presentation += ', '
            # end if
        # end for
        return presentation
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__
# end class DpiResolutions


class ProfileButton:
    """
    Profile Button class definition
    """

    DATA_SIZE = 4

    @unique
    class Category(IntEnum):
        """
        Button behavior (i.e. Byte 0)
        """
        EXECUTE_MACRO = 0x00
        STOP_MACRO = 0x10
        STOP_ALL_MACRO = 0x20
        BUTTON_REMAPPING = 0x80
        FUNCTION_EXECUTION = 0x90
        UNUSED = 0xFF
    # end class Category

    @unique
    class ButtonRemapping(IntEnum):
        """
        Button remapping Opcode (i.e. Byte 1)
        """
        BUTTON_NOT_SENT = 0x00
        GENERIC_MOUSE_BUTTON = 0x01
        STANDARD_KEY = 0x02
        CONSUMER_KEY = 0x03
    # end class ButtonRemapping

    @unique
    class ButtonMask(IntEnum):
        """
        Mouse button bit definition P1 & P2 (i.e. Byte 2 & 3)
        """
        BUTTON_1 = 0x0001
        BUTTON_2 = 0x0002
        BUTTON_3 = 0x0004
        BUTTON_4 = 0x0008
        BUTTON_5 = 0x0010
        BUTTON_6 = 0x0020
        BUTTON_7 = 0x0040
        BUTTON_8 = 0x0080
        BUTTON_9 = 0x0100
        BUTTON_10 = 0x0200
        BUTTON_11 = 0x0400
        BUTTON_12 = 0x0800
        BUTTON_13 = 0x1000
        BUTTON_14 = 0x2000
        BUTTON_15 = 0x4000
        BUTTON_16 = 0x8000
    # end class ButtonMask

    @unique
    class ButtonType(IntEnum):
        """
        Profile Button Type definition class
        """
        BUTTON = 0
        G_SHIFT = 1
    # end def ButtonType

    @unique
    class ButtonIndex(IntEnum):
        """
        Profile Button/GShift Button Index definition in a profile instance.
        """
        BUTTON_1 = 0
        BUTTON_2 = 1
        BUTTON_3 = 2
        BUTTON_4 = 3
        BUTTON_5 = 4
        BUTTON_6 = 5
        BUTTON_7 = 6
        BUTTON_8 = 7
        BUTTON_9 = 8
        BUTTON_10 = 9
        BUTTON_11 = 10
        BUTTON_12 = 11
        BUTTON_13 = 12
        BUTTON_14 = 13
        BUTTON_15 = 14
        BUTTON_16 = 15
    # end def ButtonIndex

    @unique
    class Modifier(IntEnum):
        """
        Modifier key - p1 (i.e. Byte2)

        NB: The modifier key could be any combination, the modifiers listed in this class are the common usages.
            (i.e. The modifier value for "LEFT_CTRL + LEFT_SHIFT" = 0x03)
        """
        NO_ACTION = 0x00
        LEFT_CTRL = 0x01
        LEFT_SHIFT = 0x02
        LEFT_ALT = 0x04
        LEFT_GUI = 0x08
        RIGHT_CTRL = 0x10
        RIGHT_SHIFT = 0x20
        RIGHT_ALT = 0x40
        RIGHT_GUI = 0x80
    # end class Modifier

    @unique
    class FunctionExecution(IntEnum):
        """
        Function execution Opcode (i.e. Byte 1)
        """
        NO_ACTION = 0x00
        TILT_LEFT = 0x01
        TILT_RIGHT = 0x02
        SELECT_NEXT_DPI = 0x03
        SELECT_PREVIOUS_DPI = 0x04
        CYCLE_THROUGH_DPI = 0x05
        DEFAULT_DPI = 0x06
        DPI_SHIFT = 0x07
        SELECT_NEXT_PROFILE = 0x08
        SELECT_PREVIOUS_PROFILE = 0x09
        CYCLE_THROUGH_PROFILE = 0x0A
        G_SHIFT = 0x0B
        BATTERY_LIFE_INDICATOR = 0x0C
        SWITCH_TO_SPECIFIC_PROFILE = 0x0D
        PERFORMANCE_OFFICE_MODE_SWITCH = 0x0E
        HOST_BUTTON = 0x0F
        SCROLL_DOWN = 0x10
        SCROLL_UP = 0x11
    # end class FunctionExecution

    @unique
    class MouseButton(IntEnum):
        """
        Mouse Button (i.e. Byte 4)
        """
        LEFT = 0x01
        RIGHT = 0x02
        MIDDLE = 0x04
        BACKWARD = 0x08
        FORWARD = 0x10
    # end class MouseButton

    KEY_ID_TO_MOUSE_BUTTON_MASK = {
        KEY_ID.BUTTON_1:    ButtonMask.BUTTON_1,
        KEY_ID.BUTTON_2:    ButtonMask.BUTTON_2,
        KEY_ID.BUTTON_3:    ButtonMask.BUTTON_3,
        KEY_ID.BUTTON_4:    ButtonMask.BUTTON_4,
        KEY_ID.BUTTON_5:    ButtonMask.BUTTON_5,
        KEY_ID.BUTTON_6:    ButtonMask.BUTTON_6,
        KEY_ID.BUTTON_7:    ButtonMask.BUTTON_7,
        KEY_ID.BUTTON_8:    ButtonMask.BUTTON_8,
        KEY_ID.BUTTON_9:    ButtonMask.BUTTON_9,
        KEY_ID.BUTTON_10:   ButtonMask.BUTTON_10,
        KEY_ID.BUTTON_11:   ButtonMask.BUTTON_11,
        KEY_ID.BUTTON_12:   ButtonMask.BUTTON_12,
        KEY_ID.BUTTON_13:   ButtonMask.BUTTON_13,
        KEY_ID.BUTTON_14:   ButtonMask.BUTTON_14,
        KEY_ID.BUTTON_15:   ButtonMask.BUTTON_15,
        KEY_ID.BUTTON_16:   ButtonMask.BUTTON_16,
    }

    KEY_ID_TO_FUNCTION_TYPE = {
        KEY_ID.NO_ACTION:                           FunctionExecution.NO_ACTION,
        KEY_ID.TILT_LEFT:                           FunctionExecution.TILT_LEFT,
        KEY_ID.TILT_RIGHT:                          FunctionExecution.TILT_RIGHT,
        KEY_ID.SELECT_NEXT_DPI:                     FunctionExecution.SELECT_NEXT_DPI,
        KEY_ID.SELECT_PREV_DPI:                     FunctionExecution.SELECT_PREVIOUS_DPI,
        KEY_ID.CYCLE_THROUGH_DPI:                   FunctionExecution.CYCLE_THROUGH_DPI,
        KEY_ID.DEFAULT_DPI:                         FunctionExecution.DEFAULT_DPI,
        KEY_ID.DPI_SHIFT:                           FunctionExecution.DPI_SHIFT,
        KEY_ID.SELECT_NEXT_ONBOARD_PROFILE:         FunctionExecution.SELECT_NEXT_PROFILE,
        KEY_ID.SELECT_PREV_ONBOARD_PROFILE:         FunctionExecution.SELECT_PREVIOUS_PROFILE,
        KEY_ID.CYCLE_THROUGH_ONBOARD_PROFILE:       FunctionExecution.CYCLE_THROUGH_PROFILE,
        KEY_ID.BATTERY_LIFE_INDICATOR:              FunctionExecution.BATTERY_LIFE_INDICATOR,
        KEY_ID.SWITCH_TO_SPECIFIC_ONBOARD_PROFILE:  FunctionExecution.SWITCH_TO_SPECIFIC_PROFILE,
    }

    class Button(BitFieldContainerMixin):
        """
        Button settings class definition
        """

        class FID:
            """
            Field Identifiers
            """
            PARAM_1 = 0xFF
            PARAM_2 = PARAM_1 - 1
            PARAM_3 = PARAM_2 - 1
            PARAM_4 = PARAM_3 - 1
        # end class FID

        class LEN:
            """
            Field Lengths in bits
            """
            PARAM_1 = 0x08
            PARAM_2 = 0x08
            PARAM_3 = 0x08
            PARAM_4 = 0x08
        # end class LEN

        FIELDS = (
            BitField(
                fid=FID.PARAM_1,
                length=LEN.PARAM_1,
                title='Param_1',
                name='param_1',
                checks=(CheckHexList(LEN.PARAM_1 // 8), CheckByte(),), ),
            BitField(
                fid=FID.PARAM_2,
                length=LEN.PARAM_2,
                title='Param_2',
                name='param_2',
                checks=(CheckHexList(LEN.PARAM_2 // 8), CheckByte(),), ),
            BitField(
                fid=FID.PARAM_3,
                length=LEN.PARAM_3,
                title='Param_3',
                name='param_3',
                checks=(CheckHexList(LEN.PARAM_3 // 8), CheckByte(),), ),
            BitField(
                fid=FID.PARAM_4,
                length=LEN.PARAM_4,
                title='Param_4',
                name='param_4',
                checks=(CheckHexList(LEN.PARAM_4 // 8), CheckByte(),), ),
        )
    # end class Button

    @classmethod
    def create_execute_macro(cls, sector_id, address):
        """
        Create execute macro settings

        :param sector_id: The sector id of the Macro
        :type sector_id: ``int``
        :param address: The starting address of the Macro
        :type address: ``int``

        :return: The settings of the profile button
        :rtype: ``ProfileButton.Button``
        """
        numeral_sector_id = Numeral(sector_id, byteCount=2)
        assert numeral_sector_id[0] in [0, 1]  # OOB sector: numeral_sector_id[0] = 1
        numeral_address = Numeral(address, byteCount=2)
        param_1 = cls.Category.EXECUTE_MACRO | numeral_sector_id[0]
        return cls.Button(param_1=param_1, param_2=numeral_sector_id[1],
                          param_3=numeral_address[0], param_4=numeral_address[1])
    # end def create_execute_macro

    @classmethod
    def create_stop_macro(cls, sector_id, address):
        """
        Create stop the macro settings

        :param sector_id: The sector id of the Macro
        :type sector_id: ``int``
        :param address: The starting address of the Macro
        :type address: ``int``

        :return: The settings of the profile button
        :rtype: ``ProfileButton.Button``
        """
        numeral_sector_id = Numeral(sector_id, byteCount=2)
        assert numeral_sector_id[0] in [0, 1]  # OOB sector: numeral_sector_id[0] = 1
        numeral_address = Numeral(address, byteCount=2)
        param_1 = cls.Category.STOP_MACRO | numeral_sector_id[0]
        return cls.Button(param_1=param_1, param_2=numeral_sector_id[1],
                          param_3=numeral_address[0], param_4=numeral_address[1])
    # end def create_stop_macro

    @classmethod
    def create_stop_all_macros(cls):
        """
        Create stop all macros settings

        :return: The settings of the profile button
        :rtype: ``ProfileButton.Button``
        """
        return cls.Button(param_1=cls.Category.STOP_ALL_MACRO, param_2=0, param_3=0, param_4=0)
    # end def create_stop_all_macros

    @classmethod
    def create_button_not_sent(cls):
        """
        Create button not sent settings

        :return: The settings of the profile button
        :rtype: ``ProfileButton.Button``
        """
        return cls.Button(param_1=cls.Category.BUTTON_REMAPPING, param_2=0, param_3=0, param_4=0)
    # end def create_button_not_sent

    @classmethod
    def create_mouse_button(cls, button_mask):
        """
        Create mouse button settings

        :param button_mask: Mouse button mask
        :type button_mask: ``ProfileButton.ButtonMask | ProfileButton.MouseButton``

        :return: The settings of the profile button
        :rtype: ``ProfileButton.Button``
        """
        numeral_mouse_button = Numeral(button_mask, byteCount=2)
        return cls.Button(param_1=cls.Category.BUTTON_REMAPPING, param_2=cls.ButtonRemapping.GENERIC_MOUSE_BUTTON,
                          param_3=numeral_mouse_button[0], param_4=numeral_mouse_button[1])
    # end def create_mouse_button

    @classmethod
    def create_standard_key(cls, modifier=0, key_id=0):
        """
        Create standard key settings

        :param modifier: The modifier keys - OPTIONAL
        :type modifier: ``int | ProfileButton.Modifier``
        :param key_id: The key id - OPTIONAL
        :type key_id: ``KEY_ID``

        :return: The settings of the profile button
        :rtype: ``ProfileButton.Button``
        """
        assert modifier != 0 or key_id != 0
        return cls.Button(param_1=cls.Category.BUTTON_REMAPPING, param_2=cls.ButtonRemapping.STANDARD_KEY,
                          param_3=modifier, param_4=STANDARD_KEYS[key_id])
    # end def create_standard_key

    @classmethod
    def get_consumer_usage(cls, key_id, os_variant):
        """
        Get consumer usage code

        :param key_id: The key id of the consumer key
        :type key_id: ``KEY_ID``
        :param os_variant: The OS variant
        :type os_variant: ``OS``

        :return: The consumer usage code. Return 0 if the key is not a consumer key for the given OS.
        :rtype: ``int``
        """
        consumer_usage = 0
        try:
            consumer_key_info = HidData.CONSUMER_KEYS[key_id]
            for os in list(consumer_key_info.keys()):
                if os == OS.ALL or os_variant == os:
                    consumer_usage = HidData.CONSUMER_KEYS[key_id][os]
                # end if
            # end for
        except KeyError:
            warnings.warn(f'The key {key_id!s} is not a consumer keys in {os_variant}')
        # end try
        return 0 if consumer_usage == 0 else consumer_usage
    # end def get_consumer_usage

    @classmethod
    def get_consumer_key_id(cls, consumer_usage, os_variant):
        """
        Get key_id by the consumer usage code

        :param consumer_usage: Consumer HID Usage
        :type consumer_usage: ``ConsumerHidUsage | int``
        :param os_variant: The OS variant
        :type os_variant: ``OS``

        :return: The key id of consumer usage code.
        :rtype: ``KEY_ID``

        :raise ``AssertionError``: If found multiple keys or key not found
        """
        found_key_ids = []
        for key_id, consumer_usage_in_os in HidData.CONSUMER_KEYS.items():
            if consumer_usage_in_os.get(os_variant) == consumer_usage:
                found_key_ids.append(key_id)
            else:
                if os_variant != OS.ALL and consumer_usage_in_os.get(OS.ALL) == consumer_usage:
                    found_key_ids.append(key_id)
                # end if
            # end if
        # end for
        assert len(found_key_ids) == 1
        return found_key_ids[0]
    # end def get_consumer_usage

    @classmethod
    def create_consumer_button(cls, key_id, os_variant=OS.WINDOWS):
        """
        Create consumer button settings

        :param key_id: The consumer key
        :type key_id: ``KEY_ID``
        :param os_variant: The OS variant used for the key code translation - OPTIONAL
        :type os_variant: ``OS``

        :return: The settings of the profile button
        :rtype: ``ProfileButton.Button``
        """
        consumer_usage = Numeral(cls.get_consumer_usage(key_id=key_id, os_variant=os_variant), byteCount=2)
        return cls.Button(param_1=cls.Category.BUTTON_REMAPPING, param_2=cls.ButtonRemapping.CONSUMER_KEY,
                          param_3=consumer_usage[0], param_4=consumer_usage[1])
    # end def create_consumer_button

    # noinspection PyShadowingBuiltins
    @classmethod
    def create_function_button(cls, function_type, profile_number=None):
        """
        Create function execution button settings

        :param function_type: Function execution button
        :type function_type: ``ProfileButton.FunctionExecution``
        :param profile_number: The parameter be used for Enabled Profile specific number - OPTIONAL
        :type profile_number: ``int | None``

        :return: The settings of the profile button
        :rtype: ``ProfileButton.Button``

        :raise ``AssertionError``: If the function type is out of range
        """
        assert ProfileButton.FunctionExecution.NO_ACTION <= function_type <= ProfileButton.FunctionExecution.SCROLL_UP
        if function_type != cls.FunctionExecution.SWITCH_TO_SPECIFIC_PROFILE:
            return cls.Button(param_1=cls.Category.FUNCTION_EXECUTION, param_2=function_type, param_3=0, param_4=0)
        else:
            return cls.Button(param_1=cls.Category.FUNCTION_EXECUTION, param_2=function_type, param_3=0,
                              param_4=profile_number)
        # end if
    # end def create_function_button

    @classmethod
    def convert_modifier_to_key_id(cls, modifier):
        """
        Convert Profile.Modifier to KEY_ID

        :param modifier: The modifier
        :type modifier: ``ProfileButton.Modifier``

        :return: The KEY_ID of the modifier
        :rtype: ``KEY_ID | None``

        :raise ``ValueError``: If the input modifier is unsupported.
        """
        if modifier == cls.Modifier.NO_ACTION:
            return None
        elif modifier == cls.Modifier.LEFT_GUII:
            return KEY_ID.KEYBOARD_LEFT_BRACKET_AND_BRACE
        elif modifier == cls.Modifier.LEFT_CTRL:
            return KEY_ID.KEYBOARD_LEFT_CONTROL
        elif modifier == cls.Modifier.LEFT_SHIFT:
            return KEY_ID.KEYBOARD_LEFT_SHIFT
        elif modifier == cls.Modifier.LEFT_ALT:
            return KEY_ID.KEYBOARD_LEFT_ALT
        elif modifier == cls.Modifier.RIGHT_GUI:
            return KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION
        elif modifier == cls.Modifier.RIGHT_CTRL:
            return KEY_ID.KEYBOARD_RIGHT_CONTROL
        elif modifier == cls.Modifier.RIGHT_SHIFT:
            return KEY_ID.KEYBOARD_RIGHT_SHIFT
        elif modifier == cls.Modifier.RIGHT_ALT:
            return KEY_ID.KEYBOARD_RIGHT_ALT
        else:
            raise ValueError(f'Unknown modifier: {modifier!s}')
        # end if
    # end def convert_modifier_to_key_id

    @classmethod
    def convert_key_id_to_button_mask(cls, key_id):
        """
        Convert ``KEY_ID`` to ``ButtonMask`

        :param key_id: Mouse button KEY_ID
        :type key_id: ``KEY_ID``

        :return: ``ProfileButton.ButtonMask`` object
        :rtype: ``ProfileButton.ButtonMask``
        """
        return cls.KEY_ID_TO_MOUSE_BUTTON_MASK[key_id]
    # end def convert_key_id_to_button_mask

    @classmethod
    def convert_button_mask_to_key_id(cls, button_mask):
        """
        Convert ``ButtonMask` to ``KEY_ID``

        :param button_mask: Mouse button mask
        :type button_mask: ``ProfileButton.ButtonMask | int``

        :return: ``KEY_ID`` object
        :rtype: ``KEY_ID``

        :raise ``AssertionError``: If cannot convert the button_mask to KEY_ID
        """
        key_id = next((k for k, v in cls.KEY_ID_TO_MOUSE_BUTTON_MASK.items() if v == button_mask), None)
        assert key_id is not None
        return key_id
    # end def convert_button_mask_to_key_id

    @classmethod
    def convert_key_id_to_function_type(cls, key_id):
        """
        Convert ``KEY_ID`` to ``ProfileButton.FunctionExecution``

        :param key_id: Key id corresponding to the FunctionExecution type
        :type key_id: ``KEY_ID``

        :return: Function type defined in ProfileButton.FunctionExecution
        :rtype: ``ProfileButton.FunctionExecution``
        """
        return cls.KEY_ID_TO_FUNCTION_TYPE[key_id]
    # end def convert_key_id_to_function_type

    @classmethod
    def convert_function_type_to_key_id(cls, function_type):
        """
        Convert ``ProfileButton.FunctionExecution`` to ``KEY_ID``

        :param function_type: FunctionExecution type
        :type function_type: ``ProfileButton.FunctionExecution``

        :return: Key id corresponding to the FunctionExecution type
        :rtype: ``KEY_ID``

        :raise ``AssertionError``: If cannot convert the function_type to KEY_ID
        """
        key_id = next((k for k, v in cls.KEY_ID_TO_FUNCTION_TYPE.items() if v == function_type), None)
        assert key_id is not None
        return key_id
    # end def convert_function_type_to_key_id
# end class ProfileButton


class MacroCommand0(BitFieldContainerMixin):
    """
    Macro command which has no input parameters
    """

    DATA_SIZE = 1

    class FID:
        """
        Field Identifiers
        """
        OP_CODE = 0xFF
    # end class FID

    class LEN:
        """
        Field Lengths in bits
        """
        OP_CODE = 0x08
    # end class LEN

    FIELDS = (
        BitField(
            fid=FID.OP_CODE,
            length=LEN.OP_CODE,
            title='OpCode',
            name='op_code',
            checks=(CheckHexList(LEN.OP_CODE // 8), CheckByte(),), ),
    )
# end class MacroCommand0


class MacroCommand1(MacroCommand0):
    """
    Macro command which has 1 input parameters
    """

    DATA_SIZE = 2

    class FID(MacroCommand0.FID):
        # See ``MacroCommand0.FID``
        P1 = MacroCommand0.FID.OP_CODE - 1
    # end class FID

    class LEN(MacroCommand0.LEN):
        # See ``MacroCommand0.LEN``
        P1 = 0x08
    # end class LEN

    FIELDS = MacroCommand0.FIELDS + (
        BitField(
            fid=FID.P1,
            length=LEN.P1,
            title='P1',
            name='p1',
            checks=(CheckHexList(LEN.P1 // 8), CheckByte(),), ),
    )
# end class MacroCommand1


class MacroCommand2(MacroCommand1):
    """
    Macro command which has 2 input parameters
    """

    DATA_SIZE = 3

    class FID(MacroCommand1):
        # See ``MacroCommand1.FID``
        P2 = MacroCommand1.FID.P1 - 1
    # end class FID

    class LEN(MacroCommand1.LEN):
        # See ``MacroCommand1.LEN``
        P2 = 0x08
    # end class LEN

    FIELDS = MacroCommand1.FIELDS + (
        BitField(
            fid=FID.P2,
            length=LEN.P2,
            title='P2',
            name='p2',
            checks=(CheckHexList(LEN.P2 // 8), CheckByte(),), ),
    )
# end class MacroCommand2


class MacroCommand4(MacroCommand2):
    """
    Macro command which has 4 input parameters
    """

    DATA_SIZE = 5

    class FID(MacroCommand2.FID):
        # See ``MacroCommand2.FID``
        P3 = MacroCommand2.FID.P2 - 1
        P4 = P3 - 1
    # end class FID

    class LEN(MacroCommand2.LEN):
        # See ``MacroCommand2.LEN``
        P3 = 0x08
        P4 = 0x08
    # end class LEN

    FIELDS = MacroCommand2.FIELDS + (
        BitField(
            fid=FID.P3,
            length=LEN.P3,
            title='P3',
            name='p3',
            checks=(CheckHexList(LEN.P3 // 8), CheckByte(),), ),
        BitField(
            fid=FID.P4,
            length=LEN.P4,
            title='P4',
            name='p4',
            checks=(CheckHexList(LEN.P4 // 8), CheckByte(),), ),
    )
# end class MacroCommand4


class ProfileMacro:
    """
    Profile Macro class implementation
    """

    class Opcode:
        """
        Operation codes of Macro (i.e. Byte 0)

        cf - https://docs.google.com/document/d/1Xkh0JiA6CkMnYoA9g28qj7wJzs-k7eP3NFuZKDenAXE/view#heading=h.5mv09q68jdyj
        """
        NO_OPERATION = 0x00
        WAIT_FOR_RELEASE = 0x01
        REPEAT_WHILE_PRESSED = 0x02
        REPEAT_UNTIL_CANCEL = 0x03
        ROLLER = 0x20
        AC_PAN = 0x21
        WAIT_FOR_X_MS = 0x40
        BUTTON_DOWN = 0x41
        BUTTON_UP = 0x42
        KEY_DOWN = 0x43
        KEY_UP = 0x44
        CONS_DOWN = 0x45
        CONS_UP = 0x46
        JUMP = 0x60
        XY = 0x61
        MACRO_END = 0xFF
    # end class OpCode

    @classmethod
    def create_no_operation(cls):
        """
        Create a "no operation" macro command

        :return: No Operation command
        :rtype: ``MacroCommand0``
        """
        return MacroCommand0(op_code=cls.Opcode.NO_OPERATION)
    # end def create_no_operation

    @classmethod
    def create_repeat_while_pressed(cls):
        """
        Create a "repeat while pressed" macro command

        :return: Repeat While Pressed command
        :rtype: ``MacroCommand0``
        """
        return MacroCommand0(op_code=cls.Opcode.REPEAT_WHILE_PRESSED)
    # end def create_repeat_while_pressed

    @classmethod
    def create_repeat_until_cancel(cls):
        """
        Create a "repeat until cancel" macro command

        :return: Repeat Until Cancel command
        :rtype: ``MacroCommand0``
        """
        return MacroCommand0(op_code=cls.Opcode.REPEAT_UNTIL_CANCEL)
    # end def create_repeat_until_cancel

    @classmethod
    def create_wait_for_release(cls):
        """
        Create a "wait for release" macro command

        :return: Wait for Release command
        :rtype: ``MacroCommand0``
        """
        return MacroCommand0(op_code=cls.Opcode.WAIT_FOR_RELEASE)
    # end def create_wait_for_release

    @classmethod
    def create_macro_end(cls):
        """
        Create a "macro end" macro command

        :return: Macro End command
        :rtype: ``MacroCommand0``
        """
        return MacroCommand0(op_code=cls.Opcode.MACRO_END)
    # end def create_macro_end

    @classmethod
    def create_roller(cls, v_wheel):
        """
        Create a "roller" macro command

        :param v_wheel: The movement of vertical scroll
        :type v_wheel: ``int``

        :return: Roller command
        :rtype: ``MacroCommand1``
        """
        v_wheel = Numeral(v_wheel, byteCount=1)
        return MacroCommand1(op_code=cls.Opcode.ROLLER, p1=v_wheel)
    # end def create_roller

    @classmethod
    def create_ac_pan(cls, h_wheel):
        """
        Create a "ac pan" macro command

        :param h_wheel: The movement of horizontal scroll
        :type h_wheel: ``int``

        :return: AC Pan command
        :rtype: ``MacroCommand1``
        """
        h_wheel = Numeral(h_wheel, byteCount=1)
        return MacroCommand1(op_code=cls.Opcode.AC_PAN, p1=h_wheel)
    # end def create_ac_pan

    @classmethod
    def create_button_down(cls, button_mask):
        """
        Create a "button down" macro command

        :param button_mask: Mouse button
        :type button_mask: ``ProfileButton.ButtonMask``

        :return: Button Down command
        :rtype: ``MacroCommand2``
        """
        numeral_button_mask = Numeral(button_mask, byteCount=2)
        return MacroCommand2(op_code=cls.Opcode.BUTTON_DOWN, p1=numeral_button_mask[0], p2=numeral_button_mask[1])
    # end def create_button_down

    @classmethod
    def create_button_up(cls, button_mask):
        """
        Create a "button up" macro command

        :param button_mask: Mouse button
        :type button_mask: ``ProfileButton.ButtonMask``

        :return: Button Up command
        :rtype: ``MacroCommand2``
        """
        numeral_button_mask = Numeral(button_mask, byteCount=2)
        return MacroCommand2(op_code=cls.Opcode.BUTTON_UP, p1=numeral_button_mask[0], p2=numeral_button_mask[1])
    # end def create_button_up

    @classmethod
    def create_button_stroke(cls, button_mask):
        """
        Create a "button down and up" macro commands

        :param button_mask: Mouse button
        :type button_mask: ``ProfileButton.ButtonMask``

        :return: Button Down and Up commands
        :rtype: ``tuple[MacroCommand2, MacroCommand2]``
        """
        numeral_button_mask = Numeral(button_mask, byteCount=2)
        button_down = MacroCommand2(op_code=cls.Opcode.BUTTON_DOWN, p1=numeral_button_mask[0],
                                    p2=numeral_button_mask[1])
        button_up = MacroCommand2(op_code=cls.Opcode.BUTTON_UP, p1=numeral_button_mask[0], p2=numeral_button_mask[1])
        return button_down, button_up
    # end def create_button_stroke

    @classmethod
    def create_std_key_down(cls, modifier=0, key_id=0):
        """
        Create a "key down" macro command

        :param modifier: The modifier keys - OPTIONAL
        :type modifier: ``int | ProfileButton.Modifier``
        :param key_id: The key id - OPTIONAL
        :type key_id: ``KEY_ID``

        :return: Key Down command
        :rtype: ``MacroCommand2``

        :raise ``AssertionError``: If both of modifier and key_id equal to 0
        """
        assert modifier != 0 or key_id != 0
        return MacroCommand2(op_code=cls.Opcode.KEY_DOWN, p1=modifier, p2=STANDARD_KEYS[key_id])
    # end def create_key_down

    @classmethod
    def create_std_key_up(cls, modifier=0, key_id=0):
        """
        Create a "key up" macro command

        :param modifier: The modifier keys - OPTIONAL
        :type modifier: ``int | ProfileButton.Modifier``
        :param key_id: The key id - OPTIONAL
        :type key_id: ``KEY_ID``

        :return: Key Up command
        :rtype: ``MacroCommand2``

        :raise ``AssertionError``: If both of modifier and key_id equal to 0
        """
        assert modifier != 0 or key_id != 0
        return MacroCommand2(op_code=cls.Opcode.KEY_UP, p1=modifier, p2=STANDARD_KEYS[key_id])
    # end def create_std_key_up

    @classmethod
    def create_std_key_stroke(cls, modifier=0, key_id=0):
        """
        Create a "key down and up" macro commands

        :param modifier: The modifier keys - OPTIONAL
        :type modifier: ``int | ProfileButton.Modifier``
        :param key_id: The key id - OPTIONAL
        :type key_id: ``KEY_ID``

        :return: Key Down and Up commands
        :rtype: ``tuple[MacroCommand2, MacroCommand2]``

        :raise ``AssertionError``: If both of modifier and key_id equal to 0
        """
        assert modifier != 0 or key_id != 0
        key_down = MacroCommand2(op_code=cls.Opcode.KEY_DOWN, p1=modifier, p2=STANDARD_KEYS[key_id])
        key_up = MacroCommand2(op_code=cls.Opcode.KEY_UP, p1=modifier, p2=STANDARD_KEYS[key_id])
        return key_down, key_up
    # end def create_std_key_stroke

    @classmethod
    def create_cons_key_down(cls, key_id, os_variant=OS.WINDOWS):
        """
        Create a "consumer key down" macro command

        :param key_id: The consumer key
        :type key_id: ``KEY_ID``
        :param os_variant: The OS variant - OPTIONAL
        :type os_variant: ``OS``

        :return: Consumer Key Down command
        :rtype: ``MacroCommand2``
        """
        consumer_usage = Numeral(ProfileButton.get_consumer_usage(key_id=key_id, os_variant=os_variant), byteCount=2)
        return MacroCommand2(op_code=cls.Opcode.CONS_DOWN, p1=consumer_usage[0], p2=consumer_usage[1])
    # end def create_cons_key_down

    @classmethod
    def create_cons_key_up(cls, key_id, os_variant=OS.WINDOWS):
        """
        Create a "consumer key up" macro command

        :param key_id: The consumer key
        :type key_id: ``KEY_ID``
        :param os_variant: The OS variant - OPTIONAL
        :type os_variant: ``OS``

        :return: Consumer Key Up command
        :rtype: ``MacroCommand2``
        """
        consumer_usage = Numeral(ProfileButton.get_consumer_usage(key_id=key_id, os_variant=os_variant), byteCount=2)
        return MacroCommand2(op_code=cls.Opcode.CONS_UP, p1=consumer_usage[0], p2=consumer_usage[1])
    # end def create_cons_key_up

    @classmethod
    def create_cons_key_stroke(cls, key_id, os_variant=OS.WINDOWS):
        """
        Create a "consumer key up" macro command

        :param key_id: The consumer key
        :type key_id: ``KEY_ID``
        :param os_variant: The OS variant - OPTIONAL
        :type os_variant: ``OS``

        :return: Consumer Key Up command
        :rtype: ``MacroCommand2``
        """
        consumer_usage = Numeral(ProfileButton.get_consumer_usage(key_id=key_id, os_variant=os_variant), byteCount=2)
        cons_down = MacroCommand2(op_code=cls.Opcode.CONS_DOWN, p1=consumer_usage[0], p2=consumer_usage[1])
        cons_up = MacroCommand2(op_code=cls.Opcode.CONS_UP, p1=consumer_usage[0], p2=consumer_usage[1])
        return cons_down, cons_up
    # end def create_cons_key_stroke

    @classmethod
    def create_delay(cls, time_ms):
        """
        Create a "delay" macro command

        :param time_ms: Time in milli-second
        :type time_ms: ``int``

        :return: Delay command
        :rtype: ``MacroCommand2``
        """
        numeral_time_ms = Numeral(time_ms, byteCount=2)
        return MacroCommand2(op_code=cls.Opcode.WAIT_FOR_X_MS, p1=numeral_time_ms[0], p2=numeral_time_ms[1])
    # end def create_delay

    @classmethod
    def create_jump(cls, sector_id, address):
        """
        Create a "jump" macro command

        :param sector_id: The sector id
        :type sector_id: ``int``
        :param address: The address
        :type address: ``int``

        :return: Jump command
        :rtype: ``MacroCommand4``
        """
        numeral_sector_id = Numeral(sector_id, byteCount=2)
        numeral_address = Numeral(address, byteCount=2)
        return MacroCommand4(op_code=cls.Opcode.JUMP, p1=numeral_sector_id[0], p2=numeral_sector_id[1],
                             p3=numeral_address[0], p4=numeral_address[1])
    # end def create_jump

    @classmethod
    def create_xy_movement(cls, x_pos, y_pos):
        """
        Create a "xy movement" macro command

        :param x_pos: The x position
        :type x_pos: ``int``
        :param y_pos: The y position
        :type y_pos: ``int``

        :return: XY Movement command
        :rtype: ``MacroCommand4``
        """
        numeral_x_pos = Numeral(x_pos, byteCount=2)
        numeral_y_pos = Numeral(y_pos, byteCount=2)
        return MacroCommand4(op_code=cls.Opcode.XY, p1=numeral_x_pos[0], p2=numeral_x_pos[1],
                             p3=numeral_y_pos[0], p4=numeral_y_pos[1])
    # end def create_xy_movement

    @classmethod
    def get_data_class(cls, op_code):
        """
        Get the corresponding data class by opcode

        :param op_code: Macro opcode
        :type op_code: ``Opcode | int``

        :return: Macro command class and parameter count
        :rtype: ``tuple[MacroCommand0 | MacroCommand1 | MacroCommand2 | MacroCommand4, int]``

        :raise ``ValueError``: If the opcode is unknown
        """
        command_type = op_code & 0xF0
        if command_type == 0x00 or op_code in [ProfileMacro.Opcode.MACRO_END,
                                               ProfileMacro.Opcode.WAIT_FOR_RELEASE,
                                               ProfileMacro.Opcode.REPEAT_WHILE_PRESSED,
                                               ProfileMacro.Opcode.REPEAT_UNTIL_CANCEL]:
            return MacroCommand0(op_code=op_code), 0
        elif command_type == 0x20:
            return MacroCommand1(op_code=op_code), 1
        elif command_type == 0x40:
            return MacroCommand2(op_code=op_code), 2
        elif command_type == 0x60:
            return MacroCommand4(op_code=op_code), 4
        else:
            raise ValueError(f'Unknown opcode: {op_code}')
        # end if
    # end def get_data_class
# end class ProfileMacro


class PresetMacroEntry:
    """
    Tool class for Macro entries fixed data set configuration
    """

    def __init__(self, commands):
        """
        :param commands:
        :type commands: ``list[WaitForReleaseCommand | RepeatWhilePressedCommand | RepeatUntilCancelCommand |
                          MacroEndCommand | NoOperationCommand | WaitForXmsCommand | JumpCommand | StandardKeyCommand |
                          MouseButtonCommand | ConsumerKeyCommand | XYCommand | RollerCommand | AcPanCommand]``

        :raise ``AssertionError``: If the last command is not related to the macro end commands
        """
        assert type(commands[-1]) in [WaitForReleaseCommand, RepeatWhilePressedCommand,
                                      RepeatUntilCancelCommand, MacroEndCommand, JumpCommand]
        self.commands = commands
    # end def __int__

    def __str__(self):
        return f'<PresetMacroEntry> commands: {self.commands}'
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__
# end def PresetMacroEntry


class WaitForReleaseCommand:
    """
    Macro entries fixed data WaitForRelease command class definition
    """
    TYPE = ProfileMacro.Opcode.WAIT_FOR_RELEASE
    COMMAND_LEN = 1

    def __str__(self):
        return 'WaitForReleaseCommand()'
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__

    def __len__(self):
        return self.COMMAND_LEN
    # end def __len__
# end class WaitForReleaseCommand


class RepeatWhilePressedCommand:
    """
    Macro entries fixed data RepeatWhilePressed command class definition
    """
    TYPE = ProfileMacro.Opcode.REPEAT_WHILE_PRESSED
    COMMAND_LEN = 1

    def __str__(self):
        return 'RepeatWhilePressedCommand()'
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__

    def __len__(self):
        return self.COMMAND_LEN
    # end def __len__
# end class RepeatWhilePressedCommand


class RepeatUntilCancelCommand:
    """
    Macro entries fixed data RepeatUntilCancel command class definition
    """
    TYPE = ProfileMacro.Opcode.REPEAT_UNTIL_CANCEL
    COMMAND_LEN = 1

    def __str__(self):
        return 'RepeatUntilCancelCommand()'
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__

    def __len__(self):
        return self.COMMAND_LEN
    # end def __len__
# end class RepeatUntilCancelCommand


class MacroEndCommand:
    """
    Macro entries fixed data MacroEndCommand command class definition
    """
    TYPE = ProfileMacro.Opcode.MACRO_END
    COMMAND_LEN = 1

    def __str__(self):
        return 'MacroEndCommand()'
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__

    def __len__(self):
        return self.COMMAND_LEN
    # end def __len__
# end class MacroEndCommand


class NoOperationCommand:
    """
    Macro entries fixed data NoOperationCommand command class definition
    """
    TYPE = ProfileMacro.Opcode.NO_OPERATION
    COMMAND_LEN = 1

    def __str__(self):
        return f'NoOperationCommand()'
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__

    def __len__(self):
        return self.COMMAND_LEN
    # end def __len__
# end class NoOperationCommand


class WaitForXmsCommand:
    """
    Macro entries fixed data WaitForXms command class definition
    """
    TYPE = ProfileMacro.Opcode.WAIT_FOR_X_MS
    G_HUB_DEFAULT_DELAY = 25  # unit: ms
    COMMAND_LEN = 3

    def __init__(self, ms=G_HUB_DEFAULT_DELAY):
        """
        :param ms: Time in milli-second - OPTIONAL
        :type ms: ``int``
        """
        self.ms = ms
    # end def __init__

    def __str__(self):
        return f'WaitForXmsCommand(delay={self.ms} ms)'
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__

    def __len__(self):
        return self.COMMAND_LEN
    # end def __len__
# end class WaitForXmsCommand


class JumpCommand:
    """
    Macro entries fixed data Jump command class definition
    """
    TYPE = ProfileMacro.Opcode.JUMP
    COMMAND_LEN = 5

    def __init__(self, sector_id, address):
        """
        :param sector_id: The sector id
        :type sector_id: ``int``
        :param address: The address
        :type address: ``int``
        """
        self.sector_id = sector_id
        self.address = address
    # end def __init__

    def __str__(self):
        return f'JumpCommand(sector_id={self.sector_id}, address={self.address})'
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__

    def __len__(self):
        return self.COMMAND_LEN
    # end def __len__
# end class JumpCommand


@unique
class KeyAction(IntEnum):
    """
    Key action definition class
    """
    KEYSTROKE = 1
    PRESS = 2
    RELEASE = 3
# end class Action


class StandardKeyCommand:
    """
    Macro entries fixed data StandardKey command class definition
    """
    TYPE = ProfileMacro.Opcode.KEY_DOWN
    COMMAND_LEN = 3

    def __init__(self, key_id, action=KeyAction.KEYSTROKE):
        """
        :param key_id: The standard key id
        :type key_id: ``KEY_ID | RemappedKey.RandomKey``
        :param action: The key action - OPTIONAL
        :type action: ``KeyAction``
        """
        self.key_id = key_id
        self.action = action
    # end def __init__

    def __str__(self):
        return f'StandardKeyCommand(key_id={self.key_id!s}, action={self.action!s})'
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__

    def __len__(self):
        return self.COMMAND_LEN * 2 if self.action == KeyAction.KEYSTROKE else self.COMMAND_LEN
    # end def __len__
# end class StandardKeyCommand


class MouseButtonCommand:
    """
    Macro entries fixed data MouseButton command class definition
    """
    TYPE = ProfileMacro.Opcode.BUTTON_DOWN
    COMMAND_LEN = 3

    def __init__(self, key_id, action=KeyAction.KEYSTROKE):
        """
        :param key_id: The mouse button key id
        :type key_id: ``KEY_ID``
        :param action: The key action - OPTIONAL
        :type action: ``KeyAction``
        """
        self.key_id = key_id
        self.action = action
    # end def __init__

    def __str__(self):
        return f'MouseButtonCommand(key_id={self.key_id!s}, action={self.action!s})'
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__

    def __len__(self):
        return self.COMMAND_LEN * 2 if self.action == KeyAction.KEYSTROKE else self.COMMAND_LEN
    # end def __len__
# end class MouseButtonCommand


class ConsumerKeyCommand:
    """
    Macro entries fixed data ConsumerKey command class definition
    """
    TYPE = ProfileMacro.Opcode.CONS_DOWN
    COMMAND_LEN = 3

    def __init__(self, key_id, action=KeyAction.KEYSTROKE, os_variant=OS.WINDOWS):
        """
        :param key_id: The consumer key id
        :type key_id: ``KEY_ID``
        :param action: The key action - OPTIONAL
        :type action: ``KeyAction``
        :param os_variant: The OS variant - OPTIONAL
        :type os_variant: ``OS``
        """
        self.key_id = key_id
        self.action = action
        self.os_variant = os_variant
    # end def __init__

    def __str__(self):
        return f'ConsumerKeyCommand(key_id={self.key_id!s}, action={self.action!s}, os_variant={self.os_variant})'
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__

    def __len__(self):
        return self.COMMAND_LEN * 2 if self.action == KeyAction.KEYSTROKE else self.COMMAND_LEN
    # end def __len__
# end class ConsumerKeyCommand


class XYCommand:
    """
    Macro entries fixed data XY command class definition
    """
    TYPE = ProfileMacro.Opcode.XY
    COMMAND_LEN = 5

    def __init__(self, x, y):
        """
        :param x: The x position
        :type x: ``int``
        :param y: The y position
        :type y: ``int``
        """
        self.x = x
        self.y = y
    # end def __init__

    def __str__(self):
        return f'XYCommand(x={self.x}, y={self.y})'
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__

    def __len__(self):
        return self.COMMAND_LEN
    # end def __len__
# end class XYCommand


class RollerCommand:
    """
    Macro entries fixed data Roller command class definition
    """
    TYPE = ProfileMacro.Opcode.ROLLER
    COMMAND_LEN = 2

    def __init__(self, wheel):
        """
        :param wheel: The movement of vertical scroll
        :type wheel: ``int``
        """
        self.wheel = wheel
    # end def __init__

    def __str__(self):
        return f'RollerCommand(wheel={self.wheel})'
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__

    def __len__(self):
        return self.COMMAND_LEN
    # end def __len__
# end class RollerCommand


class AcPanCommand:
    """
    Macro entries fixed data AcPan command class definition
    """
    TYPE = ProfileMacro.Opcode.AC_PAN
    COMMAND_LEN = 2

    def __init__(self, ac_pan):
        """
        :param ac_pan: The movement of horizontal scroll
        :type ac_pan: ``int``
        """
        self.ac_pan = ac_pan
    # end def __init__

    def __str__(self):
        return f'AcPanCommand(ac_pan={self.ac_pan})'
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__

    def __len__(self):
        return self.COMMAND_LEN
    # end def __len__
# end class AcPanCommand


# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
