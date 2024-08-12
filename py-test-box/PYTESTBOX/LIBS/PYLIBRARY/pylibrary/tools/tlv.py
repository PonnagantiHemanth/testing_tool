#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.tlv

@brief  TLV manager

@author christophe Roquebert

@date   2018/11/06
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import copy

from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ------------------------------------------------------------------------------
# Implementation
# ------------------------------------------------------------------------------
class TlvError(Exception):
    '''
    Exception handle for Tlv
    '''
    def __init__(self, msg):
        '''
        Constructor

        @param  msg [in] (str) Exception message
        '''
        super(TlvError, self).__init__(msg)
    # end def __init__
# end class TlvError

class Tlv(object):
    '''
    A Tlv object is a hexadecimal buffer V (HexList) associated with a tag T

    The Tlv object can be represented in compact, simple or Ber TLV.

    Methods:
    - __init__: Constructor
    - __str__: String representation of the Tlv
    - copy: Deep copy of the Tlv
    .

    Attributes:
    - tag (int) is the T value of the TLV
    - mode specifies the mode of representation for the L field :
      - COMPACT : Compact TLV
      - SIMPLE  : Simple TLV
      - BER_AUTO: Ber TLV (auto)
      - BER_0   : Ber TLV forced to Lg
      - BER_1   : Ber TLV forced to 81 Lg
      - BER_2   : Ber TLV forced to 82 Lg Lg
      .
    .

    Messages and exceptions:
    - Incompatible length with the type of TLV (%X)
    .
    '''

    BER_PREFIX             = "BER_"
    BER_MULTIBYTE_TAG_MASK = 0x1F
    BER_MOREBYTES_TAG_MASK = 0x80

    ##@name Tlv mode
    ##@{
    COMPACT  = 'COMPACT'           ##< TL (< 0x10)  V
    SIMPLE   = 'SIMPLE'            ##< T L          V
    BER_AUTO = BER_PREFIX + 'AUTO' ##< T auto-L     V
    BER      = BER_AUTO            ##< Same as BER_AUTO
    BER_0    = BER_PREFIX + '0'    ##< T L (< 0x80) V
    BER_1    = BER_PREFIX + '1'    ##< T 81 L       V
    BER_2    = BER_PREFIX + '2'    ##< T 82 L L     V
    ##@{

    ##@name Tlv mode
    ##@{
    COMPACT_MAX_LEN  = 0x10
    SIMPLE_MAX_LEN   = 0x100
    BER_0_MAX_LEN    = 0x80
    BER_1_MAX_LEN    = 0x100
    BER_2_MAX_LEN    = 0x10000
    ##@{

    def __init__(self, tag,
                       value = None,
                       mode  = SIMPLE):
        '''
        Constructor

        @param  tag     [in]  (int) from 0x01 to 0xFE
        @option value   [in]  (HexList) The TLV value
        @option mode    [in]  (int) by default #SIMPLE
        '''
        self._tag   = None
        self._value = None
        self._mode  = mode

        self.setTag(tag)
        self.setValue(value)
    # end def __init__

    def __str__(self):
        '''
        Convert a Tlv to a String

        @return (str) String representation
        '''
        if (self._mode == self.COMPACT):
            formatStr = "%X %X %s"
        elif (self._mode == self.SIMPLE):
            formatStr = "%02X %02X %s"
        elif (self._mode.startswith(self.BER_PREFIX)):
            if (self._mode == self.BER_AUTO):
                if (self.getLength() < self.BER_0_MAX_LEN):
                    lengthByteCount = 0
                else:
                    lengthByteCount = len(HexList(Numeral(self.getLength())))
                # end if
            else:
                lengthByteCount = int(self._mode[len(self.BER_PREFIX):])
            # end if

            tagByteCount    = len(HexList(Numeral(self.getTag())))
            if (lengthByteCount == 0):
                formatStr = "%%0%dX %%02X %%s" % (2*tagByteCount,)
            else:
                formatStr = "%%0%dX 8%d%%0%dX %%s" % (2*tagByteCount, lengthByteCount, 2*lengthByteCount,)
            # end if
        else:
            raise TlvError("Invalid encoding")
        # end if

        return formatStr % (self.getTag(), self.getLength(), self.getValue())
    # end def __str__

    def __len__(self):
        '''
        Get length of self

        @return (int) Length (in byte) of self
        '''
        return len(HexList(self))
    # end def __len__

    __repr__ = __str__

    def copy(self):
        '''
        Copy of Tlv

        @return (Tlv) a copy of the Tlv
        '''
        return copy.copy(self)
    # end def copy


    def getMode(self):
        '''
        Get the current Tlv mode

        @return mode
        '''
        return self._mode
    # end def getMode

    def setMode(self, mode):
        '''
        Get the new Tlv mode

        @param  mode [in] (int) #COMPACT .. #BER_2

        @exception TlvError if mode is incompatible with the current value length
        '''
        length = self.getLength()

        if (    (   (mode == self.COMPACT)
                and (length <  self.COMPACT_MAX_LEN))
            or  (   (mode == self.SIMPLE)
                and (length <  self.SIMPLE_MAX_LEN))
            or  (   (mode == self.BER_0)
                and (length <  self.BER_0_MAX_LEN))
            or  (   (mode == self.BER_1)
                and (length <  self.BER_1_MAX_LEN))
            or  (   (mode == self.BER_2)
                and (length <  self.BER_2_MAX_LEN))
            or  (    mode == self.BER_AUTO)):

            self._mode = mode
        else:
            raise TlvError("Tlv mode incompatible with value length")
        # end if
    # end def setMode

    mode = property(getMode, setMode)

    def getTag(self):
        '''
        Get the current Tlv tag

        @return tag
        '''
        return self._tag
    # end def getTag

    def setTag(self, tag):
        '''
        Set the new Tlv tag

        @param tag  [in] (int) The tag to set

        @exception TlvError if tag is incompatible with the current mode
        '''
        if (self._mode.startswith(self.BER_PREFIX)):

            # check for ASN.1 encoding rule on the TLV:
            tag, _ = self._parseBerTag(HexList(Numeral(tag)), 0, self._mode)
        # end if

        if  (   (tag < 0x01)
              or  (    (tag > 0xFE)
                   and (not self._mode.startswith(self.BER_PREFIX)))
              or  (    (self._mode == self.COMPACT)
                   and (tag > 0x0F))):
            raise TlvError("Invalid Tag: %d" % (tag,))
        # end if

        self._tag = tag
    # end def setTag

    tag = property(getTag, setTag)

    def getLength(self):
        '''
        Get the current value length

        @return length
        '''
        result = self._value
        if isinstance(result, (Tlv, TlvList)):
            result = HexList(result)
        # end if
        return len(result)
    # end def getLength

    def getTagLength(self):
        '''
        Get the (Tag, Length)

        @return HexList(tag, length)
        - COMPACT:  ((TL),())
        - SIMPLE:   ((T), (L))
        - BER_AUTO: Any of the following
        - BER_0:    ((T), (L))
        - BER_1:    ((T),(0x81, L))
        - BER_2:    ((T),(0x82, L, L))
        .
        '''
        if (self._mode == self.COMPACT):
            tag      = (self._tag * 0x10) + self.getLength()
            length   = None

        elif (self._mode == self.SIMPLE):
            tag    = self.getTag()
            length = self.getLength()

        elif (self._mode.startswith(self.BER_PREFIX)):
            if (self._mode == self.BER_AUTO):
                # Adapt the length to the data length
                if (self.getLength() < self.BER_0_MAX_LEN):
                    byteCount = 0
                else:
                    byteCount = len(HexList(Numeral(self.getLength(), fixedLength=True)))
                # end if
            else:
                byteCount = int(self._mode[len(self.BER_PREFIX)])
            # end if

            tag       = self.getTag()
            if (byteCount == 0):
                length = self.getLength()
                assert length < 0x80, "The length this BER TLV is restricted to 0x7F"
            else:
                length = HexList(0x80 + byteCount, Numeral(self.getLength(), byteCount, fixedLength=True))
                assert self.getLength() < (1 << (8*byteCount)), \
                       ("The length this BER TLV is restricted to 0x%%0%dX" % (2*byteCount)) % ((1 << (8*byteCount)) - 1)
            # end if
            tag = Numeral(tag, fixedLength=True)
        else:
            raise ValueError('Invalid mode')
        # end if

        return HexList(tag, length)
    # end def getTagLength

    def getValue(self):
        '''
        Get the current value

        @return value
        '''
        return self._value
    # end def getValue

    class CustomValue(object):
        '''
        Class used to prevent conversion of value into HexList in setValue method
        '''

    # end class CustomValue

    def setValue(self, value):
        '''
        Set the new value

        @param  value [in] (int, HexList) The value to set

        @exception TlvError if value length is incompatible with the current mode
        '''
        if (value is None):
            value = HexList()

        elif (isinstance(value, int)):
            value = HexList.fromLong(value, None)

        elif (isinstance(value, (Tlv, TlvList, Tlv.CustomValue))):
            pass

        else:
            value = HexList(value)
        # end if

        if (( (self._mode == self.COMPACT)
                and (len(value) <  self.COMPACT_MAX_LEN))
            or  (   (self._mode == self.SIMPLE)
                and (len(value) <  self.SIMPLE_MAX_LEN))
            or  (   (self._mode == self.BER_0)
                and (len(value) <  self.BER_0_MAX_LEN))
            or  (   (self._mode == self.BER_1)
                and (len(value) <  self.BER_1_MAX_LEN))
            or  (   (self._mode == self.BER_2)
                and (len(value) <  self.BER_2_MAX_LEN))
            or  (   (self._mode == self.BER_AUTO))):

            self._value  = value
        else:
            raise TlvError("Incompatible value length with the TLV mode")
        # end if
    # end def setValue

    value = property(getValue, setValue)

    @classmethod
    def _parseBerTag(cls, data, offset, mode):
        '''
        Extract a tag from a HexList, according to the specified encoding

        Note that the _full_ tag is extracted, further processing is required
        to extract the tag number part of the tag.

        @param  data   [in] (HexList) The data to extract the value from
        @param  offset [in] (int)    The offset at which to start extracting the TLV
        @param  mode   [in] (str)    The mode in which to extract the data

        @return A tuple(tag, bytecount)
        '''

        assert mode.startswith(cls.BER_PREFIX), "Mode is not one of the allowed BER modes"
        result = HexList(data[offset])


        # If bits 5 to 1 are all set to 1, the tag field continues on one or
        # more subsequent bytes
        # Bit 8 of each subsequent byte shall be set to 1, unless it is the
        #  last subsequent byte.
        # Bits 7 to 1 of the first subsequent byte shall not be all set to 0.
        # Bits 7 to 1 of the first subsequent byte, followed by bits 7 to 1
        #  of each further subsequent byte, up to and including bits 7 to 1
        #  of the last subsequent byte encode a tag number.
        if ((data[offset] & cls.BER_MULTIBYTE_TAG_MASK) == cls.BER_MULTIBYTE_TAG_MASK):

            firstByte = True
            offset += 1
            if (offset >= len(data)):
                raise TlvError("Tlv tag out of buffer bounds")
            # end if

            while (data[offset] & cls.BER_MOREBYTES_TAG_MASK):
                # This is a subsequent byte
                if (firstByte):
                    # This value is prohibited for the first subsequent byte
                    assert (data[offset] & ~(cls.BER_MOREBYTES_TAG_MASK)), \
                        "Incorrect subsequent byte value: 0x%02X" % data[offset]
                # end if

                result.append(data[offset])
                firstByte = False
                offset += 1
                if (offset >= len(data)):
                    raise TlvError("Tlv tag out of buffer bounds")
                # end if
            # end while
            result.append(data[offset])
        # end if

        return (int(Numeral(result)), len(result))
    # end def _parseBerTag

    @classmethod
    def _parseBerLength(cls, data, offset, mode):
        '''
        Extract a length from a HexList, according to the specified encoding

        @param  data   [in] (HexList) The data to extract the value from
        @param  offset [in] (int)    The offset at which to start extracting the TLV
        @param  mode   [in] (str)    The mode in which to extract the data

        @return A tuple (parsed length, byte encoding count)
        '''
        assert mode.startswith(cls.BER_PREFIX), "Mode is not one of the allowed BER modes"

        firstByte = data[offset]
        if (firstByte <= 0x7F):
            result = firstByte
            encodingLength = 1
        elif (firstByte == 0x80):
            raise TlvError('The 0x80 length specified is not supported')
        else:
            byteCount =  (firstByte & 0x7F)
            if (mode == cls.BER_AUTO):
                expectedByteCount = byteCount # No check
            else:
                expectedByteCount = int(mode[len(cls.BER_PREFIX)])
            # end if

            if (byteCount != expectedByteCount):
                raise TlvError("Length byte count does not match the BER type")
            # end if
            result = int(Numeral(data[offset+1:offset+1+byteCount], byteCount))
            encodingLength = byteCount + 1
        # end if

        return (result, encodingLength)
    # end def _parseBerLength

    @classmethod
    def _parse(cls, data, mode):
        '''
        Parse an HexList to extract a Tlv suite

        @param  data [in] (HexList) The buffer to parse
        @param  mode [in] (int) The mode of the TLV to be parsed

        @return (tagOffset, length, valueOffset) list
        '''

        result      = []
        try:
            offset   = 0
            while (offset < len(data)):

                if (mode == Tlv.COMPACT):

                    # tag         = (data[offset] >> 4)    # Tag in bits 8..5 of the first byte
                    length      = data[offset] & 0x0F    # Length in bits 4..1 of the first byte
                    valOffset   = offset + 1             # Data follows

                elif (mode == Tlv.SIMPLE):
                    # tag         = data[offset]           # Tag in the first byte
                    length      = data[offset+1]         # Length in the second byte
                    valOffset   = offset + 1 + 1         # Data follows

                elif (mode.startswith(cls.BER_PREFIX)):
                    _, tagByteCount = cls._parseBerTag(data, offset, mode)

                    length, lenByteCount = cls._parseBerLength(data,
                                                            offset+tagByteCount,
                                                            mode)

                    valOffset = offset + tagByteCount + lenByteCount
                else:
                    raise TlvError("Invalid TLV data")
                # end if

                result.append((offset, length, valOffset))
                offset += length
            # end while
        except IndexError:
            raise TlvError("Invalid TLV data")
        # end try

        return result
    # end def _parse


    @classmethod
    def fromHexList(cls, data,
                        offset = 0,
                        mode   = SIMPLE):
        '''
        Build a Tlv from an HexList

        @param  data   [in] (HexList) The data to parse
        @option offset [in] (int) The offset at which to parse the data
        @option mode   [in] (int) The mode for parsing the HexList

        @return Tlv

        @exception  TlvError if invalid data
        '''
        if (not isinstance(data, HexList)):
            data = HexList(data)
        # end if

        if (len(data) == 0):
            raise TlvError("Invalid TLV data")
        # end if

        if (mode == Tlv.COMPACT):

            tag         = (data[offset] >> 4)    # Tag in bits 8..5 of the first byte
            length      = data[offset] & 0x0F    # Length in bits 4..1 of the first byte
            valOffset   = offset + 1             # Data follows

        elif (mode == Tlv.SIMPLE):
            tag         = data[offset]           # Tag in the first byte
            length      = data[offset+1]         # Length in the second byte
            valOffset   = offset + 1 + 1         # Data follows

        elif (mode.startswith(cls.BER_PREFIX)):
            tag, tagByteCount = cls._parseBerTag(data, offset, mode)

            length, lenByteCount = cls._parseBerLength(data,
                                                    offset+tagByteCount,
                                                    mode)

            valOffset = offset + tagByteCount + lenByteCount
        else:
            raise TlvError("Invalid TLV mode")
        # end if

        if (valOffset+length > len(data)):
            raise TlvError("Not enough data to parse the TLV")
        # end if

        return cls(tag,
                   data[valOffset:valOffset+length],
                   mode)
    # end def fromHexList

    def __hexlist__(self):
        '''
        Converts the Tlv into an HexList

        @return (HexList) The current object as an HexList
        '''
        return HexList(self.getTagLength(), self._value)
    # end def __hexlist__

    def __eq__(self, other):
        '''
        Check equality between self and other

        @param  other [in] (Tlv) Other to compare with

        @return (bool) Equality result
        '''
        result = isinstance(other, self.__class__)

        if result:
            result = (HexList(self) == HexList(other))
        # end if

        return result
    # end def __eq__

# end class Tlv


class TlvList(list):
    '''
    List of Tlv
    '''

    def __init__(self, *tlvs):
        '''
        Constructor

        @option tlvs [in] (tuple) List of Tlv
        '''
        sequence = []

        # Parameter of type list of Tlv
        for tlv in tlvs:

            # Parameter of type Tlv
            if (isinstance(tlv, Tlv)):
                sequence.append(tlv)

            elif (isinstance(tlv, list)):
                # Parameter of type list
                sequence.extend(tlv)
            else:
                # Unknown type
                raise TlvError("%s is not a supported type !" \
                             % (tlv.__class__.__name__,))
            # end if
        # end for

        super(TlvList, self).__init__(sequence)
    # end def __init__

    def __str__(self):
        '''
        Convert the TlvList into a string

        @return String representation
        '''
        return ' '.join([str(tlv) for tlv in self])
    # end def __str__

    __repr__ = __str__

    def __contains__(self, tag):
        '''
        Search of a tag in TlvBuf

        @param  tag [in] (int) Tag to search

        @return True if tag found
        '''
        for tlv in self:
            if (tlv.getTag() == tag):
                return True
            # end if
        # end for
        return False
    # end def __contains__

    def copy(self):
        '''
        Copy all the content of TlvList

        @return copy of TlvList
        '''
        return TlvList([x.copy() for x in self])
    # end def copy


    def __hexlist__(self):
        '''
        Convert a TlvList to an HexList

        @return (HexList)
        '''
        return HexList([HexList(tlv) for tlv in self])
    # end def __hexlist__

    @staticmethod
    def fromHexList(data, mode = Tlv.SIMPLE):
        '''
        Build a TlvList from an HexList

        @param  data [in] (HexList) The data to parse
        @option mode [in] (int) The mode of the TLV

        @return TlvList

        @exception  TlvError if invalid data
        '''
        if (not isinstance(data, HexList)):
            data  = HexList(data)
        # end if

        result = []
        if (len(data) > 0):
            offset = 0
            while (offset < len(data)):
                tlv = Tlv.fromHexList(data, offset, mode)
                offset += len(tlv.getTagLength()) + len(tlv.getValue())

                result.append(tlv)
            # end while
        # end if

        return TlvList(*result)
    # end def fromHexList

# end class TlvList

# ------------------------------------------------------------------------------
#  END OF FILE
# ------------------------------------------------------------------------------
