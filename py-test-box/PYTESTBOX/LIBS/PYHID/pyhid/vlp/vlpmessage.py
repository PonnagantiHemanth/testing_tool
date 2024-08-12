#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.vlp.vlpmessage
:brief: VLP message format definition
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2023/07/10
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import TimestampedBitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class VlpMessageHeader(TimestampedBitFieldContainerMixin):
    """
    Define the common header format of all VLP commands.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportId                      8
    DeviceIdx                     8
    FeatureIdx                    8
    FunctionId                    4
    SoftwareId                    4
    Begin                         1
    End                           1
    Ack                           1
    Reserved                      1
    SequenceNumber                4
    ============================  ==========
    """
    FEATURE_ID = None
    MSG_TYPE = None
    VERSION = None
    ACK = 1
    NACK = 0

    class FID:
        """
        Field Identifiers
        """
        REPORT_ID = 0xFF
        DEVICE_INDEX = REPORT_ID - 1
        FEATURE_INDEX = DEVICE_INDEX - 1
        FUNCTION_ID = FEATURE_INDEX - 1
        SOFTWARE_ID = FUNCTION_ID - 1
        VLP_BEGIN = SOFTWARE_ID - 1
        VLP_END = VLP_BEGIN - 1
        VLP_ACK = VLP_END - 1
        VLP_RESERVED = VLP_ACK - 1
        VLP_SEQUENCE_NUMBER = VLP_RESERVED - 1
    # end class FID

    class LEN:
        """
        Field Lengths in bits
        """
        REPORT_ID = 8
        DEVICE_INDEX = 8
        FEATURE_INDEX = 8
        FUNCTION_ID = 4
        SOFTWARE_ID = 4
        VLP_BEGIN = 1
        VLP_END = 1
        VLP_ACK = 1
        VLP_RESERVED = 1
        VLP_SEQUENCE_NUMBER = 4
    # end class LEN

    class DEFAULT:
        """
        Fields Default values
        """
        REPORT_ID_NORMAL_VLP_MESSAGE = 0x13
        REPORT_ID_EXTENDED_VLP_MESSAGE = 0x14
        REPORT_ID = REPORT_ID_NORMAL_VLP_MESSAGE
        SOFTWARE_ID = 0xF  # Test value
        VLP_BEGIN = 1   # Default value for a single packet VLP transfer, most common use case
        VLP_END = 1     # Default value for a single packet VLP transfer, most common use case
        VLP_ACK = 1     # Default value to get an acknowledgment, a response or an error, most common use case
        VLP_SEQUENCE_NUMBER = 0x0
        PADDING = 0x00
        RESERVED = 0
    # end class DEFAULT

    REPORT_ID_LIST = [DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE, DEFAULT.REPORT_ID_EXTENDED_VLP_MESSAGE]

    FIELDS = (
        BitField(fid=FID.REPORT_ID,
                 length=LEN.REPORT_ID,
                 title='Report ID',
                 name='report_id',
                 aliases=('reportId',),
                 default_value=DEFAULT.REPORT_ID,
                 checks=(CheckHexList(LEN.REPORT_ID // 8), CheckByte(),)),
        BitField(fid=FID.DEVICE_INDEX,
                 length=LEN.DEVICE_INDEX,
                 title='Device Index',
                 name='device_index',
                 aliases=('deviceIndex',),
                 checks=(CheckHexList(LEN.DEVICE_INDEX // 8), CheckByte(),)),
        BitField(fid=FID.FEATURE_INDEX,
                 length=LEN.FEATURE_INDEX,
                 title='Feature Index',
                 name='feature_index',
                 aliases=('featureIndex',),
                 checks=(CheckHexList(LEN.FEATURE_INDEX // 8), CheckByte(),)),
        BitField(fid=FID.FUNCTION_ID,
                 length=LEN.FUNCTION_ID,
                 title='Function Index',
                 name='function_index',
                 aliases=('functionIndex',),
                 checks=(CheckInt(0, pow(2, LEN.FUNCTION_ID) - 1),)),
        BitField(fid=FID.SOFTWARE_ID,
                 length=LEN.SOFTWARE_ID,
                 title='Software Id',
                 name='software_id',
                 aliases=('softwareId',),
                 default_value=DEFAULT.SOFTWARE_ID,
                 checks=(CheckInt(0, pow(2, LEN.SOFTWARE_ID) - 1),)),
        BitField(fid=FID.VLP_BEGIN,
                 length=LEN.VLP_BEGIN,
                 title='VlpBegin',
                 name='vlp_begin',
                 aliases=('begin',),
                 default_value=DEFAULT.VLP_BEGIN,
                 checks=(CheckInt(0, pow(2, LEN.VLP_BEGIN) - 1),)),
        BitField(fid=FID.VLP_END,
                 length=LEN.VLP_END,
                 title='VlpEnd',
                 name='vlp_end',
                 aliases=('end',),
                 default_value=DEFAULT.VLP_END,
                 checks=(CheckInt(0, pow(2, LEN.VLP_END) - 1),)),
        BitField(fid=FID.VLP_ACK,
                 length=LEN.VLP_ACK,
                 title='VlpAck',
                 name='vlp_ack',
                 aliases=('ack',),
                 default_value=DEFAULT.VLP_ACK,
                 checks=(CheckInt(0, pow(2, LEN.VLP_ACK) - 1),)),
        BitField(fid=FID.VLP_RESERVED,
                 length=LEN.VLP_RESERVED,
                 title='VlpReserved',
                 name='vlp_reserved',
                 default_value=DEFAULT.RESERVED,
                 checks=(CheckInt(0, pow(2, LEN.VLP_RESERVED) - 1),)),
        BitField(fid=FID.VLP_SEQUENCE_NUMBER,
                 length=LEN.VLP_SEQUENCE_NUMBER,
                 title='VlpSequenceNumber',
                 name='vlp_sequence_number',
                 aliases=('seqn',),
                 default_value=DEFAULT.VLP_SEQUENCE_NUMBER,
                 checks=(CheckInt(0, pow(2, LEN.VLP_SEQUENCE_NUMBER) - 1),)),
    )

    HEADER_SIZE = sum([field.length for field in FIELDS])
    HEADER_SIZE_BYTES = HEADER_SIZE // 8
# end class VlpMessageHeader


VlpMessage = VlpMessageHeader


class VlpMessageRawPayload(VlpMessage):
    """
    Define the common format of all VLP commands.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    VLP Header                    40
    VLP Payload                   Variable length
    ============================  ==========
    """

    class FID(VlpMessage.FID):
        # See ``VlpMessageHeader.FID``
        VLP_PAYLOAD = VlpMessageHeader.FID.VLP_SEQUENCE_NUMBER - 1
    # end class FID

    FIELDS = VlpMessage.FIELDS + (
        BitField(fid=FID.VLP_PAYLOAD,
                 title='VlpPayload',
                 name='vlp_payload',
                 aliases=('payload',),
                 optional=True),)

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        # See ``TimestampedBitFieldContainerMixin.fromHexList``
        data = None
        if 'data' in kwargs:
            data = kwargs['data']
        elif len(args) > 0:
            data = args[0]
        # end if
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.get_field_from_name('vlp_payload').length = (len(data) -
                                                                                 VlpMessageHeader.HEADER_SIZE // 8)
        inner_field_container_mixin.vlp_payload = data[VlpMessageHeader.HEADER_SIZE // 8:]
        return inner_field_container_mixin
    # end def fromHexList
# end class VlpMessageRawPayload


class VlpMessageRaw(VlpMessageRawPayload):
    """
    Raw unparsed VLP message
    """
# end class VlpMessageRaw

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
