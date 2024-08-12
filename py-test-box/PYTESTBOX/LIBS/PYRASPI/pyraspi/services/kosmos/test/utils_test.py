#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.test.utils_test
:brief: Tests for Kosmos Utils class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/05/07
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from itertools import chain
from typing import Generator
from unittest import TestCase

from pyraspi.services.kosmos.utils import all_permutations
from pyraspi.services.kosmos.utils import find_duplicates
from pyraspi.services.kosmos.utils import get_attributes
from pyraspi.services.kosmos.utils import is_unique
from pyraspi.services.kosmos.utils import pretty_class
from pyraspi.services.kosmos.utils import pretty_dict
from pyraspi.services.kosmos.utils import pretty_list
from pyraspi.services.kosmos.utils import sign_ext_12bits
from pyraspi.services.kosmos.utils import sign_ext_3bits
from pyraspi.services.kosmos.utils import sort_attributes_by_value
from pyraspi.services.kosmos.utils import sort_dict


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class KosmosUtilsTestCase(TestCase):
    """
    Unitary Test for Kosmos Utils class.
    """

    def test_is_unique(self):
        """
        Validate ``pyraspi.services.kosmos.utils.is_unique`` method.
        """
        # Test all valid bitfields
        expected_values = [([], True),
                           ([1, 2, 3, 4], True),
                           ([1, 2, 2, 3, 3, 3, 4], False),
                           (['l', 'i', 'l', 'a'], False),
                           ('hello world', False)]
        for input_list, expected_uniqueness in expected_values:
            self.assertEqual(expected_uniqueness, is_unique(input_list), msg=input_list)
        # end for
    # end def test_is_unique

    def test_find_duplicates(self):
        """
        Validate ``pyraspi.services.kosmos.utils.find_duplicates`` method.
        """
        # Test all valid bitfields
        expected_values = [([], []),
                           ([1, 2, 3, 4], []),
                           ([1, 2, 2, 3, 3, 3, 4], [2, 3]),
                           ([3, 3, 2, 2, 2, 2, 1], [3, 2]),
                           (['l', 'i', 'l', 'a'], ['l']),
                           ('hello world', list('lo'))]
        for input_sequence, expected_duplicates in expected_values:
            duplicates = find_duplicates(input_sequence)
            self.assertEqual(expected_duplicates, duplicates, msg=input_sequence)
            self.assertTrue(is_unique(duplicates), msg=duplicates)
        # end for
    # end def test_find_duplicates

    def test_sign_ext_3bits(self):
        """
        Validate ``pyraspi.services.kosmos.utils.sign_ext_3bits`` method.
        """
        # Test all valid bitfields
        expected_values = [(0x00, 0), (0x01, 1), (0x02, 2), (0x03, 3),
                           (0x04, -4), (0x05, -3), (0x06, -2), (0x07, -1)]
        for bitfield, signed_int in expected_values:
            self.assertEqual(signed_int, sign_ext_3bits(bitfield), msg=hex(bitfield))
        # end for

        # Test out-of-bounds bitfield
        with self.assertRaises(AssertionError):
            sign_ext_3bits(0x07 + 1)
        # end with
    # end def test_sign_ext_3bits

    def test_sign_ext_12bits(self):
        """
        Validate ``pyraspi.services.kosmos.utils.sign_ext_12bits`` method.
        """
        # Test all valid bitfields
        pos_values = ((i, i) for i in range(0, 0x7FF + 1))
        neg_values = ((i, (n - 0x800)) for n, i in enumerate(range(0x800, 0xFFF + 1)))
        expected_values = chain(pos_values, neg_values)

        for bitfield, signed_int in expected_values:
            self.assertEqual(signed_int, sign_ext_12bits(bitfield), msg=hex(bitfield))
        # end for

        # Test out-of-bounds bitfield
        with self.assertRaises(AssertionError):
            sign_ext_12bits(0x0FFF + 1)
        # end with
    # end def test_sign_ext_12bits

    def test_all_permutations(self):
        """
        Validate ``pyraspi.services.kosmos.utils.all_permutations`` method.
        """
        self.assertEqual({(bool,), (int,)},
                         all_permutations([bool, int], r=1))
        self.assertEqual({(1, 2), (3, 2), (1, 3), (3, 3), (3, 1), (2, 1), (2, 3), (2, 2), (1, 1)},
                         all_permutations({1, 2, 3}, r=2))
        self.assertEqual({('a', 'a', 'z'), ('a', 'a', 'a'), ('z', 'z', 'z'), ('a', 'z', 'z')},
                         all_permutations('az', r=3))
    # end def test_all_permutations

    def test_get_attributes(self):
        """
        Validate ``pyraspi.services.kosmos.utils.get_attributes`` method.
        """
        class Klass:
            """
            Test class
            """
            a = 1
            b = 2
            c = 3
        # end class Klass
        self.assertIsInstance(get_attributes(Klass), Generator)
        self.assertEqual([('a', 1), ('b', 2), ('c', 3)], list(get_attributes(Klass)))
        self.assertEqual([('a', 1), ('b', 2), ('c', 3)], list(get_attributes(Klass())))
        self.assertEqual({'a': 1, 'b': 2, 'c': 3}, dict(get_attributes(Klass)))
        self.assertEqual([], list(get_attributes(object())))
    # end def test_get_attributes

    def test_sort_attributes_by_value(self):
        """
        Validate ``pyraspi.services.kosmos.utils.sort_attributes_by_value`` method.
        """
        class Klass:
            """
            Test class
            """
            z = 9
            a = 1
        # end class Klass
        self.assertEqual({'a': 1, 'z': 9}, sort_attributes_by_value(Klass))
        self.assertEqual({'a': 1, 'z': 9}, sort_attributes_by_value(Klass()))
        self.assertEqual(dict(), sort_attributes_by_value(object))
    # end def test_sort_attributes_by_value

    def test_sort_dict(self):
        """
        Validate ``pyraspi.services.kosmos.utils.sort_dict`` method.
        """
        self.assertEqual({'a': 1, 'z': 9}, sort_dict({'z': 9, 'a': 1}))
        self.assertEqual(dict(), sort_dict(dict()))
    # end def test_sort_dict

    def test_pretty_dict(self):
        """
        Validate ``pyraspi.services.kosmos.utils.pretty_dict`` method.
        """
        self.assertEqual('{1 = a,\n 2 = b,\n 3 = c}', pretty_dict({1: 'a', 2: 'b', 3: 'c'}))
        self.assertEqual('{1 = A,\n 2 = B,\n 3 = C}', pretty_dict({1: 'a', 2: 'b', 3: 'c'}, formatter=str.upper))
        self.assertEqual('{}', pretty_dict(dict()))
    # end def test_pretty_dict

    def test_pretty_list(self):
        """
        Validate ``pyraspi.services.kosmos.utils.pretty_list`` method.
        """
        self.assertEqual('[1,\n 2,\n 3]', pretty_list([1, 2, 3]))
        self.assertEqual('[0x1,\n 0x2,\n 0x3]', pretty_list([1, 2, 3], formatter=hex))
        self.assertEqual('[]', pretty_list(dict()))
    # end def test_pretty_list

    def test_pretty_class(self):
        """
        Validate ``pyraspi.services.kosmos.utils.pretty_class`` method.
        """
        class Klass:
            """
            Test class
            """
            a = 1
            b = 2
            c = 3
        # end class Klass
        self.assertEqual('{a = 1,\n b = 2,\n c = 3}', pretty_class(Klass))
        self.assertEqual('{a = 1,\n b = 2,\n c = 3}', pretty_class(Klass()))
        self.assertEqual('{a = 0x1,\n b = 0x2,\n c = 0x3}', pretty_class(Klass, formatter=hex))
        self.assertEqual('{a = 0x1,\n b = 0x2,\n c = 0x3}', pretty_class(Klass(), formatter=hex))
        self.assertEqual('{}', pretty_class(object()))
    # end def test_pretty_class
# end class KosmosUtilsTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
