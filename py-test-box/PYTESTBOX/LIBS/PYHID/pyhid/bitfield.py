#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
"""
:package: pyhid.bitfield
:brief: BitField definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/12/18
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import copy
import warnings
from functools import reduce
from traceback import extract_stack
from types import FunctionType

from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
def getElement(data, offset, elementLength):
    """
    Deprecated function. See ``get_element``.

    :param data: Data to parse
    :type data: ``HexList``
    :param offset: Bit offset in data
    :type offset: ``int``
    :param elementLength: Element length
    :type elementLength: ``int``

    :return: Element extracted from data
    :rtype: ``int``
    """
    warnings.warn(
        'This function is deprecated, use get_element() instead', DeprecationWarning)

    return get_element(data, offset, elementLength)
# end def getElement


def get_element(data, offset, element_length):
    """
    Get bit count sized element from data

    :param data: Data to parse
    :type data: ``HexList``
    :param offset: Bit offset in data
    :type offset: ``int``
    :param element_length: Element length
    :type element_length: ``int``

    :return: Element extracted from data
    :rtype: ``int``
    """
    byte_offset, bit_offset = divmod(offset, 8)
    byte_length = ((bit_offset + element_length - 1) // 8) + 1
    buf = reduce(lambda x, y: (x << 8) | y, data[byte_offset: byte_offset + byte_length])
    result = ((buf >> (byte_length * 8 - (bit_offset + element_length))) & ((1 << element_length) - 1))
    return result
# end def get_element


def byteFieldFromHexList(container, bitField, data, offset=0, limit=None, exceptOnOverflow=True):
    """
    Deprecated function. See ``byte_field_from_hex_list``

    :param container: The object that contains the field.
    :type container: ``FieldContainerMixin``
    :param bitField: Result format
    :type bitField: ``BitField``
    :param data: The HexList to parse
    :type data: ``HexList``
    :param offset: The offset in the HexList at which to start parsing - OPTIONAL
    :type offset: ``int``
    :param limit: Max length of data to parse - OPTIONAL
    :type limit: ``int``
    :param exceptOnOverflow: Raises an exception on overflow - OPTIONAL
    :type exceptOnOverflow: ``bool``

    :return: Parsed bit field
    :rtype: ``tuple[int, HexList|None]``
    """
    warnings.warn(
        'This function is deprecated, use byte_field_from_hex_list() instead', DeprecationWarning)

    return byte_field_from_hex_list(container, bitField, data, offset=offset,
                                    limit=limit, except_on_overflow=exceptOnOverflow)
# end def byteFieldFromHexList


def byte_field_from_hex_list(container, bit_field, data, offset=0, limit=None, except_on_overflow=True):
    """
    Parse the field from HexList format

    :param container: The object that contains the field.
    :type container: ``FieldContainerMixin``
    :param bit_field: Result format
    :type bit_field: ``BitField``
    :param data: The HexList to parse
    :type data: ``HexList``
    :param offset: The offset in the HexList at which to start parsing - OPTIONAL
    :type offset: ``int``
    :param limit: Max length of data to parse - OPTIONAL
    :type limit: ``int``
    :param except_on_overflow: Raises an exception on overflow - OPTIONAL
    :type except_on_overflow: ``bool``

    :return: Parsed bit field
    :rtype: ``tuple[int, HexList|None]``

    :raise ``ValueError``: If the field has a tag or is of variable length and the except_on_overflow option is in use.
    """
    limit = limit if limit is not None else len(data) * 8
    # Check of the end of the buffer to analyze
    if offset >= limit:
        if bit_field.is_optional(container):
            return offset, None
        elif (bit_field.has_tag or bit_field.variable) and except_on_overflow:
            raise ValueError(f"Mandatory field not found: {container.__class__.__name__}.{bit_field.name}")
        else:
            length = bit_field.get_length(container, data, offset=offset, length=limit - offset)
            value = None
            if (length is None) or (length == 0):
                value = HexList()
            elif except_on_overflow:
                raise ValueError(f"Mandatory field not found: {container.__class__.__name__}.{bit_field.name}")
            # end if

            return offset, value
        # end if
    # end if

    # If the field has a tag, check it and/or skip it
    if bit_field.has_tag:
        fid = get_element(data, offset, bit_field._fid_length)
        if bit_field.fid != fid:
            # Field not present
            return offset, None
        else:
            # Skip tag
            offset += bit_field._fid_length
        # end if
    # end if

    if bit_field.variable:
        length = get_element(data, offset, bit_field._len_length)
        offset += bit_field._len_length
    else:
        length = bit_field.get_length(container, data, offset=offset, length=limit - offset)
    # end if

    # Initialization of the value
    if length is None:
        value = data[offset:]
        length = len(value)

    else:
        if length > 0:
            if (offset % 8 == 0) and (length % 8 == 0):
                value = data[offset // 8: offset // 8 + length // 8]
            else:
                value = get_element(data, offset, length)
            # end if
        else:
            value = HexList()
        # end if
    # end if

    return offset + length, value
# end def byte_field_from_hex_list


def bit_field_from_hex_list(container, bit_field, data, offset=0, limit=None, except_on_overflow=True):
    """
    Parse the field from HexList format

    :param container: The object that contains the field.
    :type container: ``FieldContainerMixin``
    :param bit_field: Result format
    :type bit_field: ``BitField``
    :param data: The HexList to parse
    :type data: ``HexList``
    :param offset: The offset in the HexList at which to start parsing - OPTIONAL
    :type offset: ``int``
    :param limit: Max length of data to parse - OPTIONAL
    :type limit: ``int``
    :param except_on_overflow: Raises an exception on overflow - OPTIONAL
    :type except_on_overflow: ``bool``

    :return: Parsed bit field
    :rtype: ``tuple[int, HexList|None]``

    :raise ``ValueError``: If the field has a tag or is of variable length and the except_on_overflow option is in use.
    """
    limit = limit if limit is not None else len(data) * 8
    # Check of the end of the buffer to analyze
    if offset >= limit:
        if bit_field.is_optional(container):
            return offset, None
        elif (bit_field.has_tag or bit_field.variable) and except_on_overflow:
            raise ValueError(f"Mandatory field not found: {container.__class__.__name__}.{bit_field.name}")
        else:
            length = bit_field.get_length(container, data, offset=offset, length=limit - offset)
            value = None
            if (length is None) or (length == 0):
                value = HexList()
            elif except_on_overflow:
                raise ValueError(f"Mandatory field not found: {container.__class__.__name__}.{bit_field.name}")
            # end if

            return offset, value
        # end if
    # end if

    # If the field has a tag, check it and/or skip it
    if bit_field.has_tag:
        fid = get_element(data, offset, bit_field._fid_length)
        if bit_field.fid != fid:
            # Field not present
            return offset, None
        else:
            # Skip tag
            offset += bit_field._fid_length
        # end if
    # end if

    if bit_field.variable:
        length = get_element(data, offset, bit_field._len_length) * 8
        offset += bit_field._len_length
    else:
        length = bit_field.get_length(container, data, offset=offset, length=limit - offset)
    # end if

    if not bit_field.is_optional(container):
        # Initialization of the value
        if length is None:
            value = data[offset:]
            length = len(value)
        else:
            if (offset % 8 == 0) and (length % 8 == 0):
                value = data[offset // 8: offset // 8 + length // 8]
            else:
                value = get_element(data, offset, length)
            # end if
        # end if

        return offset + length, value

    else:
        if length is None:
            value = data[offset:]
            length = len(value)
        else:
            if length > 0:
                value = get_element(data, offset, length)
            else:
                value = HexList()
            # end if
        # end if

        return offset + length, value
    # end if
# end def bit_field_from_hex_list


class BitField(object):
    """
    Field definition with lengths in bit

    Warning:
    Do no confuse BitField acceptable and BitField accept methods:
     - BitField acceptable:  Checks whether an attribute name is acceptable for this field
     - BitField accept: Checks if the HexList data are interpretable by self
    """

    def __init__(self, fid=None, length=0x00, fid_length=0x00, len_length=0x00, default_value=None,
                 title='Undefined Field', name=None, checks=None, conversions=None, aliases=tuple(), optional=None,
                 parser=byte_field_from_hex_list, interpreter=None, zero_print=False):
        """
        :param fid: Field identifier - OPTIONAL
        :type fid: ``int``
        :param length: Field value length - OPTIONAL
        :type length: ``int``
        :param fid_length: Field identifier length - OPTIONAL
        :type fid_length: ``int``
        :param len_length: Field value length's length - OPTIONAL
        :type len_length: ``int``
        :param default_value: Default value for the has_tag non-variable parameters - OPTIONAL
        :type default_value: ``object``
        :param title: Title of the Field - OPTIONAL
        :type title: ``str``
        :param name: Name of this Field. The name is used to provide quick access to the Field through its parent
                     attributes - OPTIONAL
        :type name: ``str``
        :param checks: List of checks on the value - OPTIONAL
        :type checks: ``list[Checks]`` or ``tuple[Checks]``
        :param conversions: Dict that maps an input type to a conversion routine - OPTIONAL
        :type conversions: ``dict[sourceType, converter]``
        :param aliases: List of alternative names by which to reference this field - OPTIONAL
        :type aliases: ``tuple``
        :param optional: Whether the field is optional - OPTIONAL
        :type optional: ``bool or callable``
        :param parser: From HexList parsing method - OPTIONAL
        :type parser: ``callable``
        :param interpreter: Interpretation dictionary - OPTIONAL
        :type interpreter: ``dict``
        :param zero_print: Flag indicating if the field should be printed when its value is 0 - OPTIONAL
        :type zero_print: ``bool``
        """
        self._fid = None
        self._length = None
        self._fid_length = fid_length
        self._len_length = len_length
        self._default_value = None
        self._optional = None
        self._parser = parser
        self._interpreter = None
        self._name = None
        self._conversions = None
        self._aliases = None
        self._title = None

        self.conversions = conversions
        self.checks = checks
        self.name = name
        self.set_default_value(default_value)
        self.fid = fid
        self.set_length(length)
        self.title = title
        self.aliases = aliases
        self.set_optional(optional)
        self.interpreter = interpreter
        self.zero_print = zero_print

        # Locate where the field is instantiated.
        # This will be useful when a check fails, in order to pinpoint the error
        this_file = __file__.rsplit('.', 1)[0]
        for file_name, line_number, function_name, text in reversed(extract_stack()):
            if file_name.rsplit('.', 1)[0] != this_file:
                self.__instantiation_file = file_name
                self.__instantiation_line = line_number
                self.__instantiation_function_name = function_name
                self.__instantiation_text = text
                break
            # end if
        # end for

        self._acceptable = None
        self._confusing = None
    # end def __init__

    def __len__(self):
        """
        Get length of self

        :return: Length of self
        :rtype: ``int``
        """
        result = self._fid_length + self._len_length
        if self._len_length > 0:
            result += self.length
        # end if
        return result
    # end def __len__

    def acceptable(self, attribute_name):
        """
        Check whether an attribute name is acceptable for this field.

        :param attribute_name: The name to check
        :type attribute_name: ``str``

        :return: Flag indicating if the name is acceptable
        :rtype: ``bool``
        """
        if self._acceptable is None:
            acceptable = set(self.aliases)
            if self.name is not None:
                acceptable.add(self.name)
            # end if

            self._acceptable = acceptable
        # end if

        return attribute_name in self._acceptable
    # end def acceptable

    def confusing(self, attribute_name_lower):
        """
        Check whether an attribute name could be confused with another one.

        :param attribute_name_lower: The name to check
        :type attribute_name_lower: ``str``

        :return: Flag indicating if the name can be confused with another one
        :rtype: ``bool``
        """
        if self._confusing is None:
            confusing = set((name.lower() for name in self.aliases))
            if self.name is not None:
                confusing.add(self.name.lower())
            # end if

            self._confusing = confusing
        # end if

        return attribute_name_lower in self._confusing
    # end def confusing

    def __eq__(self, other):
        """
        Test the equality of Field with the other.

        :param other: Other Field instance
        :type other: ``Field``

        :return: Comparison result
        :rtype: ``bool``

        :raise ``TypeError``: If other is not of ``BitField`` type
        """
        if other is None:
            return False
        # end if

        if not isinstance(other, BitField):
            raise TypeError(f"Wrong other type: {type(other).__name__}. Should be of type BitField")
        # end if

        result = (self.fid == other.fid)

        if result:
            result = (self.length == other.length)
        # end if

        if result:
            result = (self.fid_length == other.fid_length)
        # end if

        if result:
            result = (self.len_length == other.len_length)
        # end if

        if result:
            result = (self.default_value == other.default_value)
        # end if

        if result:
            result = (self.title == other.title)
        # end if

        if result:
            result = (self.name == other.name)
        # end if

        if result:
            result = (self.aliases == other.aliases)
        # end if

        if result:
            result = (self.interpreter == other.interpreter)
        # end if

        return result
    # end def __eq__

    def __ne__(self, other):
        """
        Test the difference between Field and other.

        :param other: Other Field instance
        :type other: ``Field``

        :return: Comparison result
        :rtype: ``bool``
        """
        return not (self == other)
    # end def __ne__

    def copy(self):
        """
        Return a copy of itself

        :return: Copy of itself
        :rtype: ``BitField``
        """
        return copy.copy(self)
    # end def copy

    def deepcopy(self):
        """
        Return a deep copy of itself

        :return: Copy of itself
        :rtype: ``BitField``
        """
        return self.__class__(self.fid, self.length, self._fid_length, self._len_length, self.default_value,
                              self.title, self.name, self.checks, self.conversions, self.aliases)
    # end def deepcopy

    def getFid(self):
        """
        Deprecated function. See property ``fid``.

        :return: Field identifier value
        :rtype: ``int``
        """
        return self.fid
    # end def getFid

    @property
    def fid(self):
        """
        Get field identifier value

        :return: Field identifier value
        :rtype: ``int``
        """
        return self._fid
    # end def fid

    def setFid(self, fid):
        """
        Deprecated function. See property ``fid``.

        :param fid: Field identifier
        :type fid: ``int``
        """
        self.fid = fid
    # end def setFid

    @fid.setter
    def fid(self, fid):
        """
        Set Field identifier

        :param fid: Field identifier
        :type fid: ``int``

        :raise ``TypeError``: If fid is not an ``int``
        :raise ``ValueError``: If the fid is not of the right length
        """
        if fid is not None:
            if not isinstance(fid, int):
                raise TypeError(f"Wrong fid type: {type(fid).__name__}. Should be an integer instead.")
            # end if

            if self._fid_length > 0:
                if len(f"{fid:b}") > self._fid_length:
                    raise ValueError(f"Wrong fid ({fid}) length, should be {self._fid_length} bit length")
                # end if
            # end if
        # end if

        self._fid = fid
    # end def fid

    @property
    def fid_length(self):
        """
        Get fid_length value

        :return: FID length
        :rtype: ``int``
        """
        return self._fid_length
    # end def fid_length

    @fid_length.setter
    def fid_length(self, fid_length):
        """
        Set FID length

        :param fid_length: FID length
        :type fid_length: ``int``
        """
        self._fid_length = fid_length
    # end def fid_length

    @property
    def len_length(self):
        """
        Get len_length value

        :return: LEN length
        :rtype: ``int``
        """
        return self._len_length
    # end def len_length

    @len_length.setter
    def len_length(self, len_length):
        """
        Set LEN length

        :param len_length: LEN length
        :type len_length: ``int``
        """
        self._len_length = len_length
    # end def len_length

    def get_has_tag(self, container=None):
        """
        Return True if the Field has a tag.

        :param container: The object that contains the field. - OPTIONAL
        :type container: ``FieldContainerMixin``

        :return: Flag indicating if the Field has a tag
        :rtype: ``bool``
        """
        has_tag = (self.fid_length != 0)
        if callable(has_tag):
            has_tag = has_tag(container)
        # end if
        return has_tag
    # end def get_has_tag

    has_tag = property(get_has_tag)

    @property
    def variable(self):
        """
        Return True if Field has a variable length.

        :return: Flag indicating if the Field has a variable length
        :rtype: ``bool``
        """
        return self.len_length != 0
    # end def variable

    def get_length(self, container=None, value=None, offset=0, length=None):
        """
        Get field length

        :param container: The object that contains the field - OPTIONAL
        :type container: ``FieldContainerMixin``
        :param value: The value to parse - OPTIONAL
        :type value: ``HexList``
        :param offset: The offset at which to start parsing - OPTIONAL
        :type offset: ``int``
        :param length: The length for which to parse - OPTIONAL
        :type length: ``int``

        :return: Length of the field
        :rtype: ``int``
        """
        length = self._length
        if callable(length):
            length = length(container)
        # end if

        # If the length cannot be deduced easily, and a value is available,
        # look for a lengthFromHexList method in the HexList conversion utility
        if (length is None) and (value is not None):
            converter = self.conversions.get(value.__class__, None)
            if (converter is not None) and (hasattr(converter, 'lengthFromHexList')):
                length = converter.lengthFromHexList(value, offset=offset, length=length)
            # end if
        # end if

        return length
    # end def get_length

    def set_length(self, length):
        """
        Set Field value length

        :param length: Field value length
        :type length: ``int`` or ``None``

        :raise ``TypeError``: If fid is not an ``int``
        :raise ``ValueError``: If the fid is not positive or of the right length
        """
        if length is not None:
            if not callable(length):
                if not isinstance(length, int):
                    raise TypeError(f"Wrong length type: {type(length).__name__}. Should be an integer instead.")
                # end if

                if length < 0:
                    raise ValueError(f"Wrong length value: {length}. Should be positive.")
                # end if

                if self._len_length != 0:
                    if len(f"{length:b}") > self._len_length:
                        raise ValueError(f"Wrong length ({length}) length, should be {self._len_length} bit length")
                    # end if
                # end if
            # end if
        # end if

        self._length = length
    # end def set_length

    length = property(get_length, set_length)

    def get_default_value(self, context=None):
        """
        Get the default_value of the Field.

        :param context: The context in which to evaluate the default value. The context must have a FIELDS attribute
                        and a getValue method - OPTIONAL
        :type context: ``object``

        :return: default_value default_value
        :rtype: ``object``
        """
        if callable(self._default_value):
            default_value = self._default_value(context)
        else:
            default_value = self._default_value
        # end if

        return default_value
    # end def get_default_value

    def has_default_value(self):
        """
        Check whether the field has a default value definition.

        :return: Flag indicating if the field has a default value definition.
        :rtype: ``bool``
        """
        return self._default_value is not None
    # end def has_default_value

    def set_default_value(self, default_value):
        """
        Set the default_value of the Field.

        :param default_value: default_value default_value
        :type default_value: ``object``

        :raise ``TypeError``: If the default_value is a ``callable`` and contains context as a parameter
        """
        if default_value is not None:

            # A callable would be a problem, as we are (not yet) within a
            # FieldContainerMixin.
            if not callable(default_value):
                self.check_value(default_value)
                default_value = self.convert_value(default_value, self)

            elif 'context' not in default_value.__code__.co_varnames:
                raise TypeError(f"Wrong callable default value for {self.name}: {default_value}. "
                                "Must have context as its only parameter")
            # end if
        # end if

        self._default_value = default_value
    # end def set_default_value

    default_value = property(get_default_value, set_default_value)

    @property
    def title(self):
        """
        Get the Title of the Field.

        :return: Title title
        :rtype: ``str``
        """
        return self._title
    # end def title

    @title.setter
    def title(self, title):
        """
        Set the Title of the Field.

        :param title: Title title
        :type title: ``str``

        :raise ``TypeError``: If title is not a ``str``
        """
        if not isinstance(title, str):
            raise TypeError(f"Wrong Title type: {type(title).__name__}. Must be a str.")
        # end if

        self._title = title
    # end def title

    @property
    def name(self):
        """
        Get the Name of the Field.

        The name is used to provide quick access to the Field through its parent
        attributes

        :return: The Field name
        :rtype: ``str``
        """
        return self._name
    # end def name

    @name.setter
    def name(self, name):
        """
        Set the Name of the Field.

        The name is used to provide quick access to the Field through its parent
        attributes

        :param name: The Field name
        :type name: ``str``

        :raise ``TypeError``: If name is not a ``str``
        """
        if not isinstance(name, str) and name is not None:
            raise TypeError(f"Wrong Title type: {type(name).__name__}. Must be a str.")
        # end if

        self._name = name
        self._acceptable = None
        self._confusing = None
    # end def name

    @property
    def conversions(self):
        """
        Obtain the conversion table

        :return: A copy of conversion table
        :rtype: ``dict``
        """
        return dict(self._conversions)
    # end def conversions

    @conversions.setter
    def conversions(self, conversions):
        """
        Set the conversion table and schedule the conversion lookup order

        :param conversions: The conversion table
        :type conversions: ``dict``

        :raise ``TypeError``: If conversions is not of ``dict`` or ``None`` type
        """
        if conversions is None:
            conversions = []

        elif isinstance(conversions, dict):
            # Compute the conversions weight
            def conversion_weight(conversion):
                """
                Computes the relative weight of the conversions keys, by allocating a weight based on the
                conversion key's hierarchy.

                :param conversion: The conversion to compute the weight for
                :type conversion: ``type``

                :return: The conversion's weight, versus the whole conversion list.
                :rtype: ``int``
                """
                result = 0
                for index, target in enumerate(conversions.keys()):
                    result += (2 ** index) if issubclass(conversion, target) else 0
                # end for

                return result
            # end def conversion_weight

            conversions = [item for item in sorted(list(conversions.items()), reverse=True,
                                                   key=lambda x: conversion_weight(x[0]))]
        else:
            raise TypeError(f"Conversions should be a dict of type->callable or None,"
                            f"found {type(conversions).__name__}")
        # end if

        self._conversions = conversions
    # end def conversions

    @property
    def aliases(self):
        """
        Get the Aliases of the Field.

        The aliases are used to provide quick access to the Field through an
        alternative, allowed names.

        :return: The Field aliases
        :rtype: ``tuple or None``
        """
        return self._aliases
    # end def aliases

    @aliases.setter
    def aliases(self, aliases):
        """
        Set the Aliases of the Field.

        The aliases are used to provide quick access to the Field through
        alternative, allowed names.

        :param aliases: The Field aliases
        :type aliases: ``tuple``

        :raise ``TypeError``: If aliases is not of ``tuple`` type
        """
        if not isinstance(aliases, (tuple, list)):
            raise TypeError(f"Wrong Aliases type: {type(aliases).__name__}. Should be a tuple")
        # end if

        self._aliases = aliases
        self._acceptable = None
        self._confusing = None
    # end def aliases

    def add_alias(self, alias):
        """
        Add an alias to the field

        :param alias: Alias to add
        :type alias: ``str``

        :raise ``TypeError``: If alias is not of ``tuple`` type
        """
        if not isinstance(alias, str):
            raise TypeError("Wrong alias type: Alias should be a string")
        # end if

        self.aliases = self._aliases + (alias,)
    # end def add_alias

    @property
    def checks(self):
        """
        Obtain the checks to be done.

        :return: A list of checks
        :rtype: ``list or None``
        """
        return self._checks
    # end def checks

    @checks.setter
    def checks(self, checks):
        """
        Set the checks to be done

        :param checks: The list of checks to do
        :type checks: ``list``

        :raise ``AssertionError``: If checks is not a ``list or tuple`` or if check is not a ``Check``
        """
        if checks is not None:
            assert isinstance(checks, (list, tuple)), \
                TypeError('checks should be a iterable')
            for check in checks:
                assert isinstance(check, Check), \
                    TypeError(f"{check} should be an instance of Check")
            # end for
        # end if

        self._checks = checks
    # end def checks

    @property
    def interpreter(self):
        """
        Get the interpreter dictionary

        :return: Interpreter value
        :rtype: ``dict or None``
        """
        return self._interpreter
    # end def interpreter

    @interpreter.setter
    def interpreter(self, interpreter):
        """
        Set interpreter dictionary

        :param interpreter: New interpreter value
        :type interpreter: ``dict or None``

        :raise ``AssertionError``: If interpreter is not a ``dict``
        """
        if interpreter is not None:
            assert isinstance(interpreter, dict), \
                TypeError('Interpreter should be a dictionary if not None')
        # end if

        self._interpreter = interpreter
    # end def interpreter

    def create_summary(self, append_fid=True):
        """
        Create a summary of the Field.

        :param append_fid: Append FID value or not - OPTIONAL
        :type append_fid: ``bool``

        :return: Summary of the command
        :rtype: ``str``
        """
        if (append_fid
                and (self._fid_length > 0)
                and (self._fid >= 0)):
            log = '%s: (0x%2.2X)' % (self._title, self._fid)

        else:
            log = f"{self._title}:"

        # end if

        return log
    # end def create_summary

    def __get_instantiation_location(self):
        """
        Obtain the instantiation location for this object.

        :return: A tuple (file_name, line_number, function_name, text) of the instantiation location.
        :rtype: ``tuple``
        """
        return (self.__instantiation_file, self.__instantiation_line, self.__instantiation_function_name,
                self.__instantiation_text)
    # end def __get_instantiation_location

    def check_value(self, value, container=None):
        """
        Check the value of the Field.

        :param value: The value to test
        :type value: ``object``
        :param container: The object that contains the field - OPTIONAL
        :type container: ``BitFieldContainerMixin``

        :return: Flag indicating if value is correct or undefined and optional
        :rtype: ``bool``

        :raise ``TypeError``: If there's a wrong check type
        """
        if ((self._checks is not None)
                and not ((self.is_optional(container))
                         and (value is None))):
            for check in self._checks:
                if check(value, self.name):
                    return True
                # end if
            # end for

            file_name, line_number, function_name, _ = self.__get_instantiation_location()
            raise TypeError(f"Wrong check type ({type(value).__name__}) for {self.name} parameter at:"
                            f"\n  File \"{file_name}\", line {line_number}, in {function_name}")

        else:
            # Ok when no check to verify
            return True
        # end if
    # end def check_value

    def convert_value(self, value, container=None):
        """
        Convert a value, from a known (unstructured) type to a rich type.

        For instance, this will usually convert an HexList type to DateTime instance.

        :param value: The value to convert.
        :type value: ``object``
        :param container: The FieldContainerMixin containing the object to convert - OPTIONAL
        :type container: ``object``

        :return: The converted (or unchanged value)
        :rtype: ``object``
        """
        result = value

        if self._conversions is not None:
            for class_type, converter in self._conversions:
                if isinstance(value, class_type):
                    # If the callable has a 'container' keyword argument, use it
                    if ((container is not None)
                            and (isinstance(converter, FunctionType))
                            and ('container' in converter.__code__.co_varnames)):
                        result = converter(value, container=container)

                    else:
                        result = converter(value)
                    # end if

                    break
                # end if
            # end for
        # end if

        return result
    # end def convert_value

    def __str__(self):
        """
        Convert the current object to a string

        :return: String representation of the field
        :rtype: ``str``
        """
        return str(self.create_summary())
    # end def __str__

    def __repr__(self):
        """
        Convert the current object to a string

        :return: A string representation of the instance
        :rtype: ``str``
        """
        arg_names = ('fid', 'length', 'default_value', 'title', 'name', 'checks', 'conversions', 'aliases')

        arg_repr = ", ".join((f"{arg_name} = {repr(getattr(self, f'_{arg_name}'))}" for arg_name in arg_names))

        return f"{self.__class__.__name__}({arg_repr})"
    # end def __repr__

    def to_bit_list(self):
        """
        Get field representation as (len, value)

        :return: List of fields as (len, value)
        :rtype: ``list``
        """
        bit_list = []
        if self._fid_length > 0:
            bit_list.append([self._fid_length, self._fid])
        # end if
        if self._len_length > 0:
            bit_list.append([self._len_length, self._length])
        # end if
        return bit_list
    # end def to_bit_list

    def is_optional(self, container=None):
        """
        Return True if the field is optional

        :param container: The object that contains the field. - OPTIONAL
        :type container: ``FieldContainerMixin``

        :return: Flag indicating of the field is optional
        :rtype: ``bool``
        """
        result = self._optional
        if callable(result):
            result = result(container)
        # end if

        return result
    # end def is_optional

    def set_optional(self, optional):
        """
        Set whether the field is optional.

        :param optional: Whether the field has an optional tag
        :type optional: ``int``
        """
        if optional is None:
            optional = (self._length == 0) and (self._len_length == 0)
        # end if

        self._optional = optional
    # end def set_optional

    optional = property(is_optional, set_optional)

    def accept(self, container, data, offset=0, limit=None):
        """
        Check if the HexList data are interpretable by self

        :param container: The object that contains the field.
        :type container: ``FieldContainerMixin``
        :param data: Data to interpret
        :type data: ``HexList``
        :param offset: The offset in the HexList at which to start parsing - OPTIONAL
        :type offset: ``int``
        :param limit: Max length of data to parse - OPTIONAL
        :type limit: ``int``

        :return: Flag indicating if data is interpretable
        :rtype: ``bool``
        """
        limit = limit if limit is not None else len(data) * 8
        # Check of the end of the buffer to analyze
        if offset >= limit:
            return self.is_optional(container)
        # end if

        if self.has_tag:
            fid = get_element(data, offset, self._fid_length)
            return self.fid == fid
        # end if
        return True
    # end def accept

    def fromHexList(self, container, data, offset=0, limit=None, exceptOnOverflow=True):
        """
        Deprecated function. See ``from_hex_list``

        :param container: The object that contains the field.
        :type container: ``FieldContainerMixin``
        :param data: The HexList to parse
        :type data: ``HexList``
        :param offset: The offset in the HexList at which to start parsing - OPTIONAL
        :type offset: ``int``
        :param limit: Max length of data to parse - OPTIONAL
        :type limit: ``int``
        :param exceptOnOverflow: Raises an exception on overflow - OPTIONAL
        :type exceptOnOverflow: ``bool``

        :return: Parsed bit field
        :rtype: ``tuple[offset, BitField]``
        """
        warnings.warn('This function is deprecated, use from_hex_list() instead', DeprecationWarning)

        return self.from_hex_list(container, data, offset=offset, limit=limit, except_on_overflow=exceptOnOverflow)
    # end def fromHexList

    def from_hex_list(self, container, data, offset=0, limit=None, except_on_overflow=True):
        """
        Parse a field from HexList format

        :param container: The object that contains the field.
        :type container: ``FieldContainerMixin``
        :param data: The HexList to parse
        :type data: ``HexList``
        :param offset: The offset in the HexList at which to start parsing - OPTIONAL
        :type offset: ``int``
        :param limit: Max length of data to parse - OPTIONAL
        :type limit: ``int``
        :param except_on_overflow: Raises an exception on overflow - OPTIONAL
        :type except_on_overflow: ``bool``

        :return: Parsed bit field
        :rtype: ``tuple[offset, BitField]``

        :raise ``TypeError``: If the parser does not have the right type
        :raise ``ValueError``: If the function is unable to parse a mandatory field or if no parser was found
        """
        value = None
        if self._parser is not None:
            if self.accept(container, data, offset, limit):
                if hasattr(self._parser, 'fromHexList'):
                    offset, value = self._parser.fromHexList(container, self, data, offset, limit, except_on_overflow)
                elif callable(self._parser):
                    offset, value = self._parser(container, self, data, offset, limit, except_on_overflow)
                else:
                    raise TypeError(f"Wrong parser type: {type(self._parser).__name__}")
                # end if
                return offset, value
            else:
                if self.is_optional(container):
                    return offset, None
                else:
                    raise ValueError(f"Unable to parse mandatory field: {self.name}")
                # end if
            # end if
        # end if
        raise ValueError('No parser found')
    # end def from_hex_list
# end class BitField


class Check(object):
    """
    Object that checks for a condition on a value.
    """

    def __call__(self, value, name=None):
        """
        The actual check to perform.

        :param value: The value to check
        :type value: ``object``
        :param name: Field name for debug message purpose - OPTIONAL
        :type name: ``str``
        """
        raise NotImplementedError
    # end def __call__
# end class Check


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
