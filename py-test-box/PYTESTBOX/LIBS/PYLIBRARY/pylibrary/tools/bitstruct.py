#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.tools.bitstruct
:brief: BitStruct interface definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/06/23
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import copy
from warnings import warn

from pylibrary.tools.diff import DiffableMixin
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BitStruct(DiffableMixin):
    """
    ``BitStruct`` is a ``HexList-compatible`` object, that contains field definitions
    destined to be stored at bit positions within a ``HexList``.

    The ``BitStruct`` class helps the user to:

        * Test, set, clear, update and invert a bit in a bitstruct
        * Convert a ``BitStruct`` to a ``HexList``, and provide a string representation.
        * Compare two ``BitStructs`` for equality
        * Access the length of a ``BitStruct``
        * Make a copy/deepcopy

    See ``BitStruct``'s constructor for detailed examples.
    """

    # Mode Big Endian definition (MSB First / LSB Last)
    # bit Power    7   6   5   4   3   2   1   0
    #             MSB                         LSB
    MODE_BIG_ENDIAN = 0

    # Mode Little Endian definition (LSB First / MSB Last)
    # bit Power    0   1   2   3   4   5   6   7
    #             LSB                         MSB
    MODE_LITTLE_ENDIAN = 1

    # Offset used to format the summary of dictionary elements
    ELEMENT_OFFSET = 25

    def __init__(self, _value, _dictionary=None, _interpreter=None, _mode=None, _aliases=None, _hidden=None, **kwargs):
        """
        Create a new BitStruct

        :param _value: Value of the ``BitStruct``
        :type _value: ``HexList`` or ``int`` or ``Numeral`` or ``BitStruct``
        :param _dictionary: Bit definitions of the ``BitStruct`` - OPTIONAL
        :type _dictionary: ``dict``
        :param _interpreter: Bits and masks values interpretation - OPTIONAL
        :type _interpreter: ``dict``
        :param _mode: Mode to use for ``BitStruct`` interpretation - OPTIONAL
        :type _mode: ``int``
        :param _aliases: Aliases to apply - OPTIONAL
        :type _aliases: ``dict``
        :param _hidden: List if values to hide from the summary - OPTIONAL
        :type _hidden: ``tuple``
        :param kwargs: Initialization of ``_dictionary`` elements - OPTIONAL
        :type kwargs: ``object``

        **Note**: The ``_dictionary`` matches the name of a bit to its index in the ``BitStruct``

        **Example** of _dictionary::

            _dictionary = {'nameOfBit1' : 0,
                          'nameOfBit2' : 3,
                          'nameOfMask1': (5, 2)}


        **Note**: Dictionary mask definition:
            * A mask is defined by a tuple: ``(start_bit_pos, bit_count)``
            * Or a tuple of tuples: ``((pos0, count0), (pos1, count1) ... )``


        **Example** of bit test::

            bitMap = BitStruct(HexList(0x01), _dictionary)
            # Using testBit method
            # --------------------
            if bitMap.testBit('nameOfBit1'):
                ...
            # end if

            # Directly with bit name (equivalent previous test)
            # ----------------------
            if bitMap.nameOfBit1:
                ...
            # end if


        **Example** of mask use::

            bitMap = BitStruct(HexList(0x60), _dictionary)
            maskValue = bitMap.nameOfMask1        # maskValue = 3
            bitMap.nameOfMask1 = 2                # bitMap._value = HexList(0x40)


        **Warning**: The names of bit and mask should not contain spaces or special characters.

        **Warning**: If a mask is defined with several parts, the tuples has to be sorted by position.
        Example: ``((pos0, size0), (pos1, size1), (pos2, size2))`` with ``pos0 < pos1 < pos2``
        """
        super(BitStruct, self).__init__()

        _x_input = ((_value,       'value',       None),
                    (_dictionary,  'dictionary',  None),
                    (_interpreter, 'interpreter', None),
                    (_mode,        'mode',        self.MODE_BIG_ENDIAN),
                    (_aliases,     'aliases',     None),
                    (_hidden,      'hidden',      tuple()))

        _x_dictionary = _dictionary if _dictionary is not None else kwargs.get('dictionary', {})

        # Manually handle aliases
        def _convert(_x_value, _x_key, _x_default):
            """
            Coalesces a value from the arguments, keyword arguments and dictionary to a fallback

            :param _x_value: The value, passed as a recognized parameter
            :type _x_value: ``object``
            :param _x_key: The legacy parameter name
            :type _x_key: ``str``
            :param _x_default: The default value, that should be used in the parameter
            :type _x_default: ``object``

            :return: The coalesced value
            :rtype: ``object``
            """
            _x_result = _x_value

            # An old-style keyword argument is used
            if _x_key in kwargs:
                # No new-style keyword argument is used
                if _x_value is None:
                    # The old-style argument is found in the dictionary
                    if _x_key in _x_dictionary:
                        # Warn the user, as this may cause a silent conflict
                        warn(f'BitStruct construction should define _{_x_key} instead of (or in addition to) {_x_key}',
                             DeprecationWarning,
                             stacklevel=3)

                    else:
                        _x_result = kwargs[_x_key]
                        del kwargs[_x_key]
                    # end if
                # end if
            # end if

            if _x_result is None:
                _x_result = _x_default
            # end if

            return _x_result
        # end def _convert
        _value, _dictionary, _interpreter, _mode, _aliases, _hidden = [_convert(*e) for e in _x_input]

        # Value initialization
        if not isinstance(_value, (HexList, BitStruct, Numeral, int)):
            raise TypeError(f"Inconsistent _value type {type(_value).__name__}. Should use BitStruct, HexList or "
                            f"Numeral instead")
        # end if

        if isinstance(_value, int):
            _value = Numeral(_value)
        # end if

        if isinstance(_value, Numeral):
            _value = HexList(_value.value)
        # end if

        # Dictionary, _interpreter and _aliases initialization
        self._dict = dict(_dictionary) if _dictionary is not None else {}
        self._interpreter = dict(_interpreter) if _interpreter is not None else {}
        self._aliases = dict(_aliases) if _aliases is not None else {}
        self._hidden = _hidden

        for parameter_name in ('_dictionary', '_interpreter', '_mode', '_aliases', '_hidden'):
            if parameter_name in self._dict:
                raise ValueError(f'{self.__class__.__name__} defines a BitStruct with a reserved field '
                                 f'name: {parameter_name}')
            # end if

            if parameter_name in self._interpreter:
                ValueError(f'{self.__class__.__name__} defines a BitStruct with a reserved field '
                           f'name: {parameter_name}')
            # end if
        # end for

        if isinstance(_value, BitStruct):
            self._value = _value._value
            self._dict.update(_value._dict)
            self._interpreter.update(_value._interpreter)
            self._aliases.update(_value._aliases)
        else:
            self._value = _value
        # end if

        # Mode initialization
        self._default_mode = self.MODE_BIG_ENDIAN
        self._mode = self._default_mode
        if _mode is not None:
            if not isinstance(_mode, int):
                raise TypeError(f"Inconsistent Mode type {type(_value).__name__}. Should use integer instead")
            # end if

            if _mode != self._default_mode:
                self._value = self.__convert_value(self._default_mode, _mode)
            # end if

            self._mode = _mode

        # end if

        # Initialization of _dictionary elements
        for key, _value in kwargs.items():
            setattr(self, key, _value)
        # end for

        # The summary is created with ordering bits MSB first
        self.summary_msb_first = True
    # end def __init__

    def __get_pos(self, pos_or_name):
        """
        Get position of a bit

        :param pos_or_name: Position or name of the bit
        :type pos_or_name: ``int`` or ``str``

        :return: Position of the bit
        :rtype: ``int``
        """
        if isinstance(pos_or_name, int):
            pos = pos_or_name
        elif isinstance(pos_or_name, str):
            if pos_or_name in self._dict:
                pos = self._dict[pos_or_name]
            else:
                raise KeyError(f"Position: Inconsistent value type, should use integer or "
                               f"string, instead {pos_or_name}")
            # end if
        else:
            raise TypeError(f"posOrName has an invalid type: {type(pos_or_name).__name__}")
        # end if

        if isinstance(pos, tuple):
            if pos[1] == 1:
                pos = pos[0]
            else:
                raise ValueError("A bit should have a length of 1")
            # end if
        else:
            if not isinstance(pos, int):
                raise TypeError(f"Dictionary has an invalid value type: {type(pos).__name__}")
            # end if
        # end if

        return pos
    # end def __get_pos

    def __convert_value(self, from_mode, to_mode):
        """
        Convert the value (switch mode Big Endian to Little Endian)

        :param from_mode: Mode from which to convert the value
        :type from_mode: ``int``
        :param to_mode: Mode in which to convert the value
        :type to_mode: ``int``

        :return: Converted value
        :rtype: ``HexList``
        """
        value = None
        if from_mode == self.MODE_BIG_ENDIAN:
            if to_mode == self.MODE_LITTLE_ENDIAN:
                value = self.__invert_value()
            # end if
        # end if
        return value
    # end def __convert_value

    def __invert_value(self):
        """
        Bit to bit inversion of value

        :return: Inverted value
        :rtype: ``HexList``

        **Note**: With initial value 76543210 (each number reference a bit) we obtain:
                    * After the operation v = ((v & 0x55) << 1) | ((v & 0xAA) >> 1), we have 67 45 23 01
                    * After the operation v = ((v & 0x33) << 2) | ((v & 0xCC) >> 2), we have 4567 0123
                    * After the operation v = ((v & 0x0F) << 4) | ((v & 0xF0) >> 4), we have 01234567
        """
        raw = []
        for element in reversed(self._value):
            element = ((element & 0x55) << 1) | ((element & 0xAA) >> 1)
            element = ((element & 0x33) << 2) | ((element & 0xCC) >> 2)
            element = ((element & 0x0F) << 4) | ((element & 0xF0) >> 4)
            raw.append(element)
        # end for
        result = HexList()
        result.extendRaw(raw)
        return result
    # end def __invertValue

    def __getnewargs__(self):
        """
        Used only for copy/deepcopy method

        :return: An empty tuple (no arguments to constructor)
        :rtype: ``tuple``
        """
        return tuple()
    # end def __getnewargs__

    def __getstate__(self):
        """
        Used only for copy/deepcopy method

        :return: The internal object state
        :rtype: ``dict``
        """
        return self.__dict__
    # end def __getstate__

    def __setstate__(self, state):
        """
        Used only for copy/deepcopy method

        :param state: The new internal object state
        :type state: ``dict``
        """
        self.__dict__.update(state)
    # end def __setstate__

    def _get_pos_sizes(self, name):
        """
        Extracts the tuples (position, size) for a given field definition.

        :param name: The field name
        :type name: ``str``

        :return: The wanted tuples (position, size)
        :rtype: ``tuple[tuple[int, int]]``
        """
        name = self._aliases.get(name, name)
        if name in self._dict:
            pos_sizes_pairs = None
            mask_value = self._dict[name]
            if isinstance(mask_value, int):
                pos_sizes_pairs = ((mask_value, 1),)
            elif isinstance(mask_value, (tuple, list)):
                if isinstance(mask_value[0], int):
                    pos_sizes_pairs = (mask_value,)
                else:
                    pos_sizes_pairs = mask_value
                # end if
            # end if
        else:
            raise AttributeError(f"{self.__class__.__name__} has no attribute {name}")
        # end if

        return pos_sizes_pairs
    # end def _get_pos_sizes

    def __getattr__(self, name):
        """
        Get the value of an attribute

        :param name: The name of the decorated function or member
        :type name: ``str``

        :return: Bit status or mask value
        :rtype: ``bool`` or ``int``
        """
        shift = 0
        value = self._value.toLong()
        result = 0
        for position, size in self._get_pos_sizes(name):
            result |= ((value >> position) & ((1 << size) - 1)) << shift
            shift += size
        # end for

        return result
    # end def __getattr__

    def __setattr__(self, name, value):
        """
        Set the value of an attribute

        :param name: Name of the mask or bit
        :type name: ``str``
        :param value: Value of the mask or bit
        :type value: ``int``
        """
        if name in ('_dict', '_value', '_mode', '_default_mode', '_interpreter', '_hidden', '_aliases',
                    'summary_msb_first'):
            # Set an attribute
            self.__dict__[name] = value
        else:
            name = self._aliases.get(name, name)
            if name not in self._dict:
                raise KeyError(f"Key '{name}' not defined in dictionary.")
            else:
                new_value = 0
                new_mask = 0
                shift = 0
                max_shift = 0
                for pos, size in self._get_pos_sizes(name):
                    new_mask |= (((1 << size) - 1) << pos)
                    new_value |= ((value >> shift) & ((1 << size) - 1)) << pos
                    max_shift = max(max_shift, pos+size)
                    shift += size
                # end for

                if (value >> max_shift) != 0:
                    raise ValueError(f'Value {value} too big to fit in bitfield {name} ({max_shift} bits long)')
                # end if

                mask = ~HexList(Numeral(new_mask,  byteCount=len(self._value), fixedLength=True, littleEndian=False))
                value = HexList(Numeral(new_value,  byteCount=len(self._value), fixedLength=True, littleEndian=False))
                self._value &= mask
                self._value |= value
            # end if
        # end if
    # end def __setattr__

    def __getitem__(self, ind):
        """
        Get one element of '_value'
 
        :param ind: The index of the element(s) of value
        :type ind: ``int``
 
        :return: Value of on element of '_value'
        """
        if isinstance(ind, slice):
            return self.__getslice__(ind.start, ind.stop)
        else:
            return self._value.__getitem__(ind)
        # end if
    # end def __getitem__
 
    def __setitem__(self, ind, value):
        """
        Set one element of '_value'
 
        :param ind: Index of the element to update
        :type ind: ``int``
        :param value: New value of the element
        :type value: ``int``
        """
        warn("Use of deprecated method '__setitem__'. Should use 'setBit' and 'clearBit' instead",
             category=DeprecationWarning,
             stacklevel=2)
        self._value.__setitem__(ind, value)
    # end def __setitem__

    def __getslice__(self, ind_begin, ind_end):
        """
        Get some element(s) of self

        :param ind_begin: Index of first element to get
        :type ind_begin: ``int``
        :param ind_end: Index of element following last element to get
        :type ind_end: ``int``

        :return: Elements of '_value' or self if dictionary not empty
        :rtype: ``BitStruct``
        """
        if ind_begin is None:
            ind_begin = 0
        # end if
        
        if ind_end is None:
            ind_end = len(self)
        # end if
        
        value = self._value
        if self._mode != self._default_mode:
            value = self.__convert_value(self._default_mode, self._mode)
        # end if

        bit_map = BitStruct(value.__getslice__(ind_begin, ind_end), {}, mode=self._mode)

        # Not Empty dictionary
        if len(self._dict):
            for key, value in self._dict.items():
                if self._mode == self._default_mode:
                    nb_bit_to_move = (len(self) - ind_begin - ind_end) * 8
                else:
                    nb_bit_to_move = ind_begin * 8
                # end if
                bit_range = list(range(ind_begin * 8 + nb_bit_to_move, ind_end * 8 + nb_bit_to_move))
                if isinstance(value, int):
                    # Bit definition
                    if value in bit_range:
                        bit_map._dict[key] = value - nb_bit_to_move
                    # end if
                elif isinstance(value, tuple):
                    # Mask definition
                    if value[0] in bit_range and (value[0]+value[1]-1) in bit_range:
                        bit_map._dict[key] = (value[0] - nb_bit_to_move, value[1])
                    # end if
                # end if
            # end for
        # end if

        return bit_map
    # end def __getslice__

    def __setslice__(self, ind_begin, ind_end, value):
        """
        Get some element(s) of value

        :param ind_begin: Index of first element to get
        :type ind_begin: ``int``
        :param ind_end: Index of element following last element to get
        :type ind_end: ``int``
        :param value: New value of the elements
        :type value: ``HexList``
        """
        if not len(self._dict):
            warn("Use of deprecated method '__setslice__'. Should use '__hexlist__' instead",
                 category=DeprecationWarning,
                 stacklevel=1)
            self._value.__setslice__(ind_begin, ind_end, value)
        else:
            raise TypeError("Not empty dictionary disables '__setslice__' method")
        # end if
    # end def __setslice__

    def __len__(self):
        """
        Obtains the length of this BitStruct

        :return: The actual length of the BitStruct.
        :rtype: ``int``
        """
        return len(self._value)
    # end def __len__

    def __eq__(self, other):
        """
        Check equality between two BitStruct objects

        :param other: BitStruct object to compare to
        :type other: ``BitStruct``

        :return: Flag indicating if there is equality
        :rtype: ``bool``
        """
        return HexList(self) == HexList(other)
    # end def __eq__

    def __ne__(self, other):
        """
        Check difference between two BitStruct objects

        :param other: BitStruct object to compare to
        :type other: ``BitStruct``

        :return: Flag indicating if there is inequality
        :rtype: ``bool``
        """
        return not (self == other)
    # end def __ne__

    def __str__(self):
        """
        Convert BitStruct into string (createSummary)

        :return: Summary
        :rtype: ``str``
        """
        return self.createSummary()
    # end def __str__

    def __repr__(self):
        """
        Create a string representation of the current object

        :return: Representation of the BitStruct
        :rtype: ``str``
        """

        if len(self._dict):
            # Creation of summary from dictionary content
            args = ', '.join((f'{key}={getattr(self, key)}' for key in sorted(self._dict.keys())))
        else:
            args = repr(HexList(self))
        # end if

        return f'{self.__class__.__name__}({args})'
    # end def __repr__

    def __hexlist__(self):
        """
        Create HexList representation of the BitStruct

        :return: HexList representation
        :rtype: ``HexList``
        """
        value = self._value
        if self._mode != self._default_mode:
            value = self.__convert_value(self._default_mode, self._mode)
        # end if

        return HexList(value)
    # end def __hexlist__

    def toLong(self, littleEndian=False):
        """
        Convert BitStruct to long

        :param littleEndian: Whether the BitStruct is to be interpreted as littleEndian or not - OPTIONAL
        :type littleEndian: ``bool``

        :return: value of BitStruct
        :rtype: ``int``
        """
        return self._value.toLong(littleEndian)
    # end def toLong

    def testBit(self, posOrName):
        """
        Test a bit of the BitStruct

        :param  posOrName [in] (int, str) Position or name of the bit to test
        :type posOrName: ``int`` or ``str``

        :return: 1 if bit set, 0 in other case
        :rtype: ``int``

        **Note** ``posOrName`` = 0 => least significant bit of the string
        """
        pos = self.__get_pos(posOrName)
        if isinstance(pos, int):
            if self._value.testBit(pos):
                return 1
            else:
                return 0
            # end if
        # end if
    # end def testBit

    def setBit(self, posOrName):
        """
        Set a bit in a BitStruct.

        :param posOrName: Position or name of the bit to set
        :type posOrName: ``int`` or ``str``

        **Note** ``posOrName`` = 0 => least significant bit of the bitstruct
        """
        pos = self.__get_pos(posOrName)
        self._value.setBit(pos)
    # end def setBit

    def clearBit(self, posOrName):
        """
        Clear a bit in a BitStruct.

        :param posOrName: Position or name of the bit to clear
        :type posOrName: ``int`` or ``str``

        **Note** ``posOrName`` = 0 => least significant bit of the bitstruct
        """
        pos = self.__get_pos(posOrName)
        self._value.clearBit(pos)
    # end def clearBit

    def updateBit(self, posOrName, value):
        """
        Update a bit in a BitStruct.

        :param posOrName: Position or name of the bit to update
        :type posOrName: ``int`` or ``str``
        :param value: New value of the bit
        :type value: ``int``

        **Note** ``posOrName`` = 0 => least significant bit of the bitstruct
        """
        pos = self.__get_pos(posOrName)
        try:
            self._value.updateBit(pos, value)
        except Exception as e:
            # Trap exception, convert it to our own type
            raise ValueError(e)
        # end try
    # end def updateBit

    def invertBit(self, posOrName):
        """
        Invert a bit in a BitStruct.

        :param posOrName: Position or name of the bit to invert
        :type posOrName: ``int`` or ``str``

        **Note** ``posOrName`` = 0 => least significant bit of the bitstruct
        """
        pos = self.__get_pos(posOrName)
        self._value.invertBit(pos)
    # end def invertBit

    def copy(self):
        """
        Create a copy of itself

        :return: Copy of itself
        :rtype: ``BitStruct``
        """
        return copy.copy(self)
    # end def copy

    def deepcopy(self):
        """
        Create a deepcopy of itself

        :return: Copy of itself
        :rtype: ``BitStruct``
        """
        return copy.deepcopy(self)
    # end def deepcopy

    def __interpret(self, name, value):
        """
        Get the interpretation of the value of mask or bit

        :param name: Name of the attribute
        :type name: ``str``
        :param value: Value of the attribute
        :type value: ``int``

        :return: Interpretation of the value of the attribute
        :rtype: ``str``
        """
        result = None

        interpreter = self._interpreter.get(name, None)
        if interpreter is not None:
            args = {'value': value, 'name': name}

            formatter = interpreter.get(value, None)
            if formatter is None:
                formatter = interpreter.get(None, None)
            # end if

            if formatter is not None:
                result = f' ({formatter % args})'
            # end if
        # end if

        return result
    # end def __interpret

    def createSummary(self):
        """
        Create a summary for BitStruct

        :return: Summary of the BitStruct
        :rtype: ``str``
        """
        log_table = []
        value = self._value
        if self._mode != self._default_mode:
            value = self.__convert_value(self._default_mode, self._mode)
        # end if

        log = f'{value}'
        if len(self._dict):
            # Creation of summary from dictionary content
            for key, value in sorted(list(self._dict.items()),
                                     key=lambda x: x[-1][0] if isinstance(x[-1], tuple) else x[-1],
                                     reverse=self.summary_msb_first):
                if key not in self._hidden:
                    str_element = f'  - {key} '
                    str_element += ' ' * (self.ELEMENT_OFFSET - len(str_element))

                    value = getattr(self, key)
                    interpretation = self.__interpret(key, value)
                    if interpretation is not None:
                        str_element += f'= {value}{interpretation}'
                    else:
                        str_element += f'= {value}'
                    # end if
                    log_table.append(str_element)
                # end if
            # end for
        # end if

        if len(log_table) > 0:
            log += '\n'
        # end if

        log += '\n'.join(log_table)

        return log
    # end def createSummary

    def merge(self, dictionary, interpreter):
        """
        Merges several BitStruct definitions into one BitStruct.

        This checks that attribute definitions do not clash.

        :param dictionary: The attributes dictionary
        :type dictionary: ``dict``
        :param interpreter: The interpreters dictionary
        :type interpreter: ``dict``
        """

        def _merge_dicts(first, second):
            """
            Merges an array of dicts, checking that duplicates have the same value.

            :param first: First dict to merge
            :type first: ``dict``
            :param second: Second dict to merge
            :type second: ``dict``

            :return: A new merged dict
            :rtype: ``dict``
            """
            result = first.copy()

            for name, value in second.items():
                if (name in result) and (result[name] != value):
                    raise AttributeError(f'Inconsistent bitstruct definitions when merging: {name} is defined '
                                         f'as {value} and {result[name]}')
                # end if
            # end for
            result.update(second)

            return result
        # end def _merge_dicts

        self._dict = _merge_dicts(self._dict, dictionary)
        self._interpreter = _merge_dicts(self._interpreter, interpreter)
    # end def merge
# end class BitStruct

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
