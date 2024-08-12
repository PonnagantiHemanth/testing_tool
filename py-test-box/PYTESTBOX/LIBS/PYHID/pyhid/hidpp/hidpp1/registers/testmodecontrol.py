#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.testmodecontrol
    :brief: HID++ 1.0 Receiver Test Mode Control registers definition
    :author: Martin Cryonnet
    :date: 2020/05/08
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import IntEnum
from pyhid.bitfield import BitField
from pyhid.field import CheckInt
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel, SetRegister
from pyhid.hidpp.hidpp1.setgetregister import GetRegister, GetRegisterRequest
from pyhid.hidpp.hidpp1.setgetregister import SetRegisterResponse


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class TestModeControl:
    """
    Command specific constants
    """
    class TestModeEnable(IntEnum):
        """
        Test Mode bit 0 values
        """
        DISABLE_TEST_MODE = 0
        ENABLE_MANUFACTURING_TEST_MODE = 1
    # end class TestModeEnable
# end class TestModeControl


class TestModeControlModel(BaseRegisterModel):
    """
    Register Test Mode Control model
    """
    @classmethod
    def _get_data_model(cls):
        """
        Get model

        :return: Register model
        :rtype: ``dict``
        """
        return {
            Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER: {
                "request": GetTestModeControlRequest,
                "response": GetTestModeControlResponse
            },
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER: {
                "request": SetTestModeControlRequest,
                "response": SetTestModeControlResponse
            },
        }
    # end def _get_data_model
# end class TestModeControlModel


class GetTestModeControlRequest(GetRegisterRequest):
    """
    Read Test Mode Control request
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.TEST_MODE_CONTROL)
    # end def __init__
# end class GetTestModeControlRequest


class GetTestModeControlResponse(GetRegister):
    """
    Read Test Mode Control response
    """
    class FID(GetRegister.FID):
        """
        Field Identifiers
        """
        TEST_MODE_RESERVED = GetRegister.FID.ADDRESS - 1
        TEST_MODE_ENABLE = TEST_MODE_RESERVED - 1
        PADDING = TEST_MODE_ENABLE - 1
    # end class FID

    class LEN(GetRegister.LEN):
        """
        Field Lengths in bits
        """
        TEST_MODE_RESERVED = 0x07
        TEST_MODE_ENABLE = 0x01
        PADDING = 0x10
    # end class LEN

    FIELDS = GetRegister.FIELDS + (
        BitField(FID.TEST_MODE_RESERVED,
                 LEN.TEST_MODE_RESERVED,
                 title='TestModeReserved',
                 name='test_mode_reserved',
                 checks=(CheckHexList(LEN.TEST_MODE_RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TEST_MODE_RESERVED) - 1),)),
        BitField(FID.TEST_MODE_ENABLE,
                 LEN.TEST_MODE_ENABLE,
                 title='TestModeEnable',
                 name='test_mode_enable',
                 checks=(CheckHexList(LEN.TEST_MODE_ENABLE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TEST_MODE_ENABLE) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=GetRegister.DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self, test_mode_enable):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.TEST_MODE_CONTROL)
        self.test_mode_enable = test_mode_enable
    # end def __init__
# end class GetTestModeControlResponse


class SetTestModeControlRequest(SetRegister):
    """
    Write Test Mode Control request
    """

    class FID(SetRegister.FID):
        """
        Fields Identifiers
        """
        TEST_MODE_RESERVED = SetRegister.FID.ADDRESS - 1
        TEST_MODE_ENABLE = TEST_MODE_RESERVED - 1
        PADDING = TEST_MODE_ENABLE - 1
    # end class FID

    class LEN(SetRegister.LEN):
        """
        Fields Lengths in bits
        """
        TEST_MODE_RESERVED = 0x07
        TEST_MODE_ENABLE = 0x01
        PADDING = 0x10
    # end class LEN

    class DEFAULT(SetRegister.DEFAULT):
        """
        Fields default values
        """
        TEST_MODE_ENABLE = TestModeControl.TestModeEnable.DISABLE_TEST_MODE
        TEST_MODE_RESERVED = 0x00
    # end class DEFAULT

    FIELDS = SetRegister.FIELDS + (
        BitField(FID.TEST_MODE_RESERVED,
                 LEN.TEST_MODE_RESERVED,
                 title='TestModeReserved',
                 name='test_mode_reserved',
                 default_value=DEFAULT.TEST_MODE_RESERVED,
                 checks=(CheckHexList(LEN.TEST_MODE_RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TEST_MODE_RESERVED) - 1),)),
        BitField(FID.TEST_MODE_ENABLE,
                 LEN.TEST_MODE_ENABLE,
                 title='TestModeEnable',
                 name='test_mode_enable',
                 default_value=DEFAULT.TEST_MODE_ENABLE,
                 checks=(CheckHexList(LEN.TEST_MODE_ENABLE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TEST_MODE_ENABLE) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=SetRegister.DEFAULT.PADDING),
    )

    def __init__(self, test_mode_enable):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.TEST_MODE_CONTROL)
        self.test_mode_enable = test_mode_enable
    # end def __init__
# end class SetTestModeControlRequest


class SetTestModeControlResponse(SetRegisterResponse):
    """
    Write Test Mode Control response
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.TEST_MODE_CONTROL)
    # end def __init__
# end class SetTestModeControlResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
