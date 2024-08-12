#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.mcu.factorychunks
:brief: TDE NVS chunk definition
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date:   2020/08/05
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
class TdeMfgAccessIdChunk(BitFieldContainerMixin):
    """
    This class defines the format of the NVS_TDE_MFG_ACCESS_ID chunk
    """

    class LEN(object):
        """
        Field Lengths in bits.

        Use the max and min value from TdeMaxSize in settings.ini.

        ===================================
        Product     Bytes       Bits
        ===================================
        Catania     80 (0x50)   640 (0x280)
        Harpy       64 (0x40)   512 (0x200)
        Hyjal Hero  48 (0x30)   384 (0x180)
        Footloose   32 (0x20)   256 (0x100)
        Senna Rim   16 (0x10)   128 (0x080)
        ===================================
        """
        TDE_DATA_MAX = 0x280
        TDE_DATA_MIN = 0x80
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
# end class TdeMfgAccessIdChunk

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
