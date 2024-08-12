#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.tools.test.bitstruct
:brief: BitStruct class test module
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/06/23
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.deprecation import ignoredeprecation
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.bitstruct import BitStruct
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BitStructTestCase(TestCase):
    """
    Class of test of BitStruct class
    """

    ELT_0 = 'elt0'
    ELT_1 = 'elt1'
    ELT_2 = 'elt2'
    ELT_3 = 'elt3'
    ELT_4 = 'elt4'
    ELT_5 = 'elt5'
    ELT_6 = 'elt6'
    ELT_7 = 'elt7'
    ELT_8 = 'elt8'

    MASK_1 = 'mask1'
    MASK_2 = 'mask2'
    MASK_3 = 'mask3'

    DICTIONARY = {ELT_7: 7,
                  ELT_6: 6,
                  ELT_5: 5,
                  ELT_4: 4,
                  ELT_3: 3,
                  ELT_2: 2,
                  ELT_1: 1,
                  ELT_0: 0,
                  MASK_1: (0, 2),
                  MASK_2: (4, 4),
                  MASK_3: (3, 1)}

    INTERPRETER = {ELT_0: {0: 'bit 0 not set',
                           1: 'bit 0 set'},
                   ELT_1: {0: 'bit 1 not set',
                           1: 'bit 1 set'},
                   ELT_2: {0: 'bit 2 not set',
                           1: 'bit 2 set'},
                   ELT_3: {0: 'bit 3 not set',
                           1: 'bit 3 set'},
                   ELT_4: {0: 'bit 4 not set',
                           1: 'bit 4 set'},
                   ELT_5: {0: 'bit 5 not set',
                           1: 'bit 5 set'},
                   ELT_6: {0: 'bit 6 not set',
                           1: 'bit 6 set'},
                   ELT_7: {0: 'bit 7 not set',
                           1: 'bit 7 set'},
                   MASK_1: {None: '%(name)s value is %(value)d'}}

    class TestBitStruct(BitStruct):
        """
        Class test sub class implementation for BitStruct class
        """
        def __eq__(self, other):
            """
            @copydoc pylibrary.tools.bitstruct.BitStruct.__eq__
            """
            result = (HexList(self) == HexList(other))

            if result:
                result = (self._dict == other._dict)
            # end if

            return result
        # end def __eq__
    # end class TestBitStruct

    def test_constructor(self):
        """
        tests the constructor method
        """
        # Without dictionary
        bit_map = BitStruct(HexList(0xAA))

        value = 0
        for bit in range(8):
            self.assertEqual(value, bit_map.testBit(bit), "Inconsistent bit value")
            value = int(not bool(value))
        # end for

        # With dictionary
        bit_map = BitStruct(Numeral(0x55, 1), self.DICTIONARY)

        value = 1
        for bit in [self.ELT_0, self.ELT_1, self.ELT_2, self.ELT_3, self.ELT_4, self.ELT_5, self.ELT_6, self.ELT_7]:
            self.assertEqual(value, bit_map.testBit(bit), "Inconsistent bit value")
            value = int(not bool(value))
        # end for

        # With a BitStruct
        bit_map = BitStruct(bit_map)

        self.assertEqual(1, bit_map.testBit(self.ELT_0), "Inconsistent bit value")
        self.assertEqual(0, bit_map.testBit(self.ELT_1), "Inconsistent bit value")

        # With initialization of elements
        bit_map = BitStruct(HexList(0x00), self.DICTIONARY, elt0=1, mask2=5)

        self.assertEqual(HexList(0x51), HexList(bit_map), "Wrong elements initialization.")
    # end def test_constructor

    def test_constructor_wrong_type(self):
        """
        tests the constructor method with wrong type
        """
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            BitStruct(0.1)
        # end with
    # end def test_constructor_wrong_type

    def test_constructor_wrong_mode_type(self):
        """
        tests the constructor method with wrong mode
        """
        self.assertRaises(TypeError, BitStruct, HexList(0x01), mode="1")

        self.assertRaises(TypeError, BitStruct, HexList(0x01), mode=HexList("01"))
    # end def test_constructor_wrong_mode_type

    def test_access_invalid_key_by_api(self):
        """
        Tests the use of an invalid Key, by API access
        """
        bit_map = BitStruct(HexList(0xFF), self.DICTIONARY)

        self.assertRaises(KeyError, bit_map.testBit, self.ELT_8)
    # end def test_access_invalid_key_by_api

    def test_access_invalid_key_by_attribute(self):
        """
        Tests the use of an invalid Key, by attribute access
        """
        bit_map = BitStruct(HexList(0xFF), self.DICTIONARY)

        self.assertRaises(AttributeError, getattr, bit_map, self.ELT_8)
    # end def test_access_invalid_key_by_attribute

    def test_mode_little_endian(self):
        """
        Tests the construction method in Little Endian mode
        """
        bit_map = BitStruct(HexList(0x0F), self.DICTIONARY, mode=BitStruct.MODE_LITTLE_ENDIAN)

        bit_map.invertBit(self.ELT_0)

        self.assertEqual(HexList(0x8F), HexList(bit_map), "Inconsistent BitStruct value")
    # end def test_mode_little_endian

    def test_mode_big_endian(self):
        """
        Tests the construction method in Big Endian mode
        """
        bit_map = BitStruct(HexList(0xF0), self.DICTIONARY, mode=BitStruct.MODE_BIG_ENDIAN)

        bit_map.invertBit(self.ELT_0)

        self.assertEqual(HexList(0xF1), HexList(bit_map), "Inconsistent BitStruct value")
    # end def test_mode_big_endian

    @ignoredeprecation
    def test_get_by_index(self):
        """
        Tests the get of part of BitStruct value by index
        """
        bit_map = BitStruct(HexList("AABBCC"))

        expected_value = 0xAA
        obtained_value = bit_map[0]
        self.assertEqual(expected_value, obtained_value, "Inconsistent BitStruct byte value at offset 0")

        expected_value = 0xBB
        obtained_value = bit_map[1]
        self.assertEqual(expected_value, obtained_value, "Inconsistent BitStruct byte value at offset 1")

        expected_value = 0xCC
        obtained_value = bit_map[2]
        self.assertEqual(expected_value, obtained_value, "Inconsistent BitStruct byte value at offset 2")
    # end def test_get_by_index

    def test_get_by_slice(self):
        """
        Tests the get of part of BitStruct value by slice (index start, index stop)
        """
        bit_map = BitStruct(HexList("AABBCC"))

        expected_value = HexList("AABB")
        obtained_value = bit_map[0:2]
        self.assertEqual(expected_value, obtained_value, "Inconsistent BitStruct byte value for slice [0:2]")

        expected_value = HexList("BBCC")
        obtained_value = bit_map[1:3]
        self.assertEqual(expected_value, obtained_value, "Inconsistent BitStruct byte value for slice [1:3]")

        expected_value = HexList("AABBCC")
        obtained_value = bit_map[:]
        self.assertEqual(expected_value, obtained_value, "Inconsistent BitStruct byte value for full copy")

        # BitStruct slice
        dict_all = {self.ELT_0: 0,
                    'elt8': 8,
                    'elt16': 16,
                    'mask1': (8, 8),
                    'mask2': (4, 8),
                    'mask3': (12, 8)}

        bit_map = self.TestBitStruct(HexList("000FFF"), dict_all)

        obtained_bit_struct = bit_map[1:2]

        expected_dict = {'elt8': 8, 'mask1': (8, 8)}
        expected_bit_struct = self.TestBitStruct(HexList("0F"), expected_dict)

        self.assertEqual(expected_bit_struct, obtained_bit_struct, "Inconsistent BitStruct value for slice [1]")

        obtained_bit_struct = bit_map[:2]

        expected_dict = {'elt8': 0,
                         'elt16': 8,
                         'mask1': (0, 8),
                         'mask3': (4, 8)}
        expected_bit_struct = self.TestBitStruct(HexList("000F"), expected_dict)

        self.assertEqual(expected_bit_struct, obtained_bit_struct, "Inconsistent BitStruct value for slice [:2]")

        bit_map = self.TestBitStruct(HexList("000FFF"), dict_all, mode=BitStruct.MODE_LITTLE_ENDIAN)

        obtained_bit_struct = bit_map[:2]

        expected_dict = {'elt0': 0,
                         'elt8': 8,
                         'mask1': (8, 8),
                         'mask2': (4, 8)}
        expected_bit_struct = self.TestBitStruct(HexList("000F"), expected_dict)

        self.assertEqual(expected_bit_struct, obtained_bit_struct, "Inconsistent BitStruct value for slice [:2]")
    # end def test_get_by_slice

    @ignoredeprecation
    def test_set_by_index(self):
        """
        Tests the set of a part of BitStruct value by index
        """
        bit_map = BitStruct(HexList("AABBCC"))

        expected_value = HexList("AADDCC")
        bit_map[1] = 0xDD
        obtained_value = HexList(bit_map)

        self.assertEqual(expected_value, obtained_value, "Inconsistent BitStruct value")
    # end def test_set_by_index

    @ignoredeprecation
    def test_set_by_slice(self):
        """
        Tests the set of part of BitStruct value by slice (index start, index stop)
        """
        bit_map = BitStruct(HexList("AABBCC"))

        expected_value = HexList("EEFFCC")
        bit_map[0:2] = expected_value[0:2]
        obtained_value = HexList(bit_map)
        self.assertEqual(expected_value, obtained_value, "Inconsistent BitStruct byte value for slice [0:2]")

        expected_value = HexList("EE1122")
        bit_map[1:3] = expected_value[1:3]
        obtained_value = HexList(bit_map)
        self.assertEqual(expected_value, obtained_value, "Inconsistent BitStruct byte value for slice [1:3]")

        expected_value = HexList("334455")
        bit_map[:] = expected_value[:]
        obtained_value = HexList(bit_map)
        self.assertEqual(expected_value, obtained_value, "Inconsistent BitStruct byte value for full copy")
    # end def test_set_by_slice

    def test_set_by_slice_wrong_type(self):
        """
        Tests the set of part of BitStruct with a not empty dictionary
        """
        bit_map = BitStruct(HexList("AABBCC"), self.DICTIONARY)

        self.assertRaises(TypeError, bit_map.__setslice__, 1, 2, HexList(0x01))
    # end def test_set_by_slice_wrong_type

    def test_test_bit(self):
        """
        Tests the TestBit method
        """
        bit_map = BitStruct(HexList(0x07), self.DICTIONARY)

        self.assertEqual(1, bit_map.testBit(0), "Inconsistent bit 0")
        self.assertEqual(0, bit_map.testBit(4), "Inconsistent bit 4")
        self.assertEqual(1, bit_map.testBit(self.ELT_1), "Inconsistent bit")
        self.assertEqual(0, bit_map.testBit(self.ELT_5), "Inconsistent bit")
        self.assertEqual(1, bit_map.elt1, "Inconsistent bit")
        self.assertEqual(0, bit_map.elt5, "Inconsistent bit")
        self.assertEqual(0, bit_map.mask3, "Inconsistent bit")
    # end def test_test_bit

    def test_get_attr(self):
        """
        Tests the __getattr__ method
        """
        dic = {'mask1': (12, 4), 'mask2': ((4, 4), (16, 4))}

        bit_map = BitStruct(HexList("AABBCC"), dic)

        expected_result = 0x0B

        self.assertEqual(expected_result, bit_map.mask1, "Inconsistent mask result")

        expected_result = 0xAC

        self.assertEqual(expected_result, bit_map.mask2, "Inconsistent mask result")
    # end def test_get_attr

    def test_set_attr(self):
        """
        Tests the __setattr__ method
        """
        dic = {'mask1': (12, 4),
               'mask2': ((4, 4), (16, 4))}

        bit_map = BitStruct(HexList("A00B0C"), dic)

        expected_bit_struct = BitStruct(HexList("A0BB0C"), dic)

        bit_map.mask1 = 0x0B

        self.assertEqual(expected_bit_struct, bit_map, "Inconsistent BitStruct")

        expected_bit_struct = BitStruct(HexList("AABBCC"), dic)

        bit_map.mask2 = 0xAC

        self.assertEqual(expected_bit_struct, bit_map, "Inconsistent BitStruct")
    # end def test_set_attr

    def test_set_attr_wrong_key(self):
        """
        Tests the __setattr__ method with wrong key
        """
        mask = 'mask'

        bit_map = BitStruct(HexList("AABBCC"))

        self.assertRaises(KeyError, bit_map.__setattr__, mask, 2)
    # end def test_set_attr_wrong_key

    def test_test_bit_wrong_type(self):
        """
        Tests TestBit method with a wrong type
        """
        bit_map = BitStruct(HexList(0x0F), self.DICTIONARY)

        self.assertRaises(TypeError, bit_map.testBit, HexList(0x01))

        bit_map = BitStruct(HexList(0x0F), {'mask_invalid': [1, 2]})

        self.assertRaises(TypeError, bit_map.testBit, 'mask_invalid')
    # end def test_test_bit_wrong_type

    def test_test_bit_wrong_value(self):
        """
        Tests TestBit method with a wrong value
        """
        bit_map = BitStruct(HexList(0x0F), self.DICTIONARY)

        self.assertRaises(ValueError, bit_map.testBit, self.MASK_1)
    # end def test_test_bit_wrong_value

    def test_set_bit(self):
        """
        Tests the SetBit method
        """
        bit_map = BitStruct(HexList(0x0F), self.DICTIONARY)

        pos_or_name = 4

        self.assertEqual(0, bit_map.testBit(pos_or_name), "Inconsistent bit")

        bit_map.setBit(pos_or_name)

        self.assertEqual(1, bit_map.testBit(pos_or_name), "Inconsistent bit")

        pos_or_name = self.ELT_6

        self.assertEqual(0, bit_map.testBit(pos_or_name), "Inconsistent bit")

        bit_map.setBit(pos_or_name)

        self.assertEqual(1, bit_map.testBit(pos_or_name), "Inconsistent bit")
    # end def test_set_bit

    def test_update_bit_wrong_value(self):
        """
        Tests the SetBit method with a wrong value
        """
        bit_map = BitStruct(HexList(0x0F), self.DICTIONARY)

        self.assertRaises(ValueError, bit_map.updateBit, 1, 372)

        self.assertRaises(ValueError, setattr, bit_map, self.ELT_2, 372)
    # end def test_update_bit_wrong_value

    def test_clear_bit(self):
        """
        Tests the ClearBit method
        """
        bit_map = BitStruct(HexList(0x0F), self.DICTIONARY)

        # Find bit by position
        pos_or_name = 1

        self.assertEqual(1, bit_map.testBit(pos_or_name), "Inconsistent bit")

        bit_map.clearBit(pos_or_name)

        self.assertEqual(0, bit_map.testBit(pos_or_name), "Inconsistent bit")

        # Find bit by name
        pos_or_name = self.ELT_2

        self.assertEqual(1, bit_map.testBit(pos_or_name), "Inconsistent bit")

        bit_map.clearBit(pos_or_name)

        self.assertEqual(0, bit_map.testBit(pos_or_name), "Inconsistent bit")

        # Find bit by name: Mask of size 1
        pos_or_name = self.MASK_3

        self.assertEqual(1, bit_map.testBit(pos_or_name), "Inconsistent bit")

        bit_map.clearBit(pos_or_name)

        self.assertEqual(0, bit_map.testBit(pos_or_name), "Inconsistent bit")
    # end def test_clear_bit

    def test_clear_bit_wrong_length(self):
        """
        Tests the ClearBit method of a mask of wrong length
        """
        bit_map = BitStruct(HexList(0x0F), self.DICTIONARY)

        self.assertRaises(ValueError, bit_map.clearBit, self.MASK_2)
    # end def test_clear_bit_wrong_length

    def test_update_bit(self):
        """
        Tests the UpdateBit method
        """
        bit_map = BitStruct(HexList(0x0F), self.DICTIONARY)

        # Find bit by position
        pos_or_name = 1

        self.assertEqual(1, bit_map.testBit(pos_or_name), "Inconsistent bit")

        bit_map.updateBit(pos_or_name, 0)

        self.assertEqual(0, bit_map.testBit(pos_or_name), "Inconsistent bit")

        bit_map.updateBit(pos_or_name, 0)

        self.assertEqual(0, bit_map.testBit(pos_or_name), "Inconsistent bit")

        # Find bit by name
        pos_or_name = self.ELT_5

        self.assertEqual(0, bit_map.testBit(pos_or_name), "Inconsistent bit")

        bit_map.updateBit(pos_or_name, 1)

        self.assertEqual(1, bit_map.testBit(pos_or_name), "Inconsistent bit")

        bit_map.updateBit(pos_or_name, 1)

        self.assertEqual(1, bit_map.testBit(pos_or_name), "Inconsistent bit")

        # Find by attribute name
        self.assertEqual(0, bit_map.elt7, "Inconsistent bit")

        bit_map.elt7 = 1

        self.assertEqual(1, bit_map.elt7, "Inconsistent bit")

        # Set value with a boolean
        bit_map.elt7 = False

        self.assertEqual(0, bit_map.elt7, "Inconsistent bit")

        bit_map.elt7 = True

        self.assertEqual(1, bit_map.elt7, "Inconsistent bit")
    # end def test_update_bit

    def test_invert_bit(self):
        """
        Tests the InvertBit method
        """
        bit_map = BitStruct(HexList(0x0F), self.DICTIONARY)

        # Find bit by position
        pos_or_name = 1

        self.assertEqual(1, bit_map.testBit(pos_or_name), "Inconsistent bit")

        bit_map.invertBit(pos_or_name)

        self.assertEqual(0, bit_map.testBit(pos_or_name), "Inconsistent bit")

        # Find bit by name
        pos_or_name = self.ELT_5

        self.assertEqual(0, bit_map.testBit(pos_or_name), "Inconsistent bit")

        bit_map.invertBit(pos_or_name)

        self.assertEqual(1, bit_map.testBit(pos_or_name), "Inconsistent bit")
    # end def test_invert_bit

    def test_copy(self):
        """
        Tests the copy method
        """
        value = HexList(0x10)
        bit_map1 = BitStruct(value)

        expected_bit_struct = BitStruct(value)
        obtained_bit_struct = bit_map1.copy()

        self.assertEqual(HexList(expected_bit_struct), HexList(obtained_bit_struct), "Inconsistent BitStruct")
    # end def test_copy

    def test_deep_copy(self):
        """
        Tests the deepcopy method
        """
        value = HexList(0x10)
        bit_map1 = BitStruct(value)

        expected_bit_struct = BitStruct(value)
        obtained_bit_struct = bit_map1.deepcopy()

        self.assertEqual(HexList(expected_bit_struct), HexList(obtained_bit_struct), "Inconsistent BitStruct")

        obtained_bit_struct.setBit(0)

        self.assertNotEqual(HexList(expected_bit_struct), HexList(obtained_bit_struct), "Inconsistent BitStruct")
    # end def test_deep_copy

    def test_equal(self):
        """
        Tests __eq__ method
        """
        bit_map1 = BitStruct(HexList("0F"), self.DICTIONARY)
        bit_map2 = BitStruct(HexList("0F"), self.DICTIONARY)

        self.assertEqual(bit_map1, bit_map2, "BitStructs should be equal")

        bit_map2.elt1 = 0

        self.assertNotEqual(bit_map1, bit_map2, "BitStructs shouldn't be equal")

        bit_map2 = BitStruct(HexList("0F01"), self.DICTIONARY)

        self.assertNotEqual(bit_map1, bit_map2, "BitStructs shouldn't be equal")
    # end def test_equal

    def test_ne(self):
        """
        Tests __ne__ method
        """
        bit_map1 = BitStruct(HexList("0F"), self.DICTIONARY)
        bit_map2 = BitStruct(HexList("0F"), self.DICTIONARY)

        self.assertEqual(0, bit_map1 != bit_map2, "BitStructs should be equal")

        bit_map2.elt1 = 0

        self.assertEqual(1, bit_map1 != bit_map2, "BitStructs shouldn't be equal")

        bit_map2 = BitStruct(HexList("0F01"), self.DICTIONARY)

        self.assertEqual(1, bit_map1 != bit_map2, "BitStructs shouldn't be equal")
    # end def test_ne

    def test_len(self):
        """
        Tests the __len__ method
        """
        bit_map_value = HexList("0F")
        bit_map = BitStruct(bit_map_value, self.DICTIONARY)

        self.assertEqual(len(bit_map_value), len(bit_map), "Invalid BitStruct length")

        bit_map_value = HexList("0F0E")
        bit_map = BitStruct(bit_map_value, self.DICTIONARY)

        self.assertEqual(len(bit_map_value), len(bit_map), "Invalid BitStruct length")
    # end def test_len

    def test_create_summary(self):
        """
        Tests the CreateSummary method
        """
        # Dictionary defined
        bit_map = BitStruct(HexList(0x0F), self.DICTIONARY)

        expected_table = ['0F']
        for key, value in self.DICTIONARY.items():
            str_element = f'  - {key}'
            str_element += ' ' * (BitStruct.ELEMENT_OFFSET - len(str_element))
            if isinstance(value, int):
                if bit_map.testBit(key):
                    str_element += '= 1'
                else:
                    str_element += '= 0'
                # end if
            elif isinstance(value, tuple):
                str_element += f'= {bit_map.__getattr__(key)}'
            # end if
            expected_table.append(str_element)
        # end for

        obtained_log = bit_map.createSummary()

        obtained_table = obtained_log.split('\n')

        for elt in expected_table:
            assert (elt in obtained_table), f"Missing element of log! {elt}"
        # end for

        for elt in obtained_table:
            assert (elt in expected_table), f"Surplus element of log! '{elt}'"
        # end for

        # Dictionary not defined
        bit_map = BitStruct(HexList(0x0F))
        expected_log = "0F"
        obtained_log = bit_map.createSummary()

        self.assertEqual(expected_log, obtained_log, "Inconsistent log value")

        # Mode Little Endian
        bit_map = BitStruct(HexList(0x0F), mode=BitStruct.MODE_LITTLE_ENDIAN)
        expected_log = "0F"
        obtained_log = bit_map.createSummary()

        self.assertEqual(expected_log, obtained_log, "Inconsistent log value")

        # Hidden field:
        bit_map = BitStruct(HexList(0x0F), self.DICTIONARY, hidden=(self.MASK_2,))
        self.assertTrue(self.MASK_2 not in bit_map.createSummary(), 'Field not hidden')
    # end def test_create_summary

    def test_str(self):
        """
        Tests __str__ method
        """
        bit_map = BitStruct(HexList(0x0F), self.DICTIONARY)

        self.assertEqual(bit_map.createSummary(), str(bit_map), "Inconsistent string representation")
    # end def test_str

    def test_to_long(self):
        """
        Tests the toLong method
        """
        bit_map = BitStruct(HexList(0x10, 0x00))

        self.assertEqual(0x1000, bit_map.toLong(), "Inconsistent value of the BitStruct")

        self.assertEqual(0x0010, bit_map.toLong(True), "Inconsistent value of the BitStruct")
    # end def test_to_long

    def test_interpretation(self):
        """
        Tests the interpretation of the BitStruct values
        """
        bit_map = BitStruct(HexList(0xFF), self.DICTIONARY, interpreter=self.INTERPRETER)

        expected_table = ['FF']
        for key, value in self.DICTIONARY.items():
            str_element = f'  - {key}'
            str_element += ' ' * (BitStruct.ELEMENT_OFFSET - len(str_element))
            if isinstance(value, int):
                str_element += f'= 1 (bit {value} set)'
            elif isinstance(value, tuple):
                if key in self.INTERPRETER:
                    str_element += f'= {bit_map.__getattr__(key)} ({key} value is {bit_map.__getattr__(key)})'
                else:
                    str_element += f'= {bit_map.__getattr__(key)}'
                # end if
            # end if
            expected_table.append(str_element)
        # end for

        obtained_log = bit_map.createSummary()

        obtained_table = obtained_log.split('\n')

        for elt in expected_table:
            assert (elt in obtained_table), f"Missing element of log! {elt}"
        # end for

        for elt in obtained_table:
            assert (elt in expected_table), f"Surplus element of log! '{elt}'"
        # end for
    # end def test_interpretation

    def test_diff(self):
        """
        Tests the diff method
        """
        bit_map1 = BitStruct(HexList(0x96), self.DICTIONARY)
        bit_map2 = BitStruct(HexList(0x66), self.DICTIONARY)

        obtained = bit_map1.diff(bit_map2)
        expected = '\n'.join(('---',
                              '+++',
                              '@@ -1,9 +1,9 @@',
                              '-96',
                              '-  - elt7                 = 1',
                              '-  - elt6                 = 0',
                              '-  - elt5                 = 0',
                              '-  - elt4                 = 1',
                              '-  - mask2                = 9',
                              '+66',
                              '+  - elt7                 = 0',
                              '+  - elt6                 = 1',
                              '+  - elt5                 = 1',
                              '+  - elt4                 = 0',
                              '+  - mask2                = 6',
                              '   - elt3                 = 0',
                              '   - mask3                = 0',
                              '   - elt2                 = 1'))
        # Deployment of replacement process for python 2.6 compatibility
        while ' \n' in obtained:
            obtained = obtained.replace(' \n', '\n')
        # end while
        self.assertEqual(expected, obtained)
    # end def test_diff
# end class BitStructTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
