#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.features.common.setgetregister
    :brief: HID++ 1.0 Set Register interface definition
    :author: Stanislas Cottard
    :date: 2019/10/31
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidpp1.hidpp1message import Hidpp1Message
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class Hidpp1RegisterModel(object):
    """
    HID++ 1.0 registers types model
    """
    @classmethod
    def _get_data_model(cls):
        """
        Register types model

        :return: Register types model
        :rtype: ``dict``
        """
        return {
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER: {
                "request": SetRegisterRequest,
                "response": SetRegisterResponse
            },
            Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER: {
                "request": GetRegisterRequest,
                "response": GetRegisterResponse
            },
            Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER: {
                "request": SetLongRegisterRequest,
                "response": SetLongRegisterResponse
            },
            Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER: {
                "request": GetLongRegisterRequest,
                "response": GetLongRegisterResponse
            },
            Hidpp1Data.Hidpp1RegisterSubId.SET_VERY_LONG_REGISTER: {
                # "request": SetVeryLongRegisterRequest,
                # "response": SetVeryLongRegisterResponse
            },
            Hidpp1Data.Hidpp1RegisterSubId.GET_VERY_LONG_REGISTER: {
                # "request": GetVeryLongRegisterRequest,
                # "response": GetVeryLongRegisterResponse
            },
            # Hidpp1Data.Hidpp1RegisterSubId.ERROR_MSG: {
            #     "request": None,
            #     "response": ErrorMsg
            # }
        }
    # end def _get_data_model

    @classmethod
    def get_sub_ids(cls):
        return cls._get_data_model().keys()
    # end def get_sub_ids

    @classmethod
    def get_message_cls(cls, sub_id, message_type):
        msg_cls = None
        data_model = cls._get_data_model()
        if sub_id in data_model and message_type in data_model[sub_id]:
            msg_cls = data_model[sub_id][message_type]
        # end if
        return msg_cls
    # end def get_cls

    @classmethod
    def get_available_responses_classes(cls):
        """
        Get available responses classes in model

        :return: Available responses classes
        :rtype: ``dict``
        """
        return tuple(cls.get_available_responses_map().values())
    # end def get_available_responses_classes

    @classmethod
    def get_available_responses_map(cls):
        """
        Get available responses in model mapped with their sub id

        :return: Responses map
        :rtype: ``dict``
        """
        responses_map = {}
        for sub_id, sub_id_map in cls._get_data_model().items():
            if "response" in sub_id_map:
                responses_map[sub_id] = sub_id_map["response"]
            # end if
        # end for
        return responses_map
    # end def get_available_responses_map
# end class RegisterModel


class Register(Hidpp1Message):
    """
    This class defines the format of register

    Registers are accessed using their address.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    ============================  ==========
    """

    class FID(Hidpp1Message.FID):
        """
        Field Identifiers
        """
        ADDRESS = 0xFC
    # end class FID

    class LEN(Hidpp1Message.LEN):
        """
        Field Lengths in bits
        """
        ADDRESS = 0x08
    # end class LEN

    class OFFSET(Hidpp1Message.OFFSET):
        """
        Fields offset in bytes
        """
        ADDRESS = 0x03
    # end class OFFSET

    FIELDS = Hidpp1Message.FIELDS + (
        BitField(FID.ADDRESS,
                 LEN.ADDRESS,
                 title='Address',
                 name='address',
                 checks=(CheckHexList(LEN.ADDRESS // 8), CheckByte(),)),
    )

    def __init__(self, device_index, sub_id, address):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param sub_id: Sub ID
        :type sub_id: ``int`` or ``HexList``
        :param address: The address of the register to set
        :type address: ``int`` or ``HexList``
        """
        super().__init__()
        self.device_index = device_index
        self.sub_id = sub_id
        self.address = address
    # end def __init__
# end class Register


class SetRegister(Register):
    """
    This class defines the format of Set Register header.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    ============================  ==========
    """
    SUB_ID = Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER

    def __init__(self, device_index, address):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param address: The address of the register to set
        :type address: ``int`` or ``HexList``
        """
        super().__init__(device_index, self.SUB_ID, address)
    # end def __init__
# end class SetRegister


class SetRegisterRequest(SetRegister):
    """
    This class defines the format of Set Register request.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    P0                            8
    P1                            8
    P2                            8
    ============================  ==========
    """

    class FID(SetRegister.FID):
        """
        Field Identifiers
        """
        P0 = 0xFB
        P1 = 0xFA
        P2 = 0xF9
    # end class FID

    class LEN(SetRegister.LEN):
        """
        Field Lengths in bits
        """
        P0 = 0x08
        P1 = 0x08
        P2 = 0x08
    # end class LEN

    class OFFSET(SetRegister.OFFSET):
        """
        Fields offset in bytes
        """
        P0 = 0x04
        P1 = 0x05
        P2 = 0x06
    # end class OFFSET

    class DEFAULT(SetRegister.DEFAULT):
        """
        Fields default values
        """
        P0 = 0x00
        P1 = 0x00
        P2 = 0x00
    # end class DEFAULT

    FIELDS = SetRegister.FIELDS + (
        BitField(FID.P0,
                 LEN.P0,
                 title='P0',
                 name='p0',
                 checks=(CheckHexList(LEN.P0 // 8), CheckByte())),
        BitField(FID.P1,
                 LEN.P1,
                 title='P1',
                 name='p1',
                 checks=(CheckHexList(LEN.P1 // 8), CheckByte())),
        BitField(FID.P2,
                 LEN.P2,
                 title='P2',
                 name='p2',
                 checks=(CheckHexList(LEN.P2 // 8), CheckByte())),
    )

    def __init__(self, device_index, address, p0=0, p1=0, p2=0):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param address: The address of the register to set
        :type address: ``int`` or ``HexList``
        :param p0: The value of the first register to set
        :type p0: ``int`` or ``list`` or ``HexList``
        :param p1: The value of the second register to set
        :type p1: ``int`` or ``list`` or ``HexList``
        :param p1: The value of the second register to set
        :type p1: ``int`` or ``list`` or ``HexList``
        """
        super().__init__(device_index, address)

        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
    # end def __init__
# end class SetRegisterRequest


class SetRegisterResponse(SetRegister):
    """
    This class defines the format of Set Register response.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    Padding                       24
    ============================  ==========
    """

    class FID(SetRegister.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFB
    # end class FID

    class LEN(SetRegister.LEN):
        """
        Field Lengths in bits
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = SetRegister.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Hidpp1Message.DEFAULT.PADDING),
    )

    def __init__(self, device_index, address):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param address: The address of the register to set
        :type address: ``int`` or ``HexList``
        """
        super().__init__(device_index, address)
    # end def __init__
# end class SetRegisterResponse


class GetRegister(Register):
    """
    This class defines the format of Get Register header.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    ============================  ==========
    """
    SUB_ID = Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER

    def __init__(self, device_index, address):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param address: The address of the register to set
        :type address: ``int`` or ``HexList``
        """
        super().__init__(device_index, self.SUB_ID, address)
    # end def __init__
# end class GetRegister


class GetRegisterRequest(GetRegister):
    """
    This class defines the format of Get Register request.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    R0                            8
    R1                            8
    R2                            8
    ============================  ==========
    """

    class FID(GetRegister.FID):
        """
        Field Identifiers
        """
        R0 = 0xFB
        R1 = 0xFA
        R2 = 0xF9
    # end class FID

    class LEN(GetRegister.LEN):
        """
        Field Lengths in bits
        """
        R0 = 0x08
        R1 = 0x08
        R2 = 0x08
    # end class LEN

    class OFFSET(GetRegister.OFFSET):
        """
        Fields offset in bytes
        """
        R0 = 0x04
        R1 = 0x05
        R2 = 0x06
    # end class OFFSET

    class DEFAULT(GetRegister.DEFAULT):
        """
        Fields default values
        """
        R0 = 0x00
        R1 = 0x00
        R2 = 0x00
    # end class DEFAULT

    FIELDS = GetRegister.FIELDS + (
        BitField(FID.R0,
                 LEN.R0,
                 title='R0',
                 name='r0',
                 checks=(CheckHexList(LEN.R0 // 8), CheckByte())),
        BitField(FID.R1,
                 LEN.R1,
                 title='R1',
                 name='r1',
                 checks=(CheckHexList(LEN.R1 // 8), CheckByte())),
        BitField(FID.R2,
                 LEN.R2,
                 title='R2',
                 name='r2',
                 checks=(CheckHexList(LEN.R2 // 8), CheckByte())),
    )

    def __init__(self, device_index, address, r0=0, r1=0, r2=0):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param address: The address of the register to set
        :type address: ``int`` or ``HexList``
        :param r0: The value of the first register to set
        :type r0: ``int`` or ``list`` or ``HexList``
        :param r1: The value of the second register to set
        :type r1: ``int`` or ``list`` or ``HexList``
        :param r1: The value of the second register to set
        :type r1: ``int`` or ``list`` or ``HexList``
        """
        super().__init__(device_index, address)

        self.r0 = r0
        self.r1 = r1
        self.r2 = r2
    # end def __init__
# end class GetRegisterRequest


class GetRegisterResponse(GetRegister):
    """
    This class defines the format of Get Register response.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    Value                         24
    ============================  ==========
    """
    class FID(GetRegister.FID):
        """
        Field Identifiers
        """
        VALUE = 0xFB
    # end class FID

    class LEN(GetRegister.LEN):
        """
        Field Lengths in bits
        """
        VALUE = 0x18
    # end class LEN

    FIELDS = GetRegister.FIELDS + (
        BitField(FID.VALUE,
                 LEN.VALUE,
                 0x00,
                 0x00,
                 title='Value',
                 name='value',
                 checks=(CheckHexList(LEN.VALUE // 8), CheckByte()),
                 default_value=Hidpp1Message.DEFAULT.PADDING),
    )

    def __init__(self, device_index, address, value):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param address: The address of the register to set
        :type address: ``int`` or ``HexList``
        :param value: The value of the register to set
        :type value: ``int`` or ``list`` or ``HexList``
        """
        super().__init__(device_index, address)
        self.value = value
    # end def __init__
# end class GetRegisterResponse


class SetLongRegister(SetRegister):
    """
    This class defines the format of Set Long Register header.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    ============================  ==========
    """
    SUB_ID = Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER

    def __init__(self, device_index, address):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param address: The address of the register to set
        :type address: ``int`` or ``HexList``
        """
        super().__init__(device_index, address)
        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
    # end def __init__
# end class SetLongRegister


class SetLongRegisterRequest(SetRegisterRequest):
    """
    This class defines the format of Set Long Register request.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    P0                            8
    P1                            8
    P2                            8
    Value                         104
    ============================  ==========
    """
    SUB_ID = SetLongRegister.SUB_ID

    class FID(SetRegisterRequest.FID):
        """
        Field Identifiers
        """
        VALUE = SetRegisterRequest.FID.P2 - 1
    # end class FID

    class LEN(SetRegisterRequest.LEN):
        """
        Field Lengths in bits
        """
        VALUE = 0x68
    # end class LEN

    FIELDS = SetRegisterRequest.FIELDS + (
        BitField(FID.VALUE,
                 LEN.VALUE,
                 title='Value',
                 name='value',
                 checks=(CheckHexList(LEN.VALUE // 8), CheckByte(),)),
    )

    def __init__(self, device_index, address, value=0):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param address: The address of the register to set
        :type address: ``int`` or ``HexList``
        """
        super().__init__(device_index, address)

        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.value = value
    # end def __init__
# end class SetLongRegisterRequest


class SetLongRegisterResponse(SetRegisterResponse):
    """
    This class defines the format of Set Long Register response.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    Padding                       24
    ============================  ==========
    """
    SUB_ID = SetLongRegister.SUB_ID
# end class SetLongRegisterResponse


class GetLongRegister(GetRegister):
    """
    This class defines the format of Get Long Register request.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    ============================  ==========
    """
    SUB_ID = Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER
# end class GetLongRegister


class GetLongRegisterRequest(GetRegisterRequest):
    """
    This class defines the format of Get Long Register request.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    Parameters                    24
    ============================  ==========
    """
    SUB_ID = GetLongRegister.SUB_ID
# end class GetLongRegister


class GetLongRegisterResponse(GetRegisterResponse):
    """
    This class defines the format of Get Register response.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    SubId                         8
    Address                       8
    Value                         128
    ============================  ==========
    """
    SUB_ID = GetLongRegister.SUB_ID

    class LEN(GetRegisterResponse.LEN):
        """
        Field Lengths in bits
        """
        VALUE = 0x80
    # end class LEN

    FIELDS = GetRegister.FIELDS + (
        BitField(GetRegisterResponse.FID.VALUE,
                 LEN.VALUE,
                 title='Value',
                 name='value',
                 checks=(CheckHexList(LEN.VALUE // 8), CheckByte()),
                 default_value=Hidpp1Message.DEFAULT.PADDING),
    )

    def __init__(self, device_index, address, value):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param address: The address of the register to set
        :type address: ``int`` or ``HexList``
        """
        super().__init__(device_index, address, value)

        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
    # end def __init__
# end class GetLongRegisterResponse


class BaseRegisterModel(object):
    """
    Base register model class for registers in the register map
    """
    @classmethod
    def _get_data_model(cls):
        """
        Register data model
        """
        raise NotImplementedError("Data model should be implemented")
    # end def _get_data_model

    @classmethod
    def get_sub_ids(cls):
        """
        Get sub ids available in the register
        """
        sub_ids = list(cls._get_data_model().keys())
        if "r0" in sub_ids:
            sub_ids.remove("r0")
        return sub_ids
    # end def get_sub_ids

    @classmethod
    def has_r0(cls):
        """
        Return true if R0 is in the register
        """
        return True if "r0" in cls._get_data_model() else False
    # end def has_r0

    @classmethod
    def get_r0s(cls):
        """
        Get R0 available values
        """
        return cls._get_data_model()["r0"].keys() if cls.has_r0() else []
    # end def get_r0s

    @classmethod
    def get_message_cls(cls, sub_id, message_type, r0=None):
        """
        Get message class from the data model
        """
        msg_cls = None
        data_model = cls._get_data_model()
        if r0 is not None and "r0" in data_model and r0 in data_model["r0"] and sub_id in data_model["r0"][r0] and \
                message_type in data_model["r0"][r0][sub_id]:
            msg_cls = data_model["r0"][r0][sub_id][message_type]
        elif sub_id in data_model and message_type in data_model[sub_id]:
            msg_cls = data_model[sub_id][message_type]
        return msg_cls
    # end get_message_cls

    @classmethod
    def get_available_requests_classes(cls):
        """
        Get available requests classes from the data model
        """
        return cls._find(cls._get_data_model(), "request")
    # end def get_available_requests_classes

    @classmethod
    def get_available_responses_classes(cls):
        """
        Get available responses classes from the data model
        """
        return cls._find(cls._get_data_model(), "response")
    # end def get_available_responses_classes

    @classmethod
    def get_available_classes(cls):
        """
        Get available responses classes from the data model
        """
        return cls.get_available_requests_classes() + cls.get_available_responses_classes()
    # end def get_available_classes

    @classmethod
    def _find(cls, model, key):
        """
        Recursively find response classes in model
        """
        values = []
        for value in model.values():
            if isinstance(value, dict):
                if key in value:
                    values.append(value[key])
                else:
                    values += cls._find(value, key)
        return values
    # end def _find_responses
# end class BaseRegisterModel

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
