#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.mcu.devicefriendlynamechunks
:brief: DeviceFriendlyName NVS chunk definition
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date:   2020/11/09
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckHexList


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DeviceFriendlyNameIdChunk(BitFieldContainerMixin):
    """
    This class defines the format of the NVS_DEVICE_FRIENDLY_NAME_ID chunk
    """

    class LEN(object):
        """
        Field Lengths in bits.

        Use the max and min value from DeviceFriendlyName in settings.ini.
        Max length is 18 bytes if BLE Pro does not need to be supported.
        Max length is 16 if BLE Pro needs to be supported.
        Max length is 14 if BLE Pro & Swift pair need to be supported.

        ==================================
        Size        Bytes       Bits
        ==================================
        Max         18 (0x12)   144 (0x90)
        Min         14 (0x0E)   112 (0x70)
        ==================================
        """
        TDE_DATA_MAX = 0x90
        TDE_DATA_MIN = 0x70
    # end class LEN

    class FID(object):
        """
        Field Identifiers
        """
        DATA = 0xFF
    # end class FID

    FIELDS = (BitField(
            fid=FID.DATA, length=LEN.TDE_DATA_MAX,
            title='Data', name='data',
            checks=(CheckHexList(max_length=(LEN.TDE_DATA_MAX // 8), min_length=(LEN.TDE_DATA_MIN // 8), ),)),)

    def __init__(self, data, **kwargs):
        """
        Constructor
        :param data: data
        :type data: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(**kwargs)
        self.data = data
    # end def __init__
# end class DeviceFriendlyNameIdChunk

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
