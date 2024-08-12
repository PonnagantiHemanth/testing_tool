#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.field
:brief: PyHid Field implementation module
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/12/18
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from traceback import extract_stack

from pyhid.bitfield import BitField
from pyhid.bitfield import Check
from pyhid.bitfield import byte_field_from_hex_list
from pylibrary.tools.bitstruct import BitStruct
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
def field_from_hex_list(container, field, data, offset=0, limit=None, except_on_overflow=True):
    """
    Parse the field from HexList format

    :param  container: The object that contains the field.
    :type container: ``FieldContainerMixin``
    :param  field: Result format
    :type field: ``Field``
    :param data: The HexList to parse
    :type data: ``HexList``
    :param offset: The offset in the HexList at which to start parsing` - OPTIONAL
    :type offset: ``int``
    :param limit: Max length of data to parse - OPTIONAL
    :type limit: ``int`` or ``None``
    :param except_on_overflow: Flag indicating if this raises an exception on overflow - OPTIONAL
    :type except_on_overflow: ``bool``

    :return: Parsed bit field
    :rtype: ``tuple[int, Field]``

    :raise ``ValueError``: If the field has a tag or is of variable length and the except_on_overflow option is in use.
    """
    limit = limit if limit is not None else len(data)
    # Check of the end of the buffer to analyze
    if offset >= limit:
        if field.is_optional(container):
            return offset, None
        elif (field.has_tag or field.variable) and except_on_overflow:
            raise ValueError(f"Mandatory field not found: {container.__class__.__name__}.{field.name}")
        else:
            length = field.get_length(container, data, offset=offset, length=limit - offset)
            value = None
            if length is None or length == 0:
                value = HexList()
            elif except_on_overflow:
                raise ValueError(f"Mandatory field not found: {container.__class__.__name__}.{field.name}")
            # end if

            return offset, value
        # end if
    # end if

    # If the field has a tag, check it and/or skip it
    if field.has_tag:
        if field.fid != data[offset]:
            # Field not present
            return offset, None
        else:
            # Skip tag
            offset += 1
        # end if
    # end if

    if field.variable:
        length = data[offset]
        offset += 1
    else:
        length = field.get_length(container, data, offset=offset, length=limit - offset)
    # end if

    if not field.is_optional(container):

        # Initialization of the value
        if length is None:
            hex_value = data[offset:]
            length = len(hex_value)
        else:
            hex_value = data[offset:offset + length]
        # end if

        return offset + length, hex_value

    else:

        if length is None:
            hex_value = data[offset:]
            length = len(hex_value)
        else:
            hex_value = data[offset: offset + length]
        # end if

        return offset + length, hex_value
    # end if
# end def field_from_hex_list


class Field(BitField):
    """
    Record and EXM Field class.
    """

    MODE_AUTO = 0
    MODE_RAW = 1
    MODE_DEFAULT = MODE_AUTO

    VARIABLE_LEN = None

    def __init__(self, fid=None, length=0x00, has_tag=None, variable=None, finger_print=False, default_value=None,
                 title='Undefined Field', name=None, mode=None, checks=None, conversions=None, aliases=tuple(),
                 optional=None, parser=None, interpreter=None):
        """
        :param fid: Field identifier - OPTIONAL
        :type fid: ``int`` or ``None``
        :param length: Field value length - OPTIONAL
        :type length: ``int``
        :param has_tag: Flag indicating if the Tag is generated as a prefix to the element - OPTIONAL
        :type has_tag: ``bool`` or ``None``
        :param variable: Flag indicating if the Length is generated as a prefix to the element - OPTIONAL
        :type variable: ``bool``  or ``None``
        :param finger_print: Flag indicating if the Field is used for Rivet/Integra computation - OPTIONAL
        :type finger_print: ``bool``
        :param default_value: Default value for the has_tag non-variable parameters - OPTIONAL
        :type default_value: ``object``
        :param title: Title of the Field - OPTIONAL
        :type title: ``str``
        :param name: Name of this Field. The name is used to provide quick access to the Field through
                    its parent attributes - OPTIONAL
        :type name: ``str`` or ``None``
        :param mode: Mode of the Field.
        :type mode: ``int`` or ``None``
        :param checks: List of checks on the value - OPTIONAL
        :type checks: ``list[Checks]`` or ``tuple[Checks]``  or ``None``
        :param conversions: Dict that maps an input type to a conversion routine - OPTIONAL
        :type conversions: ``dict[sourceType, converter]``  or ``None``
        :param aliases: List of alternative names by which to reference this field - OPTIONAL
        :type aliases: ``tuple``
        :param optional: Flag indicating if the field is optional - OPTIONAL
        :type optional: ``bool`` or ``callable`` or ``None``
        :param parser: From HexList parsing method - OPTIONAL
        :type parser: ``callable`` or ``None``
        :param interpreter: Interpretation dictionary - OPTIONAL
        :type interpreter: ``dict`` or ``None``

        :raise ``ValueError``: If has_tag or variable are None or if the field defines both has_tag and an internal tag
        :raise ``AssertionError``: If has_tag or variable are None or if the field defines both has_tag
                                  and an internal tag
        """

        assert has_tag is not None, ValueError("has_tag should not be None")
        assert variable is not None, ValueError("variable should not be None")
        assert (not (has_tag and (fid < 0))), ValueError(f"Field {name} defines both has_tag and an internal tag")
        if parser is None:
            parser = field_from_hex_list
        # end if

        # Note that due to automatic property behavior, the initialization must
        # be done (at least) in the following order:
        # - has_tag
        #  - optional
        # - conversions
        #  - mode
        # - checks
        #  - name
        #   - default_value
        self.conversions = conversions
        self.mode = mode
        super().__init__(fid, length, 0x08 if has_tag else 0x00, 0x08 if variable else 0x00,
                         default_value=default_value, title=title, name=name, checks=checks, conversions=conversions,
                         aliases=aliases, optional=optional, parser=parser, interpreter=interpreter)
        self.finger_print = finger_print

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
    # end def __init__

    def __eq__(self, other):
        """
        Tests the equality of Field with another field.

        :param  other: Other Field instance
        :type other: ``Field`` or ``None``

        :return: Comparison result
        :rtype: ``bool``

        :raise ``TypeError``: If other is not of type ``Field``
        """
        if other is None:
            return False
        # end if

        if not isinstance(other, Field):
            raise TypeError(f"Wrong other type: {type(other).__name__}. Should be of type Field")
        # end if

        result = (self.fid == other.fid)

        if result:
            result = (self.length == other.length)
        # end if

        if result:
            result = (self.has_tag == other.has_tag)
        # end if

        if result:
            result = (self.variable == other.variable)
        # end if

        if result:
            result = (self._finger_print == other.finger_print)
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

        return result
    # end def __eq__

    def deepcopy(self):
        # See ``BitField.deepcopy``
        return self.__class__(self.fid, self.length, self.has_tag, self.variable, self.finger_print, self.default_value,
                              self.title, self.name, self.mode, self.checks, self.conversions, self.aliases)
    # end def deepcopy

    @BitField.fid.setter
    def fid(self, fid):
        # See ``BitField.fid``
        if isinstance(fid, int) and (fid > 255):
            raise ValueError(f"Wrong Fid value: {fid}. Must be less or equal to 255.")
        # end if

        BitField.fid.fset(self, fid)
    # end def fid

    @property
    def fid_length(self):
        # See ``Bitfield.fid_length``
        return self._fid_length / 8
    # end def fid_length

    @BitField.fid_length.setter
    def fid_length(self, fid_length):
        # See ``Bitfield.fid_length``

        self._fid_length = fid_length * 8
    # end def fid_length

    @property
    def len_length(self):
        # See ``Bitfield.len_length``
        return self._len_length / 8
    # end def len_length

    @BitField.len_length.setter
    def len_length(self, len_length):
        # See ``Bitfield._len_length``
        self._len_length = len_length * 8
    # end def len_length

    @BitField.has_tag.setter
    def has_tag(self, has_tag):
        """
        Sets the has_tag property for the Field.

        :param has_tag: Flag indicating if the field has an optional tag
        :type has_tag: ``int`` or ``bool`` or ``callable``
        """
        if isinstance(has_tag, (bool, int)):
            if has_tag not in [0, 1]:
                raise ValueError(f"Wrong has_tag value: {has_tag:d}. Must be in range [0..1].")
            # end if
        elif not callable(has_tag):
            raise TypeError(f"Wrong has_tag type: {type(has_tag).__name__}. Should be a boolean, integer or callable.")
        # end if

        self.fid_length = has_tag
    # end def has_tag

    def set_has_tag(self, has_tag):
        """
        Deprecated function. See property ``has_tag``.

        :param has_tag: Flag indicating if the field has an optional tag
        :type has_tag: ``int`` or ``bool`` or ``callable``
        """
        self.has_tag = has_tag
    # end def set_has_tag

    def set_length(self, length):
        # See ``BitField.set_length``
        if length is not None and not callable(length) and isinstance(length, int) and length not in range(256):
                raise ValueError(f"Wrong Length value: {length:d}. Should be in range [0..255] instead.")
        # end if

        super().set_length(length)
    # end def set_length

    def set_optional(self, optional):
        """
        Set Flag indicating if the field is optional.

        :param optional: Flag indicating if the field has an optional tag
        :type optional: ``int`` or ``None``
        """
        if optional is None:
            optional = self.has_tag
        # end if

        self._optional = optional
    # end def set_optional

    optional = property(BitField.is_optional, set_optional)

    @BitField.variable.setter
    def variable(self, variable):
        """
        Sets the Variable of the Field.

        :param variable: Variable value
        :type variable: ``int`` or ``bool``
        """
        if not isinstance(variable, int):
            raise TypeError(f"Wrong Variable type: {type(variable).__name__}. Should be a boolean or an integer.")
        elif isinstance(variable, bool):
            variable = self.length // 255 + 1 if variable else 0

        # end if

        if variable not in range(2):
            raise ValueError(f"Wrong Variable value: {variable:d}. Should be in range [0..1].")
        # end if

        self.len_length = variable
    # end def variable

    def set_variable(self, variable):
        """
        deprecated function. See property ``variable``.

        :param variable: Variable value
        :type variable: ``int`` or ``bool``
        """
        self.variable = variable
    # end def set_variable

    @property
    def finger_print(self):
        """
        Flag indicating if field is relevant for Rivet/Integra computation

        :return: FingerPrint status
        :rtype: ``bool``
        """
        return self._finger_print
    # end def finger_print

    @finger_print.setter
    def finger_print(self, finger_print):
        """
        Set flag indicating if field is relevant for Rivet/Integra computation

        :param finger_print: Field is used for Rivet/Integra computation
        :type finger_print: ``bool`` or ``int``
        """
        if not isinstance(finger_print, (bool, int)):
            raise TypeError(f"Wrong FingerPrint type: {type(finger_print).__name__}. Should be a boolean or"
                            " an integer.")
        # end if

        if finger_print not in range(2):
            raise ValueError(f"Wrong FingerPrint value: {finger_print:d}. Should be in range [0..1].")
        # end if

        self._finger_print = finger_print
    # end def finger_print

    def set_finger_print(self, finger_print):
        """
        Deprecated function. See property ``finger_print``

        :param finger_print: Field is used for Rivet/Integra computation
        :type finger_print: ``bool`` or ``int``
        """
        self.finger_print = finger_print
    # end def set_finger_print

    @property
    def mode(self):
        """
        Gets the Mode of the Field.

        The mode is used to provide quick access to the Field through its parent
        attributes

        :return: The Field mode
        :rtype: ``int``
        """
        return self._mode
    # end def mode

    @mode.setter
    def mode(self, mode):
        """
        Sets the Mode of the Field.

        The mode is used to provide quick access to the Field through its parent
        attributes

        :param mode: The Field mode
        :type mode: ``int`` or ``None``

        :raise ``TypeError``: If the wrong type for the mode parameter is passed
        """
        if mode is None:
            if self._conversions:
                mode = self.MODE_AUTO
            else:
                mode = self.MODE_DEFAULT
            # end if
        elif not isinstance(mode, int):
            raise TypeError(f"Wrong Mode type: {type(mode).__name__}. Should be an int")
        # end if

        self._mode = mode
    # end def mode

    def __get_instantiation_location(self):
        """
        Obtains the instantiation location for this object.

        :return: A tuple (fileName, lineNumber, functionName, text) of the instantiation location.
        :rtype: ``tuple[str, str, str, str]``
        """
        return (self.__instantiation_file,
                self.__instantiation_line,
                self.__instantiation_function_name,
                self.__instantiation_text)
    # end def __get_instantiation_location

    def __repr__(self):
        """
        String representation of the field

        :return: A string representation of the instance
        :rtype: ``str``
        """
        arg_names = ("fid", "length", "has_tag", "variable", "finger_print", "default_value", "title", "name", "mode",
                    "checks", "conversions", "aliases", "optional")
        attr_text = ", ".join((f"{arg_name} = {repr(getattr(self, f'_{arg_name}', None))}" for arg_name in arg_names))
        return f"{self.__class__.__name__}({attr_text})"
    # end def __repr__

    def create_summary(self, append_fid=True):
        # See ``BitField.create_summary``
        if append_fid and (self._fid >= 0):
            log = f"{self._title}: (0x{self._fid:02x})"
        else:
            log = f"{self._title}:"
        # end if

        return log
    # end def create_summary

    def accept(self, container, data, offset=0, limit=None):
        # See ``BitField.accept``
        limit = limit if limit is not None else len(data) * 8
        # Check of the end of the buffer to analyze
        if offset >= limit:
            return self.is_optional(container)
        # end if

        if self.has_tag:
            return self.fid == data[offset]
        # end if
        return True
    # end def accept
# end class Field


class CheckBool(Check):
    """
    Checks a boolean
    """

    def __call__(self, value, name=None):
        # See ``Check.__call__``
        return isinstance(value, bool)
    # end def __call__

    def __repr__(self):
        """
        Displays a Debugger-friendly name for this check

        :return: The current object, as a string.
        :rtype: ``str``
        """
        return f"{self.__class__.__name__}()"
    # end def __repr__
# end class CheckBool


# Defined CheckBool as an alias of the class
checkBool = CheckBool


class CheckInt(Check):
    """
    Checks an integer against minimum and maximum bounds
    """

    def __init__(self, min_value=None, max_value=None):
        """
        :param min_value: The min range value accepted - OPTIONAL
        :type min_value: ``int`` or ``None``
        :param max_value: The max range value accepted - OPTIONAL
        :type max_value: ``int`` or ``None``
        """
        super().__init__()

        self._min_value = min_value
        self._max_value = max_value
    # end def __init__

    def __call__(self, value, name=None):
        """
        The actual check to perform.

        :param value: The value to check
        :type value: ``object``
        :param name: Field name for debug message purpose - OPTIONAL
        :type name: ``str`` or ``None``

        :return: The check result.
        :rtype: ``bool``

        :raise ``ValueError``:  Value not in the correct range
        """
        if isinstance(value, int):
            result = True
            if self._min_value is not None:
                if value < self._min_value:
                    result = False
                # end if
            # end if
            if self._max_value is not None:
                if value > self._max_value:
                    result = False
                # end if
            # end if
            if result:
                return True
            else:
                ending = "." if name is None else f" for {name}."
                raise ValueError(f"Value is not in a correct range [{self._min_value}, {self._max_value}]{ending}")
            # end if

        else:
            return False
        # end if
    # end def __call__

    def __repr__(self):
        """
        Displays a Debugger-friendly name for this check

        :return: The current object, as a string.
        :rtype: ``str``
        """
        return f"{self.__class__.__name__}(min_value = {self._min_value!r}, max_value = {self._max_value!r})"
    # end def __repr__
# end class CheckInt


# Defined CheckInt as an alias of the class
checkInt = CheckInt


class CheckByte(CheckInt):
    """
    Checks if the parameter is a Byte integer.
    """

    def __init__(self):
        super().__init__(min_value=0, max_value=255)
    # end def __init__

    def __repr__(self):
        # See ``CheckInt.__repr__``
        return f"{self.__class__.__name__}"
    # end def __repr__
# end class CheckByte


checkByte = CheckByte


class CheckHexList(Check):
    """
    Checks a value as an ``HexList``
    """

    def __init__(self, length=None, min_length=None, max_length=None):
        """
        :param length: The expected parameter length - OPTIONAL
        :type length: ``int`` or ``None``
        :param  min_length: The min length accepted - OPTIONAL
        :type min_length: ``int`` or ``None``
        :param max_length: The max length accepted - OPTIONAL
        :type max_length: ``int`` or ``None``
        """
        super(CheckHexList, self).__init__()

        self._length = length
        self._min_length = min_length
        self._max_length = max_length
    # end def __init__

    def __call__(self, value, name=None):
        """
        The actual check to perform.

        :param value: The value to check
        :type value: ``object``
        :param name: Field name for debug message purpose - OPTIONAL
        :type name: ``str`` or ``None``

        :return: The check result.
        :rtype: ``bool``

        :raise ``ValueError``:  length of the value not in the correct range
        """
        if (isinstance(value, HexList) or isinstance(value, RandHexList) or hasattr(value, 'toHexList')
                or hasattr(value, '__hexlist__')):
            # Check value which is not variable
            check_status = (self._length == Field.VARIABLE_LEN)
            if not check_status:
                if isinstance(self._length, int):
                    check_status = (len(value) == self._length)
                elif isinstance(self._length, tuple):
                    check_status = (len(value) in self._length)
                # end if
                if not check_status:
                    if isinstance(self._length, int):
                        ending = "." if name is None else f" for {name}."
                        raise ValueError(f"When encoded in a HexList, {value} should be"
                                         f" {self._length:d}-byte long{ending}")
                    elif isinstance(self._length, tuple):
                        ending = "." if name is None else f" for {name}."
                        raise ValueError(f"When encoded in a HexList, {value} should"
                                         f" have a length in range {self._length}{ending}")
                    # end if
                else:
                    return True
                # end if
            else:
                if (self._min_length is not None) and (len(value) < self._min_length):
                    ending = "." if name is None else f" for {name}."
                    raise ValueError(f"When encoded in a HexList, {value} should"
                                     f" have a length greater than {self._min_length}{ending}")
                # end if

                if (self._max_length is not None) and (len(value) > self._max_length):
                    ending = "." if name is None else f" for {name}."
                    raise ValueError(f"When encoded in a HexList, {value} should"
                                     f" have a length smaller than {self._max_length}{ending}")
                # end if

                return True
            # end if
        else:
            return False
        # end if
    # end def __call__

    def __repr__(self):
        """
        Displays a Debugger-friendly name for this check

        :return: The current object, as a string.
        :rtype: ``str``
        """
        return f"{self.__class__.__name__}(length = {self._length!r}, min_length = {self._min_length!r}, " \
               f"max_length = {self._max_length!r})"
    # end def __repr__
# end class CheckHexList


checkHexList = CheckHexList


class CheckString(Check):
    """
    Checks if the parameter is a String type.
    """

    def __init__(self, length=None, min_length=None, max_length=None):
        """
        :param length: The expected parameter length or a tuple of possible lengths - OPTIONAL
        :type length: ``int`` or ``None``
        :param  min_length: The min length accepted - OPTIONAL
        :type min_length: ``int`` or``tuple[int]`` or ``None``
        :param  max_length: The max length accepted - OPTIONAL
        :type max_length: ``int`` or ``None``
        """
        super().__init__()

        self._length = length
        self._min_length = min_length
        self._max_length = max_length
    # end def __init__

    def __call__(self, value, name=None):
        """
        The actual check to perform.

        :param value: The value to check
        :type value: ``object``
        :param name: Field name for debug message purpose - OPTIONAL
        :type name: ``str`` or ``None``

        :return: The check result.
        :rtype: ``bool``

        :raise ``ValueError``:  length of the value not in the correct range
        """
        if isinstance(value, str):
            check_status = (self._length == Field.VARIABLE_LEN)
            if not check_status:
                if isinstance(self._length, int):
                    check_status = (len(value) == self._length)
                elif isinstance(self._length, tuple):
                    check_status = (len(value) in self._length)
                # end if
                if not check_status:
                    if isinstance(self._length, int):
                        ending = "." if name is None else f" for {name}."
                        raise ValueError(f"When encoded in a String, {value} should be"
                                         f" {self._length:d}-byte long{ending}")
                    elif isinstance(self._length, tuple):
                        ending = "." if name is None else f" for {name}."
                        raise ValueError(f"When encoded in a String, {value} should"
                                         f" have a length in range {self._length}{ending}")
                    # end if
                else:
                    return True
                # end if
            else:
                if (self._min_length is not None) and (len(value) < self._min_length):
                    ending = "." if name is None else f" for {name}."
                    raise ValueError(f"When encoded in a String,{value} should"
                                     f" have a length greater than {self._min_length}{ending}")
                # end if

                if (self._max_length is not None) and (len(value) > self._max_length):
                    ending = "." if name is None else f" for {name}."
                    raise ValueError(f"When encoded in a String, {value} should"
                                     f" have a length smaller than {self._max_length}{ending}")
                # end if
                return True
            # end if
        else:
            return False
        # end if
    # end def __call__

    def __repr__(self):
        """
        Displays a Debugger-friendly name for this check

        :return: The current object, as a string.
        :rtype: ``str``
        """
        return f"{self.__class__}(length = {self._length!r}, minLength = {self._min_length!r}, " \
               f"maxLength = {self._max_length!r})"
    # end def __repr__
# end class CheckString


checkString = CheckString


class CheckBitStruct(Check):
    """
    Checks if the parameter is a BitStruct type.
    """

    def __init__(self, length):
        """
        :param length: The expected parameter length
        :type length: ``int``
        """
        super().__init__()

        self._length = length
    # end def __init__

    def __call__(self, value, name=None):
        """
        The actual check to perform.

        :param value: The value to check
        :type value: ``object``
        :param name: Field name for debug message purpose - OPTIONAL
        :type name: ``str`` or ``None``

        :return: The check result.
        :rtype: ``bool``

        :raise ``ValueError``:  if the length of the value not in the correct range
        """
        if isinstance(value, BitStruct):
            if len(value) != self._length:
                ending = "." if name is None else f" for {name}."
                raise ValueError(f"When encoded in a BitStruct, {value} should be"
                                 f"{self._length:d}-byte long{ending}")
            else:
                return True
            # end if
        else:
            return False
        # end if
    # end def __call__

    def __repr__(self):
        """
        Displays a Debugger-friendly name for this check

        :return: The current object, as a string.
        :rtype: ``str``
        """
        return f"{self.__class__.__name__}(length = {self._length!r})"
    # end def __repr__
# end class CheckBitStruct


checkBitStruct = CheckBitStruct


class CheckType(Check):
    """
    Checks if the parameter is a classType type.
    """

    def __init__(self, class_type):
        """
        :param class_type: the type to check
        :type class_type: ``type``
        """
        super().__init__()

        self._class_type = class_type
    # end def __init__

    def __call__(self, value, name=None):
        # See ``Check.__call__``
        return isinstance(value, self._class_type)
    # end def __call__

    def __repr__(self):
        """
        Displays a Debugger-friendly name for this check

        :return: The current object, as a string.
        :rtype: ``str``
        """
        return f"{self.__class__.__name__}(class_type = {self._class_type!r})"
    # end def __repr__
# end class CheckType


checkType = CheckType


class CheckNone(Check):
    """
    Checks that None is an acceptable value
    """

    def __call__(self, value, name=None):
        # See ``Check.__call__``
        return value is None
    # end def __call__

    def __repr__(self):
        """
        Displays a Debugger-friendly name for this check

        :return: The current object, as a string.
        :rtype: ``str``
        """
        return f"{self.__class__.__name__}()"
    # end def __repr__
# end class CheckNone


checkNone = CheckNone


class CheckList(Check):
    """
    Checks if the parameter is a List type.
    """

    def __init__(self, length=None):
        """
        :param length: The expected parameter length - OPTIONAL
        :type length: ``int`` or ``None``
        """
        super().__init__()

        self._length = length
    # end def __init__

    def __call__(self, value, name=None):
        """
        The actual check to perform.

        :param value: The value to check
        :type value: ``object``
        :param name: Field name for debug message purpose - OPTIONAL
        :type name: ``str`` or ``None``

        :return: The check result.
        :rtype: ``bool``

        :raise ``ValueError``: If the length of the value not in the correct range
        :raise ``TypeError``: If the items inside the list of value are not compatible with numbers or HexList
        """
        if isinstance(value, (list, tuple)):
            # Check value which is not variable
            if (self._length != Field.VARIABLE_LEN) and (len(value) != self._length):
                ending = "." if name is None else f" for {name}."
                # end if
                raise ValueError(f"When encoded in a List, {value} should be"
                                 f" {self._length:d}-byte long{ending}")
            else:
                for item in value:
                    if (not isinstance(item, (int, HexList))) and (not hasattr(item, "__hexlist__")):
                        ending = "." if name is None else f" for {name}."
                        raise TypeError(f"When encoded in a List, {item} should be"
                                        f" int/long/HexList type or convertible"
                                        f" into HexList{ending}")
                    # end if
                    if (not isinstance(item, HexList)) and (not hasattr(item, "__hexlist__")):
                        if (item < 0) or (item > 255):
                            ending = "." if name is None else f" for {name}."
                            raise ValueError(f"When encoded in a List, {item} should"
                                             f" be in range [0..255]{ending}")
                        # end if
                    # end if
                # end for
                return True
            # end if
        else:
            return False
        # end if
    # end def __call__

    def __repr__(self):
        """
        Displays a Debugger-friendly name for this check

        :return: The current object, as a string.
        :rtype: ``str``
        """
        return f"{self.__class__.__name__}(length = {self._length!r})"
    # end def __repr__


# end class CheckList
checkList = CheckList


class CheckBCD(CheckHexList):
    """
    Checks if the parameter is a Binary coded decimal (BCD) type.
    """

    def __init__(self, length=None):
        """
        :param length: The expected parameter length - OPTIONAL
        :type length: ``int`` or ``None``
        """
        super().__init__(length)
    # end def __init__

    def __call__(self, value, name=None):
        # See ``Check.__call__``
        result = super().__call__(value, name)

        for i in range(self._length):
            if value[i] & 0xF > 9:
                result = False
            # end if
            if (value[i] >> 4) & 0xF > 9:
                result = False
            # end if
        # end for
        return result
    # end def __call__
# end class CheckBCD


class CheckBCDorValue(CheckBCD):
    """
    Checks if the parameter is a Binary coded decimal (BCD) type or a specific value.
    """

    def __init__(self, length=None, value_to_check=None):
        """
        :param  length: The expected parameter length - OPTIONAL
        :type length: ``int`` or ``None``
        :param value_to_check: the value to compare with - OPTIONAL
        :type value_to_check: ``HexList`` or ``None``
        """
        assert isinstance(value_to_check, HexList), "The value to check should be a HexList object"
        self.value_to_check = value_to_check
        super().__init__(length)
    # end def __init__

    def __call__(self, value, name=None):
        # See ``Check.__call__``
        if value == self.value_to_check:
            return True
        # end if

        return super().__call__(value, name)
    # end def __call__
# end class CheckBCDorValue


checkBCD = CheckBCD

checkBCDorValue = CheckBCDorValue


def field_length(fid=None, fids=None, before_fid=None, after_fid=None, delta=0):
    """
    Obtains the length of the given field, by its fid.

    This is needed for default values, when the default value should be the
    length of the next field.

    In such cases, the FIELDS should be declared as follows:
    ``
    FIELDS = (Field(FID_MYLENGTH...,
                    default_value = fieldLength(FID_MYVALUE),
                    ...),
              Field(FID_MYVALUE,
                    ...),
             )
    ``

    :param fid: Unique field id for which to compute the length - Callback
    :type fid: ``int`` or ``None``
    :param fids: List of field ids for which to add the lengths - Callback
    :type fids: ``tuple[int]`` or ``None``
    :param before_fid: Unique field id marking the (non-inclusive) start of the fids - Callback
    :type before_fid: ``int`` or ``None``
    :param after_fid:  Unique field id marking the (non-inclusive) end of the fids - Callback
    :param after_fid: ``int`` or ``None``
    :param delta: Value to add to the field length. - Callback
    :type delta: ``int``

    :return: callback for default value resolution
    :rtype: ``func``

    :raise ``ValueError``: if all the parameters that can be None are none, at least one must be non-None
    """
    not_none_count = ((1 if fid is not None else 0) +
                      (1 if fids is not None else 0) +
                      (1 if before_fid is not None else 0) +
                      (1 if after_fid is not None else 0)
                      )
    assert (not_none_count >= 1), ValueError('At least one of fid, fids, beforeFids or afterFid must be non-None')

    def callback(context):
        """
        Extract value from context

        :param context: The context to extract the value from.
        :type context: ``AbstractFieldContainerMixin``
        :return: The value
        :rtype: ``int``
        """
        if context is None:
            return None
        # end if

        if fid is not None:
            fid_list = (fid,)
        else:
            fid_list = [field.fid for field in context.FIELDS]
        # end if

        if before_fid is not None:
            fid_list = fid_list[:fid_list.index(before_fid)]
        # end if

        if after_fid is not None:
            fid_list = fid_list[fid_list.index(after_fid) + 1:]
        # end if

        return sum((len(HexList(context.getValue(f))) for f in fid_list)) + delta
    # end def callback
    return callback
# end def field_length


class ArrayField(Field):
    """
    Overload of a field that is actually an array of identical fields.
    """

    class ArrayWrapper(object):
        """
        A wrapper around an array, that enforces field access like a ContainerMixin
        """

        def __init__(self, field, values):
            """
            :param field: The field definition
            :type field: ``Field``
            :param values: The value to wrap
            :type values: ``list``
            """
            self._field = field
            self._values = values
        # end def __init__

        def __str__(self):
            """
            Converts the current values to a string

            :return: The current values, as a string.
            :rtype: ``str``
            """
            return str(self._values)
        # end def __str__

        def __repr__(self):
            """
            Displays a Debugger-friendly name for this field

            :return: The current object, as a string.
            :rtype: ``str``
            """
            return f"{self.__class__.__name__}(field={self._field!r}, values={self._values!r})"
        # end def __repr__

        def __setitem__(self, key, values):
            """
            Sets an item or a slice

            :param key: The key for which to obtain the value
            :type key: ``object``
            :param values: List of element to use as replacement
            :type values: ``list``
            """
            field = super(self._field.__class__, self._field)
            if isinstance(key, slice):
                new_values = []
                for value in values:
                    field.check_value(value, self)  # Value consistency check
                    value = field.convert_value(value)  # Rich type conversion
                    new_values.append(value)
                # end for
            else:
                value = values
                field.check_value(value, self)  # Value consistency check
                value = field.convert_value(value)  # Rich type conversion
                new_values = value
                # Handle value expansion.
                if key == len(self._values):
                    self._values.append(None)
                # end if
            # end if

            self._values[key] = new_values
        # end def __setitem__

        def __getitem__(self, key):
            """
            Gets an item or a slice from the array


            :param key: The key for which to obtain the value
            :type key: ``object``
            :return: the values
            :rtype: ``list``
            """

            return self._values[key]
        # end def __getitem__

        def __len__(self):
            """
            Obtains the array length.

            :return: The array length
            :rtype: ``int``
            """
            return len(self._values)
        # end def __len__

        def __iter__(self):
            """
            Obtains an iterator on the array

            :return: An iterator on the array.
            :rtype: ``iterator``
            """
            return iter(self._values)
        # end def __iter__

        def __eq__(self, other):
            """
            Check objects for equality

            :param other: The other object to compare
            :type other: ``ArrayWrapper``
            :return: The comparison results
            :rtype: ``bool``
            """

            result = isinstance(other, self.__class__)

            if result:
                result = self._values == other._values
            # end if

            return result
        # end def __eq__

        def __ne__(self, other):
            """
            Check objects for inequality

            :param other: The other object to compare
            :type other: ``ArrayWrapper``
            :return: The comparison results
            :rtype: ``bool``
            """
            return not (self == other)
        # end def __ne__

        @staticmethod
        def _indent_log(log):
            """
            Increases the indentation of a log

            :param log: Log to indent
            :type log: ``str``
            :return: Re-indented log
            :rtype: ``str``
            """
            return '  ' + log.replace('\n', '\n  ')
        # end def _indent_log

        def create_summary(self):
            """
            Creates a summary of the array.

            :return: Summary of the array
            :rtype: ``str``
            """

            summary_entries = [str(HexList(self))]

            for index, field_value in enumerate(self._values):
                name = f"{self._field.name}[{index:d}]"

                if hasattr(field_value, "create_summary"):
                    field_value = field_value.create_summary()
                # end if

                logEntry = f"- {name}: value = {field_value}"

                summary_entries.append(self._indent_log(logEntry))
                # end if
            # end for

            return '\n'.join(summary_entries)
        # end def create_summary
    # end class ArrayWrapper

    def __init__(self, fid=None, length=0x00, has_tag=None, variable=None, finger_print=False, default_value=None,
                 title='Undefined Field', name=None, mode=None, checks=None, conversions=None, aliases=tuple(),
                 optional=None, size=None, ignore=lambda x: False, parser=None, interpreter=None, **kwargs):
        """
        :param fid: Field identifier - OPTIONAL
        :type fid: ``int`` or ``None``
        :param length: Field value length - OPTIONAL
        :type length: ``int``
        :param has_tag: Flag indicating if the Tag is generated as a prefix to the element - OPTIONAL
        :type has_tag: ``bool`` or ``None``
        :param variable: Flag indicating if the Length is generated as a prefix to the element - OPTIONAL
        :type variable: ``bool`` or ``None``
        :param finger_print: Flag indicating if Field is used for Rivet/Integra computation - OPTIONAL
        :type finger_print: ``bool`` or ``None``
        :param default_value: Default value for the has_tag non-variable parameters - OPTIONAL
        :type default_value: ``object`` or ``None``
        :param title: Title of the Field - OPTIONAL
        :type title: ``str``
        :param name: Name of this Field. The name is used to provide quick access to the Field through its parent
                     attributes - OPTIONAL
        :type name: ``str`` or ``None``
        :param mode: Mode of the Field.
        :type mode: ``int`` or ``None``
        :param checks: List of checks on the value - OPTIONAL
        :type checks: ``list[Checks]`` or ``tuple[Checks]`` or ``None``
        :param conversions: Dict that maps an input type to a conversion routine - OPTIONAL
        :type conversions: ``dict[sourceType, converter]`` or ``None``
        :param aliases: List of alternative names by which to reference this field - OPTIONAL
        :type aliases: ``tuple``
        :param optional: Flag indicating if the field is optional - OPTIONAL
        :type optional: ``bool`` or ``callable`` or ``None``
        :param size: The number of elements in this array, None for unbounded - OPTIONAL
        :type size: ``int`` or ``None``
        :param ignore: A filter that check whether an element should be ignored or not on HexList parsing. -OPTIONAL
        :type ignore: ``callable``
        :param parser: From HexList parsing method - OPTIONAL
        :type parser: ``callable`` or ``None``
        :param interpreter: Interpretation dictionary - OPTIONAL
        :type interpreter: ``dict`` or ``None``
        :param kwargs: Extra arguments, ignored
        :type kwargs: ``dict`` or ``None``
        """

        self._size = None
        self._ignore = None
        super().__init__(fid, length, has_tag=has_tag, variable=variable, finger_print=finger_print,
                         default_value=default_value, title=title, name=name, mode=mode, checks=checks,
                         conversions=conversions, aliases=aliases, optional=optional, parser=parser,
                         interpreter=interpreter, **kwargs)

        self.size = size
        self.ignore = ignore
    # end def __init__

    def convert_value(self, value, container=None):
        # See ``Field.convert_value``
        result = [super(ArrayField, self).convert_value(v, container) for v in value]

        return self.ArrayWrapper(self, result)
    # end def convert_value

    def check_value(self, value, container=None):
        # See ``Field.convert_value``
        result = all([super(ArrayField, self).check_value(v) for v in value])
        return result
    # end def check_value

    @property
    def size(self):
        """
        Gets the size of the array, in number of elements

        :return: The array size, None for unbounded
        :rtype: ``int`` or ``None``
        """
        return self._size
    # end def size

    @size.setter
    def size(self, size):
        """
        Sets the size attribute of the Field.

        :param size: size The array size, None for unbounded
        :type size: ``int`` or ``bool`` or  ``None``
        """
        if not isinstance(size, (bool, int, None)):
            raise TypeError(f"Wrong Size type: {type(size).__name__}. Should be a int or None")
        # end if

        self._size = size
    # end def size

    @property
    def ignore(self):
        """
        Gets the ignore predicate

        :return: A predicate that tells whether a HexList must be ignored on parse or not.
        :rtype: ``callable``
        """
        return self._ignore
    # end def ignore

    @ignore.setter
    def ignore(self, ignore):
        """
        Sets the size attribute of the Field.

        :param ignore: A predicate that tells whether a HexList must be ignored on parse or not.
        :type ignore: ``callable``

        :raise ``TypeError``: If ignore parameter isn't a callable
        """
        if not callable(ignore):
            raise TypeError("ignore must be a 1-parameter callable")
        # end if

        self._ignore = ignore
    # end def ignore

    def get_default_value(self, context=None):
        # See ``BitField.get_default_value``
        if self.size is None:
            default_value = self.ArrayWrapper(self, [])
        else:
            field = super(ArrayField, self)
            default_value = self.ArrayWrapper(self, [field.get_default_value(context) for _ in range(self._size)])
        # end if

        default_value.__class__.__name__ = self.__class__.__name__
        return default_value
    # end def get_default_value

    def set_default_value(self, default_value):
        # See ``BitField.set_default_value``
        if default_value is not None:

            field = super(ArrayField, self)
            # A callable would be a problem, as we are (not yet) within a FieldContainerMixin.
            if not callable(default_value):
                field.check_value(default_value, None)
                default_value = field.convert_value(default_value)
            elif 'context' not in default_value.__code__.co_varnames:
                raise TypeError(f"Wrong callable default value: {default_value}. "
                                "Must have context as its only parameter")
            # end if
        # end if

        self._default_value = default_value
    # end def set_default_value

    default_value = property(get_default_value, set_default_value)
# end class ArrayField


class BitField8(BitField):
    """
    Field of length 1 byte (8 bits)
    """

    def __init__(self, fid=None, length=0x08, fid_length=0x00, len_length=0x00, default_value=None,
                 title='Undefined Field', name=None, checks=None, conversions=None, aliases=tuple(), optional=None,
                 parser=byte_field_from_hex_list, interpreter=None):
        # See ``BitField.__init__``
        super(BitField8, self).__init__(fid, length, fid_length, len_length, default_value, title, name, checks,
                                        conversions, aliases, optional, parser, interpreter)

        if checks is None:
            self.checks = (CheckHexList(0x01), CheckByte())
        # end if

        if conversions is None:
            self.conversions = {HexList: lambda x: x[0]}
        # end if
    # end def __init__
# end class BitField8

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
