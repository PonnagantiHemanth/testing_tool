#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.utils
:brief: Kosmos utils classes and miscellaneous code
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/03/09
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from ctypes import c_int16
from ctypes import c_int8
from enum import Enum
from itertools import chain
from itertools import combinations_with_replacement
from itertools import permutations
from operator import itemgetter
from textwrap import indent
from typing import Dict
from typing import Generator
from typing import Iterable
from typing import Mapping
from typing import Sequence
from typing import Set
from typing import Tuple


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class AutoNameEnum(str, Enum):
    """
    Base class for String Enum. This adds the required method called by `auto()` to guaranty that:
     - Enum member names are uppercase;
     - Enum member values are lowercase, and are automatically deduced from the members' name using `auto()`.
    """
    @staticmethod
    def _generate_next_value_(name, *args, **kwargs):
        """
        Callback for `Enum.auto()` method that returns the lowercase string value of the uppercase enum entry name.

        :param name: Enum member name. Must be uppercase because it is a constant.
        :type name: ``str``
        :param args: Other unused parameters: start, count, last_values
        :type args: ``tuple[Any]``
        :param kwargs: Other unused parameters: start, count, last_values
        :type kwargs: ``dict[str, Any]``

        :return: lowercase string value of the enum entry name
        :rtype: ``str``

        :raise ``AssertionError``: enum name is not uppercase
        """
        assert name.isupper(), f'Enum entry name must be uppercase, got {name}.'
        return name.lower()
    # end def _generate_next_value_
# end class AutoNameEnum


def is_unique(lst):
    """
     Test if all items in a list are unique.

     Example:
      - ``is_unique([])``                    returns ``True``
      - ``is_unique([1, 2, 3, 4])``          returns ``True``
      - ``is_unique([1, 2, 2, 3, 3, 3, 4])`` returns ``False``
      - ``is_unique(['l', 'i', 'l', 'a'])``  returns ``False``
      - ``is_unique('hello world')``         returns ``False``

    :param lst: List of items to compare for equality
    :type lst: ``Iterable``

    :return: ``True`` if all item in the list are unique, ``False`` otherwise
    :rtype: ``bool``
    """
    return len(lst) == len(set(lst))
# end def is_unique


def find_duplicates(input_sequence):
    """
     Find all duplicates items in a Sequence. Preserve order.

     Example:
      - ``find_duplicates([])``                    returns ``[]`` (empty list)
      - ``find_duplicates([1, 2, 3, 4])``          returns ``[]`` (empty list)
      - ``find_duplicates([1, 2, 2, 3, 3, 3, 4])`` returns ``[2, 3]``
      - ``find_duplicates([3, 3, 2, 2, 2, 1])``    returns ``[3, 2]``
      - ``find_duplicates(['l', 'i', 'l', 'a'])``  returns ``['l']``
      - ``find_duplicates('hello world')``         returns ``list('lo')``

     Complexity: O(n^3)

    :param input_sequence: Sequence of items to look for duplicate
    :type input_sequence: ``Sequence``

    :return: Unique list of duplicated items, in the order they appear in the input Sequence
    :rtype: ``List``
    """
    duplicates = []
    for index_next, item in enumerate(input_sequence[:-1], 1):
        if item in input_sequence[index_next:] and item not in duplicates:
            duplicates.append(item)
        # end if
    # end for
    return duplicates
# end def find_duplicates


def sign_ext_3bits(bitfield):
    """
    Sign-extend a ctypes 3-bit signed integer into a Python signed integer.

    :param bitfield: 3-bit signed integer (from ctypes bitfield)
    :type bitfield: ``int``

    :return: signed integer (Python)
    :rtype: ``int``

    :raise ``AssertionError``: Out-of-bounds 3-bit bitfield
    """
    assert not (bitfield & ~0x7), f'Out-of-bounds 3-bit bitfield {bitfield:#x}'
    if bitfield & 0x04:  # bitfield is 3-bit wide; bit[2] set == negative number
        return c_int8(bitfield | 0xF8).value  # Two's complement sign extension
    else:
        return bitfield
    # end if
# end def sign_ext_3bits


def sign_ext_12bits(bitfield):
    """
    Sign-extend a ctypes 12-bit signed integer into a Python signed integer.

    :param bitfield: 12-bit signed integer (from ctypes bitfield)
    :type bitfield: ``int``

    :return: signed integer (Python)
    :rtype: ``int``

    :raise ``AssertionError``: Out-of-bounds 12-bit bitfield
    """
    assert not (bitfield & ~0xFFF), f'Out-of-bounds 12-bit bitfield {bitfield:#x}'
    if bitfield & 0x800:  # bitfield is 12-bit wide; bit[11] set == negative number
        return c_int16(bitfield | 0xF000).value  # Two's complement sign extension
    else:
        return bitfield
    # end if
# end def sign_ext_12bits


def all_permutations(iterable, r):
    """
    Return all r-length combinations and permutations, from a given iterable of values.

    Examples:
         - ``all_permutations({1, 2, 3}, r=2)`` returns:
           ``{(1, 2), (3, 2), (1, 3), (3, 3), (3, 1), (2, 1), (2, 3), (2, 2), (1, 1)}``
         - ``all_permutations('az', r=3)`` returns:
           ``{('a', 'a', 'z'), ('a', 'a', 'a'), ('z', 'z', 'z'), ('a', 'z', 'z')}``

    :param iterable: Collection of item to make combinations and permutations from
    :type iterable: ``Iterable``
    :param r: Length of each combination and permutation. i.e ``r=2`` will produce tuples of two items.
    :type r: ``int``

    :return: Set of all combinations and permutations
    :rtype: ``Set[Tuple]``
    """
    return set(chain(combinations_with_replacement(iterable=iterable, r=r),
                     permutations(iterable=iterable, r=r)))
# end def all_permutations


def get_attributes(myclass):
    """
    Get name:value class/object attributes, excluding methods and attributes starting by an underscore.

    :param myclass: Class or object to look for arguments
    :type myclass: ``Type or object``

    :return: <name:value> class attributes mapping, sorted by name
    :rtype: ``Generator[Tuple[str, int]]``
    """
    return ((name, getattr(myclass, name)) for name in dir(myclass)
            if not name.startswith('_') and not callable(getattr(myclass, name)))
# end def get_attributes


def sort_attributes_by_value(myclass):
    """
    Get name:value class/object attributes, excluding methods and attributes starting by an underscore.

    :param myclass: Class or object to look for arguments
    :type myclass: ``Type or object``

    :return: <name:value> class attributes mapping, sorted by value
    :rtype: ``Dict[str, int]``
    """
    return dict(sorted(get_attributes(myclass), key=itemgetter(1)))
# end def sort_attributes_by_value


def sort_dict(mydict, key=None):
    """
    Return a new sorted dictionary.

    :param mydict: dictionary to be sorted
    :type mydict: ``Mapping``
    :param key: function of one argument that is used to extract a comparison key from each element in iterable
                (for example, key=str.lower), defaults to None (compare the elements directly) - OPTIONAL
    :type key: ``Callable or None``

    :return: New sorted dictionary
    :rtype: ``Dict``
    """
    return dict(sorted(mydict.items(), key=key))
# end def sort_dict


def pretty_dict(mydict, formatter=str):
    """
    Pretty-format Dictionary to String.

    Example:
    ``pretty_dict({1:'a', 2:'b', 3:'c'})`` returns::
        {1 = a,
         2 = b,
         3 = c}

    :param mydict: List to be pretty-formatted to string
    :type mydict: ``Mapping``
    :param formatter: Value formatter method, defaults to __str__ representation - OPTIONAL
    :type formatter: ``Callable``

    :return: pretty-formatted string
    :rtype: ``str``
    """
    return '{' + indent(',\n'.join(f'{k} = {formatter(v)}' for k, v in mydict.items()), ' ')[1:] + '}'
# end def pretty_dict


def pretty_list(mylist, formatter=str):
    """
    Pretty-format List to String.

    Example:
    ``pretty_list([1, 2, 3])`` returns:
        [1,
         2,
         3]

    :param mylist: List to be pretty-formatted to string
    :type mylist: ``Iterable``
    :param formatter: Value formatter method, defaults to __str__ representation - OPTIONAL
    :type formatter: ``Callable``

    :return: pretty-formatted string
    :rtype: ``str``
    """
    return '[' + indent(',\n'.join(map(formatter, mylist)), ' ')[1:] + ']'
# end def pretty_list


def pretty_class(myclass, formatter=str):
    """
    Pretty-format Class or Class Instance members to String.

    Example::
    class Klass:
        a = 1
        b = 2
        c = 3
    # end def Klass
    ``pretty_class(Klass)`` returns:
        {a = 1,
         b = 1,
         c = 3}

    :param myclass: Class to be pretty-formatted to string
    :type myclass: ``Type or object``
    :param formatter: Value formatter method, defaults to __str__ representation - OPTIONAL
    :type formatter: ``Callable``

    :return: pretty-formatted string
    :rtype: ``str``
    """
    return pretty_dict(dict(get_attributes(myclass)), formatter=formatter)
# end def pretty_class

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
