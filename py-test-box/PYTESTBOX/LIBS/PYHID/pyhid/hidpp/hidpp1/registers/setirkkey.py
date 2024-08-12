#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.setirkkey
    :brief: HID++ 1.0 Set IRK Key registers definition
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
class SetIRKKeyCentralModel(BaseRegisterModel):
    """
    Register Set IRK Key Central model
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
                "request": SetIRKKeyCentralRequest,
                "response": SetIRKKeyCentralResponse
            },
        }
    # end def _get_data_model
# end class SetIRKKeyCentralModel


class SetIRKKeyCentralRequest(SetKeyRequest):
    """
    Write IRK Key Central request
    """
    def __init__(self, key_value):
        """
        Constructor
        """
        super().__init__(address=Hidpp1Data.Hidpp1RegisterAddress.SET_IRK_KEY_CENTRAL, key_value=key_value)
        self.key_value = key_value
        # end if
    # end def __init__
# end class SetIRKKeyCentralRequest


class SetIRKKeyCentralResponse(SetKeyResponse):
    """
    Write IRK Key Central response
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(address=Hidpp1Data.Hidpp1RegisterAddress.SET_IRK_KEY_CENTRAL)
    # end def __init__
# end class SetIRKKeyCentralResponse


class SetIRKKeyPeripheralModel(BaseRegisterModel):
    """
    Register Set IRK Key Peripheral model
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
                "request": SetIRKKeyPeripheralRequest,
                "response": SetIRKKeyPeripheralResponse
            },
        }
    # end def _get_data_model
# end class SetIRKKeyPeripheralModel


class SetIRKKeyPeripheralRequest(SetKeyRequest):
    """
    Write IRK Key Peripheral request
    """
    def __init__(self, key_value):
        """
        Constructor
        """
        super().__init__(address=Hidpp1Data.Hidpp1RegisterAddress.SET_IRK_KEY_PERIPHERAL, key_value=key_value)
        self.key_value = key_value
        # end if
    # end def __init__
# end class SetIRKKeyPeripheralRequest


class SetIRKKeyPeripheralResponse(SetKeyResponse):
    """
    Write IRK Key Peripheral response
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(address=Hidpp1Data.Hidpp1RegisterAddress.SET_IRK_KEY_PERIPHERAL)
    # end def __init__
# end class SetIRKKeyPeripheralResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
