#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hid.hidcallstatemanagementcontrol
:brief: HID call state management control response interface definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/04/25
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import TimestampedBitFieldContainerMixin
from pyhid.field import CheckInt
from pyhid.hidpp.hidppmessage import TYPE


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class HidCallStateManagementControl(TimestampedBitFieldContainerMixin):
    """
    Define the USB HID Call State Management Control Page report.

    Format:
    ================   =========
    Name               Bit count
    ================   =========
    Call Mute Toggle     1
    Reserved            15
    ================   =========
    """
    MSG_TYPE = TYPE.RESPONSE
    BITFIELD_LENGTH = 1  # Byte

    class FID:
        """
        Field Identifiers
        """
        CALL_MUTE_TOGGLE = 0xFF
        RESERVED = CALL_MUTE_TOGGLE - 1
    # end class FID

    class LEN:
        """
        Field Lengths in bits
        """
        CALL_MUTE_TOGGLE = 1
        RESERVED = 15
    # end class LEN

    class DEFAULT:
        """
        Fields Default values
        """
        RELEASED = 0
    # end class DEFAULT

    FIELDS = (BitField(fid=FID.CALL_MUTE_TOGGLE,
                       length=LEN.CALL_MUTE_TOGGLE,
                       title='CallMuteToggle',
                       name='call_mute_toggle',
                       checks=(CheckInt(0, pow(2, LEN.CALL_MUTE_TOGGLE) - 1),),
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
# end class HidCallStateManagementControl

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
