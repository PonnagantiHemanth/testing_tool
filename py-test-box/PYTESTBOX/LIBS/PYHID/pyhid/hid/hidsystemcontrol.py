#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hid.hidsystemcontrol
:brief: HID system control response interface definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/07/28
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import TimestampedBitFieldContainerMixin
from pyhid.field import CheckHexList, CheckInt


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class HidSystemControl(TimestampedBitFieldContainerMixin):  # pylint:disable=W0223
    """
    Define the USB HID System Control Page report.

    Format:
    ===========    =========
    Name           Bit count
    ===========    =========
    Power State    2
    Do Not Disturb 1
    Micro Mute     1        // Keyboard only (i.e. not supported by BOLT receiver)
    Reserved       4
    ===========    =========
    """
    MSG_TYPE = 1  # RESPONSE
    BITFIELD_LENGTH = 1  # Byte

    class FID:
        """
        Field Identifiers
        """
        POWER_STATE = 0xFF
        DO_NOT_DISTURB = POWER_STATE - 1
        MICROPHONE_MUTE = DO_NOT_DISTURB - 1
        RESERVED = MICROPHONE_MUTE - 1
    # end class FID

    class LEN:
        """
        Field Lengths in bits
        """
        POWER_STATE = 2
        DO_NOT_DISTURB = 1
        MICROPHONE_MUTE = 1
        RESERVED = 4
    # end class LEN

    class DEFAULT:
        """
        Fields Default values
        """
        RELEASED = 0
    # end class DEFAULT

    class POSITION:
        """
        Define the targeted usage position in the usage array inside the Generic Desktop System Control HID descriptor:
        https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/edit#bookmark=id.7ysta15v66yk
        Extract:
            Usage (System Sleep) - 09 82
            Usage (System Power Down) - 09 81
            Usage (System Wake Up) - 09 83
        """
        SYSTEM_SLEEP = 0x01
        SYSTEM_POWER_DOWN = 0x02
        SYSTEM_WAKE_UP = 0x03
    # end class POSITION

    FIELDS = (BitField(fid=FID.POWER_STATE,
                       length=LEN.POWER_STATE,
                       title='PowerState',
                       name='power_state',
                       checks=(CheckInt(0, pow(2, LEN.POWER_STATE) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.DO_NOT_DISTURB,
                       length=LEN.DO_NOT_DISTURB,
                       title='DoNotDisturb',
                       name='do_not_disturb',
                       aliases=('system_do_not_disturb',),
                       checks=(CheckInt(0, pow(2, LEN.DO_NOT_DISTURB) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.MICROPHONE_MUTE,
                       length=LEN.MICROPHONE_MUTE,
                       title='MicrophoneMute',
                       name='microphone_mute',
                       checks=(CheckInt(0, pow(2, LEN.MICROPHONE_MUTE) - 1),),
                       default_value=DEFAULT.RELEASED),
              BitField(fid=FID.RESERVED,
                       length=LEN.RESERVED,
                       title='Reserved',
                       name='reserved',
                       checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                       default_value=DEFAULT.RELEASED),
              )

    def __init__(self, *args, **kwargs):
        """
        :param args: Positional arguments.
        :type args: ``tuple``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        super().__init__(*args, **kwargs)
    # end def __init__
# end class HidSystemControl

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
