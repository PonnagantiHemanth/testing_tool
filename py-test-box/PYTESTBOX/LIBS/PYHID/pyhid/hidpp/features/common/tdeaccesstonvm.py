#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.common.tdeaccesstonvm
:brief: HID++ 2.0 ``TdeAccessToNvm`` command interface definition
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2020/07/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TdeAccessToNvm(HidppMessage):
    """
    Define TdeAccessToNvm implementation
    """
    FEATURE_ID = 0x1EB0
    MAX_FUNCTION_INDEX = 3
    MAX_PACKET_SIZE = 0x0E

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(deviceIndex=device_index, featureIndex=feature_index, **kwargs)
    # end def __init__
# end class TdeAccessToNvm


class TdeAccessToNvmModel(FeatureModel):
    """
    Define ``TdeAccessToNvm`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_TDE_MEM_LENGTH = 0
        TDE_WRITE_DATA = 1
        TDE_READ_DATA = 2
        TDE_CLEAR_DATA = 3
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``TdeAccessToNvm`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_TDE_MEM_LENGTH: {
                    "request": GetTdeMemLength,
                    "response": GetTdeMemLengthResponse
                },
                cls.INDEX.TDE_WRITE_DATA: {
                    "request": TdeWriteData,
                    "response": TdeWriteDataResponse
                },
                cls.INDEX.TDE_READ_DATA: {
                    "request": TdeReadData,
                    "response": TdeReadDataResponse
                },
                cls.INDEX.TDE_CLEAR_DATA: {
                    "request": TdeClearData,
                    "response": TdeClearDataResponse
                }
            }
        }

        return {
            "feature_base": TdeAccessToNvm,
            "versions": {
                TdeAccessToNvmV0.VERSION: {
                    "main_cls": TdeAccessToNvmV0,
                    "api": function_map_v0
                }
            }
        }
    # end def _get_data_model
# end class TdeAccessToNvmModel


class TdeAccessToNvmFactory(FeatureFactory):
    """
    Get ``TdeAccessToNvm`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``TdeAccessToNvm`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``TdeAccessToNvmInterface``
        """
        return TdeAccessToNvmModel.get_main_cls(version)()
    # end def create
# end class TdeAccessToNvmFactory


class TdeAccessToNvmInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``TdeAccessToNvm``
    """

    def __init__(self):
        # Requests
        self.get_tde_mem_length_cls = None
        self.tde_write_data_cls = None
        self.tde_read_data_cls = None
        self.tde_clear_data_cls = None

        # Responses
        self.get_tde_mem_length_response_cls = None
        self.tde_write_data_response_cls = None
        self.tde_read_data_response_cls = None
        self.tde_clear_data_response_cls = None
    # end def __init__
# end class TdeAccessToNvmInterface


class TdeAccessToNvmV0(TdeAccessToNvmInterface):
    """
    Define ``TdeAccessToNvmV0`` feature

    This feature provides model and unit specific information for version 0

    [0] GetTdeMemLength() -> memoryLength

    [1] TdeWriteData(startingPosition, numberOfBytes, dataToWrite0..13) -> None

    [2] TdeReadData(startingPosition, numberOfBytesToRead) -> startingPosition, numberOfBytes, dataToRead0..13

    [3] TdeClearData() -> None
    """
    VERSION = 0

    def __init__(self):
        # See ``TdeAccessToNvm.__init__``
        super().__init__()
        index = TdeAccessToNvmModel.INDEX

        # Requests
        self.get_tde_mem_length_cls = TdeAccessToNvmModel.get_request_cls(
            self.VERSION, index.GET_TDE_MEM_LENGTH)
        self.tde_write_data_cls = TdeAccessToNvmModel.get_request_cls(
            self.VERSION, index.TDE_WRITE_DATA)
        self.tde_read_data_cls = TdeAccessToNvmModel.get_request_cls(
            self.VERSION, index.TDE_READ_DATA)
        self.tde_clear_data_cls = TdeAccessToNvmModel.get_request_cls(
            self.VERSION, index.TDE_CLEAR_DATA)

        # Responses
        self.get_tde_mem_length_response_cls = TdeAccessToNvmModel.get_response_cls(
            self.VERSION, index.GET_TDE_MEM_LENGTH)
        self.tde_write_data_response_cls = TdeAccessToNvmModel.get_response_cls(
            self.VERSION, index.TDE_WRITE_DATA)
        self.tde_read_data_response_cls = TdeAccessToNvmModel.get_response_cls(
            self.VERSION, index.TDE_READ_DATA)
        self.tde_clear_data_response_cls = TdeAccessToNvmModel.get_response_cls(
            self.VERSION, index.TDE_CLEAR_DATA)
    # end def __init__

    def get_max_function_index(self):
        # See ``TdeAccessToNvmInterface.get_max_function_index``
        return TdeAccessToNvmModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class TdeAccessToNvmV0


class ShortEmptyPacketDataFormat(TdeAccessToNvm):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetTdeMemLength
        - TdeClearData

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(TdeAccessToNvm.FID):
        # See ``TdeAccessToNvm.FID``
        PADDING = TdeAccessToNvm.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(TdeAccessToNvm.LEN):
        # See ``TdeAccessToNvm.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = TdeAccessToNvm.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TdeAccessToNvm.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(TdeAccessToNvm):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - TdeWriteDataResponse
        - TdeClearDataResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(TdeAccessToNvm.FID):
        # See ``TdeAccessToNvm.FID``
        PADDING = TdeAccessToNvm.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(TdeAccessToNvm.LEN):
        # See ``TdeAccessToNvm.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = TdeAccessToNvm.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TdeAccessToNvm.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class TdeAccessToNvmPacketDataFormat(TdeAccessToNvm):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - TdeWriteData
        - TdeReadDataResponse

    Format:
    ================================  ==========
    Name                              Bit count
    ================================  ==========
    Starting Position                 8
    Number Of Bytes To Read Or Write  8
    Data Byte 0                       8
    Data Byte 1                       8
    Data Byte 2                       8
    Data Byte 3                       8
    Data Byte 4                       8
    Data Byte 5                       8
    Data Byte 6                       8
    Data Byte 7                       8
    Data Byte 8                       8
    Data Byte 9                       8
    Data Byte 10                      8
    Data Byte 11                      8
    Data Byte 12                      8
    Data Byte 13                      8
    ================================  ==========
    """

    class FID(TdeAccessToNvm.FID):
        # See ``TdeAccessToNvm.FID``
        STARTING_POSITION = TdeAccessToNvm.FID.SOFTWARE_ID - 1
        NUMBER_OF_BYTES_TO_READ_OR_WRITE = STARTING_POSITION - 1
        DATA_BYTE_0 = NUMBER_OF_BYTES_TO_READ_OR_WRITE - 1
        DATA_BYTE_1 = DATA_BYTE_0 - 1
        DATA_BYTE_2 = DATA_BYTE_1 - 1
        DATA_BYTE_3 = DATA_BYTE_2 - 1
        DATA_BYTE_4 = DATA_BYTE_3 - 1
        DATA_BYTE_5 = DATA_BYTE_4 - 1
        DATA_BYTE_6 = DATA_BYTE_5 - 1
        DATA_BYTE_7 = DATA_BYTE_6 - 1
        DATA_BYTE_8 = DATA_BYTE_7 - 1
        DATA_BYTE_9 = DATA_BYTE_8 - 1
        DATA_BYTE_10 = DATA_BYTE_9 - 1
        DATA_BYTE_11 = DATA_BYTE_10 - 1
        DATA_BYTE_12 = DATA_BYTE_11 - 1
        DATA_BYTE_13 = DATA_BYTE_12 - 1
    # end class FID

    class LEN(TdeAccessToNvm.LEN):
        # See ``TdeAccessToNvm.LEN``
        STARTING_POSITION = 0x8
        NUMBER_OF_BYTES_TO_READ_OR_WRITE = 0x8
        DATA_BYTE_0 = 0x8
        DATA_BYTE_1 = 0x8
        DATA_BYTE_2 = 0x8
        DATA_BYTE_3 = 0x8
        DATA_BYTE_4 = 0x8
        DATA_BYTE_5 = 0x8
        DATA_BYTE_6 = 0x8
        DATA_BYTE_7 = 0x8
        DATA_BYTE_8 = 0x8
        DATA_BYTE_9 = 0x8
        DATA_BYTE_10 = 0x8
        DATA_BYTE_11 = 0x8
        DATA_BYTE_12 = 0x8
        DATA_BYTE_13 = 0x8
    # end class LEN

    FIELDS = TdeAccessToNvm.FIELDS + (
        BitField(fid=FID.STARTING_POSITION, length=LEN.STARTING_POSITION,
                 title="StartingPosition", name="starting_position",
                 checks=(CheckHexList(LEN.STARTING_POSITION // 8),
                         CheckByte(),)),
        BitField(fid=FID.NUMBER_OF_BYTES_TO_READ_OR_WRITE, length=LEN.NUMBER_OF_BYTES_TO_READ_OR_WRITE,
                 title="NumberOfBytesToReadOrWrite", name="number_of_bytes_to_read_or_write",
                 checks=(CheckHexList(LEN.NUMBER_OF_BYTES_TO_READ_OR_WRITE // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_BYTE_0, length=LEN.DATA_BYTE_0,
                 title="DataByte0", name="data_byte_0",
                 checks=(CheckHexList(LEN.DATA_BYTE_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_BYTE_1, length=LEN.DATA_BYTE_1,
                 title="DataByte1", name="data_byte_1",
                 checks=(CheckHexList(LEN.DATA_BYTE_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_BYTE_2, length=LEN.DATA_BYTE_2,
                 title="DataByte2", name="data_byte_2",
                 checks=(CheckHexList(LEN.DATA_BYTE_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_BYTE_3, length=LEN.DATA_BYTE_3,
                 title="DataByte3", name="data_byte_3",
                 checks=(CheckHexList(LEN.DATA_BYTE_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_BYTE_4, length=LEN.DATA_BYTE_4,
                 title="DataByte4", name="data_byte_4",
                 checks=(CheckHexList(LEN.DATA_BYTE_4 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_BYTE_5, length=LEN.DATA_BYTE_5,
                 title="DataByte5", name="data_byte_5",
                 checks=(CheckHexList(LEN.DATA_BYTE_5 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_BYTE_6, length=LEN.DATA_BYTE_6,
                 title="DataByte6", name="data_byte_6",
                 checks=(CheckHexList(LEN.DATA_BYTE_6 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_BYTE_7, length=LEN.DATA_BYTE_7,
                 title="DataByte7", name="data_byte_7",
                 checks=(CheckHexList(LEN.DATA_BYTE_7 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_BYTE_8, length=LEN.DATA_BYTE_8,
                 title="DataByte8", name="data_byte_8",
                 checks=(CheckHexList(LEN.DATA_BYTE_8 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_BYTE_9, length=LEN.DATA_BYTE_9,
                 title="DataByte9", name="data_byte_9",
                 checks=(CheckHexList(LEN.DATA_BYTE_9 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_BYTE_10, length=LEN.DATA_BYTE_10,
                 title="DataByte10", name="data_byte_10",
                 checks=(CheckHexList(LEN.DATA_BYTE_10 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_BYTE_11, length=LEN.DATA_BYTE_11,
                 title="DataByte11", name="data_byte_11",
                 checks=(CheckHexList(LEN.DATA_BYTE_11 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_BYTE_12, length=LEN.DATA_BYTE_12,
                 title="DataByte12", name="data_byte_12",
                 checks=(CheckHexList(LEN.DATA_BYTE_12 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_BYTE_13, length=LEN.DATA_BYTE_13,
                 title="DataByte13", name="data_byte_13",
                 checks=(CheckHexList(LEN.DATA_BYTE_13 // 8),
                         CheckByte(),)),
    )
# end class TdeAccessToNvmPacketDataFormat


class GetTdeMemLength(ShortEmptyPacketDataFormat):
    """
    Define ``GetTdeMemLength`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetTdeMemLengthResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetTdeMemLength


class GetTdeMemLengthResponse(TdeAccessToNvm):
    """
    Define ``GetTdeMemLengthResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Memory Length                 8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetTdeMemLength,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(TdeAccessToNvm.FID):
        # See ``TdeAccessToNvm.FID``
        MEMORY_LENGTH = TdeAccessToNvm.FID.SOFTWARE_ID - 1
        PADDING = MEMORY_LENGTH - 1
    # end class FID

    class LEN(TdeAccessToNvm.LEN):
        # See ``TdeAccessToNvm.LEN``
        MEMORY_LENGTH = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = TdeAccessToNvm.FIELDS + (
        BitField(fid=FID.MEMORY_LENGTH, length=LEN.MEMORY_LENGTH,
                 title="MemoryLength", name="memory_length",
                 checks=(CheckHexList(LEN.MEMORY_LENGTH // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TdeAccessToNvm.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, memory_length, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param memory_length: Number of accessible bytes
        :type memory_length: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.memory_length = memory_length
    # end def __init__
# end class GetTdeMemLengthResponse


class TdeWriteData(TdeAccessToNvmPacketDataFormat):
    """
    Define ``TdeWriteData`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, starting_position, number_of_bytes_to_read_or_write, data_byte_0=0,
                 data_byte_1=0, data_byte_2=0, data_byte_3=0, data_byte_4=0, data_byte_5=0, data_byte_6=0,
                 data_byte_7=0, data_byte_8=0, data_byte_9=0, data_byte_10=0, data_byte_11=0, data_byte_12=0,
                 data_byte_13=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param starting_position: Starting Position
        :type starting_position: ``int`` or ``HexList``
        :param number_of_bytes_to_read_or_write: Number Of Bytes To Read Or Write
        :type number_of_bytes_to_read_or_write: ``int`` or ``HexList``
        :param data_byte_0: Data Byte 0
        :type data_byte_0: ``int`` or ``HexList``
        :param data_byte_1: Data Byte 1
        :type data_byte_1: ``int`` or ``HexList``
        :param data_byte_2: Data Byte 2
        :type data_byte_2: ``int`` or ``HexList``
        :param data_byte_3: Data Byte 3
        :type data_byte_3: ``int`` or ``HexList``
        :param data_byte_4: Data Byte 4
        :type data_byte_4: ``int`` or ``HexList``
        :param data_byte_5: Data Byte 5
        :type data_byte_5: ``int`` or ``HexList``
        :param data_byte_6: Data Byte 6
        :type data_byte_6: ``int`` or ``HexList``
        :param data_byte_7: Data Byte 7
        :type data_byte_7: ``int`` or ``HexList``
        :param data_byte_8: Data Byte 8
        :type data_byte_8: ``int`` or ``HexList``
        :param data_byte_9: Data Byte 9
        :type data_byte_9: ``int`` or ``HexList``
        :param data_byte_10: Data Byte 10
        :type data_byte_10: ``int`` or ``HexList``
        :param data_byte_11: Data Byte 11
        :type data_byte_11: ``int`` or ``HexList``
        :param data_byte_12: Data Byte 12
        :type data_byte_12: ``int`` or ``HexList``
        :param data_byte_13: Data Byte 13
        :type data_byte_13: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=TdeWriteDataResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.starting_position = starting_position
        self.number_of_bytes_to_read_or_write = number_of_bytes_to_read_or_write
        self.data_byte_0 = data_byte_0
        self.data_byte_1 = data_byte_1
        self.data_byte_2 = data_byte_2
        self.data_byte_3 = data_byte_3
        self.data_byte_4 = data_byte_4
        self.data_byte_5 = data_byte_5
        self.data_byte_6 = data_byte_6
        self.data_byte_7 = data_byte_7
        self.data_byte_8 = data_byte_8
        self.data_byte_9 = data_byte_9
        self.data_byte_10 = data_byte_10
        self.data_byte_11 = data_byte_11
        self.data_byte_12 = data_byte_12
        self.data_byte_13 = data_byte_13
    # end def __init__
# end class TdeWriteData


class TdeWriteDataResponse(LongEmptyPacketDataFormat):
    """
    Define ``TdeWriteDataResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (TdeWriteData,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class TdeWriteDataResponse


class TdeReadData(TdeAccessToNvm):
    """
    Define ``TdeReadData`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Starting Position             8
    Number Of Bytes To Read       8
    Padding                       8
    ============================  ==========
    """

    class FID(TdeAccessToNvm.FID):
        # See ``TdeAccessToNvm.FID``
        STARTING_POSITION = TdeAccessToNvm.FID.SOFTWARE_ID - 1
        NUMBER_OF_BYTES_TO_READ = STARTING_POSITION - 1
        PADDING = NUMBER_OF_BYTES_TO_READ - 1
    # end class FID

    class LEN(TdeAccessToNvm.LEN):
        # See ``TdeAccessToNvm.LEN``
        STARTING_POSITION = 0x8
        NUMBER_OF_BYTES_TO_READ = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = TdeAccessToNvm.FIELDS + (
        BitField(fid=FID.STARTING_POSITION, length=LEN.STARTING_POSITION,
                 title="StartingPosition", name="starting_position",
                 checks=(CheckHexList(LEN.STARTING_POSITION // 8),
                         CheckByte(),)),
        BitField(fid=FID.NUMBER_OF_BYTES_TO_READ, length=LEN.NUMBER_OF_BYTES_TO_READ,
                 title="NumberOfBytesToRead", name="number_of_bytes_to_read",
                 checks=(CheckHexList(LEN.NUMBER_OF_BYTES_TO_READ // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TdeAccessToNvm.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, starting_position, number_of_bytes_to_read, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param starting_position: Starting Position
        :type starting_position: ``int`` or ``HexList``
        :param number_of_bytes_to_read: Number Of Bytes To Read
        :type number_of_bytes_to_read: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=TdeReadDataResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.starting_position = starting_position
        self.number_of_bytes_to_read = number_of_bytes_to_read
    # end def __init__
# end class TdeReadData


class TdeReadDataResponse(TdeAccessToNvmPacketDataFormat):
    """
    Define ``TdeReadDataResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (TdeReadData,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, starting_position, number_of_bytes_to_read_or_write, data_byte_0=0,
                 data_byte_1=0, data_byte_2=0, data_byte_3=0, data_byte_4=0, data_byte_5=0, data_byte_6=0,
                 data_byte_7=0, data_byte_8=0, data_byte_9=0, data_byte_10=0, data_byte_11=0, data_byte_12=0,
                 data_byte_13=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param starting_position: Starting Position
        :type starting_position: ``int`` or ``HexList``
        :param number_of_bytes_to_read_or_write: Number Of Bytes To Read Or Write
        :type number_of_bytes_to_read_or_write: ``int`` or ``HexList``
        :param data_byte_0: Data Byte 0
        :type data_byte_0: ``int`` or ``HexList``
        :param data_byte_1: Data Byte 1
        :type data_byte_1: ``int`` or ``HexList``
        :param data_byte_2: Data Byte 2
        :type data_byte_2: ``int`` or ``HexList``
        :param data_byte_3: Data Byte 3
        :type data_byte_3: ``int`` or ``HexList``
        :param data_byte_4: Data Byte 4
        :type data_byte_4: ``int`` or ``HexList``
        :param data_byte_5: Data Byte 5
        :type data_byte_5: ``int`` or ``HexList``
        :param data_byte_6: Data Byte 6
        :type data_byte_6: ``int`` or ``HexList``
        :param data_byte_7: Data Byte 7
        :type data_byte_7: ``int`` or ``HexList``
        :param data_byte_8: Data Byte 8
        :type data_byte_8: ``int`` or ``HexList``
        :param data_byte_9: Data Byte 9
        :type data_byte_9: ``int`` or ``HexList``
        :param data_byte_10: Data Byte 10
        :type data_byte_10: ``int`` or ``HexList``
        :param data_byte_11: Data Byte 11
        :type data_byte_11: ``int`` or ``HexList``
        :param data_byte_12: Data Byte 12
        :type data_byte_12: ``int`` or ``HexList``
        :param data_byte_13: Data Byte 13
        :type data_byte_13: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.starting_position = starting_position
        self.number_of_bytes_to_read_or_write = number_of_bytes_to_read_or_write
        self.data_byte_0 = data_byte_0
        self.data_byte_1 = data_byte_1
        self.data_byte_2 = data_byte_2
        self.data_byte_3 = data_byte_3
        self.data_byte_4 = data_byte_4
        self.data_byte_5 = data_byte_5
        self.data_byte_6 = data_byte_6
        self.data_byte_7 = data_byte_7
        self.data_byte_8 = data_byte_8
        self.data_byte_9 = data_byte_9
        self.data_byte_10 = data_byte_10
        self.data_byte_11 = data_byte_11
        self.data_byte_12 = data_byte_12
        self.data_byte_13 = data_byte_13
    # end def __init__
# end class TdeReadDataResponse


class TdeClearData(ShortEmptyPacketDataFormat):
    """
    Define ``TdeClearData`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=TdeClearDataResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class TdeClearData


class TdeClearDataResponse(LongEmptyPacketDataFormat):
    """
    Define ``TdeClearDataResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (TdeClearData,)
    VERSION = (0,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class TdeClearDataResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
