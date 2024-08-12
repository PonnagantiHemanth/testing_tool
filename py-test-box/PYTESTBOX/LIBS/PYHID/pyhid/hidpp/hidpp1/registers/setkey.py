#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.setkey
    :brief: HID++ 1.0 Set Key base class definition
    :author: Martin Cryonnet
    :date: 2020/05/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.field import CheckInt
from pyhid.field import CheckHexList
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.setgetregister import SetLongRegisterResponse
from pyhid.hidpp.hidpp1.setgetregister import SetLongRegister


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SetKeyRequest(SetLongRegister):
    """
    Write Key request
    """
    class FID(SetLongRegister.FID):
        """
        Fields Identifiers
        """
        KEY_VALUE = SetLongRegister.FID.ADDRESS - 1
    # end class FID

    class LEN(SetLongRegister.LEN):
        """
        Fields Lengths in bits
        """
        KEY_VALUE = 0x80
    # end class LEN

    FIELDS = SetLongRegister.FIELDS + (
        BitField(FID.KEY_VALUE,
                 LEN.KEY_VALUE,
                 title='KeyValue',
                 name='key_value',
                 checks=(CheckHexList(LEN.KEY_VALUE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.KEY_VALUE) - 1),)),
    )

    def __init__(self, address, key_value):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER, address=address)
        self.key_value = key_value
        # end if
    # end def __init__
# end class SetKeyRequest


class SetKeyResponse(SetLongRegisterResponse):
    """
    Write Key response
    """
    def __init__(self, address):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=address)
    # end def __init__
# end class SetKeyResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
