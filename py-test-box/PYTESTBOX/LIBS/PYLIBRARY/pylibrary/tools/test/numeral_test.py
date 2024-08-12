#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.test.numeral

@brief Numeral test implementation

@author christophe.roquebert

@date   2018/09/20
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import RandNumeral
from unittest                import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class NumeralTestCase( TestCase ):
    '''
    Numeral test implementation.
    '''

    def setUp( self ):
        '''
        Initialize test
        '''
        TestCase.setUp(self)
    # end def setUp

    def test_Length(self):
        '''
        Tests the length of an Numeral
        '''

        vectors = ( (Numeral(0x12345), 3),
                    (Numeral(0x12345, 7), 7),
                    )

        for value, length in vectors:
            self.assertEqual(length,
                             len(value),
                             'Invalid compted Numeral value')
        # end for
    # end def test_Length

    def test_GetItem(self):
        '''
        Tests item access on a Numeral
        '''

        value = Numeral(0x012345, byteCount = 3, fixedLength=True, littleEndian=False)
        self.assertEqual(0x01,
                         value[0],
                         'Invalid __getitem__ access: big endian')
        self.assertEqual(0x45,
                         value[-1],
                         'Invalid __getitem__ access: big endian')
        self.assertEqual(HexList(0x23, 0x45),
                         value[1:3],
                         'Invalid __getitem__ slice access: big endian')

        value = Numeral(0x012345, byteCount = 3, fixedLength=True, littleEndian=True)
        self.assertEqual(0x45,
                         value[0],
                         'Invalid __getitem__ access: little endian')
        self.assertEqual(0x01,
                         value[-1],
                         'Invalid __getitem__ access: little endian')
        self.assertEqual(HexList(0x23, 0x01),
                         value[1:3],
                         'Invalid __getitem__ slice access: little endian')
    # end def test_GetItem

    def test_SetItem(self):
        '''
        Tests item access on a Numeral
        '''

        reference = Numeral(0x012345, byteCount = 3, fixedLength=True, littleEndian = False)

        value = Numeral(reference)
        value[0] = 0x22
        self.assertEqual(Numeral(0x222345, byteCount = 3, fixedLength = True, littleEndian = False),
                         value,
                         'Invalid __setitem__ access: big endian')

        value = Numeral(reference)
        value[-1] = 0x44
        self.assertEqual(Numeral(0x012344, byteCount = 3, fixedLength = True, littleEndian = False),
                         value,
                         'Invalid __setitem__ access: big endian')

        value = Numeral(reference)
        value[1:3] = HexList(0x77, 0x88)
        self.assertEqual(Numeral(0x017788, byteCount = 3, fixedLength = True, littleEndian = False),
                         value,
                         'Invalid __setitem__ slice access: big endian')

        # On to little endianness
        reference = Numeral(0x012345, byteCount = 3, fixedLength=True, littleEndian = True)

        value = Numeral(reference)
        value[0] = 0x22
        self.assertEqual(Numeral(0x012322, byteCount = 3, fixedLength = True, littleEndian = True),
                         value,
                         'Invalid __setitem__ access: little endian')

        value = Numeral(reference)
        value[-1] = 0x44
        self.assertEqual(Numeral(0x442345, byteCount = 3, fixedLength = True, littleEndian = True),
                         value,
                         'Invalid __setitem__ access: little endian')

        value = Numeral(reference)
        value[1:3] = HexList(0x77, 0x88)
        self.assertEqual(Numeral(0x887745, byteCount = 3, fixedLength = True, littleEndian = True),
                         value,
                         'Invalid __setitem__ slice access: little endian')
    # end def test_SetItem

    def test_Constructor(self):
        '''
        Tests the construction of an Numeral
        '''

        num1 = Numeral(0x12345)
        self.assertEqual(0x12345,
                         num1.value,
                         "Invalid value")

        num1 = Numeral(-1)
        self.assertEqual(-1,
                         num1.value,
                         "Invalid value")

        num1 = Numeral(HexList("012345"))
        self.assertEqual(0x12345,
                         num1.value,
                         "Invalid value")

        num1 = Numeral("012345")
        self.assertEqual(0x12345,
                         num1.value,
                         "Invalid value")

        num1 = Numeral(HexList("452301"), littleEndian=True)
        self.assertEqual(0x12345,
                         num1.value,
                         "Invalid value")

        num1 = Numeral(Numeral(0x12345))
        self.assertEqual(0x12345,
                         num1.value,
                         "Invalid value")
    # end def test_Constructor

    def test_Constructor_FixedLength(self):
        '''
        Tests constuction when fixed length is forced
        '''
        num1 = Numeral(0x001234, fixedLength = True)
        self.assertEqual(True,
                         num1.fixedLength,
                         'fixedLength not set')
        self.assertEqual(2,
                         num1.byteCount,
                         'fixedLength did not auto-set byteCount')

        num1 = Numeral(HexList(0x00, 0x12, 0x34), fixedLength = True)
        self.assertEqual(True,
                         num1.fixedLength,
                         'fixedLength not set')
        self.assertEqual(3,
                         num1.byteCount,
                         'fixedLength did not auto-set byteCount')

        num1 = Numeral(Numeral(0x001234, fixedLength = True, byteCount=4))
        self.assertEqual(True,
                         num1.fixedLength,
                         'fixedLength not set')
        self.assertEqual(4,
                         num1.byteCount,
                         'fixedLength did not auto-set byteCount')
    # end def test_Constructor_FixedLength

    def test_ConversionToHexList(self):
        '''
        Tests the conversion to and from HexList
        '''

        self.assertEqual(HexList(0x33),
                         Numeral(0x33, 1),
                         "Invalid conversion")

        self.assertEqual(HexList(0x33, 0x34),
                         Numeral(0x3334, 2),
                         "Invalid conversion")

        self.assertEqual(HexList(0x33, 0x34),
                         Numeral(0x3334, 2, littleEndian=False),
                         "Invalid conversion")

        self.assertEqual(HexList(0x33, 0x34),
                         Numeral(0x3433, 2, littleEndian=True),
                         "Invalid conversion")

        self.assertEqual(Numeral(0, 3),
                         Numeral(HexList(0x00), 3),
                         "Invalid conversion")
    # end def test_ConversionToHexList

    def test_ConversionToLong(self):
        '''
        Tests the conversion to and from HexList
        '''

        self.assertEqual(0x33,
                         int(Numeral(0x33, 1)),
                         "Invalid conversion")

        self.assertEqual(0x3334,
                         int(Numeral(0x3334, 2)),
                         "Invalid conversion")

        self.assertEqual(0x3334,
                         int(Numeral(0x3334, 2, littleEndian=False)),
                         "Invalid conversion")

        self.assertEqual(0x3433,
                         int(Numeral(0x3433, 2, littleEndian=True)),
                         "Invalid conversion")

        self.assertEqual(0x00,
                         int(Numeral(HexList(0x00), 3)),
                         "Invalid conversion")
    # end def test_ConversionToLong

    def test_Comparison(self):
        '''
        Tests the comparison of two Numerals
        '''

        num1 = Numeral(0x12345)
        num2 = Numeral(0x12345)
        self.assertEqual(num1,
                         num2,
                         "Invalid comparison")

        num3 = Numeral(0x12346)
        self.assertTrue(num1 < num3,
                        "Invalid inequality")

        self.assertTrue(num3 > num1,
                        "Invalid inequality")
    # end def test_Comparison

    def test_Serialization(self):
        '''
        Tests the serialization of two Numerals
        '''

        num1 = Numeral(0x12345)
        hex1 = HexList("012345")
        self.assertEqual(hex1,
                         HexList(num1),
                         "Invalid serialization")

        num2 = Numeral(0x12345, littleEndian=True)
        hex2 = HexList("452301")
        self.assertEqual(hex2,
                         HexList(num2),
                         "Invalid serialization")

        num3 = Numeral(-1, 1)
        hex3 = HexList(0xFF)
        self.assertEqual(hex3,
                         HexList(num3),
                         "Invalid serialization")

        num4 = Numeral(-2039, 2)
        hex4 = HexList(0xF8, 0x09)
        self.assertEqual(hex4,
                         HexList(num4),
                         "Invalid serialization")
    # end def test_Serialization

    def test_Add(self):
        '''
        Tests the addition of two Numerals
        '''

        num1 = Numeral(0x12345)
        num2 = Numeral(0x01)
        num3 = Numeral(0x12346)

        self.assertEqual(num3,
                         num1 + num2,
                         "Invalid addition")

        num1 = Numeral(0xFFFFFF, fixedLength=True)
        num2 = Numeral(0x01)

        self.assertRaises(AssertionError,
                          lambda: num1+num2)
    # end def test_Add

    def test_iAdd(self):
        '''
        Tests +=
        '''

        num1 = Numeral(0x12345)
        num2 = Numeral(0x01)
        num3 = Numeral(0x12346)

        expected = Numeral(num3)
        obtained = num1
        reference = obtained
        obtained += num2

        self.assertEqual(expected,
                         obtained,
                         'Invalid +=')
        self.assertTrue(reference is obtained,
                        '+= did not replace the reference')

    # end def test_iAdd

    def test_Sub(self):
        '''
        Tests the subtraction of two Numerals
        '''

        num1 = Numeral(0x12345)
        num2 = Numeral(0x01)
        num3 = Numeral(0x12344)

        self.assertEqual(num3,
                         num1 - num2,
                         "Invalid addition")

        num1 = Numeral(0x012345)
        num2 = Numeral(0x012346)

        self.assertRaises(AssertionError,
                          lambda: num1-num2)
    # end def test_Sub

    def test_iSub(self):
        '''
        Tests -=
        '''

        num1 = Numeral(0x12345)
        num2 = Numeral(0x01)
        num3 = Numeral(0x12344)


        expected = Numeral(num3)
        obtained = num1
        reference = obtained
        obtained -= num2
        self.assertEqual(expected,
                         obtained,
                        'Invalid -=')
        self.assertTrue(reference is obtained,
                        '-= did not replace the reference')
    # end def test_iSub

    def test_Mul(self):
        '''
        Tests the multiplication of two Numerals
        '''

        num1 = Numeral(0x1234)
        num2 = Numeral(0x02)
        num3 = Numeral(0x2468)

        self.assertEqual(num3,
                         num1 * num2,
                         "Invalid multiplication")

        num1 = Numeral(0xFFFFFF, fixedLength=True)
        num2 = Numeral(0x02)

        self.assertRaises(AssertionError,
                          lambda: num1*num2)
    # end def test_Mul

    def test_iMul(self):
        '''
        Tests the multiplication of two Numerals
        '''

        num1 = Numeral(0x1234)
        num2 = Numeral(0x02)
        num3 = Numeral(0x2468)

        expected = Numeral(num3)
        obtained = num1
        reference = obtained
        obtained *= num2
        self.assertEqual(expected,
                         obtained,
                        'Invalid *=')
        self.assertTrue(reference is obtained,
                        '*= did not replace the reference')
    # end def test_iMul

    def test_Div(self):
        '''
        Tests the division of two Numerals
        '''

        num1 = Numeral(0x1234)
        num2 = Numeral(0x02)
        num3 = Numeral(0x091A)

        self.assertEqual(num3,
                         num1 // num2,
                         "Invalid division")

        num1 = Numeral(0xFFFFFF, fixedLength=True)
        num2 = Numeral(0x100)
        hex3 = HexList(0xFF, 0xFF)
        hex3.addPadding(3)

        self.assertEqual(hex3,
                         num1 // num2,
                         "Invalid division")

        num1 = Numeral(17)
        num2 = Numeral(2)
        num3 = Numeral(8)
        self.assertEqual(num3,
                         num1 // num2,
                         "Invalid division")
    # end def test_Div

    def test_iDiv(self):
        '''
        Tests the division of two Numerals
        '''

        num1 = Numeral(0x1234)
        num2 = Numeral(0x02)
        num3 = Numeral(0x091A)

        expected = Numeral(num3)
        obtained = num1
        reference = obtained
        obtained //= num2
        self.assertEqual(expected,
                         obtained,
                        'Invalid /=')
        self.assertTrue(reference is obtained,
                        '/= did not replace the reference')
    # end def test_iDiv

    def test_Mod(self):
        '''
        Tests the modulus of two Numerals
        '''

        num1 = Numeral(0x1234)
        num2 = Numeral(0x100)
        num3 = Numeral(0x34)

        self.assertEqual(num3,
                         num1 % num2,
                         "Invalid modulus")

        num1 = Numeral(0x1234)
        num2 = Numeral(0x100)
        hex3 = HexList(0x00, 0x34)
        hex3.addPadding(2)

        self.assertEqual(hex3,
                         num1 % num2,
                         "Invalid modulus")
    # end def test_Mod

    def test_iMod(self):
        '''
        Tests the modulus of two Numerals
        '''

        num1 = Numeral(0x1234)
        num2 = Numeral(0x100)
        num3 = Numeral(0x34)

        expected = Numeral(num3)
        obtained = num1
        reference = obtained
        obtained %= Numeral(num2)
        self.assertEqual(expected,
                         obtained,
                        'Invalid %=')
        self.assertTrue(reference is obtained,
                        '%= did not replace the reference')
    # end def test_iMod

    def test_lShift(self):
        '''
        Tests Numeral shifting
        '''
        num1 = Numeral(0x1234)
        num2 = Numeral(0x08)
        hex3 = HexList(0x12, 0x34, 0x00)

        self.assertEqual(hex3,
                         num1 << num2,
                         "Invalid shift left")
    # end def test_lShift

    def test_ilShift(self):
        '''
        Tests Numeral shifting
        '''
        num1 = Numeral(0x1234)
        num2 = Numeral(0x08)
        num3 = Numeral(HexList(0x12, 0x34, 0x00))

        expected = Numeral(num3)
        obtained = num1
        reference = obtained
        obtained <<= num2

        self.assertEqual(expected,
                         obtained,
                        'Invalid <<=')
        self.assertTrue(reference is obtained,
                        '<<= did not replace the reference')
    # end def test_ilShift

    def test_rShift(self):
        '''
        Tests Numeral shifting
        '''
        num1 = Numeral(0x1234)
        num2 = Numeral(0x08)
        num3 = Numeral(0x12)

        self.assertEqual(num3,
                         num1 >> num2,
                         "Invalid shift right")

        expected = Numeral(0x12345)
        obtained = expected
        obtained >>= Numeral(0x99)
        self.assertTrue(expected is obtained,
                        '>>= did not replace the reference')
    # end def test_rShift

    def test_irShift(self):
        '''
        Tests Numeral shifting
        '''
        num1 = Numeral(0x1234)
        num2 = Numeral(0x08)
        num3 = Numeral(0x12)

        expected = Numeral(num3)
        obtained = num1
        reference = obtained
        obtained >>= num2
        self.assertEqual(expected,
                         obtained,
                        'Invalid >>=')
        self.assertTrue(reference is obtained,
                        '>>= did not replace the reference')
    # end def test_irShift

    def test_BitCount(self):
        '''
        Tests the bit count.
        '''
        vectors = ((Numeral(0x10), 5),
                   (Numeral(0x12345), 17),
                   (Numeral(0x800000), 24),
                   )

        for source, expected in vectors:
            self.assertEqual(expected,
                             source.bitCount(),
                             "Invalid bit count for value: 0x%s" % source)
        # end for
    # end def test_BitCount

    def test_BinaryAnd(self):
        '''
        Tests the binary AND operator
        '''
        # Test vectors: a, b, c, exception expected
        vectors = ( # Nominal
                   (Numeral(0x1234),
                    Numeral(0xF0F0),
                    Numeral(0x1030)),
                    # Nominal, littleEndian
                   (Numeral(0x1234, littleEndian = True),
                    Numeral(0xF0F0, littleEndian = True),
                    Numeral(0x1030, littleEndian = True)),
                    # Nominal, fixedLength
                   (Numeral(0x1234, fixedLength = True),
                    Numeral(0xF0F0, fixedLength = True),
                    Numeral(0x1030, fixedLength = True)),
                    # Nominal, fixedLength & bytecount
                   (Numeral(0x1234, fixedLength = True, byteCount = 3),
                    Numeral(0xF0F0, fixedLength = True, byteCount = 3),
                    Numeral(0x1030, fixedLength = True, byteCount = 3)),
                    # Nominal, fixedLength & bytecount, mixed
                   (Numeral(0x1234, fixedLength = False),
                    Numeral(0x00F0F0F0, fixedLength = True, byteCount = 4),
                    Numeral(0x00001030, fixedLength = True, byteCount = 4)),
                    # Exception, littleEndian
                   (Numeral(0x1234, littleEndian = True),
                    Numeral(0xF0F0, littleEndian = False),
                    None),
                    # Exception, fixedLength & byteCount
                   (Numeral(0x1234, fixedLength = True, byteCount = 4),
                    Numeral(0xF0F0, fixedLength = True, byteCount = 3),
                    None),
                 )

        for a, b, expected in vectors:                                                                                  # pylint:disable=C0103

            try:
                obtained = a & b
            except Exception as exception:                                                                              # pylint:disable=W0703
                self.assertEqual(True,
                                 expected is None,
                                 "Exception occurred in binary AND for %s & %s:\n%s" % (a, b, exception))
            # end try

            if (expected is not None):
                self.assertEqual(expected,
                                 obtained,
                                 "Invalid binary AND for %s & %s" % (a, b))
            # end if

            try:
                obtained = Numeral(a)
                reference = obtained
                obtained &= b
            except Exception as exception:                                                                              # pylint:disable=W0703
                self.assertEqual(True,
                                 expected is None,
                                 "Exception occurred in binary AND for %s & %s:\n%s" % (a, b, exception))
            # end try

            if (expected is not None):
                self.assertEqual(expected,
                                 obtained,
                                 "Invalid binary AND for %s & %s" % (a, b))
                self.assertTrue(reference is obtained,
                                 "Binary AND did not keep reference")
            # end if
        # end for


    # end def test_BinaryAnd

    def test_BinaryOr(self):
        '''
        Tests the binary OR operator
        '''
        # Test vectors: a, b, c, exception expected
        vectors = ( # Nominal
                   (Numeral(0x1234),
                    Numeral(0xF0F0),
                    Numeral(0xF2F4)),
                    # Nominal, littleEndian
                   (Numeral(0x1234, littleEndian = True),
                    Numeral(0xF0F0, littleEndian = True),
                    Numeral(0xF2F4, littleEndian = True)),
                    # Nominal, fixedLength
                   (Numeral(0x1234, fixedLength = True),
                    Numeral(0xF0F0, fixedLength = True),
                    Numeral(0xF2F4, fixedLength = True)),
                    # Nominal, fixedLength & bytecount
                   (Numeral(0x1234, fixedLength = True, byteCount = 3),
                    Numeral(0xF0F0, fixedLength = True, byteCount = 3),
                    Numeral(0xF2F4, fixedLength = True, byteCount = 3)),
                    # Nominal, fixedLength & bytecount, mixed
                   (Numeral(0x1234, fixedLength = False),
                    Numeral(0x00F0F0F0, fixedLength = True, byteCount = 4),
                    Numeral(0x00F0F2F4, fixedLength = True, byteCount = 4)),
                    # Exception, littleEndian
                   (Numeral(0x1234, littleEndian = True),
                    Numeral(0xF0F0, littleEndian = False),
                    None),
                    # Exception, fixedLength & byteCount
                   (Numeral(0x1234, fixedLength = True, byteCount = 4),
                    Numeral(0xF0F0, fixedLength = True, byteCount = 3),
                    None),
                 )

        for a, b, expected in vectors:                                                                                  # pylint:disable=C0103

            try:
                obtained = a | b
            except Exception as exception:                                                                              # pylint:disable=W0703
                self.assertEqual(True,
                                 expected is None,
                                 "Exception occurred in binary OR for %s & %s:\n%s" % (a, b, exception))
            # end try

            if (expected is not None):
                self.assertEqual(expected,
                                 obtained,
                                 "Invalid binary OR for %s & %s" % (a, b))
            # end if

            try:
                obtained = Numeral(a)
                reference = obtained
                obtained |= b
            except Exception as exception:                                                                              # pylint:disable=W0703
                self.assertEqual(True,
                                 expected is None,
                                 "Exception occurred in binary OR for %s & %s:\n%s" % (a, b, exception))
            # end try


            if (expected is not None):
                self.assertEqual(expected,
                                 obtained,
                                 "Invalid binary OR for %s & %s" % (a, b))
                self.assertTrue(reference is obtained,
                                 "Binary OR did not keep reference")
            # end if

        # end for

        expected = Numeral(0x12345)
        obtained = expected
        obtained |= Numeral(0x99)
        self.assertTrue(expected is obtained,
                        '|= did not replace the reference')
    # end def test_BinaryOr

    def test_BinaryXor(self):
        '''
        Tests the binary XOR operator
        '''
        # Test vectors: a, b, c, exception expected
        vectors = ( # Nominal
                   (Numeral(0x1234),
                    Numeral(0xF0F0),
                    Numeral(0xE2C4)),
                    # Nominal, littleEndian
                   (Numeral(0x1234, littleEndian = True),
                    Numeral(0xF0F0, littleEndian = True),
                    Numeral(0xE2C4, littleEndian = True)),
                    # Nominal, fixedLength
                   (Numeral(0x1234, fixedLength = True),
                    Numeral(0xF0F0, fixedLength = True),
                    Numeral(0xE2C4, fixedLength = True)),
                    # Nominal, fixedLength & bytecount
                   (Numeral(0x1234, fixedLength = True, byteCount = 3),
                    Numeral(0xF0F0, fixedLength = True, byteCount = 3),
                    Numeral(0xE2C4, fixedLength = True, byteCount = 3)),
                    # Nominal, fixedLength & bytecount, mixed
                   (Numeral(0x1234, fixedLength = False),
                    Numeral(0x00F0F0F0, fixedLength = True, byteCount = 4),
                    Numeral(0x00F0E2C4, fixedLength = True, byteCount = 4)),
                    # Exception, littleEndian
                   (Numeral(0x1234, littleEndian = True),
                    Numeral(0xF0F0, littleEndian = False),
                    None),
                    # Exception, fixedLength & byteCount
                   (Numeral(0x1234, fixedLength = True, byteCount = 4),
                    Numeral(0xF0F0, fixedLength = True, byteCount = 3),
                    None),
                 )

        for a, b, expected in vectors:                                                                                  # pylint:disable=C0103

            try:
                obtained = a ^ b
            except Exception as exception:                                                                              # pylint:disable=W0703
                self.assertEqual(True,
                                 expected is None,
                                 "Exception occurred in binary XOR for %s & %s:\n%s" % (a, b, exception))
            # end try


            if (expected is not None):
                self.assertEqual(expected,
                                 obtained,
                                 "Invalid binary XOR for %s & %s" % (a, b))
            # end if

            try:
                obtained = Numeral(a)
                reference = obtained
                obtained ^= b
            except Exception as exception:                                                                              # pylint:disable=W0703
                self.assertEqual(True,
                                 expected is None,
                                 "Exception occurred in binary XOR for %s & %s:\n%s" % (a, b, exception))
            # end try


            if (expected is not None):
                self.assertEqual(expected,
                                 obtained,
                                 "Invalid binary XOR for %s & %s" % (a, b))
                self.assertTrue(reference is obtained,
                                 "Binary XOR did not keep reference")
            # end if
        # end for
    # end def test_BinaryXor

    def test_BinaryNot(self):
        '''
        Tests the binary NOT operator
        '''
        # Test vectors: a, c (c set to None if an exception is expected)
        vectors = ( # Nominal
                   (Numeral(0x1234, fixedLength = True),
                    Numeral(0xEDCB, fixedLength = True)),
                    # Nominal, large value
                   (Numeral(0xFF1234, fixedLength = True, byteCount = 3),
                    Numeral(0x00EDCB, fixedLength = True, byteCount = 3)),
                    # Exception, fixedLength
                   (Numeral(0x1234),
                    None),
                 )

        for a, expected in vectors:                                                                                     # pylint:disable=C0103

            try:
                obtained = ~a
            except Exception as exception:                                                                              # pylint:disable=W0703
                self.assertEqual(True,
                                 expected is None,
                                 "Exception occurred in binary NOT for ~%s:\n%s" % (a, exception))
            # end try


            if (expected is not None):
                self.assertEqual(expected,
                                 obtained,
                                 "Invalid binary NOT for ~%s" % (a))
            # end if
        # end for
    # end def test_BinaryNot

    def test_gcd(self):
        '''
        Computes the gcd of two numerals
        '''

        operand1 = Numeral(2*3*5*7)
        operand2 = Numeral(7*11*13*17)
        expected = Numeral(7)

        obtained = Numeral.gcd(operand1, operand2)
        self.assertEqual(expected,
                         obtained,
                         "Incorrect gcd")

        operand1 = Numeral(2*3*5*7, littleEndian = True)
        operand2 = Numeral(7*11*13*17, littleEndian = True)
        expected = Numeral(7)

        obtained = Numeral.gcd(operand1, operand2)
        self.assertEqual(expected,
                         obtained,
                         "Incorrect gcd")

        self.assertEqual(True,
                         obtained.littleEndian,
                         "Incorrect endianness")
    # end def test_gcd

    def test_DivMod(self):
        '''
        Tests the divmod operations
        '''
        operand1 = Numeral(17)
        operand2 = Numeral(5)

        expected1 = Numeral(3)
        expected2 = Numeral(2)

        self.assertEqual((expected1, expected2),
                         divmod(operand1, operand2),
                         'Invalid divmod')
    # end def test_DivMod

    def test_Pow(self):
        '''
        Tests the pow operation
        '''
        operand1 = Numeral(0x12)
        operand2 = Numeral(0x34)

        expected = Numeral(0x12 ** 0x34)
        self.assertEqual(expected,
                         pow(operand1, operand2),
                         'Invalid pow')

        self.assertEqual(expected,
                         operand1 ** operand2,
                         'Invalid pow')
    # end def test_Pow

    def test_iPow(self):
        '''
        Tests **=
        '''
        operand1 = Numeral(0x12)
        operand2 = Numeral(0x34)
        expected = Numeral(0x12 ** 0x34)

        obtained = Numeral(operand1)
        reference = obtained
        obtained **= operand2
        self.assertTrue(reference is obtained,
                        '**= did not keep reference')
        self.assertEqual(expected,
                         obtained,
                         'Invalid **=')

    # end def test_iPow

    def test_FloorDiv(self):
        '''
        Tests the floordiv operation
        '''
        operand1 = Numeral(0x12)
        operand2 = Numeral(0x34)

        expected = Numeral(0x12 // 0x34)
        self.assertEqual(expected,
                         operand1 // operand2,
                         'Invalid floordiv')
    # end def test_FloorDiv

    def test_iFloorDiv(self):
        '''
        Tests the floordiv operation
        '''
        operand1 = Numeral(0x12)
        operand2 = Numeral(0x34)
        expected = Numeral(0x12 // 0x34)

        obtained = operand1
        reference = obtained
        obtained //= operand2

        self.assertEqual(expected,
                         obtained,
                         'Invalid floordiv')
        self.assertTrue(reference is obtained,
                         '//= did not keep the reference')
    # end def test_iFloorDiv

    def test_InvMod(self):
        '''
        Tests modular inversion
        '''
        operand1 = Numeral(0x03)
        operand2 = Numeral(0x0B)
        expected = Numeral(0x04)
        obtained = operand1.__invmod__(operand2)

        self.assertEqual(expected,
                         obtained,
                         'Invalid modular inverse')
    # end def test_InvMod
# end class NumeralTestCase

class RandNumeralTestCase(TestCase):
    '''
    Tests the RandNumeral class
    '''

    def test_VariousValues(self):
        '''
        Attempts to generate RandNumerals on various byte counts and max values
        '''

        byteCounts = (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024)
        for byteCount in byteCounts:
            hexNum = RandNumeral(byteCount)
            self.assertEqual(True,
                             hexNum is not None,
                             "Invalid Numeral")
        # end for
    # end def test_VariousValues

    def test_Bounds(self):
        '''
        Attempts to generate RandNumerals on various minimum and maximum values
        '''

        bounds = ( (2,       0x1234,       0x1235),
                   (5, 0x0000000000, 0x1122334455),
                   )
        for byteCount, minVal, maxVal in bounds:
            hexNum = RandNumeral(byteCount, maxVal, minVal)
            self.assertEqual(True,
                             (hexNum <= maxVal),
                             "Invalid upper bound")

            self.assertEqual(True,
                            (hexNum >= minVal),
                            "Invalid lower bound")
        # end for
    # end def test_Bounds

    def test_InvalidValues(self):
        '''
        Attempts to generate RandNumerals on various byte counts and max values
        '''

        invalidValues = (   (1, 0,  0x100),
                            (2, 0,  0x10000),
                            (-1, 0, 0),
                            (1, -1, 2),
                            )
        for byteCount, minVal, maxVal in invalidValues:
            hexNum = None
            try:
                hexNum = RandNumeral(byteCount, maxVal, minVal)
                excepted = False
            except Exception:                                                                                           # pylint:disable=W0703
                excepted = True
                self.assertEqual(True,
                                 hexNum is None,
                                 "Invalid non-nominal construction")
            # end try

            self.assertTrue(excepted,
                            "Should have raise an exception")

        # end for
    # end def test_InvalidValues
# end class RandNumeralTestCase
# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
