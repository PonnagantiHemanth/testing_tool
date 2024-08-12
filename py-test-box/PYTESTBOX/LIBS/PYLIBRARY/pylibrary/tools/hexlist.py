#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pylibrary.tools.hexlist

@brief  Hexadecimal buffer implementation

@author christophe Roquebert

@date   2018/09/11
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from array import array
from binascii import a2b_hex
from binascii import b2a_hex
from struct import pack
from traceback import extract_stack
from types import MethodType
import copy
import random
import warnings
from functools import reduce


# ------------------------------------------------------------------------------
# Implementation
# ------------------------------------------------------------------------------

class HexListError(Exception):
    """
    Exception handle for HexList
    """

    def __init__(self, msg):
        """
        Constructor

        @param  msg [in] (str) Message of the exception
        """
        super(HexListError, self).__init__(msg)
    # end def __init__


# end class HexListError

class HexListable(object):
    """
    Marker class for HexList compatibility.

    This class adds a contract on the following methods:
    - __hexlist__
    - fromHexList
    .
    """

    def __hexlist__(self):
        """
        Converts the current object to a HexList

        @return The current object, converted to its HexList form.
        """
        raise NotImplementedError()

    # end def __hexlist__

    @classmethod
    def fromHexList(cls, data, offset=0, length=None):
        """
        Creates a new instance of the object, parsed from HexList data.

        @param  data   [in] (HexList) the data to parse.
        @option offset [in] (int) The offset at which to start parsing.
        @option length [in] (int) The length of the data to parse.

        @return A new instance of the current type.
        """
        raise NotImplementedError()
    # end def fromHexList


# end class HexListable


# Knuth-Morris-Pratt string matching
# David Eppstein, UC Irvine, 1 Mar 2002
def KnuthMorrisPratt(text, pattern):  # pylint:disable=C0103
    r"""Yields all starting positions of copies of the pattern in the text.
Calling conventions are similar to string.find, but its arguments can be
lists or iterators, not just strings, it returns all matches, not just
the first one, and it does not need the whole text in memory at once.
Whenever it yields, it will have read the text exactly up to and including
the match that caused the yield.

    @param  text    [in] (str,list) List to research in
    @param  pattern [in] (str,list) SubList to research

    @return (int) Possible pattern position
    """

    # allow indexing into pattern and protect against change during yield
    pattern = list(pattern)

    # build table of shift amounts
    shifts = [1] * (len(pattern) + 1)
    shift = 1
    for pos in range(len(pattern)):
        while shift <= pos and pattern[pos] != pattern[pos - shift]:
            shift += shifts[pos - shift]
        # end while
        shifts[pos + 1] = shift
    # end for

    # do the actual search
    startPos = 0
    matchLen = 0
    for c in text:
        while matchLen == len(pattern) or \
                matchLen >= 0 and pattern[matchLen] != c:
            startPos += shifts[matchLen]
            matchLen -= shifts[matchLen]
        # end while
        matchLen += 1
        if matchLen == len(pattern):
            yield startPos
        # end if
    # end for


# end def KnuthMorrisPratt

kmp = KnuthMorrisPratt  # pylint:disable=C0103


class HexList(list, HexListable):
    """ The HexList object

    == Declaration ==

    An HexList object is a list of hexadecimal value. It's initialized with a
    nested sequences of type int, string representing a suite of hexadecimal
    values, and all type which its __str__ method return a string a suite of
    hexadecimal values

    @remark spaces in a string parameter are allowed.

    @code
    hexBuf = HexList(0xAA, 2, (1, 2, 3), [1, 2], "01 0203")
    @endcode
    is equivalent to
    @code
    hexBuf = HexList("AA020102030102010203")
    @endcode
    or
    @code
    hexBuf = HexList(0xAA, 2, 1, 2, 3, 1, 2, 1, 2, 3 )
    @endcode

    == methods ==

    || Operation            || String result        ||
    || h1 = HexList("0102") || "0102"               ||
    || h1 = h1 + "ABCD"     || "0102ABCD"           ||
    || h1 = h1 * 2          || "0102ABCD0102ABCD"   ||
    ||                      ||                      ||
    || h1[1]                || 2 (an int)           ||
    ||                      ||                      ||
    || h1[1] = 0xAA         || "01AA02ABCD0102ABCD" ||
    || h1[1:1] = "BB"       || "01BB02ABCD0102ABCD" ||

    == Attributes ==
    None

    == Messages and exceptions ==
    - at creation:
      - String representation of HexList is not even
      - No hexadecimal representation
      - Element is not a byte
      - Type of Element is unknown
    """

    __BYTE_RANGE = list(range(0, 256))

    DEBUG_ACTIVATE_IADD = True

    class Parser(object):
        """
        A Parser object, able to:
        - Identify if an object can be converted to HexList (actually: to a list of bytes)
        - Concatenate an object to a string of bytes
        """

        @staticmethod
        def accept(value):
            """
            Whether the parser can parse the value

            @param value [in] (object) The value to parse.
            @return True if the parser can parse the object
            """
            raise NotImplementedError

        # end def accept

        @staticmethod
        def parse(value, collector):
            """
            Parses the value, and append it to the collector.

            @param value [in] (object) The object to parse
            @param collector [in] (list) The list of bytes to extend
            """
            raise NotImplementedError
        # end def parse

    # end class Parser

    class StringParser(Parser):
        """
        A Parser dedicated to string processing.
        """

        @staticmethod
        def accept(value):
            """
            @copydoc pylibrary.tools.hexlist.HexList.Parser.accept
            """
            return isinstance(value, str) and (not hasattr(value, '__hexlist__'))

        # end def accept

        @staticmethod
        def parse(value, collector):
            """
            @copydoc pylibrary.tools.hexlist.HexList.Parser.parse
            """
            # The element is a string
            value = value.replace(' ', '')

            try:
                parseVal = array("B")
                parseVal.frombytes(a2b_hex(value))
                collector.extend(parseVal)
            except Exception as excp:
                raise HexListError("%s (%s)" % (excp, value))
            # end try
        # end def parse

    # end class StringParser

    class IntegerParser(Parser):
        """
        Parser dedicated to int and long processing
        """
        __BYTE_RANGE = list(range(0, 256))

        @staticmethod
        def accept(value):
            """
            @copydoc pylibrary.tools.hexlist.HexList.Parser.accept
            """
            return isinstance(value, int)

        # end def accept

        @classmethod
        def parse(cls, value, collector):  # pylint:disable=W0221
            """
            @copydoc pylibrary.tools.hexlist.HexList.Parser.parse
            """

            # The element is an integer or long
            if value not in cls.__BYTE_RANGE:
                raise HexListError("Element is not an unsigned byte (%s)!" % value)
            else:
                collector.append(value)
            # end if
        # end def parse

    # end class IntegerParser

    class HexListParser(Parser):
        """
        Parser dedicated to HexList type processing
        """

        @staticmethod
        def accept(value):
            """
            @copydoc pylibrary.tools.hexlist.HexList.Parser.accept
            """
            return isinstance(value, HexList)

        # end def accept

        @staticmethod
        def parse(value, collector):
            """
            @copydoc pylibrary.tools.hexlist.HexList.Parser.parse
            """
            collector.extend(value)
        # end def parse

    # end class HexListParser

    class HexListableParser(Parser):
        """
        Parser dedicated to __hexlist__ processing
        """

        @staticmethod
        def accept(value):
            """
            @copydoc pylibrary.tools.hexlist.HexList.Parser.accept
            """
            return hasattr(value, '__hexlist__') and (isinstance(value.__hexlist__, MethodType))

        # end def accept

        @staticmethod
        def parse(value, collector):
            """
            @copydoc pylibrary.tools.hexlist.HexList.Parser.parse
            """
            collector.extend(value.__hexlist__())
        # end def parse

    # end class HexListableParser

    class IterableParser(Parser):
        """
        Parser dedicated to __iter__ processing

        This MUST be at the end of the type tests.
        Otherwise, any object that implements both __hexlist__ and __iter__
        would be treated as iterable.
        """

        @staticmethod
        def accept(value):
            """
            @copydoc pylibrary.tools.hexlist.HexList.Parser.accept
            """
            return hasattr(value, '__iter__')

        # end def accept

        @staticmethod
        def parse(value, collector):
            """
            @copydoc pylibrary.tools.hexlist.HexList.Parser.parse
            """
            for subValue in value:
                collector.extend(HexList(subValue))
            # end for
        # end def parse

    # end class IterableParser

    class NoneParser(Parser):
        """
        Parser dedicated to None processing
        """

        @staticmethod
        def accept(value):
            """
            @copydoc pylibrary.tools.hexlist.HexList.Parser.accept
            """
            return value is None

        # end def accept

        @classmethod
        def parse(cls, value, collector):  # pylint:disable=W0221
            """
            @copydoc pylibrary.tools.hexlist.HexList.Parser.parse
            """
            pass
        # end def parse

    # end class NoneParser

    # ORDER IS IMPORTANT HERE !
    __PARSERS = (IntegerParser(),
                 StringParser(),
                 HexListParser(),
                 HexListableParser(),
                 IterableParser(),
                 NoneParser())

    def _getParser(self, value):
        """
        Obtains a parser for given value

        @param value [in] (object) The value to parse
        @return The parser, or raise an error if not found.
        """
        for parser in self.__PARSERS:
            if parser.accept(value):
                return parser
            # end if
        # end for
        raise HexListError("Type of Element is unknown (%s)!" % (value,))

    # end def _getParser

    def __init__(self, *initValue):  # pylint:disable=R0912
        """
        Constructor

        Initialization accepts a sequence of values

        @param  initValue [in] (tuple) sequence of data to merge in an HexList
        """
        glistVal = []

        for itemValue in initValue:
            parser = self._getParser(itemValue)
            parser.parse(itemValue, glistVal)
        # end for

        super(HexList, self).__init__(glistVal)
        self._readOnly = False

    # end def __init__

    def _checkReadOnly(self):
        """
        Checks whether the current object is read-only
        """
        if ((hasattr(self, '_readOnly'))
                and self._readOnly):
            raise HexListError('The current object is read-only')
        # end if

    # end def _checkReadOnly

    # --------------------------------------------------------------------------
    # list methods are re-implemented from here
    # --------------------------------------------------------------------------
    def __str__(self):
        """
        Convert an HexList into a string

        @return (str) String representation of HexList
        """
        return b2a_hex(pack('%dB' % (len(self),), *self)).upper().decode('utf8')

    # end def __str__

    def __repr__(self):
        """
        Converts an HexList to a string representation.

        @return (str) The HexList, as a string representation.
        """
        return "%s('%s')" % (self.__class__.__name__, self)

    # end def __repr__

    def __add__(self, hexBuf):
        """
        Concatenate two HexLists

        @param  hexBuf [in] (HexList) Elements to append to HexList

        @return new HexList
        """
        return HexList(self, hexBuf)

    # end def __add__

    def __iadd__(self, hexBuf):
        """
        Concatenate two HexLists

        @param  hexBuf [in] (HexList) Elements to append to HexList

        @return new HexList
        """
        if self.DEBUG_ACTIVATE_IADD and not self._readOnly:
            if not isinstance(hexBuf, HexList):
                hexBuf = HexList(hexBuf)
            # end if

            self.extendRaw(hexBuf)
            return self
        else:
            # default behavior
            return self.__add__(hexBuf)
        # end if

    # end def __iadd__

    def __getslice__(self, i,
                     j):
        """
        Get some elements of HexList

        @param  i [in] (int) Index of first element to get
        @param  j [in] (int) Index of element following last element to get

        @return elements of HexList
        """
        result = HexList()

        if i is None:
            i = 0
        # end if

        if j is None:
            j = len(self)
        # end if

        sl = slice(max(0, i), max(0, j), 1)
        result.extend(list.__getitem__(self, sl))
        return result

    # end def __getslice__

    def __setslice__(self, i,
                     j,
                     hexBuf):
        """
        Update some elements of HexList

        @param  i      [in] (int) Index of first element to update
        @param  j      [in] (int) Index of element following last element to update
        @param  hexBuf [in] (HexList,string) List of element to put in HexList
        """
        self._checkReadOnly()

        if not isinstance(hexBuf, HexList):
            hexBuf = HexList(hexBuf)
        # end if
        # list.__setslice__(self, i, j, hexBuf)
        sl = slice(max(0, i), max(0, j), 1)
        list.__setitem__(self, sl, hexBuf)

    # end def __setslice__

    def __getitem__(self, key):
        """
        Extract an element of HexList

        @param  key     [in] (int, slice) index (or slice) of the element to extract

        @return The extracted element.
        """
        result = super(HexList, self).__getitem__(key)

        if type(result) is list:
            value = HexList()
            value.extendRaw(result)
            result = value
        # end if

        return result

    # end def __getitem__

    def __setitem__(self, sl,
                    value):
        """
        Update of an element of HexList

        @param  sl      [in] (slice or int) index of the element to update
        @param  value   [in] (int) element to put in HexList
        """
        self._checkReadOnly()

        if isinstance(sl, int):
            endIndex = sl + 1
            if endIndex == 0: endIndex = len(self)
            # sl = slice(max(0, sl), max(0, sl)+1, 1)
            sl = slice(sl, endIndex, 1)
        # end if

        if not isinstance(sl, slice):
            raise TypeError('sl type shall be slice, not %s' % str(type(sl)))

        if not isinstance(value, HexList):
            value = HexList(value)
        # end if

        list.__setitem__(self, sl, value)

    # end def __setitem__

    def __mul__(self, value):
        """
        Duplication of HexList

        @param  value [in] (int) Number of iteration of HexList

        @return New HexList
        """
        result = HexList()
        result.extendRaw(list.__mul__(self, value))

        return result

    # end def __mul__

    def __xor__(self,
                value):
        """
        arithmetic @e xor of self with value

        @param  value [in] (HexList,string) operand

        @return (HexList) new HexList
        """
        hexBuf = HexList(value)
        if len(hexBuf) != len(self):
            warnings.warn('Both operands of a HexList AND should have the same length. Extending to the larger one.',
                          DeprecationWarning,
                          stacklevel=2)
        # end if

        minimum = min(len(self), len(hexBuf))
        for ind in range(-minimum, 0):
            list.__setitem__(hexBuf, ind, hexBuf[ind] ^ self[ind])
        # end for

        if len(self) > len(hexBuf):
            hexBuf[:0] = self[:-minimum]
        # end if

        return hexBuf

    # end def __xor__

    def __or__(self, value):
        """
        Arithmetic @e or of self with value

        @param  value [in] (HexList,string) operand

        @return (HexList) New HexList
        """
        hexBuf = HexList(value)
        if len(hexBuf) != len(self):
            warnings.warn('Both operands of a HexList AND should have the same length. Extending to the larger one.',
                          DeprecationWarning,
                          stacklevel=2)
        # end if

        minimum = min(len(self), len(hexBuf))
        for ind in range(-minimum, 0):
            hexBuf[ind] |= self[ind]
        # end for
        if len(self) > len(hexBuf):
            return HexList(self[0:-minimum], hexBuf)
        else:
            return hexBuf
        # end if

    # end def __or__

    def __and__(self, value):
        """
        Arithmetic @e and of self with value

        @param  value [in] (HexList,string) operand

        @return (HexList) New HexList

        @note   HexList(0x11, 0x22, 0x33) & HexList(0x02, 0x34) => HexList(0x02, 0x30)
                The result is not padded to greatest parameter
        """
        hexBuf = HexList(value)
        if len(hexBuf) != len(self):
            warnings.warn('Both operands of a HexList AND should have the same length. Truncating to the smaller one.',
                          DeprecationWarning,
                          stacklevel=2)
        # end if

        minimum = min(len(self), len(hexBuf))
        for ind in range(-minimum, 0):
            hexBuf[ind] &= self[ind]
        # end for
        if len(self) > len(hexBuf):
            return hexBuf
        else:
            return hexBuf[-minimum:]
        # end if

    # end def __and__

    def __invert__(self):
        """
        Arithmetic @e not of self

        @return (HexList) Invert of HexList
        """
        result = HexList(self)
        for ind in range(len(self)):
            list.__setitem__(result, ind, (~(self[ind])) & 0xFF)
        # end for
        return result

    # end def __invert__

    def __hexlist__(self):
        """
        Clone the current object to a new HexList

        @return (HexList) The current object, cloned to a new instance.
        """
        return HexList(self)

    # end def __hexlist__

    def __contains__(self, item):
        """
        Check item, element of list of elements, membership in self

        @param  item [in] (int,HexList) Element or list of elements to research

        @return (bool) Presence flag of item in self
        """
        result = False
        if isinstance(item, HexList):
            l2 = len(item)
            for i in kmp(self, item):
                if self[i: i + l2] == item:
                    return True
                # end if
            # end for
        else:
            result = super(HexList, self).__contains__(item)
        # end if
        return result

    # end def __contains__

    def index(self, x,
              i=0,
              j=-1):
        """
        Find item index of element or list of elements in self or part of self

        @param  x [in] (int,HexList) Element or list of elements to research
        @option i [in] (int) Min index
        @option j [in] (int) Max index

        @return (bool) Presence flag of item in self
        """
        result = 0
        if isinstance(x, HexList):
            l1 = len(self) if j == -1 else j
            l2 = len(x)
            for ind in kmp(self[i: l1], x):
                if self[ind: ind + l2] == x:
                    result = i + ind
                    break
                # end if
            else:
                raise ValueError('Pattern %s not found in %s'
                                 % (x, self[i: l1]))
            # end for
        else:
            result = super(HexList, self).index(x, i, j)
        # end if
        return result

    # end def index

    @classmethod
    def fromHexList(cls, data, offset=0, length=None):
        """
        @copydoc pylibrary.tools.hexlist.HexListable.fromHexList
        """
        if length is None:
            length = max(len(data) - offset, 0)
        # end if

        return cls(data[offset:offset + length])

    # end def fromHexList

    @classmethod
    def fromLong(cls, value, count, littleEndian=False):
        """
        Create an HexList, from the given value, with the specified number of bytes.

        Note: Handling longs and ints as an HexList is not advised.
              Use the Numeral class instead, which has better support of endianness,
              as well as support for arithmetical operations.

        @param value        [in] (long)    The value to convert
        @param count        [in] (int)     The number of bytes to use, or None to auto-size
        @param littleEndian [in] (bool) Whether the value is encoded as little-endian or big-endian
        @return A new HexList object, parsed from the parameter @c value, on @c count bytes.
        """

        result = HexList()

        # defensive cast: Compatible with __long__-enabled instances
        value = int(value)
        if value < 0:
            raise ValueError("Value must be equal or greater than zero")
        # end if

        if count is not None:

            if count < 1:
                raise ValueError("Count must be greater than zero")
            # end if

            for _ in range(count):
                result.insert(0, value & 0xFF)
                value = value >> 8
            # end for

        elif value:
            while value:
                result.insert(0, value & 0xFF)
                value = value >> 8
            # end while

        else:
            result.insert(0, 0x00)
        # end if

        if littleEndian:
            result.reverse()
        # end if

        return cls(result) if cls is not HexList else result

    # end def fromLong

    def insert(self, i,
               hexBuf):
        """
        Insert an element in the HexList

        @param  i      [in] (int) Index where to insert hexBuf
        @param  hexBuf [in] (HexList) HexList to insert
        """
        self._checkReadOnly()

        if i < 0:
            i += len(self)
        # end if

        if not isinstance(hexBuf, HexList):
            hexBuf = HexList(hexBuf)
        # end if

        sl = slice(max(0, i), max(0, i), 1)
        list.__setitem__(self, sl, HexList(hexBuf))

    # end def insert

    def extend(self, *hexBuf):
        """
        Extend of HexList

        @option hexBuf [in] (HexList,list,string) HexList to append
        """
        self._checkReadOnly()

        list.extend(self, HexList(*hexBuf))

    # end def extend

    def extendRaw(self, *seq):
        """
        Extends the current object, using the RAW supplied data.

        @option seq [in] (list) sequence of bytes to extend the object with.
        """
        self._checkReadOnly()

        list.extend(self, *seq)

    # end def extendRaw

    def append(self, value):
        """
        Appends a byte to the current object.

        This checks that the value is really a byte between 0 and 255, inclusive.

        @param  value [in] (int) Value to append, in range [0..255]
        """
        self._checkReadOnly()

        assert value in self.__BYTE_RANGE, \
            'Value %s (%s) is not an int in range [0..255]' % (value, type(value))

        list.append(self, value)

    # end def append

    def appendRaw(self, value):
        """
        Appends a raw value to the underlying list

        @param  value [in] (object) the value to append.
        """
        self._checkReadOnly()

        list.append(self, value)

    # end def appendRaw

    def copy(self):
        """
        Copy of HexList

        @return (HexList) A copy of the current object.
        """
        return copy.copy(self)

    # end def copy

    def testHexa(self, pos):
        """
        Test if pos is valid within the HexList length

        @param  pos [in] (int) position of a bit

        @return (int) offset of the byte this bit is present in HexList

        @note   pos = 0 => rightmost bit of the string
        """
        offset = len(self) - (pos // 8) - 1  # // floor division discards the fractional part

        if offset < 0:
            raise HexListError("Pos too high: %d" % (pos,))
        # end if

        return offset

    # end def testHexa

    def setBit(self, pos):
        """
        Set a bit at a given position in an HexList.

        @param  pos [in] (int) position of the bit to set

        @note pos = 0 => rightmost bit of the string
        """
        self._checkReadOnly()

        offset = self.testHexa(pos)
        self[offset] = self[offset] | (1 << pos % 8)

    # end def setBit

    def clearBit(self, pos):
        """
        Clear a bit at a given position in an HexList.

        @param  pos [in] (int) position of the bit to clear

        @note pos = 0 => right bit of the string
        """
        self._checkReadOnly()

        offset = self.testHexa(pos)
        self[offset] = self[offset] & (0xFF ^ (1 << pos % 8))

    # end def clearBit

    def updateBit(self, pos,
                  value):
        """
        Clear/Set a bit at a given position in an HexList.

        @param  pos   [in] (int) Position of the bit to clear
        @param  value [in] (0,1) Value of the bit (0 or 1)

        @note pos = 0 => right bit of the string
        """
        self._checkReadOnly()

        if value != 0 and value != 1:
            raise HexListError("%i is not supported as value (only 0 or 1) !"
                               % (value,))
        # end if

        if value == 0:
            self.clearBit(pos)
        else:
            self.setBit(pos)
        # end if

    # end def updateBit

    def testBit(self, pos):
        """
        Test a bit at a given position in an HexList.

        @param  pos [in] (int) position of the bit to test

        @return (bool) True if bit set

        @note pos = 0 => right bit of the string
        """
        offset = self.testHexa(pos)

        return (self[offset] & (1 << pos % 8)) != 0x00

    # end def testBit

    def invertBit(self, pos):
        """
        Invert a bit at a given position in an HexList.

        @param  pos [in] (int) Position of the bit to invert

        @note pos = 0 => right bit of the string
        """
        self._checkReadOnly()

        if self.testBit(pos):
            self.clearBit(pos)
        else:
            self.setBit(pos)
        # end if

    # end def invertBit

    def toLong(self, littleEndian=False):
        """
        Convert HexList to long

        @option littleEndian [in] (bool) Whether the HexList is to be interpreted as littleEndian or not.
                                         Defaults to False
        @return (long) value of HexList
        """
        if littleEndian:
            value = reversed(self)
        else:
            value = self
        # end if

        return reduce(lambda x=0, y=0: x * 256 + y, value, 0)

    # end def toLong
    hexToLong = toLong

    def toString(self):
        """
        Convert an HexList to a String

        @return (str) string
        """
        return ''.join([chr(x) for x in self])

    # end def toString

    @classmethod
    def fromString(cls, msg):
        """
        Create an HexList from a String

        @param  msg [in] (str) The string to convert from

        @return HexList
        """
        result = cls()
        if result._readOnly:  # pylint:disable=W0212
            result = cls((ord(c) for c in msg))
        else:
            result.extendRaw((ord(c) for c in msg))
        # end if

        return result

    # end def fromString

    def addPadding(self, size,
                   pattern=0,
                   fromLeft=True):
        """
        Append pattern until self size is length

        @param  size     [in] (int)     Final size of self
        @option pattern  [in] (HexList)  Pattern to append to self
        @option fromLeft [in] (bool) Append pattern to end
        """
        self._checkReadOnly()

        if size < len(self):
            raise HexListError("%d is smaller than initial HexList size (%d) !"
                               % (size, len(self)))
        # end if

        paddingSize = size - len(self)

        if not isinstance(pattern, HexList):
            pattern = HexList(pattern)
        # end if

        if fromLeft:
            self.insert(0, pattern * paddingSize)
        else:
            self.extend(pattern * paddingSize)
        # end if

    # end def addPadding

    def setReadOnly(self):
        """
        Sets this instance read-only.

        This replaces all mutable methods by a stub that raises an exception.
        """
        self._readOnly = True
    # end def setReadOnly

    def ascii_converter(self):
        """
        Converting HexList byte list into letter representation

        :return: The ascii string representation of the input value
        :rtype: ``str``
        """
        result = ''
        data_length = len(self)
        for i in range(data_length):
            if self[i] != 0:
                result += chr(self[i])
            # end if
        # end for
        return result
    # end def ascii_converter
# end class HexList


class RandHexList(HexList):
    """
    Create An HexList filled with random values
    """

    def __init__(self, size,
                 maxVal=255,
                 minVal=0):
        """
        Constructor

        @param  size   [in] (int) Size of RandHexList to create
        @option maxVal [in] (int) Maximum value of each bytes of generated rand, non-conlusive
        @option minVal [in] (int) Minimum value of each bytes of generated rand, inclusive
        """
        if size < 0:
            raise HexListError("Invalid size (%i)!" % (size,))
        # end if

        maxVal = min(255, maxVal)
        minVal = max(0, minVal)

        if maxVal < minVal:
            maxVal, minVal = minVal, maxVal
        # end if

        super(RandHexList, self).__init__()
        self.extendRaw([random.randint(minVal, maxVal) for _ in range(0, size)])
    # end def __init__


# end class RandHexList

class ReadOnlyHexList(HexList):
    """
    A Read-only implementation of the HexList class
    """

    def __init__(self, *values):
        """
        Constructor

        @option values [in] (tuple) Parent constructor parameters
        """
        super(ReadOnlyHexList, self).__init__(*values)

        self.__hash = None
        self.setReadOnly()

    # end def __init__

    def __hash__(self):
        """
        Computes a hash on the current object

        @return A has of the current object
        """
        if self.__hash is None:
            self.__hash = hash(tuple(self))
        # end if

        return self.__hash

    # end def __hash__

    def copy(self):
        """
        @copydoc pylibrary.tools.hexlist.HexList.copy
        """
        return self.__class__(self)
    # end def copy

# end class ReadOnlyHexList

# ------------------------------------------------------------------------------
#  END OF FILE
# ------------------------------------------------------------------------------
