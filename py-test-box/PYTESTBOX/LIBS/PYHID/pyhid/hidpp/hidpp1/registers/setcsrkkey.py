#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.setcsrkkey
    :brief: HID++ 1.0 Set CSRK Key registers definition
    :author: Martin Cryonnet
    :date: 2020/05/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.registers.setkey import SetKeyRequest, SetKeyResponse
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SetCSRKKeyCentralModel(BaseRegisterModel):
    """
    Register Set CSRK Key Central model
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
                "request": SetCSRKKeyCentralRequest,
                "response": SetCSRKKeyCentralResponse
            },
        }
    # end def _get_data_model
# end class SetIRKKeyCentralModel


class SetCSRKKeyCentralRequest(SetKeyRequest):
    """
    Write CSRK Key Central request
    """
    def __init__(self, key_value):
        """
        Constructor
        """
        super().__init__(address=Hidpp1Data.Hidpp1RegisterAddress.SET_CSRK_KEY_CENTRAL, key_value=key_value)
        self.key_value = key_value
        # end if
    # end def __init__
# end class SetCSRKKeyCentralRequest


class SetCSRKKeyCentralResponse(SetKeyResponse):
    """
    Write CSRK Key Central response
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(address=Hidpp1Data.Hidpp1RegisterAddress.SET_CSRK_KEY_CENTRAL)
    # end def __init__
# end class SetCSRKKeyCentralResponse


class SetCSRKKeyPeripheralModel(BaseRegisterModel):
    """
    Register Set CSRK Key Peripheral model
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
                "request": SetCSRKKeyPeripheralRequest,
                "response": SetCSRKKeyPeripheralResponse
            },
        }
    # end def _get_data_model
# end class SetCSRKKeyPeripheralModel


class SetCSRKKeyPeripheralRequest(SetKeyRequest):
    """
    Write CSRK Key Peripheral request
    """
    def __init__(self, key_value):
        """
        Constructor
        """
        super().__init__(address=Hidpp1Data.Hidpp1RegisterAddress.SET_CSRK_KEY_PERIPHERAL, key_value=key_value)
        self.key_value = key_value
        # end if
    # end def __init__
# end class SetCSRKKeyPeripheralRequest


class SetCSRKKeyPeripheralResponse(SetKeyResponse):
    """
    Write CSRK Key Peripheral response
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(address=Hidpp1Data.Hidpp1RegisterAddress.SET_CSRK_KEY_PERIPHERAL)
    # end def __init__
# end class SetCSRKKeyPeripheralResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
