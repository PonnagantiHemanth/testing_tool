#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pylibrary.mcu.kbdmasktablechunk
:brief: Keyboard mask table NVS chunk definition
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/03/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckHexList
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KbdColumnMask(BitFieldContainerMixin):
    """
    Define the column mask unit in the NVS_KBD_MASK_TABLE_ID chunk
    """

    class LEN:
        """
        Field Lengths in bits
        """
        PORT_ROW_MASK = 0x20
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        PORT_ROW_MASK = 0xFF
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.PORT_ROW_MASK,
            length=LEN.PORT_ROW_MASK,
            title='Port Row Mask',
            name='port_row_mask',
            checks=(CheckHexList(LEN.PORT_ROW_MASK // 8), ), ),
    )
# end class KbdColumnMask


class KbdMaskTableChunk:
    """
    Define the format of the NVS_KBD_MASK_TABLE_ID chunk
    """

    BYTES_PER_MASK = 4

    def __init__(self, col_masks):
        """
        :param col_masks: The column mask list
        :type col_masks: ``list[KbdColumnMask]``
        """
        self.col_masks = col_masks
    # end def __init__

    @classmethod
    def fromHexList(cls, data):
        """
        Initialize ``KbdMaskTableChunk`` from the raw hex list of NVS_KBD_MASK_TABLE_ID chunk

        :param data: The hex list of NVS_KBD_MASK_TABLE_ID chunk
        :type data: ``HexList``

        :return: The ``KbdMaskTableChunk`` object
        :rtype: ``KbdMaskTableChunk``
        """
        col_masks = []
        start_pos = 0
        data_length = len(data)
        while start_pos * cls.BYTES_PER_MASK < data_length:
            col_data = data[start_pos * cls.BYTES_PER_MASK: (start_pos + 1) * cls.BYTES_PER_MASK]
            col_masks.append(KbdColumnMask.fromHexList(col_data))
            start_pos += 1
        # end while
        return KbdMaskTableChunk(col_masks=col_masks)
    # end def fromHexList

    def __hexlist__(self):
        """
        Convert ``KbdMaskTableChunk`` to its ``HexList`` representation

        :return: KbdMaskTableChunk data in ``HexList``
        :rtype: ``HexList``
        """
        kbd_mask_table = HexList()
        for col_mask in self.col_masks:
            kbd_mask_table += HexList(col_mask)
        # end for
        return kbd_mask_table
    # end def __hexlist__
# end class KbdMaskTableChunk
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
