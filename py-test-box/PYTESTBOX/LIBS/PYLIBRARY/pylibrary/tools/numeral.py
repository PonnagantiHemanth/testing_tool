#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.numeral

@brief Numeral handles an integer, that can be converted to and from an HexList

@author christophe.roquebert

@date   2018/04/20
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist          import HexList
from functools                       import total_ordering
from random                          import randint


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
def to_int(value, little_endian=False):
    """
    Transform a value to an ``int`` format

    :param value: Value to transform to ``int``
    :type value: ``HexList`` or ``Numeral`` or ``int`` or ``long``
    :param little_endian: Flag indicating if the value is in little endian (``False`` means big endian) - OPTIONAL
    :type little_endian: ``bool``

    :return: ``int`` format of the given value
    :rtype: ``int``
    """
    return int(Numeral(value, littleEndian=little_endian))
# end def to_int


def to_endian_list(value, byte_count=None, little_endian=False):
    """
    Transform a value to a ``list`` format with a wanted endian representation

    :param value: Value to transform to ``int``
    :type value: ``HexList`` or ``Numeral`` or ``int`` or ``long``
    :param byte_count: Number of byte to represent, if ``None`` it will be automatically decided - OPTIONAL
    :type byte_count: ``int`` or ``None``
    :param little_endian: Flag indicating if little endian format is requested, if ``False`` big endian will be
                          used - OPTIONAL
    :type little_endian: ``bool``

    :return: List of bytes converted into ``int``
    :rtype: ``list[int]``
    """
    return list(Numeral(source=value, byteCount=byte_count, littleEndian=little_endian, fixedLength=True))
# end def to_endian_list


@total_ordering
class Numeral(object):                                                                                                   # pylint:disable=R0924
    '''
    The Numeral class represents a @b number, that can be converted to and from
    an Hexadecimal representation, in a way similar to an HexList.

    The compatibilities with the HexList class are limited to:
     - The constructor
     - fromHexList
     - __hexlist__

    Note that concatenation (+) and multiplication (*) applicable to an HexList
    will not work on a Numeral, and will behave as the standard addition and
    multiplication on numbers.

    In order to perform checks, it is the left-hand operand that is the reference.

    Example:
    @code
    num1 = Numeral(0x1234, fixedLength=False)
    num2 = Numeral(0xFFFF, fixedLength=True)

    # This will work
    result = num1 + num2

    # This will raise an exception
    result = num2 + num1
    @endcode

    '''

    def __init__(self, source       = None,                                                                             # pylint:disable=R0912
                       byteCount    = None,
                       littleEndian = None,
                       fixedLength  = None):
        '''
        Builds a new Numeral.

        By default, the Numeral is 0-length, and its value is 0

        @param source       [in] (HexList,Numeral,int,long) The value to be converted as an Numeral
        @param byteCount    [in] (int) The number of bytes to use as the hexadecimal representation.
                                    Automatically defined if not specified.
        @param littleEndian [in] (bool) Whether the hexadecimal representation will be bigEndian or littleEndian.
        @param fixedLength  [in] (bool) Will cause an exception if any operation
                                          grows the Numeral beyond its byteCount.
        '''

        # Simple conversions
        source = source.__numeral__() if hasattr(source, '__numeral__')   else source
        source = HexList(source)      if isinstance(source, str) else source

        # The value is parsed, depending on the source type
        if (isinstance(source, Numeral)):
            # We do not need to parse further, but rather implement a copy constructor
            self.value = source.value

            # If overridden values are specified, use them, otherwise copy them
            # from the other object.
            if (byteCount is None):
                byteCount = source.byteCount
            # end if
            if (littleEndian is None):
                littleEndian = source.littleEndian
            # end if
            if (fixedLength is None):
                fixedLength = source.fixedLength
            # end if

        elif (isinstance(source, int)):

            # source is a python integer or long
            if (byteCount is not None):
                # Check that the supplied value is in the correct boundaries
                assert (1 << (byteCount * 8)) > source, \
                       "The supplied value %d is encoded on more than %d bytes" % (source, byteCount)
            # end if
            if (    (fixedLength)
                and (byteCount is None)):

                byteCount = 1
                while not ((1 << (byteCount * 8)) > source):
                    byteCount += 1
                # end while
            # end if

            self.value = int(source)

        elif (isinstance(source, HexList)):

            # source is an HexList
            hexValue = source

            if (byteCount is not None):
                assert (len(source) <= byteCount), \
                       "The supplied value %s is encoded in more than %d bytes" % (source, byteCount)
            # end if

            if (    (fixedLength)
                and (byteCount is None)):
                byteCount = len(source)
            # end if

            if (littleEndian):
                hexValue = HexList(source)
                hexValue.reverse()
            # end if

            self.value = hexValue.toLong()
        elif (source is None):
            self.value = 0
        else:
            raise ValueError("Invalid type %s" % (type(source),))
        # end if

        self.byteCount    = byteCount
        self.littleEndian = littleEndian
        self.fixedLength  = fixedLength
    # end def __init__

    def _checkAndAssign(self, value):
        '''
        Assigns a new value to this Numeral, after checking the value consistency

        @param value [in] (int) The new value
        '''
        assert (value >= 0), ValueError('Value should be a positive integer')

        if (self.fixedLength):
            if (self.byteCount is not None):
                assert (value < (1 << (self.byteCount * 8))), ValueError('Value is encoded on more than %d bytes: 0x%X' % (self.byteCount, value))
            # end if
        # end if

        self.value = value
    # end def _checkAndAssign


    def __getitem__(self, key):
        '''
        Obtains the item (or slice) for the given key.

        If key is an integer, then a byte is returned, that matches the byte
        at the key offset in HexList conversion.

        If key is a slice, then the converted HexList is used to access the
        object.

        @note The current implementationis non-optimal, resulting in too many
              intermediate objects.

        @param key [in] (int, slice) The key at which to get the element.
        @return int (if key is int) or HexList (if key is slice) of the extracted element.
        '''

        return HexList(self).__getitem__(key)
    # end def __getitem__

    def __setitem__(self, key, value):
        '''
        Sets the item (or slice) for the given key.

        If key is an integer, the element is replaced by the value argument,
        which is converted to HexList beforehand, and must then be 1-byte long.

        Note that this may expand the current Numeral beyond the boundaries.

        @param key [in] (int, slice) The key at which to get the element.
        @param value [in] (int, HexList) The value to replace with.
        '''

        if isinstance(key, int):
            if isinstance(value, HexList):
                pass # Will be checked later
            elif isinstance(value, int):
                assert value in range(256), 'Value must be in range [0..255]'
            else:
                value = HexList(value)
            # end if

            if isinstance(value, HexList):
                assert (len(value) == 1), 'Value must be exactly 1 byte long'
                value = value[0]
            # end if
        # end if

        temp = HexList(self)
        temp.__setitem__(key, value)
        temp = Numeral(temp,
                      byteCount    = self.byteCount,
                      littleEndian = self.littleEndian,
                      fixedLength  = self.fixedLength)
        self.value = temp.value
    # end def __setitem__

    def __setslice__(self,
                     i,
                     j,
                     hexBuf):
        '''
        Update some elements of HexList

        @param  i       [in] (int) Index of first element to update
        @param  j       [in] (int) Index of element following last element to update
        @param  hexBuf  [in] (HexList,string) List of element to put in HexList
        '''
        temp = HexList(self)
        temp[i:j] = hexBuf
        temp = Numeral(temp,
                      byteCount    = self.byteCount,
                      littleEndian = self.littleEndian,
                      fixedLength  = self.fixedLength)
        self.value = temp.value
    # end def __setslice__

    def __hexlist__(self):
        '''
        Converts the current object to an HexList

        @return The HexList representation of the current object.
        '''

        result = HexList()

        value = self.value

        if (self.byteCount is not None):
            for _ in range(self.byteCount):
                result.insert(0, value & 0xFF)
                value = value >> 8
            # end for
        else:
            assert (value >= 0), "Negative values cannot be converted to HexList without specifying a byte count."
            if (value == 0):
                result.append(0)
            # end if

            while (value != 0):
                result.insert(0, value & 0xFF)
                value = value >> 8
            # end while
        # end if

        if (self.littleEndian):
            result.reverse()
        # end if

        return result
    # end def __hexlist__

    @staticmethod
    def fromHexList(value, offset = 0,
                          length = None):
        '''
        Creates a new Numeral from an HexList

        The create Numeral is big endian, with a fixed length set to the number of read bytes.

        @param value  [in] (HexList) The HexList to parse
        @param offset [in] (int) The offset at which to start parsing.
        @param length [in] (int) The length to parse.
                           Defaults to the remaining length of the buffer if unspecified.
        @return A new Numeral, build from the given value
        '''

        if (length is None):
            length = len(value) - offset
        # end if

        result = Numeral(value[offset:offset+length], length, False, True)

        return result
    # end def fromHexList

    @staticmethod
    def __intValue(other):
        '''
        Obtains the int value of an input.
        This also checks that the input if of a size compatible with the current object.

        @param other [in] (object) The input to parse
        @return The input's int value
        '''
        if isinstance(other, int):
            return other
        elif isinstance(other, Numeral):
            return other.value
        else:
            return Numeral(other).value
        # end if
    # end def __intValue

    def __add__(self, other):
        '''
        Creates a new Numeral, containing the addition of the current Numeral
        with the supplied one.

        @param      other [in] (Numeral, int, long) The value to add
        @return     The result of the addition
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        result = Numeral(self.value + value,
                        byteCount    = self.byteCount,
                        fixedLength  = self.fixedLength,
                        littleEndian = self.littleEndian)

        return result
    # end def __add__

    def __iadd__(self, other):
        '''
        Updates the current Numeral, with the addition of the current Numeral
        and the supplied one.

        @param      other [in] (Numeral, int, long) The value to add
        @return     The result of the addition (self)
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        self._checkAndAssign(self.value + value)

        return self
    # end def __iadd__

    def __sub__(self, other):
        '''
        Creates a new Numeral, containing the subtraction of the current Numeral
        with the supplied one.

        @param other [in] (Numeral, int, long) The value to subtract
        @return The result of the addition
        @exception ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)
        value = self.value - value

        assert value >= 0, "Negative result for subtraction: %d" % (value,)

        result = Numeral(value,
                        byteCount    = self.byteCount,
                        fixedLength  = self.fixedLength,
                        littleEndian = self.littleEndian)

        return result
    # end def __sub__

    def __isub__(self, other):
        '''
        Updates the current Numeral, with the subtraction of the current Numeral
        and the supplied one.

        @param      other [in] (Numeral, int, long) The value to add
        @return     The result of the subraction (self)
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        self._checkAndAssign(self.value - value)

        return self
    # end def __isub__

    def __mul__(self, other):
        '''
        Creates a new Numeral, containing the multiplication of the current Numeral
        with the supplied one.

        @param      other [in] (Numeral, int, long) The value to multiply
        @return     The result of the multiplication
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        result = Numeral(self.value * value,
                        byteCount    = self.byteCount,
                        fixedLength  = self.fixedLength,
                        littleEndian = self.littleEndian)

        return result
    # end def __mul__

    def __imul__(self, other):
        '''
        Updates the current Numeral, with the multiplication of the current Numeral
        and the supplied one.

        @param      other [in] (Numeral, int, long) The value to add
        @return     The result of the multiplication (self)
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        self._checkAndAssign(self.value * value)

        return self
    # end def __imul__

    def __div__(self, other):
        '''
        Creates a new Numeral, containing the division of the current Numeral
        with the supplied one.

        @param      other [in] (Numeral, int, long) The value to divide by
        @return     The result of the multiplication
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        result = Numeral(self.value / value,
                        byteCount    = self.byteCount,
                        fixedLength  = self.fixedLength,
                        littleEndian = self.littleEndian)

        return result
    # end def __div__

    def __idiv__(self, other):
        '''
        Updates the current Numeral, with the division of the current Numeral
        and the supplied one.

        @param      other [in] (Numeral, int, long) The value to add
        @return     The result of the division (self)
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        self._checkAndAssign(self.value / value)

        return self
    # end def __idiv__

    def __mod__(self, other):
        '''
        Creates a new Numeral, containing the modulus of the current Numeral
        with the supplied one.

        @param      other [in] (Numeral, int, long) The value to use for the modulus
        @return     The result of the modulus
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        result = Numeral(self.value % value,
                        byteCount    = self.byteCount,
                        fixedLength  = self.fixedLength,
                        littleEndian = self.littleEndian)

        return result
    # end def __mod__

    def __imod__(self, other):
        '''
        Updates the current Numeral, with the modulus of the current Numeral
        and the supplied one.

        @param      other [in] (Numeral, int, long) The value to add
        @return     The result of the modulus (self)
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        self._checkAndAssign(self.value % value)

        return self
    # end def __imod__

    def __divmod__(self, other):
        '''
        Creates two new Numerals, containing the division and modulus of the current Numeral
        with the supplied one.

        @param      other [in] (Numeral, int, long) The value to divide by
        @return     The result of the multiplication
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        rDiv, rMod = divmod(self.value, value)

        result = (Numeral(rDiv,
                         byteCount    = self.byteCount,
                         fixedLength  = self.fixedLength,
                         littleEndian = self.littleEndian),
                  Numeral(rMod,
                         byteCount    = self.byteCount,
                         fixedLength  = self.fixedLength,
                         littleEndian = self.littleEndian))
        return result
    # end def __divmod__

    def __invmod__(self, other):
        '''
        Computes the modular inverse of self with other.

        @param other [in] (Numeral, int, long) The modulus
        @return The modular inverse, None if not defined
        '''
        def egcd(_a, _b):
            '''
            Returns a triple (g, x, y) such that a x + b y = g = gcd(a, b).
            Assumes a, b >= 0

            @param _a [in] (int) first integer
            @param _b [in] (int) second integer
            @return (g, x, y)
            '''
            if _a == 0:
                return (_b, 0, 1)
            else:
                _g, y, x = egcd(_b % _a, _a)
                return (_g, x - (_b // _a) * y, y)
            # end if
        # end def egcd

        _a = self.value
        _m = self.__intValue(other)

        _g, x, _ = egcd(_a, _m)
        if _g != 1:
            raise ValueError('No modular inverse for %s and %s' % (self, other))
        # end if

        return Numeral(x % _m,
                      byteCount    = self.byteCount,
                      fixedLength  = self.fixedLength,
                      littleEndian = self.littleEndian)
    # end def __invmod__

    def __pow__(self, other):
        '''
        Computes self to the power of other.

        @param      other [in] (Numeral, int, long) The value to put to the power of
        @return     The result of the power
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        result = Numeral(pow(self.value, value),
                        byteCount    = self.byteCount,
                        fixedLength  = self.fixedLength,
                        littleEndian = self.littleEndian)
        return result
    # end def __pow__

    def __ipow__(self, other):
        '''
        Updates the current Numeral, with the power of the current Numeral
        and the supplied one.

        @param      other [in] (Numeral, int, long) The value to add
        @return     The result of the power (self)
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        self._checkAndAssign(self.value ** value)

        return self
    # end def __ipow__


    def __floordiv__(self, other):
        '''
        Computes the floored division of self by other.

        @param      other [in] (Numeral, int, long) The value to divide with
        @return     The result of the division
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        result = Numeral(self.value // value,
                        byteCount    = self.byteCount,
                        fixedLength  = self.fixedLength,
                        littleEndian = self.littleEndian)
        return result
    # end def __floordiv__

    def __ifloordiv__(self, other):
        '''
        Updates the current Numeral, with the floor division of the current Numeral
        and the supplied one.

        @param      other [in] (Numeral, int, long) The value to add
        @return     The result of the floor division (self)
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        self._checkAndAssign(self.value // value)

        return self
    # end def __ifloordiv__

    def __rshift__(self, other):
        '''
        Creates a new Numeral, containing the current Numeral right-shifted by the supplied amount.

        @param      other [in] (Numeral, int, long) The value to shift by
        @return     The result of the shift
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        result = Numeral(self.value >> value,
                        byteCount    = self.byteCount,
                        fixedLength  = self.fixedLength,
                        littleEndian = self.littleEndian)

        return result
    # end def __rshift__

    def __irshift__(self, other):
        '''
        Updates the current Numeral, with the right shift of the current Numeral
        and the supplied one.

        @param      other [in] (Numeral, int, long) The value to add
        @return     The result of the right shift (self)
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        self._checkAndAssign(self.value >> value)

        return self
    # end def __irshift__


    def __lshift__(self, other):
        '''
        Creates a new Numeral, containing the current Numeral left-shifted by the supplied amount.

        @param      other [in] (Numeral, int, long) The value to shift by
        @return     The result of the shift
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        result = Numeral(self.value << value,
                        byteCount    = self.byteCount,
                        fixedLength  = self.fixedLength,
                        littleEndian = self.littleEndian)

        return result
    # end def __lshift__

    def __ilshift__(self, other):
        '''
        Updates the current Numeral, with the left shift of the current Numeral
        and the supplied one.

        @param      other [in] (Numeral, int, long) The value to add
        @return     The result of the left shift (self)
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        self._checkAndAssign(self.value << value)

        return self
    # end def __ilshift__

    @staticmethod
    def _normalize(*hexNums):
        '''
        Computes the least common byteCount, fixedLength, and endianness for
        a list of Numerals.

        @param hexNums [in] (tuple<Numeral>) The list of Numerals to normalize,
        @return A tuple(byteCount, fixedLength, littleEndian) of the expected
                normalized result
        '''

        assert len(hexNums) > 0, "Not enough elements to normalize"

        # littleEndian
        endianNesses = tuple(set([hexNum.littleEndian for hexNum in hexNums]))
        assert len(endianNesses) == 1, "Incompatible Endianness"
        littleEndian = endianNesses[0]

        # fixedLength
        fixedLengthNumerals = [hexNum for hexNum in hexNums if hexNum.fixedLength]
        fixedLength = (len(fixedLengthNumerals) > 0)

        # byteCount
        byteCount = None
        byteCounts = tuple(set([hexNum.byteCount for hexNum in fixedLengthNumerals]))
        assert len(byteCounts) <= 1, "Incompatible fixed byteCount"
        if (len(byteCounts) > 0):
            byteCount = byteCounts[0]
        # end if

        return byteCount, fixedLength, littleEndian
    # end def _normalize

    def __and__(self, other):
        '''
        Creates a new Numeral, containing the current Numeral binary-ANDed with
        the supplied parameter.

        If the supplied parameter is not an Numeral, an attempt is made at
        converting it to an Numeral, using the current instance as a template.

        Note that this operation (as all binary operations) has the following
        restrictions:
        - The endianness of the two arguments must be identical
        - If both arguments are fixed length Numeral, their size must be identical
        - If both arguments are variable-length Numeral, the result is a variable-length Numeral
        - If only one of the arguments is a variable-length Numeral, the result
          is a fixed-length Numeral using the length of the other argument.

        The following examples detail the expected results:

        Valid operations
        @code
        a = Numeral(0x1234)
        b = Numeral(0xF0F0)
        c = a & b # c is Numeral(0x1030)
        @endcode

        @param other [in] (Numeral) The other argument
        @return self & other
        '''
        if (not isinstance(other, Numeral)):
            other = Numeral(other,
                           byteCount    = self.byteCount,
                           fixedLength  = self.fixedLength,
                           littleEndian = self.littleEndian)
        # end if

        # Adapt the result to the correct settings
        byteCount, fixedLength, littleEndian = self._normalize(self, other)

        return Numeral(source       = self.value & other.value,
                      byteCount    = byteCount,
                      littleEndian = littleEndian,
                      fixedLength  = fixedLength)
    # end def __and__

    def __iand__(self, other):
        '''
        Updates the current Numeral, with the addition of the current Numeral
        and the supplied one.

        @param      other [in] (Numeral, int, long) The value to add
        @return     The result of the addition (self)
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        self._checkAndAssign(self.value & value)

        return self
    # end def __iand__

    def __or__(self, other):
        '''
        Creates a new Numeral, containing the current Numeral binary-ORed with
        the supplied parameter.

        If the supplied parameter is not an Numeral, an attempt is made at
        converting it to an Numeral, using the current instance as a template.

        Note that this operation (as all binary operations) has the following
        restrictions:
        - The endianness of the two arguments must be identical
        - If both arguments are fixed length Numeral, their size must be identical
        - If both arguments are variable-length Numeral, the result is a variable-length Numeral
        - If only one of the arguments is a variable-length Numeral, the result
          is a fixed-length Numeral using the length of the other argument.

        The following examples detail the expected results:

        Valid operations
        @code
        a = Numeral(0x1234)
        b = Numeral(0xF0F0)
        c = a | b # c is Numeral(0xF2F4)
        @endcode

        @param other [in] (Numeral) The other argument
        @return self | other
        '''
        if (not isinstance(other, Numeral)):
            other = Numeral(other,
                           byteCount = self.byteCount,
                           fixedLength  = self.fixedLength,
                           littleEndian = self.littleEndian)
        # end if

        # Adapt the result to the correct settings
        byteCount, fixedLength, littleEndian = self._normalize(self, other)

        return Numeral(source       = self.value | other.value,
                      byteCount    = byteCount,
                      littleEndian = littleEndian,
                      fixedLength  = fixedLength)
    # end def __or__

    def __ior__(self, other):
        '''
        Updates the current Numeral, with the addition of the current Numeral
        and the supplied one.

        @param      other [in] (Numeral, int, long) The value to add
        @return     The result of the addition (self)
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        self._checkAndAssign(self.value | value)

        return self
    # end def __ior__

    def __xor__(self, other):
        '''
        Creates a new Numeral, containing the current Numeral binary-ORed with
        the supplied parameter.

        If the supplied parameter is not an Numeral, an attempt is made at
        converting it to an Numeral, using the current instance as a template.

        Note that this operation (as all binary operations) has the following
        restrictions:
        - The endianness of the two arguments must be identical
        - If both arguments are fixed length Numeral, their size must be identical
        - If both arguments are variable-length Numeral, the result is a variable-length Numeral
        - If only one of the arguments is a variable-length Numeral, the result
          is a fixed-length Numeral using the length of the other argument.

        The following examples detail the expected results:

        Valid operations
        @code
        a = Numeral(0x1234)
        b = Numeral(0xF0F0)
        c = a | b # c is Numeral(0xF2F4)
        @endcode

        @param other [in] (Numeral) The other argument
        @return self ^ other
        '''
        if (not isinstance(other, Numeral)):
            other = Numeral(other,
                           byteCount = self.byteCount,
                           fixedLength  = self.fixedLength,
                           littleEndian = self.littleEndian)
        # end if

        # Adapt the result to the correct settings
        byteCount, fixedLength, littleEndian = self._normalize(self, other)

        return Numeral(source       = self.value ^ other.value,
                      byteCount    = byteCount,
                      littleEndian = littleEndian,
                      fixedLength  = fixedLength)
    # end def __xor__

    def __ixor__(self, other):
        '''
        Updates the current Numeral, with the addition of the current Numeral
        and the supplied one.

        @param      other [in] (Numeral, int, long) The value to add
        @return     The result of the addition (self)
        @exception  ValueError If the first operand is fixedLength and the result overflows
        '''

        value = self.__intValue(other)

        self._checkAndAssign(self.value ^ value)

        return self
    # end def __ixor__

    def __invert__(self):
        '''
        Creates a new Numeral, containing the current Numeral binary-NOTed.

        Note that this operation only operates on fixed-length Numerals.

        The following examples detail the expected results:

        Valid operations
        @code
        a = Numeral(0x1234, fixedLength=True)
        c = ~a # c is Numeral(0xEDCB)
        @endcode

        @return ~self
        '''
        assert self.fixedLength, "NOT only operates on fixed-length Numerals"
        assert self.byteCount is not None, "NOT only operates on Numerals with a specified byteCount"

        return Numeral(source       = (~(self.value)) & ((2<<((self.byteCount*8) - 1)) - 1),
                      byteCount    = self.byteCount,
                      fixedLength  = self.fixedLength,
                      littleEndian = self.littleEndian)
    # end def __invert__

    def __eq__(self, other):
        '''
        Compares the current object with the supplied one.

        This is a logical comparison, limited to the enclosed value.
        It does not compare fixedLength, byteCount, etc.

        @param other [in] (Numeral, int, long) The value to compare to
        @return The result of the comparison with other. (-1, 0, 1)
        '''
        if not isinstance(other, Numeral):
            other = Numeral(other, littleEndian = self.littleEndian)
        # end if
        return (self.value == other.value)
    # end def __eq__

    def __ne__(self, other):
        '''
        Compares the current object with the supplied one.

        This is a logical comparison, limited to the enclosed value.
        It does not compare fixedLength, byteCount, etc.

        @param other [in] (Numeral, int, long) The value to compare to
        @return The result of the comparison with other. (-1, 0, 1)
        '''
        if not isinstance(other, Numeral):
            other = Numeral(other, littleEndian = self.littleEndian)
        # end if
        return not (self.value == other.value)
    # end def __ne__

    def __lt__(self, other):
        '''
        Compares the current object with the supplied one.

        This is a logical comparison, limited to the enclosed value.
        It does not compare fixedLength, byteCount, etc.

        @param other [in] (Numeral, int, long) The value to compare to
        @return The result of the comparison with other. (-1, 0, 1)
        '''
        if not isinstance(other, Numeral):
            other = Numeral(other, littleEndian = self.littleEndian)
        # end if
        return (self.value < other.value)
    # end def __lt__

    def __len__(self):
        '''
        Obtains the length of this Numeral, once transformed to a HexList

        @return The actual length of the Numeral once transformed.
        '''
        if (self.byteCount is not None):
            result = self.byteCount
        else:
            result = len(HexList(self))
        # end if

        return result
    # end def __len__

    def __str__(self):
        '''
        Converts the current object to its string representation.

        @return (str) The current object, as a string.
        '''
        return str(HexList(self))
    # end def __str__

    def __repr__(self):
        '''
        Converts the current object to its string representation.

        @return (str) The current object, as a string.
        '''
        return '%s(source = %r, byteCount = %r, littleEndian = %r, fixedLength = %r)' % (self.__class__.__name__,
                                                                                         self.value,
                                                                                         self.byteCount,
                                                                                         self.littleEndian,
                                                                                         self.fixedLength)
    # end def __repr__



    def __int__(self):
        '''
        Converts the current object to its int representation.

        @return (int) The current object, as an int
        '''
        return int(self.value)
    # end def __int__

    def __long__(self):
        '''
        Converts the current object to its long representation.

        @return (long) The current object, as an long
        '''
        return int(self.value)
    # end def __long__

    def __float__(self):
        '''
        Converts the current object to its float representation.

        @return (float) The current object, as a float()
        '''
        return float(self.value)
    # end def __float__

    SHIFT_SIZE = (2048, 1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1)
    def bitCount(self):
        '''
        Computes the minimum number of bits necessary for the representation
        of this number, in binary.

        Note: 0x00 returns 0, 0x01 returns 1, 0x04 returns 3, etc...

        @return The minimum number of bits needed to represent the current value
        '''
        result = 0

        value = self.value
        for shiftSize in self.SHIFT_SIZE:
            new_value = value >> shiftSize
            while (new_value):
                value = new_value
                result += shiftSize
                new_value = value >> shiftSize
            # end while
        # end for

        result = 0
        value  = self.value

        while value:
            result += 1
            value = value >> 1
        # end while

        return result
    # end def bitCount

    @classmethod
    def gcd(cls, operand1, operand2):
        '''
        A pure python implementation of euclid's gcd algorithm.

        @param operand1 [in] (Numeral) First GCD operand
        @param operand2 [in] (Numeral) Second GCD operand
        @return The GCD of @c operand1 and @c operand2, as a Numeral
        '''
        if (isinstance(operand1, Numeral)):
            littleEndian = operand1.littleEndian
        elif (isinstance(operand2, Numeral)):
            littleEndian = operand2.littleEndian
        else:
            littleEndian = None
        # end if

        if (not isinstance(operand1, Numeral)):
            operand1 = Numeral(operand1, littleEndian = littleEndian)
        # end if

        if (not isinstance(operand2, Numeral)):
            operand2 = Numeral(operand2, littleEndian = littleEndian)
        # end if

        aa = operand1.value
        bb = operand2.value
        while (aa):
            aa, bb = bb % aa, aa
        # end while

        # Adapt the result to the correct settings
        byteCount, fixedLength, littleEndian = cls._normalize(operand1, operand2)

        return Numeral(source       = bb,
                      byteCount    = byteCount,
                      littleEndian = littleEndian,
                      fixedLength  = fixedLength)
    # end def gcd
# end class Numeral

class RandNumeral(Numeral):                                                                                               # pylint:disable=R0924
    '''
    Create An HexList filled with random values
    '''
    def __init__(self, byteCount    = None,
                       maxVal       = None,
                       minVal       = 0,
                       littleEndian = None,
                       fixedLength  = None):
        '''
        Constructor

        @param  byteCount    [in] (int) Size of RandHexList to create
        @option maxVal       [in] (int) Maximum value of each bytes of generated rand
        @option minVal       [in] (int) Minumum value of each bytes of generated rand
        @option littleEndian [in] (bool) Whether the hexadecimal representation will be bigEndian or littleEndian.
        @option fixedLength  [in] (bool) Will cause an exception if any operation
                                            grows the Numeral beyond its byteCount.
        '''
        assert (byteCount >= 0), "Invalid size (%i)!" % (byteCount, )
        assert minVal >= 0, "Invalid minimum value (%d)" % (minVal, )

        if (maxVal is None):
            maxVal = (0x1 << (8 * byteCount)) - 1
        # end if

        assert (maxVal < (0x01 << (8 * byteCount))), "Invalid maximum value (0x%X)" % (maxVal,)

        source = randint(minVal, maxVal)

        super(RandNumeral, self).__init__(source,
                                         byteCount,
                                         littleEndian,
                                         fixedLength)
    # end def __init__
# end class RandNumeral

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
