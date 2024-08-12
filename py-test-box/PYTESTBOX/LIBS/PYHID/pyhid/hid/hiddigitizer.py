#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hid.hiddigitizer
:brief: HID digitizer report format definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/02/21
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import TimestampedBitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pylibrary.tools.hexlist import HexList


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class HidFinger(TimestampedBitFieldContainerMixin):
    """
    Define the common format of an HID Finger block.

    Format:

    ==================  =========
    Name                Bit count
    ==================  =========
    Finger Contact id           6
    Finger Tip Switch           1
    Finger Touch Valid          1
    Finger TipPressure          8
    Finger X                   12
    Finger Y                   12
    ==================  =========
    """
    BITFIELD_LENGTH = 5  # Byte

    class FID:
        """
        Field Identifiers
        """
        FINGER_CONTACT_ID = 0xFF
        FINGER_TIP_SWITCH = 0xFE
        FINGER_TOUCH_VALID = 0xFD
        FINGER_TIP_PRESSURE = 0xFC
        FINGER_X = 0xFB
        FINGER_Y = 0xFA
    # end class FID

    class LEN:
        """
        Field Lengths in bits
        """
        FINGER_CONTACT_ID = 0x06
        FINGER_TIP_SWITCH = 0x01
        FINGER_TOUCH_VALID = 0x01
        FINGER_TIP_PRESSURE = 0x08
        FINGER_X = 0x0C
        FINGER_Y = 0x0C
    # end class LEN

    class DEFAULT:
        """
        Fields Default values
        """
        FINGER_CONTACT_ID = 0
        FINGER_TIP_SWITCH = 0
        FINGER_TOUCH_VALID = 0
        FINGER_TIP_PRESSURE = 0x00
        FINGER_X = 0x000
        FINGER_Y = 0x000
    # end class DEFAULT

    FIELDS = (BitField(fid=FID.FINGER_CONTACT_ID,
                       length=LEN.FINGER_CONTACT_ID,
                       title='Finger Contact Identifier',
                       name='finger_contact_id',
                       checks=(CheckInt(0, pow(2, LEN.FINGER_CONTACT_ID) - 1),),
                       default_value=DEFAULT.FINGER_CONTACT_ID),
              BitField(fid=FID.FINGER_TIP_SWITCH,
                       length=LEN.FINGER_TIP_SWITCH,
                       title='Finger Tip Switch ',
                       name='finger_tip_switch ',
                       checks=(CheckInt(0, pow(2, LEN.FINGER_TIP_SWITCH) - 1),),
                       default_value=DEFAULT.FINGER_TIP_SWITCH),
              BitField(fid=FID.FINGER_TOUCH_VALID,
                       length=LEN.FINGER_TOUCH_VALID,
                       title='Finger Touch Valid',
                       name='finger_touch_valid',
                       checks=(CheckInt(0, pow(2, LEN.FINGER_TOUCH_VALID) - 1),),
                       default_value=DEFAULT.FINGER_TOUCH_VALID),
              BitField(fid=FID.FINGER_TIP_PRESSURE,
                       length=LEN.FINGER_TIP_PRESSURE,
                       title='Finger Tip Pressure',
                       name='finger_tip_pressure',
                       checks=(CheckHexList(LEN.FINGER_TIP_PRESSURE // 8), CheckByte(),),
                       default_value=DEFAULT.FINGER_TIP_PRESSURE),
              BitField(fid=FID.FINGER_X,
                       length=LEN.FINGER_X,
                       title='Finger X',
                       name='finger_x',
                       checks=(CheckInt(0, pow(2, LEN.FINGER_X) - 1),),
                       default_value=DEFAULT.FINGER_X),
              BitField(fid=FID.FINGER_Y,
                       length=LEN.FINGER_Y,
                       title='Finger Y',
                       name='finger_y',
                       checks=(CheckInt(0, pow(2, LEN.FINGER_Y) - 1),),
                       default_value=DEFAULT.FINGER_Y),
              )
# end class HidFinger


class HidDigitizer(TimestampedBitFieldContainerMixin):
    """
    Define the common format of an HID Digitizer report.

    Format:

    ==================  =========
    Name                Bit count
    ==================  =========
    Finger1                    40
    Finger2                    40
    Finger3                    40
    Finger4                    40
    Finger5                    40
    Left Button                 1
    Contact Count               7
    Scan Time                  16
    ==================  =========
    """
    MSG_TYPE = 1  # RESPONSE
    # 28 Bytes
    BITFIELD_LENGTH = (5 * HidFinger.BITFIELD_LENGTH) + 3

    class FID:
        """
        Field Identifiers
        """
        FINGER_1 = 0xFF
        FINGER_2 = 0xFE
        FINGER_3 = 0xFD
        FINGER_4 = 0xFC
        FINGER_5 = 0xFB
        CONTACT_COUNT = 0xFA
        LEFT_BUTTON = 0xF9
        SCAN_TIME = 0xF8
    # end class FID

    class LEN:
        """
        Field Lengths in bits
        """
        FINGER = HidFinger.BITFIELD_LENGTH * 8
        CONTACT_COUNT = 0x07
        LEFT_BUTTON = 0x01
        SCAN_TIME = 0x10
    # end class LEN

    class DEFAULT:
        """
        Fields Default values
        """
        FINGER = HexList('00'*HidFinger.BITFIELD_LENGTH)
        CONTACT_COUNT = 0
        LEFT_BUTTON = 0
        SCAN_TIME = HexList('0000')
    # end class DEFAULT

    FIELDS = (BitField(fid=FID.FINGER_1,
                       length=LEN.FINGER,
                       title='Finger 1',
                       name='finger_1',
                       checks=(CheckHexList(LEN.FINGER // 8),),
                       default_value=DEFAULT.FINGER),
              BitField(fid=FID.FINGER_2,
                       length=LEN.FINGER,
                       title='Finger 2',
                       name='finger_2',
                       checks=(CheckHexList(LEN.FINGER // 8),),
                       default_value=DEFAULT.FINGER),
              BitField(fid=FID.FINGER_3,
                       length=LEN.FINGER,
                       title='Finger 3',
                       name='finger_3',
                       checks=(CheckHexList(LEN.FINGER // 8),),
                       default_value=DEFAULT.FINGER),
              BitField(fid=FID.FINGER_4,
                       length=LEN.FINGER,
                       title='Finger 4',
                       name='finger_4',
                       checks=(CheckHexList(LEN.FINGER // 8),),
                       default_value=DEFAULT.FINGER),
              BitField(fid=FID.FINGER_5,
                       length=LEN.FINGER,
                       title='Finger 5',
                       name='finger_5',
                       checks=(CheckHexList(LEN.FINGER // 8),),
                       default_value=DEFAULT.FINGER),
              BitField(fid=FID.CONTACT_COUNT,
                       length=LEN.CONTACT_COUNT,
                       title='Contact Count',
                       name='contact_count',
                       checks=(CheckInt(0, pow(2, LEN.CONTACT_COUNT) - 1),),
                       default_value=DEFAULT.CONTACT_COUNT),
              BitField(fid=FID.LEFT_BUTTON,
                       length=LEN.LEFT_BUTTON,
                       title='Left Button',
                       name='left_button',
                       checks=(CheckInt(0, pow(2, LEN.LEFT_BUTTON) - 1),),
                       default_value=DEFAULT.LEFT_BUTTON),
              BitField(fid=FID.SCAN_TIME,
                       length=LEN.SCAN_TIME,
                       title='Scan Time',
                       name='scan_time',
                       checks=(CheckHexList(LEN.SCAN_TIME // 8),),
                       default_value=DEFAULT.SCAN_TIME),
              )

    def __init__(self, *args, **kwargs):
        """
        :param args: Positional arguments.
        :type args: ``tuple``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        super().__init__(*args, **kwargs)
        self.finger_1 = HidFinger()
        self.finger_2 = HidFinger()
        self.finger_3 = HidFinger()
        self.finger_4 = HidFinger()
        self.finger_5 = HidFinger()
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        # See ``TimestampedBitFieldContainerMixin.fromHexList``
        mixin = super().fromHexList(*args, **kwargs)
        mixin.finger_1 = HidFinger.fromHexList(mixin.finger_1)
        mixin.finger_2 = HidFinger.fromHexList(mixin.finger_2)
        mixin.finger_3 = HidFinger.fromHexList(mixin.finger_3)
        mixin.finger_4 = HidFinger.fromHexList(mixin.finger_4)
        mixin.finger_5 = HidFinger.fromHexList(mixin.finger_5)
        return mixin
    # end def fromHexList
# end class HidDigitizer

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
