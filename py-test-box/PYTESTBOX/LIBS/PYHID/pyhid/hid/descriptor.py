#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hid.descriptor
:brief: report descriptor definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/01/26
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import TimestampedBitFieldContainerMixin
from pyhid.field import CheckHexList
from pylibrary.tools.hexlist import HexList


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ReportDescriptor(TimestampedBitFieldContainerMixin):
    """
    Define the 3 first fields of a descriptor starting with a 2 bytes lon usage page field.

    Format:
    ===========  =========
    Name         Bit count
    ===========  =========
    USAGE_PAGE          16
    USAGE               16
    COLLECTION          16
    ===========  =========
    """
    MSG_TYPE = 1  # RESPONSE
    BITFIELD_LENGTH = 6  # Bytes

    class FID:
        """
        FIELDS identifier
        """
        USAGE_PAGE = 0xFF
        USAGE = USAGE_PAGE - 1
        APP_COLLECTION = USAGE - 1
    # end class FID

    class LEN:
        """
        FIELDS length
        """
        EMPTY = 0x00
        USAGE_PAGE = 0x10
        LONG_USAGE_PAGE = 0x18
        USAGE = 0x10
        LONG_USAGE = 0x18
        COLLECTION = 0x10
        REPORT_ID = 0x10
        REPORT_SIZE = 0x10
        REPORT_COUNT = 0x10
        USAGE_MINIMUM = 0x10
        USAGE_MAXIMUM = 0x10
        LOGICAL_MINIMUM = 0x10
        LOGICAL_MAXIMUM = 0x10
        LONG_LOGICAL_MAXIMUM = 0x18
        PHYSICAL_MINIMUM = 0x10
        UNIT = 0x10
        INPUT_DATA = 0x10
        OUTPUT_DATA = 0x10
        OUTPUT_CST = 0x10
        FEATURE = 0x10
        END_COLLECTION = 0x08
        # Push Pop
        PUSH = 0x08
        POP = 0x08
    # end class LEN

    class DEFAULT:
        """
        FIELDS Default values
        """
        # Usage Page
        GENERIC_USAGE_PAGE = HexList("0501")
        KEYBOARD_USAGE_PAGE = HexList("0507")
        LED_USAGE_PAGE = HexList("0508")
        BUTTON_USAGE_PAGE = HexList("0509")
        CONSUMER_USAGE_PAGE = HexList("050C")
        DIGITIZER_USAGE_PAGE = HexList("050D")
        HIDPP_RECEIVER_USAGE_PAGE = HexList("0600FF")
        HIDPP_USAGE_PAGE = HexList("0643FF")
        SDATAWAY_USAGE_PAGE = HexList("0640FF")
        # Usage ID
        CONSUMER_USAGE = HexList("0901")
        MOUSE_USAGE = HexList("0902")
        TOUCHPAD_USAGE = HexList("0905")
        KEYBOARD_USAGE = HexList("0906")
        VLP_NORMAL_IN_OUT_USAGE = HexList("0908")
        VLP_EXTENDED_IN_OUT_USAGE = HexList("0910")
        CALL_STATE_USAGE = HexList("0913")
        FINGER_USAGE = HexList("0922")
        TIP_PRESSURE_USAGE = HexList("0930")
        AXIS_X_USAGE = HexList("0930")
        AXIS_Y_USAGE = HexList("0931")
        WHEEL_USAGE = HexList("0938")
        TIP_SWITCH_USAGE = HexList("0942")
        TOUCH_VALID_USAGE = HexList("0947")
        CONTACT_IDENTIFIER_USAGE = HexList("0951")
        CONTACT_COUNT_USAGE = HexList("0954")
        CONTACT_COUNT_MAXIMUM_USAGE = HexList("0955")
        SCAN_TIME_USAGE = HexList("0956")
        POWER_USAGE = HexList("0980")
        DEVICE_CERTIFICATION_USAGE = HexList("09C5")
        HIDPP7_USAGE = HexList("0A0103")
        VLP_MODE_1A02_USAGE = HexList("0A021A")
        VLP_NORMAL_USAGE = HexList("0A081A")
        VLP_EXTENDED_USAGE = HexList("0A101A")
        # Input / Output / Feature
        INPUT_DATA_ABS = HexList("8100")
        INPUT_DATA = HexList("8102")
        INPUT_CST = HexList("8103")
        INPUT_DATA_REL = HexList("8106")
        INPUT_DATA_ARY = HexList("8160")
        VLP1_DATA_ABS = HexList("820201")
        OUTPUT_DATA_ABS = HexList("9100")
        OUTPUT_CST_ARY = HexList("9101")
        OUTPUT_DATA = HexList("9102")
        OUTPUT_CST = HexList("9103")
        OUTPUT_DATA_VAR = HexList("9122")
        VLP1_OUT_DATA_ABS = HexList("920201")
        FEATURE_DATA = HexList("B102")
        # Collection
        APP_COLLECTION = HexList("A101")
        LOGICAL_COLLECTION = HexList("A102")
        END_COLLECTION = HexList("C0")
        # Report id
        EMPTY_REPORT_ID = HexList()
        KEYBOARD_REPORT_ID = HexList('8501')
        KEYBOARD6_REPORT_ID = KEYBOARD_REPORT_ID
        MOUSE_REPORT_ID = HexList("8502")
        MM_REPORT_ID = HexList("8503")
        CONS_GEN_REPORT_ID = HexList("8503")
        PWR_REPORT_ID = HexList("8504")
        CONS_MIN_REPORT_ID = HexList("8505")
        CONS_MIN_RSV_REPORT_ID = HexList("9507")
        MEDIACENTER_REPORT_ID = HexList("8508")
        TOP_RAW_REPORT_ID = HexList("8509")
        BATTERY_REPORT_ID = HexList("850A")
        CALL_STATE_REPORT_ID = HexList("850B")
        HIDPP7_REPORT_ID = HexList("8510")
        HIDPP20_REPORT_ID = HexList("8511")
        HIDPP64_REPORT_ID = HexList("8512")
        VLP_NORMAL_REPORT_ID = HexList("8513")
        VLP_EXTENDED_REPORT_ID = HexList("8514")
        GAMEPAD_REPORT_ID = HexList("8514")
        MOUSE16_REPORT_ID = HexList("8515")
        KEYBOARD_BITMAP_REPORT_ID = HexList("8518")
        WIN_DIGIT_REPORT_ID = HexList("8528")
        WIN_DEV_CAP_REPORT_ID = HexList("8529")
        WIN_DEV_CER_REPORT_ID = HexList("852A")
        FEATURE_REPORT_ID = HexList("8564")
        # Report Count
        FEATURE_IN_REPORT_COUNT = HexList("960C00")
        FEATURE_OUT_REPORT_COUNT = HexList("96FE0F")
        # Push Pop
        PUSH = HexList("A4")
        POP = HexList("B4")
    # end class DEFAULT

    FIELDS = (BitField(fid=FID.USAGE_PAGE,
                       length=LEN.USAGE_PAGE,
                       title='UsagePage',
                       name='usage_page',
                       checks=(CheckHexList(LEN.USAGE_PAGE // 8),),
                       default_value=DEFAULT.GENERIC_USAGE_PAGE),
              BitField(fid=FID.USAGE,
                       length=LEN.USAGE,
                       title='Usage',
                       name='usage',
                       checks=(CheckHexList(LEN.USAGE // 8),),
                       default_value=DEFAULT.KEYBOARD_USAGE),
              BitField(fid=FID.APP_COLLECTION,
                       length=LEN.COLLECTION,
                       title='Application Collection',
                       name='app_collection',
                       checks=(CheckHexList(LEN.COLLECTION // 8),),
                       default_value=DEFAULT.APP_COLLECTION),
              )
# end class ReportDescriptor


class LongUsagePageReportDescriptor(ReportDescriptor):
    """
    Define the 3 first fields of a descriptor starting with a 3 bytes long usage page field.

    Format:
    ===========  =========
    Name         Bit count
    ===========  =========
    USAGE_PAGE          24
    USAGE               16
    COLLECTION          16
    ===========  =========
    """
    MSG_TYPE = 1  # RESPONSE
    BITFIELD_LENGTH = 7  # Bytes

    FIELDS = (BitField(fid=ReportDescriptor.FID.USAGE_PAGE,
                       length=ReportDescriptor.LEN.LONG_USAGE_PAGE,
                       title='UsagePage',
                       name='usage_page',
                       checks=(CheckHexList(ReportDescriptor.LEN.LONG_USAGE_PAGE // 8),),
                       default_value=ReportDescriptor.DEFAULT.HIDPP_USAGE_PAGE),
              BitField(fid=ReportDescriptor.FID.USAGE,
                       length=ReportDescriptor.LEN.USAGE,
                       title='Usage',
                       name='usage',
                       checks=(CheckHexList(ReportDescriptor.LEN.USAGE // 8),), ),
              BitField(fid=ReportDescriptor.FID.APP_COLLECTION,
                       length=ReportDescriptor.LEN.COLLECTION,
                       title='Application Collection',
                       name='app_collection',
                       checks=(CheckHexList(ReportDescriptor.LEN.COLLECTION // 8),), ),
              )
# end class LongUsagePageReportDescriptor


class LongUsageReportDescriptor(ReportDescriptor):
    """
    Define the 3 first fields of a descriptor starting with a 3 bytes long usage page and 3 bytes long usage fields.

    Format:
    ===========  =========
    Name         Bit count
    ===========  =========
    USAGE_PAGE          24
    USAGE               24
    COLLECTION          16
    ===========  =========
    """
    MSG_TYPE = 1  # RESPONSE
    BITFIELD_LENGTH = 8  # Bytes

    FIELDS = (BitField(fid=ReportDescriptor.FID.USAGE_PAGE,
                       length=ReportDescriptor.LEN.LONG_USAGE_PAGE,
                       title='UsagePage',
                       name='usage_page',
                       checks=(CheckHexList(ReportDescriptor.LEN.LONG_USAGE_PAGE // 8),),
                       default_value=ReportDescriptor.DEFAULT.HIDPP_USAGE_PAGE),
              BitField(fid=ReportDescriptor.FID.USAGE,
                       length=ReportDescriptor.LEN.LONG_USAGE,
                       title='Usage',
                       name='usage',
                       checks=(CheckHexList(ReportDescriptor.LEN.LONG_USAGE // 8),), ),
              BitField(fid=ReportDescriptor.FID.APP_COLLECTION,
                       length=ReportDescriptor.LEN.COLLECTION,
                       title='Application Collection',
                       name='app_collection',
                       checks=(CheckHexList(ReportDescriptor.LEN.COLLECTION // 8),), ),
              )
# end class LongUsageReportDescriptor

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
