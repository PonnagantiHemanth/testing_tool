#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.error
:brief: HID++ 2.0 Error command interface definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/12/20
"""

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from copy import deepcopy

from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.hidpp1message import Hidpp1Message
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ErrorCodes(HidppMessage):
    """
    Error Codes implementation class for HID++ 2.0 and VLP

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportId                      8
    DeviceIdx                     8
    ErrorTag                      8
    FeatureIdx                    8
    FunctionId                    4
    SoftwareId                    4
    ErrorCode                     8
    OptionalAdditionalInfo        N
    ============================  ==========
    """
    # ERROR_TAG for HID++ 2 is the value in ErrorTag
    ERROR_TAG = 0xFF
    FEATURE_ID = 0x00FF
    MSG_TYPE = TYPE.RESPONSE
    FUNCTION_INDEX = 0
    VERSION = (0,)
    
    class FID(HidppMessage.FID):
        """
        Field Identifiers
        """
        ERROR_TAG = 0xFD
        FEATURE_INDEX = 0xFC
        FUNCTION_ID = 0xFB
        SOFTWARE_ID = 0xFA
        ERROR_CODE = 0xF9
        ADD_INFO = 0xF8
        SEQUENCE_NUMBER_EXPECTED = ERROR_CODE - 1
        TRANSACTION_ERROR_RESERVED = ERROR_CODE - 1
        SEQUENCE_NUMBER_RECEIVED = SEQUENCE_NUMBER_EXPECTED - 1
    # end class FID

    class LEN(HidppMessage.LEN):
        """
        Field Lengths in bits
        """
        ERROR_TAG = 0x08
        ERROR_CODE = 0x08
        ADD_INFO = 0x08
        ADD_INFO_LONG = 0x68
        SEQUENCE_NUMBER_EXPECTED = 0x04
        SEQUENCE_NUMBER_RECEIVED = 0x04
        TRANSACTION_ERROR_RESERVED = 0x04
    # end class LEN

    class OFFSET(HidppMessage.OFFSET):
        """
        Field offset in bytes
        """
        ERROR_TAG = 0x02
        FEATURE_INDEX = 0x03
        FUNCTION_ID = 0x04
        SOFTWARE_ID = 0x05
        ERROR_CODE = 0x06
        ADD_INFO = 0x07
    # end class OFFSET
    
    NO_ERROR = 0                # Not an error
    UNKNOWN = 1                 # RESERVED, do not use
    INVALID_ARGUMENT = 2        # A parameter falls out of the accepted range for the hidpp function called
    OUT_OF_RANGE_OBSOLETE = 3   # This error code is not sent anymore [31/Oct/2013]. InvalidArgument is sent instead
    HW_ERROR = 4                # Indicates hardware issue. Ex. non-volatile memory corruption, bus access issue.
    NOT_ALLOWED = 5             # execution of function not allowed (used for forbidding use of debug functions)
    INVALID_FEATURE_INDEX = 6
    INVALID_FUNCTION_ID = 7
    BUSY = 8                    # Device (or receiver) cannot answer immediately to this request for any reason i.e:
    # - already processing a request from the same or another SW
    # - pipe full
    # - ...
    UNSUPPORTED = 9             # Error code used to indicate that a particular function is not yet supported.
    # This should only be returned by products under development. No official product should return this value.
    INVALID_DEVICE_INDEX = 10   # The device index is invalid. For corded devices only 0xFF is a valid device index.
    SEQUENCE_ERROR = 11  # The VLP packet contained an unexpected sequence number
    TRANSACTION_ERROR = 12  # The VLP packet does not match any ongoing VLP transaction sequence.
    OUT_OF_MEMORY = 13  # The VLP packet sequence has supplied more than expected data for invoked function of feature.
    MEMORY_BUSY = 14  # The required buffer for Tx or Rx the payload of invoked function cannot be currently allocated.

    CONST_FIELDS = (
        BitField(fid=FID.REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='Report ID',
                 name='reportId',
                 aliases=('report_id',),
                 default_value=HidppMessage.DEFAULT.REPORT_ID,
                 checks=(CheckHexList(LEN.REPORT_ID // 8),
                         CheckByte(),)),
        BitField(fid=FID.DEVICE_INDEX,
                 length=LEN.DEVICE_INDEX,
                 title='Device Index',
                 name='deviceIndex',
                 aliases=('device_index',),
                 checks=(CheckHexList(LEN.DEVICE_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.ERROR_TAG,
                 length=LEN.ERROR_TAG,
                 title='Error Tag',
                 name='errorTag',
                 aliases=('error_tag',),
                 checks=(CheckHexList(LEN.ERROR_TAG // 8),
                         CheckByte(),)),
        BitField(fid=FID.FEATURE_INDEX,
                 length=LEN.FEATURE_INDEX,
                 title='Feature Index',
                 name='featureIndex',
                 aliases=('feature_index',),
                 checks=(CheckHexList(LEN.FEATURE_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.FUNCTION_ID,
                 length=LEN.FUNCTION_ID,
                 title='Function Index',
                 name='functionIndex',
                 aliases=('function_index',),
                 checks=(CheckInt(0, pow(2, LEN.FUNCTION_ID) - 1),)),
        BitField(fid=FID.SOFTWARE_ID,
                 length=LEN.SOFTWARE_ID,
                 title='Software Id',
                 name='softwareId',
                 aliases=('software_id',),
                 checks=(CheckInt(0, pow(2, LEN.SOFTWARE_ID) - 1),)),
        BitField(fid=FID.ERROR_CODE,
                 length=LEN.ERROR_CODE,
                 title='Error Code',
                 name='errorCode',
                 aliases=('error_code',),
                 checks=(CheckHexList(LEN.ERROR_CODE // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral},),
        )

    FIELDS = deepcopy(CONST_FIELDS)

    def __init__(self, device_index, feature_index):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Feature Index
        :type feature_index: ``int``
        """
        super(ErrorCodes, self).__init__()

        self.device_index = device_index
        self.feature_index = feature_index
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        # See ``HidppMessage.fromHexList``
        cls.FIELDS = deepcopy(cls.CONST_FIELDS)
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        if inner_field_container_mixin.error_code == cls.SEQUENCE_ERROR:
            cls.FIELDS += (
                BitField(
                    fid=cls.FID.SEQUENCE_NUMBER_EXPECTED,
                    length=cls.LEN.SEQUENCE_NUMBER_EXPECTED,
                    title='SEQNExpected',
                    name='seqn_expected',
                    aliases=('seqn_exp',),
                    optional=True),
                BitField(
                    fid=cls.FID.SEQUENCE_NUMBER_RECEIVED,
                    length=cls.LEN.SEQUENCE_NUMBER_RECEIVED,
                    title='SEQNReceived',
                    name='seqn_received',
                    aliases=('seqn_rcv',),
                    optional=True),
            )
            inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        elif inner_field_container_mixin.error_code == cls.TRANSACTION_ERROR:
            cls.FIELDS += (
                BitField(
                    fid=cls.FID.TRANSACTION_ERROR_RESERVED,
                    length=cls.LEN.TRANSACTION_ERROR_RESERVED,
                    title='Reserved',
                    name='reserved',
                    optional=True),
                BitField(
                    fid=cls.FID.SEQUENCE_NUMBER_RECEIVED,
                    length=cls.LEN.SEQUENCE_NUMBER_RECEIVED,
                    title='SEQNReceived',
                    name='seqn_received',
                    aliases=('seqn_rcv',),
                    optional=True),
            )
            inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        # end if

        return inner_field_container_mixin
    # end def fromHexList
# end class ErrorCodes


Hidpp2ErrorCodes = ErrorCodes
VlpErrorCodes = ErrorCodes


class Hidpp1ErrorCodes(Hidpp1Message):
    """
    Error Codes implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || SubID                  || 8            ||
    || CommandSubId           || 8            ||
    || Register               || 8            ||
    || ErrorCode              || 8            ||

    Error codes defined:
    Code (hex) | Name                    | Description
    0          | ERR_SUCCESS             | No error / undefined
    1          | ERR_INVALID_SUBID       |  Invalid SubID / command
    2          | ERR_INVALID_ADDRESS     | Invalid address
    3*         | ERR_INVALID_VALUE       | Invalid value
    4          | ERR_CONNECT_FAIL        | Connection request failed (Receiver)
    5          | ERR_TOO_MANY_DEVICES    | Too many devices connected (Receiver)
    6          | ERR_ALREADY_EXISTS      | Already exists (Receiver)
    7          | ERR_BUSY                | Busy (Receiver)
    8          | ERR_UNKNOWN_DEVICE      | Unknown device (Receiver)
    9          | ERR_RESOURCE_ERROR      | Resource error (Receiver)
    A          | ERR_REQUEST_UNAVAILABLE | "Request not valid in current context" error
    B          | ERR_INVALID_PARAM_VALUE | Request parameter has unsupported value
    C          | ERR_WRONG_PIN_CODE      | the PIN code entered on the device was wrong
    D - FF     | Reserved                |
    """
    # ERROR_TAG for HID++ 1 is the value in SubID
    ERROR_TAG = 0x8F
    FEATURE_ID = 0x008F
    MSG_TYPE = TYPE.RESPONSE
    FUNCTION_INDEX = 0
    VERSION = (0,)

    ERR_SUCCESS = 0
    ERR_INVALID_SUBID = 1
    ERR_INVALID_ADDRESS = 2
    ERR_INVALID_VALUE = 3
    ERR_CONNECT_FAIL = 4
    ERR_TOO_MANY_DEVICES = 5
    ERR_ALREADY_EXISTS = 6
    ERR_BUSY = 7
    ERR_UNKNOWN_DEVICE = 8
    ERR_RESOURCE_ERROR = 9
    ERR_REQUEST_UNAVAILABLE = 10
    ERR_INVALID_PARAM_VALUE = 11
    ERR_WRONG_PIN_CODE = 12
    ERR_UNKNOWN = 13

    SUB_ID = Hidpp1Data.Hidpp1RegisterSubId.ERROR_MSG

    class FID(Hidpp1Message.FID):
        """
        Field Identifiers
        """
        COMMAND_SUB_ID = Hidpp1Message.FID.SUB_ID - 1
        REGISTER = COMMAND_SUB_ID - 1
        ERROR_CODE = REGISTER - 1
        PADDING = ERROR_CODE - 1
    # end class FID

    class LEN(Hidpp1Message.LEN):
        """
        Field Lengths in bits
        """
        COMMAND_SUB_ID = 0x08
        REGISTER = 0x08
        ERROR_CODE = 0x08
        PADDING = 0x08
    # end class LEN

    class OFFSET(Hidpp1Message.OFFSET):
        """
        Fields offset in bytes
        """
        COMMAND_SUB_ID = Hidpp1Message.OFFSET.SUB_ID + 1
        REGISTER = COMMAND_SUB_ID + 1
        ERROR_CODE = REGISTER + 1
        PADDING = ERROR_CODE + 1
    # end class OFFSET

    FIELDS = Hidpp1Message.FIELDS + (
        BitField(FID.COMMAND_SUB_ID,
                 LEN.COMMAND_SUB_ID,
                 title='CommandSubId',
                 name='command_sub_id',
                 checks=(CheckHexList(LEN.COMMAND_SUB_ID // 8), CheckByte(),)),
        BitField(FID.REGISTER,
                 LEN.REGISTER,
                 title='Register',
                 name='register',
                 aliases=('address',),
                 checks=(CheckHexList(LEN.REGISTER // 8), CheckByte(),)),
        BitField(FID.ERROR_CODE,
                 LEN.ERROR_CODE,
                 title='ErrorCode',
                 name='error_code',
                 aliases=('errorCode',),
                 conversions={HexList: Numeral},
                 checks=(CheckHexList(LEN.ERROR_CODE // 8), CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=Hidpp1Message.DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),)),
    )

    def __init__(self, device_index, command_sub_id, register, error_code):
        """
        Constructor
        """
        super().__init__()
        self.device_index = device_index
        self.sub_id = self.SUB_ID
        self.command_sub_id = command_sub_id
        self.register = register
        self.error_code = error_code
    # end def __init__
# class Hidpp1ErrorCodes

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
