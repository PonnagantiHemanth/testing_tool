#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.setltkkey
    :brief: HID++ 1.0 Set LTK Key registers definition
    :author: Martin Cryonnet
    :date: 2020/05/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel
from pyhid.hidpp.hidpp1.registers.setkey import SetKeyRequest, SetKeyResponse


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SetLTKKeyModel(BaseRegisterModel):
    """
    Register Set LTK Key model
    """
    @classmethod
    def _get_data_model(cls):
        """
        Get model

        :return: Register model
        :rtype: ``dict``
        """
        return {
            Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER: {
                "request": SetLTKKeyRequest,
                "response": SetLTKKeyResponse
            },
        }
    # end def _get_data_model
# end class SetLTKKeyModel


class SetLTKKeyRequest(SetKeyRequest):
    """
    Write LTK Key request
    """
    def __init__(self, key_value):
        """
        Constructor
        """
        super().__init__(address=Hidpp1Data.Hidpp1RegisterAddress.SET_LTK_KEY, key_value=key_value)
        # end if
    # end def __init__
# end class SetLTKKeyRequest


class SetLTKKeyResponse(SetKeyResponse):
    """
    Write LTK Key response
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(address=Hidpp1Data.Hidpp1RegisterAddress.SET_LTK_KEY)
    # end def __init__
# end class SetLTKKeyResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
