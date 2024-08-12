#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.common.devicefriendlyname
:brief: HID++ 2.0 DeviceFriendlyName command interface definition
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2020/09/02
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from abc import ABC
from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.hexlist import HexList


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DeviceFriendlyName(HidppMessage):
    """
    The DeviceFriendlyName is the device name provided to the host during pairing or connection,
    displayed to the user to identify the device.

    This feature allows reading and changing the DeviceFriendlyName.

    Friendly Name encoding is 8 bits ASCII.
    """
    FEATURE_ID = 0x0007
    MAX_FUNCTION_INDEX = 4

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(deviceIndex=device_index, featureIndex=feature_index, **kwargs)
    # end def __init__
# end class DeviceFriendlyName


class DeviceFriendlyNameModel(FeatureModel):
    """
    DeviceFriendlyName feature model
    """
    class INDEX(object):
        """
        Functions index
        """
        GET_FRIENDLY_NAME_LEN = 0
        GET_FRIENDLY_NAME = 1
        GET_DEFAULT_FRIENDLY_NAME = 2
        SET_FRIENDLY_NAME = 3
        RESET_FRIENDLY_NAME = 4
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        DeviceFriendlyName feature data model
        """
        return {
                "feature_base": DeviceFriendlyName,
                "versions": {
                        DeviceFriendlyNameV0.VERSION: {
                                "main_cls": DeviceFriendlyNameV0,
                                "api": {
                                        "functions": {
                                                cls.INDEX.GET_FRIENDLY_NAME_LEN: {
                                                        "request": GetFriendlyNameLen,
                                                        "response": GetFriendlyNameLenResponse
                                                },
                                                cls.INDEX.GET_FRIENDLY_NAME: {
                                                        "request": GetFriendlyName,
                                                        "response": GetFriendlyNameResponse
                                                },
                                                cls.INDEX.GET_DEFAULT_FRIENDLY_NAME: {
                                                        "request": GetDefaultFriendlyName,
                                                        "response": GetDefaultFriendlyNameResponse
                                                },
                                                cls.INDEX.SET_FRIENDLY_NAME: {
                                                        "request": SetFriendlyName,
                                                        "response": SetFriendlyNameResponse
                                                },
                                                cls.INDEX.RESET_FRIENDLY_NAME: {
                                                        "request": ResetFriendlyName,
                                                        "response": ResetFriendlyNameResponse
                                                }
                                        }
                                }
                        }
                }
        }
    # end def _get_data_model
# end class DeviceFriendlyNameModel


class DeviceFriendlyNameFactory(FeatureFactory):
    """
    Factory which creates a DeviceFriendlyName object from a given version
    """
    @staticmethod
    def create(version):
        """
        DeviceFriendlyName object creation from version number

        :param version: DeviceFriendlyName feature version
        :type version: ``int``

        :return: DeviceFriendlyName object
        :rtype: ``DeviceFriendlyNameInterface``
        """
        return DeviceFriendlyNameModel.get_main_cls(version)()
    # end def create
# end class DeviceFriendlyNameFactory


class DeviceFriendlyNameInterface(FeatureInterface, ABC):
    """
    Defines required interfaces for DeviceFriendlyName classes
    """
    def __init__(self):
        """
        Constructor
        """
        # Requests
        self.get_friendly_name_len_cls = None
        self.get_friendly_name_cls = None
        self.get_default_friendly_name_cls = None
        self.set_friendly_name_cls = None
        self.reset_friendly_name_cls = None

        # Responses
        self.get_friendly_name_len_response_cls = None
        self.get_friendly_name_response_cls = None
        self.get_default_friendly_name_response_cls = None
        self.set_friendly_name_response_cls = None
        self.reset_friendly_name_response_cls = None
    # end def __init__
# end class DeviceFriendlyNameInterface


class DeviceFriendlyNameV0(DeviceFriendlyNameInterface):
    """
    DeviceFriendlyNameV0

    This feature provides model and unit specific information for version 0

    [0] getFriendlyNameLen() → nameLen, nameMaxLen, defaultNameLen

    [1] getFriendlyName(byteIndex) → string

    [2] getDefaultFriendlyName(byteIndex) → string

    [3] setFriendlyName(byteIndex, nameChunk) → nameLen

    [4] resetFriendlyName() → nameLen
    """
    VERSION = 0

    def __init__(self):
        # See ``DeviceFriendlyName.__init__``
        super().__init__()
        index = DeviceFriendlyNameModel.INDEX
        # Requests
        self.get_friendly_name_len_cls = DeviceFriendlyNameModel.get_request_cls(
                self.VERSION, index.GET_FRIENDLY_NAME_LEN)
        self.get_friendly_name_cls = DeviceFriendlyNameModel.get_request_cls(
                self.VERSION, index.GET_FRIENDLY_NAME)
        self.get_default_friendly_name_cls = DeviceFriendlyNameModel.get_request_cls(
                self.VERSION, index.GET_DEFAULT_FRIENDLY_NAME)
        self.set_friendly_name_cls = DeviceFriendlyNameModel.get_request_cls(
                self.VERSION, index.SET_FRIENDLY_NAME)
        self.reset_friendly_name_cls = DeviceFriendlyNameModel.get_request_cls(
                self.VERSION, index.RESET_FRIENDLY_NAME)

        # Responses
        self.get_friendly_name_len_response_cls = DeviceFriendlyNameModel.get_response_cls(
                self.VERSION, index.GET_FRIENDLY_NAME_LEN)
        self.get_friendly_name_response_cls = DeviceFriendlyNameModel.get_response_cls(
                self.VERSION, index.GET_FRIENDLY_NAME)
        self.get_default_friendly_name_response_cls = DeviceFriendlyNameModel.get_response_cls(
                self.VERSION, index.GET_DEFAULT_FRIENDLY_NAME)
        self.set_friendly_name_response_cls = DeviceFriendlyNameModel.get_response_cls(
                self.VERSION, index.SET_FRIENDLY_NAME)
        self.reset_friendly_name_response_cls = DeviceFriendlyNameModel.get_response_cls(
                self.VERSION, index.RESET_FRIENDLY_NAME)
    # end def __init__

    def get_max_function_index(self):
        # See ``DeviceFriendlyNameInterface.get_max_function_index``
        return DeviceFriendlyNameModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class DeviceFriendlyNameV0


class EmptyPacketDataFormat(DeviceFriendlyName):
    """
    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """
    class FID(DeviceFriendlyName.FID):
        """
        Field Identifiers
        """
        PADDING = DeviceFriendlyName.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(DeviceFriendlyName.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = DeviceFriendlyName.FIELDS + (
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title='Padding', name='padding',
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=DeviceFriendlyName.DEFAULT.PADDING),)
# end class EmptyPacketDataFormat


class GetFriendlyNameLen(EmptyPacketDataFormat):
    """
    GetFriendlyNameLen implementation class for version 0
    """
    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: device index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: feature index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetFriendlyNameLenResponse.FUNCTION_INDEX,
                         **kwargs)
    # end def __init__
# end class GetFriendlyNameLen


class GetFriendlyNameLenResponse(DeviceFriendlyName):
    """
    GetFriendlyNameLenResponse implementation class for version 0

    Get the length of current name, default name, and maximum allowed length for device name.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    NameLen                       8
    NameMaxLen                    8
    DefaultNameLen                8
    Padding                       104
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetFriendlyNameLen,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(DeviceFriendlyName.FID):
        """
        Field Identifiers
        """
        NAME_LEN = DeviceFriendlyName.FID.SOFTWARE_ID - 1
        NAME_MAX_LEN = NAME_LEN - 1
        DEFAULT_NAME_LEN = NAME_MAX_LEN - 1
        PADDING = DEFAULT_NAME_LEN - 1
    # end class FID

    class LEN(DeviceFriendlyName.LEN):
        """
        Field Lengths
        """
        NAME_LEN = 0x08
        NAME_MAX_LEN = 0x08
        DEFAULT_NAME_LEN = 0x08
        PADDING = 0x68
    # end class LEN

    FIELDS = DeviceFriendlyName.FIELDS + (
            BitField(fid=FID.NAME_LEN, length=LEN.NAME_LEN,
                     title='NameLength', name='name_len',
                     checks=(CheckHexList(LEN.NAME_LEN // 8), CheckByte(),)),
            BitField(fid=FID.NAME_MAX_LEN, length=LEN.NAME_MAX_LEN,
                     title='MaximumNameLength', name='name_max_len',
                     checks=(CheckHexList(LEN.NAME_MAX_LEN // 8), CheckByte(),)),
            BitField(fid=FID.DEFAULT_NAME_LEN, length=LEN.DEFAULT_NAME_LEN,
                     title='DefaultNameLength', name='default_name_len',
                     checks=(CheckHexList(LEN.DEFAULT_NAME_LEN // 8), CheckByte(),)),
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title='Padding', name='padding',
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=DeviceFriendlyName.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, name_len, name_max_len, default_name_len, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param name_len: Number of bytes of name length
        :type name_len: ``int`` or ``HexList``
        :param name_max_len: Number of bytes of name max length
        :type name_max_len: ``int`` or ``HexList``
        :param default_name_len: Number of bytes of default name length
        :type default_name_len: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.name_len = name_len
        self.name_max_len = name_max_len
        self.default_name_len = default_name_len
    # end def __init__
# end class GetFriendlyNameLenResponse


class DeviceFriendlyNamePacketDataFormat(DeviceFriendlyName):
    """
    DeviceFriendlyName PacketDataFormat class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ByteIndex                     8
    NameChunk                     120
    ============================  ==========
    """
    class FID(DeviceFriendlyName.FID):
        """
        Field Identifiers
        """
        BYTE_INDEX = DeviceFriendlyName.FID.SOFTWARE_ID - 1
        NAME_CHUNK = BYTE_INDEX - 1
    # end class FID

    class LEN(DeviceFriendlyName.LEN):
        """
        Field Lengths
        """
        BYTE_INDEX = 0x08
        NAME_CHUNK = 0x78
    # end class LEN

    FIELDS = DeviceFriendlyName.FIELDS + (
            BitField(fid=FID.BYTE_INDEX, length=LEN.BYTE_INDEX,
                     title='ByteIndex', name='byte_index',
                     checks=(CheckHexList(LEN.BYTE_INDEX // 8), CheckByte(), CheckInt(0, pow(2, LEN.BYTE_INDEX) - 1))),
            BitField(fid=FID.NAME_CHUNK, length=LEN.NAME_CHUNK,
                     title='NameChunk', name='name_chunk',
                     checks=(CheckHexList(LEN.NAME_CHUNK // 8), CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, byte_index, name_chunk, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param byte_index: Index of the first byte to copy [0..nameLen-1]
        :type byte_index: ``int`` or ``HexList``
        :param name_chunk: The name chunk, copied from full name byteIndex’th byte, padded with null bytes '\0' if
        the copied string is shorter than the payload size
        :type name_chunk: ``str`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         reportId=HidppMessage.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.byte_index = byte_index
        name_chunk = HexList.fromString(name_chunk) if isinstance(name_chunk, str) else name_chunk
        name_chunk_copy = HexList(name_chunk.copy())
        name_chunk_copy.addPadding(size=self.LEN.NAME_CHUNK // 8, pattern=self.DEFAULT.PADDING, fromLeft=False)
        self.name_chunk = name_chunk_copy
    # end def __init__
# end class DeviceFriendlyNamePacketDataFormat


class GetFriendlyName(DeviceFriendlyName):
    """
    GetFriendlyName implementation class for version 0

    Get a current Friendly Name chunk, starting from a byte index lower than nameLen returned by getFriendlyNameLen().

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ByteIndex                     8
    Padding                       16
    ============================  ==========
    """
    class FID(DeviceFriendlyName.FID):
        """
        Field Identifiers
        """
        BYTE_INDEX = DeviceFriendlyName.FID.SOFTWARE_ID - 1
        PADDING = BYTE_INDEX - 1
    # end class FID

    class LEN(DeviceFriendlyName.LEN):
        """
        Field Lengths
        """
        BYTE_INDEX = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = DeviceFriendlyName.FIELDS + (
            BitField(fid=FID.BYTE_INDEX, length=LEN.BYTE_INDEX,
                     title='ByteIndex', name='byte_index',
                     checks=(CheckHexList(LEN.BYTE_INDEX // 8), CheckByte(),)),
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title='Padding', name='padding',
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=DeviceFriendlyName.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, byte_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature index
        :type feature_index: ``int`` or ``HexList``
        :param byte_index: Index of the first byte to copy [0..nameLen-1].
        :type byte_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetFriendlyNameResponse.FUNCTION_INDEX,
                         **kwargs)
        self.byte_index = byte_index
    # end def __init__
# end class GetFriendlyName


class GetFriendlyNameResponse(DeviceFriendlyNamePacketDataFormat):
    """
    GetFriendlyNameResponse implementation class for version 0

    Get a current Friendly Name chunk, starting from a byte index lower than nameLen returned by getFriendlyNameLen().
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetFriendlyName,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, byte_index, name_chunk, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param byte_index: Index of the first byte to copy [0..nameLen-1]
        :type byte_index: ``int`` or ``HexList``
        :param name_chunk: The name chunk, copied from full name byteIndex’th byte, padded with null bytes '\0' if
        the copied string is shorter than the payload size
        :type name_chunk: ``str`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         byte_index=byte_index, name_chunk=name_chunk,
                         functionIndex=self.FUNCTION_INDEX,
                         **kwargs)
    # end def __init__
# end class GetFriendlyNameResponse


class GetDefaultFriendlyName(DeviceFriendlyName):
    """
    GetDefaultFriendlyName implementation class for version 0

    Get a Friendly Name chunk, starting from a byte index lower than defaultNameLen returned by getFriendlyNameLen().

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ByteIndex                     8
    Padding                       16
    ============================  ==========
    """
    class FID(DeviceFriendlyName.FID):
        """
        Field Identifiers
        """
        BYTE_INDEX = DeviceFriendlyName.FID.SOFTWARE_ID - 1
        PADDING = BYTE_INDEX - 1
    # end class FID

    class LEN(DeviceFriendlyName.LEN):
        """
        Field Lengths
        """
        BYTE_INDEX = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = DeviceFriendlyName.FIELDS + (
            BitField(fid=FID.BYTE_INDEX, length=LEN.BYTE_INDEX,
                     title='ByteIndex', name='byte_index',
                     checks=(CheckHexList(LEN.BYTE_INDEX // 8), CheckByte(),)),
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title='Padding', name='padding',
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=DeviceFriendlyName.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, byte_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature index
        :type feature_index: ``int`` or ``HexList``
        :param byte_index: Index of the first byte to copy [0..nameLen-1].
        :type byte_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetDefaultFriendlyNameResponse.FUNCTION_INDEX,
                         **kwargs)
        self.byte_index = byte_index
    # end def __init__
# end class GetDefaultFriendlyName


class GetDefaultFriendlyNameResponse(DeviceFriendlyNamePacketDataFormat):
    """
    GetDefaultFriendlyNameResponse implementation class for version 0

    Get a current Friendly Name chunk, starting from a byte index lower than nameLen returned by getFriendlyNameLen().
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetDefaultFriendlyName,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, byte_index, name_chunk, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param byte_index: Index of the first byte to copy [0..nameLen-1]
        :type byte_index: ``int`` or ``HexList``
        :param name_chunk: The name chunk, copied from full name byteIndex’th byte, padded with null bytes '\0' if
        the copied string is shorter than the payload size
        :type name_chunk: ``str`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         byte_index=byte_index, name_chunk=name_chunk,
                         functionIndex=self.FUNCTION_INDEX,
                         **kwargs)
    # end def __init__
# end class GetDefaultFriendlyNameResponse


class SetFriendlyName(DeviceFriendlyNamePacketDataFormat):
    """
    SetFriendlyName implementation class for version 0

    Set a DeviceFriendlyName chunk, starting at byteIndex. Existing string is overwritten, extended or shorten by
    the chunk, considering that resulting Friendly Name new length is byteIndex + strlen(chunk), truncated to maximum
    allowed length.

    Change is immediate (on device) but usually seen by hosts at reconnection.
    """
    def __init__(self, device_index, feature_index, byte_index, name_chunk, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param byte_index: Index of the first byte to copy [0..nameLen-1]
        :type byte_index: ``int`` or ``HexList``
        :param name_chunk: The name chunk, copied from full name byteIndex’th byte, padded with null bytes '\0' if
        the copied string is shorter than the payload size
        :type name_chunk: ``str`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         byte_index=byte_index, name_chunk=name_chunk,
                         functionIndex=SetFriendlyNameResponse.FUNCTION_INDEX,
                         **kwargs)
    # end def __init__
# end class SetFriendlyName


class SetFriendlyNameResponse(DeviceFriendlyName):
    """
    SetFriendlyNameResponse implementation class for version 0

    Set a DeviceFriendlyName chunk, starting at byteIndex. Existing string is overwritten, extended or shorten by
    the chunk, considering that resulting Friendly Name new length is byteIndex + strlen(chunk), truncated to maximum
    allowed length.

    Change is immediate (on device) but usually seen by hosts at reconnection.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    NameLen                       8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetFriendlyName,)
    VERSION = (0,)
    FUNCTION_INDEX = 3

    class FID(DeviceFriendlyName.FID):
        """
        Field Identifiers
        """
        NAME_LEN = DeviceFriendlyName.FID.SOFTWARE_ID - 1
        PADDING = NAME_LEN - 1
    # end class FID

    class LEN(DeviceFriendlyName.LEN):
        """
        Field Lengths
        """
        NAME_LEN = 0x08
        PADDING = 0x78
    # end class LEN

    FIELDS = DeviceFriendlyName.FIELDS + (
            BitField(fid=FID.NAME_LEN, length=LEN.NAME_LEN,
                     title='NameLength', name='name_len',
                     checks=(CheckHexList(LEN.NAME_LEN // 8), CheckByte(),)),
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title='Padding', name='padding',
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=DeviceFriendlyName.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, name_len, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param name_len: Resulting DeviceFriendlyName len, 0 in case of failure (HW write failure).
        :type name_len: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.name_len = name_len
    # end def __init__
# end class SetFriendlyNameResponse


class ResetFriendlyName(EmptyPacketDataFormat):
    """
    ResetFriendlyName implementation class for version 0
    """
    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=ResetFriendlyNameResponse.FUNCTION_INDEX,
                         **kwargs)
    # end def __init__
# end class ResetFriendlyName


class ResetFriendlyNameResponse(DeviceFriendlyName):
    """
    ResetFriendlyNameResponse implementation class for version 0

    Reset current DeviceFriendlyName to Default Friendly Name.

    Change is immediate (on device) but usually seen by hosts at reconnection.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    NameLen                       8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ResetFriendlyName,)
    VERSION = (0,)
    FUNCTION_INDEX = 4

    class FID(DeviceFriendlyName.FID):
        """
        Field Identifiers
        """
        NAME_LEN = DeviceFriendlyName.FID.SOFTWARE_ID - 1
        PADDING = NAME_LEN - 1
    # end class FID

    class LEN(DeviceFriendlyName.LEN):
        """
        Field Lengths
        """
        NAME_LEN = 0x08
        PADDING = 0x78
    # end class LEN

    FIELDS = DeviceFriendlyName.FIELDS + (
            BitField(fid=FID.NAME_LEN, length=LEN.NAME_LEN,
                     title='NameLength', name='name_len',
                     checks=(CheckHexList(LEN.NAME_LEN // 8), CheckByte(),)),
            BitField(fid=FID.PADDING, length=LEN.PADDING,
                     title='Padding', name='padding',
                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                     default_value=DeviceFriendlyName.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, name_len, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param name_len: Resulting DeviceFriendlyName len, 0 in case of failure (HW write failure).
        :type name_len: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.name_len = name_len
    # end def __init__
# end class ResetFriendlyNameResponse

# ------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
