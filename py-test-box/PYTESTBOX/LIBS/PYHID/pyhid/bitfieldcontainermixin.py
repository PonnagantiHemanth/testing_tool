#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyhid.bitfieldcontainermixin
:brief: BitFieldContainerMixin interface definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/12/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from collections import defaultdict
from time import perf_counter_ns

from pylibrary.system.tracelogger import TIMESTAMP_UNIT
from pylibrary.system.tracelogger import TIMESTAMP_UNIT_DIVIDER_MAP
from pylibrary.tools.bitstruct import BitStruct
from pylibrary.tools.hexlist import HexList
from pyhid.bitfield import getElement
from pyhid.field import ArrayField
from pyhid.field import Field
from pylibrary.tools.numeral import to_int


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class AbstractFieldContainerMixin:
    """
    Common class for FieldContainerMixin implementations.

    Factors common methods
    """
    FIELDS = tuple()

    # The mode for this FieldContainerMixin.
    # This can be overridden in derived classes.
    # - MODE_AUTO does no conversion and no check
    # - MODE_RAW does no conversion and no check
    # The default value is set to MODE_AUTO
    MODE_AUTO = 0
    MODE_RAW = 1
    MODE_DEFAULT = MODE_AUTO
    MODE = MODE_DEFAULT

    # Whether this FieldContainerMixin is referenced by a feature Id.
    SUB_ID = None

    class FID(object):
        """
        Generic field identifiers
        """
        DUMMY = 253

        # Minimum FID for subclass overloading
        # Using a negative value hides the FID from the trace
        MIN = -1
    # end class FID

    class LEN(object):
        """
        Generic lengths definitions
        """
        TAG_LEN = 2  # Length of standard Tag and Length parts
        # TODO: This constant exists only until TSIO will be up to date and use TAG_LEN
        TAG_LEN_SIZE = TAG_LEN
    # end class LEN

    TAG_LEN_SIZE = LEN.TAG_LEN

    def __init__(self, *args, **kwargs):
        """
        :param args: Positional Parameters
        :type args: ``tuple``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``dict``

        :raise ``AssertionError``: If the class has an invalid value for its FEATURE_ID or the FIELDS is not a tuple
        """
        assert ((self.SUB_ID is None) or (self.SUB_ID in range(0xFFFF))), \
            ValueError(f'class {self.__class__.__name__} has an invalid value {self.SUB_ID} for its FEATURE_ID')

        assert (isinstance(self.__class__.FIELDS, tuple)), \
            TypeError(f'class {self.__class__.__name__} should have an immutable FIELDS value (tuple, not list)')

        # Set automatically fids value if None
        self._initializeAutomaticallyFids()
    # end def __init__

    def _initializeAutomaticallyFids(self):
        """
        Fids attributes of FIELDS shall be set for internal use

        From external point of view fids are not always mandatory.
        As a consequence, fid is optional and automatically computed during
        instantiation of container
        """
        ind = -1
        existing_fids = [f.fid for f in self.FIELDS if f.fid is not None]
        for field in self.FIELDS:
            if field.fid is None:
                while ind in existing_fids:
                    ind -= 1
                # end while
                field.fid = ind
                existing_fids.append(ind)
            # end if
        # end for
    # end def _initializeAutomaticallyFids

    def getFieldDefinition(self, fid):
        """
        Get the field definition for a given FID.

        This is, and must stay an instance method, as long as migration from
        the former Field implementation is not complete.

        :param fid: Field Identifier
        :type fid: ``int``
        
        :return: Field definition
        :rtype: ``int``

        :raise ``ValueError``: If the FID is inconsistent for this object
        """
        for field in self.FIELDS:
            if field.getFid() == fid:
                return field
            # end if
        # end for
        raise ValueError(f'Inconsistent FID={fid} for this object!')
    # end def getFieldDefinition

    def getFieldCount(self):
        """
        Obtain the number of fields in the FieldContainerMixin.

        :return: Number of fields
        :rtype: ``int``
        """
        return len(self.FIELDS)
    # end def getFieldCount

    @staticmethod
    def _indentLog(log):
        """
        Increase the indentation of a log.

        :param log: Log
        :type log: ``str``
        
        :return: Re-indented log
        :rtype: ``str``
        """
        return '  ' + log.replace('\n', '\n  ')
    # end def _indentLog

    def create_summary(self, omitName=False, includeData=True):
        """
        Create a summary of the FieldContainerMixin.

        :param omitName: Whether the automatic name should be omitted in the generated string - OPTIONAL
        :type omitName: ``bool``
        :param includeData: Whether the hex data should be included in the generated string - OPTIONAL
        :type includeData: ``bool``
        
        :return: Summary of the FieldContainerMixin
        :rtype: ``str``
        """
        summary_entries = []

        if omitName:
            if includeData:
                summary_entries.append(str(HexList(self)))
            # end if
        else:
            if includeData:
                summary_entries.append(f'{self._name}: 0x{HexList(self)}')
            else:
                summary_entries.append(f'{self._name}: ')
            # end if
        # end if

        if len(self.FIELDS) != 0:
            if self.MODE != self.MODE_RAW:
                present_fields = [field for field in self.FIELDS
                                  if self.hasValue(field.getFid()) or
                                  field.has_default_value() and not field.is_optional(self)]

                log_entries = []
                for field in present_fields:
                    field_summary = field.create_summary()

                    field_value = self.getValue(field.getFid())
                    interpretation = None
                    if hasattr(field_value, 'create_summary'):
                        field_value = field_value.create_summary()
                    # end if

                    # bits case
                    if isinstance(field_value, int):
                        if field_value == 0 and not field.zero_print:
                            continue
                        # end if
                        if (field.get_length() % 8) != 0:
                            field_value = 'b' + format(field_value, '0%db' % (field.get_length())) + f'({field_value})'
                        else:
                            field_value = HexList.fromLong(field_value, None)
                        # end if
                    # end if

                    # bytes case
                    if isinstance(field_value, HexList) and len(field_value) > 0:
                        if to_int(field_value) == 0 and not field.zero_print:
                            continue
                        # end if
                        if field.interpreter is not None and \
                                len(field_value) == 1 and \
                                field_value.toLong() in field.interpreter:
                            interpretation = field.interpreter[field_value.toLong()]
                        # end if
                        field_value = f'0x{field_value}'
                    # end if

                    log_entry = f'- {field_summary} {field_value}'

                    if interpretation is not None:
                        log_entry += f' ({interpretation})'
                    # end if

                    log_entries.append(log_entry)

                    summary_entries.append(self._indentLog(log_entry))
                # end for
            else:
                summary_entries.extend((self._indentLog(f'- {value}') for value in list(self._values.values())))
            # end if
        # end if

        return '\n'.join(summary_entries)
    # end def create_summary
# end class AbstractFieldContainerMixin


class BitFieldContainerMixin(AbstractFieldContainerMixin):
    """
    This class defines the common format of Field Container Mixin
    """

    class _ExternalProperties(defaultdict):
        """
        Class for overriding properties, destined for formatters.
        """

        def __init__(self, default_factory=lambda: None):
            """
            :param default_factory: Default factory for the default dict - OPTIONAL
            :type default_factory: ``callable``
            """
            defaultdict.__init__(self, default_factory)
        # end def __init__

        def __getattr__(self, name):
            """
            Obtain the given attribute

            :param name: Attribute to lookup
            :type name: ``str``

            :return: The attribute
            :rtype: ``object``
            """
            return self[name]
        # end def __getattr__

        def __setattr__(self, name, value):
            """
            Set an attribute by name

            :param name: Name of the attribute to set
            :type name: ``str``
            :param value: Value of the attribute to set
            :type value: ``object``
            """
            self[name] = value
        # end def __setattr__
    # end class _ExternalProperties

    def __init__(self, *args, **kwargs):
        """
        :param args: Positional Parameters
        :type args: ``tuple``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``dict``

        :raise ``AssertionError``: If class doesn't define its MODE behavior at class level
        """
        super(BitFieldContainerMixin, self).__init__()

        assert 'mode' not in kwargs, ValueError(f'class {self.__class__.__name__} must define its MODE behavior at '
                                                f'class level, not in constructor')

        self._values = {}  # A map <fid> -> value
        self._name = self.__class__.__name__

        self._externalProperties = self._ExternalProperties()

        # Handle keyword arguments: Check names against fields
        key_to_ignore = []
        if len(kwargs):
            kw_args_order = {}
            for key in kwargs:
                for index, field in enumerate(self.FIELDS):
                    if (key == field.name) or key in field.aliases:
                        kw_args_order[key] = index
                        break
                    # end if
                else:
                    # Ignore unknown field name
                    key_to_ignore.append(key)
                # end for
            # end for

            for key in key_to_ignore:
                kwargs.pop(key)
            # end for

            for key, value in sorted(list(kwargs.items()), key=lambda x: kw_args_order[x[0]]):
                setattr(self, key, value)
            # end for
        # end if
    # end def __init__

    def __len__(self):
        """
        Give the length of the current FieldContainerMixin

        :return: Length of the FieldContainerMixin
        :rtype: ``int``
        """
        return len(HexList(self))
    # end def __len__

    @classmethod
    def get_total_length(cls):
        """
        Get total length of all the fields of the FieldContainerMixin

        :return: Total length, i.e. the sum of all fields lengths
        :rtype: ``int``
        """
        return sum([field.length for field in cls.FIELDS])
    # end def get_total_length

    def get_field_name(self):
        """
        Get the Name of the FieldContainerMixin.

        :return: Name of the FieldContainerMixin
        :rtype: ``str``
        """
        return self._name
    # end def get_field_name

    def set_field_name(self, name):
        """
        Set the Name of the FieldContainerMixin.

        :param name: Name of the FieldContainerMixin
        :type name: ``str``

        :raise ``TypeError``: If the name is not a string
        """
        if not isinstance(name, str):
            raise TypeError(f"Wrong Name type: {type(name).__name__}. Should be a str")
        # end if

        self._name = name
    # end def set_field_name

    name = property(get_field_name, set_field_name)

    def getField(self, index):
        """
        Get a field in the fields list by its index.

        :param index: Field index
        :type index: ``int``
        
        :return: Field value
        :rtype: ``Field``
        """
        return self.FIELDS[index]
    # end def getField

    def get_field_from_name(self, name):
        """
        Get first field matching name

        :param name: Name of the field
        :type name: ``str``

        :return: Field matching the name
        :rtype: ``Field``
        """
        return self.getFieldDefinition(self.getFidFromName(name))
    # end def get_field_from_name

    def setValue(self, fid, value):
        """
        Set the field value for a given FID.

        :param fid: Field Identifier
        :type fid: ``int``
        :param value: Value of the field
        :type value: ``object``
        """
        field = self.getFieldDefinition(fid)  # Check for definition
        field.check_value(value, self)  # Value consistency check
        value = field.convert_value(value, self)  # Rich type conversion
        if isinstance(value, int):
            if (field.length % 8) == 0 and field.length != 0:
                value = HexList.fromLong(value, field.length // 8)
            # end if
        # end if
        self._values[fid] = value
    # end def setValue

    def getValue(self, fid, use_default_value=True):
        """
        Get the field value for a given FID.

        :param fid: Field Identifier
        :type fid: ``int``
        :param use_default_value: Whether to use the default value if no value is supplied - OPTIONAL
        :type use_default_value: ``bool``

        :return: The value or default value of the field
        :rtype: ``object``
        """
        # Get the definition
        field = self.getFieldDefinition(fid)
        # Handle default value
        if not self.hasValue(fid) and use_default_value:
            value = field.get_default_value(self)
        else:
            value = self._values.get(fid, None)
        # end if
        return value
    # end def getValue

    def hasValue(self, fid):
        """
        Check presence of value.

        :param fid: Field Identifier
        :type fid: ``int``

        :return: True if value not None
        :rtype: ``bool``
        """
        return self._values.get(fid, None) is not None
    # end def hasValue

    def getFidFromName(self, name):
        """
        Get fid of a field from its name

        :param name: Name of the field
        :type name: ``str``
        
        :return: fid value
        :rtype: ``int``
        """
        return [f.getFid() for f in self.FIELDS if f.name == name][0]
    # end def getFidFromName

    def _debug(self):
        """
        Get the field names for debug.

        :return: The name of the Field with their associated value
        :rtype: ``dict``
        """
        result = {}
        for field in self.FIELDS:
            result[field.name] = self._values[field.fid]
        # end for
        return result
    # end def _debug

    debug = property(_debug)

    def get_default_value(self, fid):
        """
        Get the field default value for a given FID.

        :param fid: Field Identifier
        :type fid: ``int``
        
        :return: The default value of the field
        :rtype: ``object``
        """
        field = self.getFieldDefinition(fid)
        return field.get_default_value(self)
    # end def get_default_value

    def __getattr__(self, name):
        """
        Implement quick access to a field's contents.

        :param name: Name of the attribute to obtain
        :type name: ``str``
        
        :return: The attribute contents
        :rtype: ``object``

        :raise ``AttributeError``: If the attribute is not found
        """
        for field in self.FIELDS:
            if (field.name.upper() == name.upper()) or (name in field.aliases):
                return self.getValue(field.getFid())
            # end if
        # end for

        # Handle the case where the user called get<AttributeName>
        if name.startswith('get'):
            # Extract <AttributeName>
            attr_name = name[3:]

            if attr_name[0].isupper():
                attr_name = attr_name[0].lower() + attr_name[1:]

                # Create a local callback, that will be used to request the attribute value.
                def getter():
                    """
                    Inner getter for the dynamically generated attribute

                    :return: The value for the attribute extracted from the getter name
                    :rtype: ``object``
                    """
                    return getattr(self, attr_name)

                # end def getter

                return getter
            # end if
        elif name.startswith('set'):
            # Extract <AttributeName>
            attr_name = name[3:]

            if attr_name[0].isupper():
                attr_name = attr_name[0].lower() + attr_name[1:]

                # Create a local callback, that will be used to request the attribute value.
                def setter(value):
                    """
                    Inner setter for the dynamically generated attribute

                    :param value: Value to set
                    :type value: ``object``
                    """
                    for field_ in self.FIELDS:
                        if (field_.name.upper() == attr_name.upper()) or (attr_name in field_.aliases):
                            self.setValue(field_.getFid(), value)
                            break
                        # end if
                    else:
                        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr_name}'")
                    # end for

                # end def setter

                return setter
            # end if
        # end if

        if name == 'externalProperty':
            return self.getExternalProperty(name)
        # end if

        raise AttributeError(f'{self.__class__.__name__} has no attribute {name}')
    # end def __getattr__

    def __setattr__(self, name, value):
        """
        Implement quick access to a field's contents.

        :param name: Name of the attribute to set
        :type name: ``str``
        :param value: Value of the attribute to be set
        :type value: ``object``

        :raise ``AttributeError``: If the attribute is not found
        """
        lower_name = name.lower()
        for field in self.FIELDS:
            if field.acceptable(name):
                self.setValue(field.getFid(), value)
                break
            elif field.confusing(lower_name):
                raise AttributeError(f'Attribute {name} is probably mistaken with {field.name}')
            # end if
        else:
            object.__setattr__(self, name, value)
        # end for
    # end def __setattr__

    def getExternalProperties(self):
        """
        Obtain value of external property dict

        :return: Property value if found, None else
        :rtype: ``object`` or ``None``
        """
        return self._externalProperties
    # end def getExternalProperties

    externalProperties = property(getExternalProperties)

    @staticmethod
    def _bitListToHexList(bitList):
        """
        Convert list of (bitLength, value) into HexList

        :param bitList: List of (bitLength, value)
        :type bitList: ``list``

        :return: HexList representation of bitList
        :rtype: ``HexList``

        :raise ``TypeError``: If the element type is not supported
        :raise ``ValueError``: If the value is out of bound
        """
        result = HexList()
        acc_count = 0
        acc_value = 0
        element = None
        for element in bitList:
            if isinstance(element, HexList):
                if acc_count > 0:
                    result.append(acc_value << (8 - acc_count))
                    acc_count = 0
                    acc_value = 0
                # end if
                result.extend(element)
                continue
            elif isinstance(element, (tuple, list)):
                bit_count, value = element
                if hasattr(value, 'toLong'):
                    value = value.toLong()
                # end if
            else:
                raise TypeError('Unsupported element type: %s'
                                % type(element).__name__)
            # end if
            if not (0 <= value < (1 << bit_count)):
                raise ValueError('Out of bound value: %s. Max value: %d' % (value, (1 << bit_count)))
            # end if
            acc_count += bit_count
            acc_value = (acc_value << bit_count) | value

            while acc_count > 8:
                result.append(acc_value >> (acc_count - 8))
                acc_count -= 8
                acc_value = acc_value & ((1 << acc_count) - 1)
            # end while
        # end for

        while acc_count > 8:
            result.append(acc_value >> (acc_count - 8))
            acc_count -= 8
            acc_value = acc_value & ((1 << acc_count) - 1)
        # end while

        # Rest of the elements
        if acc_count > 0:
            result.append(acc_value << (8 - acc_count))
        # end if

        return result

    # end def _bitListToHexList

    def _toHex(self, field, value):
        """
        Convert a value to HexList, using the field definition.

        :param field: Field type to convert
        :type field: ``Field`` or ``ArrayField``
        :param value: Value to convert
        :type value: ``object``

        :return: The converted value
        :rtype: ``HexList``

        :raise ``AssertionError``: If the value is too long to fit in one byte or if the field is not optional
        """
        hex_field = HexList()

        if value is not None or not field.is_optional(self):

            # Convert the value to HexList: This will be useful later.
            if not isinstance(value, HexList):
                if isinstance(value, int):
                    value = HexList.fromLong(value, field.get_length(container=self))
                else:
                    value = HexList(value)
                # end if
            # end if

            if hasattr(field, '__hexlist__'):
                hex_field.appendRaw(HexList(field))

            else:
                # FID
                if field.get_has_tag(self):
                    assert (field.fid >= 0), \
                        ValueError(f'{self.__class__.__name__}.{field.name} defines both has_tag and an internal tag.')
                    hex_field.appendRaw(field.fid)
                # end if

                # Length
                if field.variable:
                    length = len(value)
                    assert (len(value) < 256), ValueError('Value is length great to fit in one byte')
                    hex_field.appendRaw(length)
                # end if
            # end if

            # Value
            hex_field.extendRaw(value)
        # end if

        return hex_field
    # end def _toHex

    def get_hex_field(self, field):
        """
        Convert the field object to its HexList representation.

        :param field:  Field object to convert
        :type field: ``Field``
        
        :return: Representation of field
        :rtype: ``HexList``
        """
        value = self.getValue(field.fid)
        if isinstance(field, ArrayField):
            values = value
            hex_field = HexList()
            hex_field.extend([self._toHex(field, value) for value in values])
        else:
            hex_field = self._toHex(field, value)
        # end if

        return hex_field
    # end def get_hex_field

    def to_bit_list(self):
        """
        Convert the field object to its (bitLength, value) representation.

        :return: Representation of field
        :rtype: ``list``
        """
        result = []

        for field in self.FIELDS:
            if self.hasValue(field.getFid()) or (not field.is_optional(self)):
                if isinstance(field, Field):
                    result.append(self.get_hex_field(field))
                    continue
                # end if
                value = self.getValue(field.fid)
                if isinstance(value, bool):
                    value = 1 if value else 0
                # end if
                bit_list = field.to_bit_list()
                if (field.len_length != 0) and (field.length == 0):
                    bit_list[-1][-1] = len(HexList(value))
                # end if
                if value is not None:
                    if hasattr(field, 'serializer'):
                        bit_list.append(field.serializer(value))
                    elif hasattr(value, 'to_bit_list'):
                        bit_list.extend(value.to_bit_list())
                    elif isinstance(value, HexList):
                        bit_list.append(value)
                    elif isinstance(value, (BitStruct, ArrayField.ArrayWrapper)):
                        bit_list.append(HexList(value))
                    elif isinstance(value, list) and (bit_list == []):
                        bit_list.append(HexList(value))
                    elif isinstance(value, list) and (value == []):
                        value = None
                    elif isinstance(value, list) and (bit_list[-1][1] is None):
                        # List of bit fields of unknown length
                        list_len = 0
                        sub_list = []
                        for val in value:
                            sub_list2 = val.to_bit_list()
                            if isinstance(sub_list2[0], int):
                                list_len += sub_list2[0]
                            else:
                                for lst in sub_list2:
                                    list_len += lst[0]
                                # end for
                            # end if
                            sub_list.extend(sub_list2)
                        # end for
                        bit_list[-1][1] = list_len
                        bit_list.extend(sub_list)
                    else:
                        if not isinstance(value, int):
                            value = HexList(value)
                        # end if
                        if not field.variable:
                            bit_list.append([field.get_length(), value])
                        else:
                            bit_list.append(value)
                        # end if
                    # end if
                # end if
                result.extend(bit_list)
            # end if
        # end for

        return result
    # end def to_bit_list

    def __hexlist__(self):
        """
        Convert the current object to its HexList representation.

       :return: HexList representation of the BitFieldContainerMixin
       :rtype: ``HexList``
        """
        bit_list = self.to_bit_list()

        data = self._bitListToHexList(bit_list)

        return data
    # end def __hexlist__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parsing from HexList instance

        @note   expected parameters:
                - data (HexList) data to parser
                - offset (int) Offset (in bits) of value to parse in data
                - length (int) Length (in bits) of value to parse in data

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Dictionary of arguments
        :type kwargs: ``dict``

        :return: Parsed object
        :rtype: ``FieldContainerMixin``
        """
        data = None
        offset = 0
        length = None
        if len(kwargs):
            if 'data' in kwargs:
                data = kwargs['data']
            # end if
            if 'offset' in kwargs:
                offset = kwargs['offset']
            # end if
            if 'length' in kwargs:
                length = kwargs['length']
            # end if
        # end if

        if len(args) in range(4):
            if len(args) > 0:
                data = args[0]
            # end if
            if len(args) > 1:
                offset = args[1]
            # end if
            if len(args) > 2:
                length = args[2]
            # end if
        else:
            data = args[2]
            offset = args[3]
            length = args[4] - offset
        # end if
        if length == 0:
            return offset, None
        # end if

        limit = offset + length if length is not None else len(data) * 8

        class InnerFieldContainerMixin(cls):  # pylint:disable=W0223
            """
            Inner class used to obtain the FIELDS of the Record
            """

            def __init__(self):
                BitFieldContainerMixin.__init__(self)
            # end def __init__

        # end class InnerFieldContainerMixin

        InnerFieldContainerMixin.__name__ = cls.__name__
        inner_field_container_mixin = InnerFieldContainerMixin()

        for field in inner_field_container_mixin.FIELDS:
            if isinstance(field, Field):
                # Adjustment of offset after handling of Field instead of BitField
                offset //= 8
                limit //= 8
                offset, value = field.fromHexList(inner_field_container_mixin, data, offset, limit)
                offset *= 8
                limit *= 8

            else:
                offset, value = field.fromHexList(inner_field_container_mixin, data, offset, limit)
            # end if

            if value is not None:
                inner_field_container_mixin.setValue(field.getFid(), value)
            # end if
        # end for

        if len(args) in range(4):
            return inner_field_container_mixin
        else:
            return offset, inner_field_container_mixin
        # end if
    # end def fromHexList

    def __eq__(self, other):
        """
        Test the equality of a FieldContainerMixin with other.

        :param other: Other FieldContainerMixin instance
        :type other: ``FieldContainerMixin``

        :return: Comparison result
        :rtype: ``bool``

        :raise ``TypeError``: If the other object is not a FieldContainerMixin
        """
        if not isinstance(other, BitFieldContainerMixin):
            raise TypeError("Other should be of type BitFieldContainerMixin")
        # end if

        self_field_ids = [field.fid for field in self.FIELDS]
        other_field_ids = [field.fid for field in other.FIELDS]

        result = (self_field_ids == other_field_ids)

        if result:
            for fid in self_field_ids:
                value1 = self.getValue(fid)
                value2 = other.getValue(fid)
                result = (value1 == value2)
                if not result:
                    break
                # end if
            # end for
        # end if

        return result
    # end def __eq__

    def __ne__(self, other):
        """
        Test the difference between FieldContainerMixin and other.

        :param other: Other FieldContainerMixin instance
        :type other: ``FieldContainerMixin``

        :return: Comparison result
        :rtype: ``bool``
        """
        return not (self == other)
    # end def __ne__

    def __str__(self):
        """
        Obtain a string representation of FieldContainerMixin.

        :return: String representation
        :rtype: ``str``
        """
        return str(self.create_summary())
    # end def __str__

    def __repr__(self):
        """
        Obtain a python string representation of BitFieldContainerMixin.

        :return: Python string representation
        :rtype: ``str``
        """
        params = []
        for field in self.FIELDS:
            name = field.name
            if self.hasValue(field.fid):
                value = self.getValue(field.fid, use_default_value=False)
            else:
                value = None
            # end if
            params.append((name, value))
        # end for

        result = f'{self.__class__.__name__}('
        first = True
        for name, value in sorted(params):
            if not first:
                result += ', '
            else:
                first = False
            # end if

            result += f'{name}={value!r}'
        # end for

        result += ')'

        return result
    # end def __repr__

    def getFieldOffset(self, fid):
        """
        Give the offset of a field in the FieldContainerMixin.

        The offset is computed from the 1st byte

        :param fid: Field Identifier
        :type fid: ``int``
        
        :return: Offset of the field
        :rtype: ``int``

        :raise ``TypeError``: If the field is not found
        """
        offset = 0

        if isinstance(fid, str):
            for field in self.FIELDS:
                if field.name == fid:
                    fid = field.fid
                    break
                # end if
            # end for
        # end if

        # Skip field preceding the given field
        for field in self.FIELDS:
            field_fid = field.fid
            field_has_default_value = field.has_default_value()
            field_has_value = self.hasValue(field_fid)
            field_is_optional = field.is_optional(self)

            if field_has_value or field_has_default_value:
                if field.has_tag:
                    offset += field._fid_length
                # end if

                if field.variable:
                    offset += field._len_length
                # end if
            # end if

            # This is the field we are looking for
            if field_fid == fid:
                return offset

            elif field_has_value or field_has_default_value:
                length = field.get_length(self)
                if length is None:
                    length = len(HexList(self.getValue(field.fid)))
                # end if

                offset += length

            elif not field_is_optional:
                pass
            # end if
        # end for

        raise TypeError(f"Field of FID: 0x{fid:02X} not found in FieldContainerMixin: {self}")
    # end def getFieldOffset

    def copy(self):
        """
        Create of copy of self

        :return: Copy of self
        :rtype: ``BitFieldContainerMixin``
        """
        result = self.__class__()

        for field in self.FIELDS:
            result.__setattr__(field.name, self.getValue(field.fid))
        # end for

        return result
    # end def copy

    #     @classmethod
    #     def accept(cls, data,
    #                     offset = 0,
    #                     limit  = None):
    #         """
    #         Check if the HexList data are interpretable by self
    #
    #         @param  data      [in] (HexList) Data to interpret
    #         @option offset    [in] (int) The offset in the HexList at which to start parsing
    #         @option limit     [in] (int) Max length of data to parse
    #
    #         @return (bool) True if data is interpretable
    #         """
    #         if (offset == limit):
    #             return False
    #         # end if
    #
    #         limit = limit if limit is not None else len(data) * 8
    #
    #         result = False
    #
    #         # Check of the end of the buffer to analyze
    #         if (offset < limit):
    #             offsetTmp = offset // 8
    #             if (cls.TAG is not None):
    #                 tag = data[offsetTmp]
    #                 result = (cls.TAG == tag)
    #                 offsetTmp += 1
    #             # end if
    #
    #             if (result):
    #                 if (cls.VARIABLE is not None):
    #                     result = len(data[offsetTmp:]) >= 1
    #                 # end if
    #             # end if
    #         # end if
    #         return result
    #     # end def accept

    @classmethod
    def acceptTrue(cls, data, offset=0, limit=None):
        """
        Accept all data

        :param data: Data to interpret - OPTIONAL
        :type data: ``HexList``
        :param offset: The offset in the HexList at which to start parsing - OPTIONAL
        :type offset: ``int``
        :param limit: Max length of data to parse - OPTIONAL
        :type limit: ``int``

        :return: True if data is interpretable
        :rtype: ``bool``
        """
        return True
    # end def acceptTrue


# end class BitFieldContainerMixin


class TimestampedBitFieldContainerMixin(BitFieldContainerMixin):
    """
    This class defines the common format of Field Container Mixin with a timestamp
    """

    def __init__(self, timestamp=None, *args, **kwargs):
        """
        :param timestamp: Timestamp of the structure - OPTIONAL
        :type timestamp: ``int``
        :param args: Positional arguments
        :type args: ``tuple``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        super().__init__(*args, **kwargs)

        self.timestamp = timestamp if timestamp is not None else perf_counter_ns()
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        # See ``BitFieldContainerMixin.fromHexList``
        to_return = super(TimestampedBitFieldContainerMixin, cls).fromHexList(*args, **kwargs)

        if 'timestamp' in kwargs:
            to_return.timestamp = kwargs['timestamp']
        else:
            to_return.timestamp = perf_counter_ns()
        # end if

        return to_return
    # end def fromHexList

    def __str__(self):
        # See ``BitFieldContainerMixin.__str__``
        to_return = super().__str__()
        if self.timestamp is not None:
            to_return += f"\nat {self.timestamp / TIMESTAMP_UNIT_DIVIDER_MAP[TIMESTAMP_UNIT]:.2f}{TIMESTAMP_UNIT}\n"
        # end if
        return to_return
    # end def __str__

    def __repr__(self):
        # See ``BitFieldContainerMixin.__repr__``
        to_return = super().__repr__()
        to_return += f"\nat {self.timestamp / TIMESTAMP_UNIT_DIVIDER_MAP[TIMESTAMP_UNIT]:.2f}{TIMESTAMP_UNIT}\n"
        return to_return
    # end def __repr__

    def copy(self):
        # See ``BitFieldContainerMixin.copy``
        to_return = super().copy()
        to_return.timestamp = self.timestamp
        return to_return
    # end def copy

    def light_str(self):
        """
        Get a light representation of the ``TimestampedBitFieldContainerMixin`` object

        :return: Object name, ``HexList`` representation and optionally the timestamp
        :rtype: ``str``
        """
        to_return = f'{self._name}: 0x{HexList(self)}'
        if self.timestamp is not None:
            to_return += f"\nat {self.timestamp / TIMESTAMP_UNIT_DIVIDER_MAP[TIMESTAMP_UNIT]:.2f}{TIMESTAMP_UNIT}\n"
        # end if
        return to_return
    # end def light_str


# end class TimestampedBitFieldContainerMixin


class BitFieldContainerMixinList(list):
    """
    List of BitFieldContainerMixin
    """

    def __init__(self, *containers):
        """
        :param containers: List of BitFieldContainerMixin
        :type containers: ``list``
        """
        super(BitFieldContainerMixinList, self).__init__(containers)
        self.refClasses = []
        self.variable = False
    # end def __init__

    def register(self, containerClass):
        """
        Register a BitFieldContainerMixin implementation of given type

        :param containerClass: BitFieldContainerMixin implementation
        :type containerClass: ``object``
        """
        self.refClasses.append(containerClass)
    # end def register

    def accept(self, data, offset=0, limit=None):
        """
        Check if the HexList data are interpretable by self

        :param data: Data to interpret
        :type data: ``HexList``
        :param offset: The offset in the HexList at which to start parsing - OPTIONAL
        :type offset: ``int``
        :param limit: Max length of data to parse - OPTIONAL
        :type limit: ``int``

        :return: True if data is interpretable
        :rtype: ``bool``
        """
        for containerClass in self.refClasses:
            if containerClass.accept(data, offset, limit):
                return True
            # end if
        # end for
        return False
    # end def accept

    @classmethod
    def acceptTrue(cls, data, offset=0, limit=None):
        """
        Accept all data

        :param data: Data to interpret - OPTIONAL
        :type data: ``HexList``
        :param offset: The offset in the HexList at which to start parsing - OPTIONAL
        :type offset: ``int``
        :param limit: Max length of data to parse - OPTIONAL
        :type limit: ``int``

        :return: True if data is interpretable
        :rtype: ``bool``
        """
        return True
    # end def acceptTrue

    @classmethod
    def fromHexList(cls, container, bitField, data, offset=0, limit=None, exceptOnOverflow=True):
        """
        Parse data to interpret as list of descriptor

        :param container: The object that contains the field
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

        :return: List of interpreted descriptors
        :rtype: ``list``
        """
        if offset == limit:
            return offset, None
        # end if

        if limit is None or bitField.variable:
            if bitField.variable:
                length = getElement(data, offset, bitField._len_length)
                offset += bitField._len_length
            else:
                length = bitField.get_length(container,
                                             data,
                                             offset=offset,
                                             length=limit - offset)
            # end if
            limit = offset + length * 8
        # end if

        if offset == limit:
            return offset, None
        # end if

        descriptor_list = cls()
        value = None
        if descriptor_list.accept(data, offset, limit):
            offset, value = descriptor_list.parseRefClasses(
                container, data, offset, limit, exceptOnOverflow)
            value.variable = bitField.variable
        # end if

        return offset, value
    # end def fromHexList

    def parseRefClasses(self, container, data, offset=0, limit=None, exceptOnOverflow=True):
        """
        Parse a field from HexList format

        :param container: The object that contains the field
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
        :rtype: ``BitField`` or ``offset``
        """
        result = self.__class__()
        while offset < limit:
            for containerClass in self.refClasses:
                if containerClass.accept(data, offset, limit):
                    container_instance = containerClass.fromHexList(data, offset, limit - offset)
                    result.append(container_instance)
                    offset += len(container_instance) * 8
                    break
                # end if
            else:
                raise ValueError(f'No parser found for data: {data[offset // 8:]}')
            # end for
        # end while
        return offset, result
    # end def parseRefClasses

    def __hexlist__(self):
        """
        Convert self into HexList

        :return: HexList representation of self
        :rtype: ``HexList``
        """
        result = HexList()
        for container in self:
            result.extend(HexList(container))
        # end for

        return result

    # end def __hexlist__

    @staticmethod
    def _indentLog(log):
        """
        Increase the indentation of a log.

        :param log: Log
        :type log: ``str``

        :return: Re-indented log
        :rtype: ``str``
        """
        log_table = log.split('\n')
        return '\n'.join(["  " + line for line in log_table])
    # end def _indentLog

    def create_summary(self):
        """
        Create a summary of the command.

        :return: Summary of the command
        :rtype: ``str``
        """
        log = ''
        if self.variable:
            log += ' Length: 0x%02.2X' % len(HexList(self))
        # end if
        log += '\n  [\n'
        log += self._indentLog('\n'.join(['- %s' % cont.create_summary() for cont in self]))

        return log + '\n  ]'
    # end def create_summary

    def __str__(self):
        """
        Obtain a string representation of FieldContainerMixin.

        :return: String representation
        :rtype: ``str``
        """
        return str(self.create_summary())
    # end def __str__

    def extendRaw(self, *seq):
        """
        Extend the current object, using the RAW supplied data.

        :param seq: Sequence of bytes to extend the object with
        :type seq: ``list``
        """
        list.extend(self, *seq)
    # end def extendRaw

    def __getslice__(self, i, j):
        """
        Get some elements of Descriptor list

        :param i: Index of first element to get
        :type i: ``int``
        :param j: Index of element following last element to get
        :type j: ``int``

        :return: Elements of Descriptor list
        :rtype: ``object``
        """
        result = self.__class__()
        result.extendRaw(list.__getslice__(self, i, j))
        return result
    # end def __getslice__

    def __getitem__(self, key):
        """
        Extract an element of DescriptorList

        :param key: Index of the element to extract
        :type key: ``int``

        :return: Extracted element
        :rtype: ``object``
        """
        result = super(BitFieldContainerMixinList, self).__getitem__(key)

        if type(result) is list:
            value = HexList()
            value.extendRaw(result)
            result = value
        # end if

        return result
    # end def __getitem__

    def __setitem__(self, i, value):
        """
        Update of an element of HexList

        :param i: Index of the element to update
        :type i: ``int``
        :param value: Element to put in HexList
        :type value: ``int``
        """
        if i < 0:
            i += len(self)
        # end if

        if not isinstance(value, BitFieldContainerMixinList):
            value = BitFieldContainerMixinList(value)
        # end if

        list.__setslice__(self, i, i + 1, value)
    # end def __setitem__

    def to_bit_list(self):
        """
        Convert the field object to its (bitLength, value) representation.

        :return: Representation of field
        :rtype: ``list``
        """
        result = []
        for cont in self:
            cont_bit_list = []
            cont_bit_list.extend(cont.to_bit_list())

            result.extend(cont_bit_list)
        # end for

        return result
    # end def to_bit_list
# end class BitFieldContainerMixinList


def remainingDataFromHexList(container, bitField, data, offset=0, limit=None, exceptOnOverflow=True):
    """
    Try to get the remaining data for the last field of BitFieldContainer

    :param container: The object that contains the field
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
    :rtype: ``BitField`` or ``offset``

    :raise ``AssertionError``: If the length is not 0
    :raise ``IndexError``: If the data is not enough to parse the field
    """
    assert bitField.len_length == 0
    if hasattr(container, 'LENGTH'):
        length = container.LENGTH * 8
    else:
        if limit is None:
            length = len(data[offset // 8:]) * 8
        else:
            length = len(data[offset // 8: limit // 8]) * 8
        # end if
    # end if
    other_field_length = len(HexList(container)) - 1

    length -= other_field_length * 8

    if length == 0:
        return offset, None
    # end if

    if limit is not None:
        if (offset + length > limit) and exceptOnOverflow:
            raise IndexError(
                f'Overflow, remaining data: {data[offset // 8:limit // 8]}, length expected: {length // 8}.')
        # end if
    # end if

    if length % 8 == 0:
        value = data[offset // 8: (offset + length) // 8]
    else:
        value = getElement(data, offset, length)
    # end if
    bitField.set_length(length)
    return offset + length, value
# end def remainingDataFromHexList

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
