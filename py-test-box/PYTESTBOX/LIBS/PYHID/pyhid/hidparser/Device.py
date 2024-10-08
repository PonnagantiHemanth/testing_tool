#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package pyhid.hidparser.device

@brief  HID parser device class

@author christophe Roquebert

@date   2019/01/24
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidparser.enums import CollectionType, ReportType, ReportFlags, UnitSystem
from pyhid.hidparser.UsagePage import UsagePage, UsageType
from pyhid.hidparser.helper import ValueRange

from copy import copy as _copy
from functools import partial as _partial
from bitstring import BitArray as _BitArray
from warnings import warn

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class Unit:
    """
    Unit for Report values.

    Attributes:
        system (UnitSystem): The system used when interpreting the
    """
    NOT_SPECIFIED = 0x00
    LUX = 0x010000E1
    KELVIN = 0x00010001
    FAHRENHEIT = 0x00010003
    PASCAL = 0xE1F1
    NEWTON = 0xE111
    METERS_PER_SECOND = 0xF011
    METERS_PER_SEC_SQRD = 0xE011
    FARAD = 0x00204FE1
    AMPERE = 0x00100001
    WATT = 0xD121
    HENRY = 0x00E0E121
    OHM = 0x00E0D121
    VOLT = 0x00F0D121
    HERTZ = 0xF001
    DEGREES = 0x14
    DEGREES_PER_SECOND = 0xF014
    DEGREES_PER_SEC_SQRD = 0xE014
    RADIANS = 0x12
    RADIANS_PER_SECOND = 0xF012
    RADIANS_PER_SEC_SQRD = 0xE012
    SECOND = 0x1001
    GAUSS = 0x00F0E101
    GRAM = 0x0101
    CENTIMETER = 0x11

    _map_nibble_exponent = {
        0x0: 0, 0x1:1, 0x2: 2, 0x3: 3, 0x4: 4, 0x5: 5, 0x6: 6, 0x7: 7,
        0x8: -8, 0x9: -7, 0xA: -6, 0xB: -5, 0xC: -4, 0xD: -3, 0xE: -2, 0xF: -1
    }

    def __init__(self):
        self.system = UnitSystem.NONE
        self.length = 0
        self.mass = 0
        self.time = 0
        self.temperature = 0
        self.current = 0
        self.luminosity = 0

    @classmethod
    def from_bytes(cls, data: bytes):
        unit = Unit()
        unit.system = UnitSystem(data[0]&0x0F)
        unit.length = cls._map_nibble_exponent[(data[0] & 0xF0) >> 4]
        if len(data) > 1:
            unit.mass = cls._map_nibble_exponent[data[1] & 0x0F]
            unit.time = cls._map_nibble_exponent[(data[1] & 0xF0) >> 4]
        if len(data) > 2:
            unit.temperature = cls._map_nibble_exponent[data[2] & 0x0F]
            unit.current = cls._map_nibble_exponent[(data[2] & 0xF0) >> 4]
        if len(data) > 3:
            unit.luminosity = cls._map_nibble_exponent[data[3] & 0x0F]


class Report:
    def __init__(
            self,
            report_type: ReportType,
            report_id: int = 0,
            usages=[],
            designators=None,
            strings=None,
            size: int=0,
            count: int=0,
            logical_range=None,
            physical_range=None,
            unit=None,
            exponent=1,
            flags=None,
            parent=None
    ):
        self.report_id = report_id
        self.report_type = report_type
        self.size = size
        self.count = count
        self.designators = designators if designators is not None else range(0)
        self.strings = strings if strings is not None else range(0)
        if type(logical_range) in (list, tuple):
            logical_range = ValueRange(*logical_range)
        if type(physical_range) in (list, tuple):
            physical_range = ValueRange(*physical_range)
        self.logical_range = logical_range if logical_range is not None else ValueRange() # type: ValueRange
        self.physical_range = physical_range if physical_range is not None else _copy(self.logical_range) # type: ValueRange

        self.unit = unit if unit is not None else Unit()
        self.unit_exponent = exponent

        if type(usages) not in (list, tuple):
            usages = (usages,)
        self.usages = usages

        self.flags = flags

        self.parent = parent
        self._values = [0]*self.count if self.count>0 else [0]

    @property
    def bits(self):
        return self.size * self.count

    @property
    def value(self):
        if self.count>1:
            if self.logical_range == self.physical_range:
                return [int(value) for value in self._values]
            return self._values
        if self.logical_range == self.physical_range:
            return int(self._values[0])
        return self._values[0]

    @value.setter
    def value(self, value):
        if self.count > 1:
            if type(value) is not list:
                raise ValueError("Can not set {} to {}".format(type(value), self.__class__.__name__))
            if len(value) != self.count:
                raise ValueError("Value must be of length {}".format(self.count))
            self._values = value
        else:
            if not self.physical_range.in_range(value):
                raise ArithmeticError("{} is not within physical range".format(value))
            self._values[0] = value

    def __getitem__(self, key):
        if self.logical_range == self.physical_range:
            return int(self._values[key])
        return self._values[key]

    def __setitem__(self, key, value):
        self._values[key] = value

    # TODO print out more meaningful information about this Report
    def __str__(self, index=0):
        result = "{}Report (size: {}, count: {})\n{}".format("  " * index, self.size, self.count,"  " * (index + 1))
        if self.flags & ReportFlags.CONSTANT:
            return result + "(Constant)"
        return result + ", ".join([usage._name_ for usage in self.usages])

    def pack(self):
        values = _BitArray(self.count*self.size)
        for i in range(self.count):
            offset = i * self.size
            try:
                values[offset:offset + self.size] = int(self.physical_range.scale_to(self.logical_range, self._values[i]))
            except ArithmeticError:
                # If the value is outside of the physical range, and NULLs are allowed, then do not modify the value
                if not self.flags & ReportFlags.NULL_STATE:
                    raise
        return values

    def unpack(self, data):
        big_endian_data = _BitArray()
        if not isinstance(data, _BitArray):
            data = _BitArray(data)
        for i in range(self.count):
            offset = i*self.size
            try:
                b = data[offset:offset + self.size]
                if self.size > 1:
                    # Call the reverse method available in bitstring v4.0.2 & v4.1.1
                    # NB: the _reverse method was removed in bitstring v4.1.1
                    b.reverse()
                # end if
                big_endian_data.append(b)
                self._values[i] = self.logical_range.scale_to(self.physical_range, b.int if self.logical_range.minimum<0 else b.uint)
            except ArithmeticError:
                # If the value is outside the logical range, NULLs are allowed and not an ARRAY,
                # then do not modify the value
                if (not self.flags & ReportFlags.NULL_STATE) and (b.int != 0):
                    raise
        return big_endian_data


class Collection:
    def __init__(self, items=None, usage=None, allowed_usage_types=None, collection_type: CollectionType=None, parent: "Collection"=None):
        if allowed_usage_types is None:
            allowed_usage_types = UsageType.collection_usage_types()
        if isinstance(allowed_usage_types, UsageType):
            allowed_usage_types = (allowed_usage_types,)
        elif type(allowed_usage_types) not in (list, tuple):
            raise ValueError("usage types must be a UsageType or a list or tuple of UsageType")

        self.collection_type = collection_type
        self._usage_types = allowed_usage_types
        self._usage = usage
        self.items = []  # type: _List[_Union[Collection, Report]]
        self._attrs = {}

        # _parent either refers to the collection it's nested in, or the collection it's derrived from
        # i.e. collections in ReportGroup.input are derrived from the collections in the Device object
        self.parent = parent

        if items is not None:
            if type(items) not in (list, tuple):
                items = [items]
            for item in items:
                self.append(item)

    @property
    def bits(self):
        # TODO Cache the total bit size, and invalidate when a child Collection or Report is added somewhere in the tree
        return sum([item.bits for item in self.items])

    def get_bit_size(self, report_type: ReportType):
        size = 0
        for item in self.items:
            if isinstance(item, Report):
                if item.report_type == report_type:
                    size += item.bits
            else:
                size += item.get_bit_size(report_type)
        return size

    def get_size(self, report_type: ReportType):
        bits = self.get_bit_size(report_type)
        # Get the result of an integer division
        return ((bits - 1) // 8) + 1

    def deserialize(self, data, report_type: ReportType):
        offset = 0
        big_endian_data = _BitArray()
        if not isinstance(data, _BitArray):
            data = _BitArray(data)
        for item in self.items:
            if isinstance(item, Report):
                if item.report_type is not report_type:
                    continue
                big_endian_data.append(item.unpack(data[offset:offset + item.bits]))
            else:
                big_endian_data.append(item.deserialize(data[offset:offset + item.bits], report_type))
            offset += item.bits
        return big_endian_data

    def serialize(self, report_type: ReportType) -> bytes:
        data = _BitArray()
        for item in self.items:
            if isinstance(item, Report):
                if item.report_type is not report_type:
                    continue
                data.append(item.pack())
            else:
                data.append(item.serialize(report_type))
        return data

    def append(self, item):
        if isinstance(item, Collection):
            self.items.append(item)
            if item._usage is not None:
                self._add_to_attr(item._usage._name_.lower(), item)
        elif isinstance(item, UsagePage):
            if not [usage_type for usage_type in item.usage_types if usage_type in self._usage_types]:
                raise ValueError()
            collection = Collection(usage=item)
            self.items.append(collection)
            self._add_to_attr(item._usage._name_.lower(), collection)
        elif isinstance(item, Report):
            if len(item.usages)>0:
                for usage in item.usages:
                    self._add_to_attr(usage._name_.lower(), property(
                        fget=_partial(item.__getitem__, item.usages.index(usage)),
                        fset=_partial(item.__setitem__, item.usages.index(usage))
                    ))
            self.items.append(item)
        else:
            raise ValueError("usage type is not UsagePage or Report")

    def _add_to_attr(self, key, item):
        if key in self._attrs.keys():
            if type(self._attrs[key]) is not list:
                self._attrs[key] = [self._attrs[key]]
            self._attrs[key].append(item)
        else:
            self._attrs[key] = item

    def extend(self, items):
        for item in items:
            self.append(item)

    def __getitem__(self, item) -> "Collection":
        return self.items[item]

    def __getattr__(self, item) -> "Collection":
        try:
            value = self._attrs[item]
            if isinstance(value, property):
                return value.fget()
            return value
        except KeyError:
            raise AttributeError()

    def __iter__(self):
        return iter(self.items)

    def __cmp__(self, other):
        if isinstance(other, UsagePage):
            return self._usage is other
        return super(Collection, self).__cmp__(other)

    # TODO print out more meaningful information about this Collection
    def __str__(self, index=0):
        result = "{}Collection {}{}".format(" " * index * 2, self.collection_type._name_, (" ("+self._usage._name_+")") if self._usage is not None else "")
        for item in self.items:
            result += "\n"+item.__str__(index+1)
        return result

    @property
    def usage(self):
        """
        getter method

        @ return self._usage
        """
        return self._usage
    # end def usage
# end class Collection


class ReportGroup:
    def __init__(self):
        self._inputs = Collection(allowed_usage_types=(UsageType.COLLECTION_APPLICATION,))
        self._input_size = None
        self._outputs = Collection(allowed_usage_types=(UsageType.COLLECTION_APPLICATION,))
        self._output_size = None
        self._features = Collection(allowed_usage_types=(UsageType.COLLECTION_APPLICATION,))
        self._feature_size = None

    @property
    def inputs(self) -> Collection:
        return self._inputs

    @property
    def input_size(self) -> int:
        if self._input_size is None:
            self._input_size = self._inputs.get_size(ReportType.INPUT)
        return self._input_size

    @property
    def outputs(self) -> Collection:
        return self._outputs

    @property
    def output_size(self) -> int:
        if self._output_size is None:
            self._output_size = self._inputs.get_size(ReportType.OUTPUT)
        return self._output_size

    @property
    def features(self) -> Collection:
        return self._features

    @property
    def feature_size(self) -> int:
        if self._feature_size is None:
            self._feature_size = self._features.get_size(ReportType.FEATURE)
        return self._feature_size


class Device:
    def deserialize(self, data: bytes, report_type: ReportType=None):
        """
        Deserialises the raw HID data received from the device.
        If ReportIDs are used, then the first byte must be the ReportID
        :param data:
        :param report_type:
        :return: None
        """
        big_endian_data = _BitArray()
        report = 0
        if len(self._reports) == 0:
            raise ValueError("No reports have been created for {}".format(self.__class__.__name__))

        if report_type is None:
            report_type = ReportType.INPUT
        if 0 not in self._reports.keys():
            report = data[0]
            data = data[1:]

        if report_type == ReportType.INPUT:
            if self._reports[report].input_size != len(data):
                warn("data({}) does not match input_size({})".format(len(data),self._reports[report].input_size))
            big_endian_data.append(self._reports[report].inputs.deserialize(data, report_type))
        if report_type == ReportType.OUTPUT:
            if self._reports[report].output_size != len(data):
                warn("data({}) does not match output_size({})".format(len(data)),self._reports[report].output_size)
            big_endian_data.append(self._reports[report].outputs.deserialize(data, report_type))
        if report_type == ReportType.FEATURE:
            if self._reports[report].feature_size != len(data):
                warn("data({}) does not match feature_size({})".format(len(data),self._reports[report].feature_size))
            big_endian_data.append(self._reports[report].features.deserialize(data, report_type))
        return big_endian_data

    def serialize(self, report: int = 0, report_type: ReportType=None) -> bytes:
        """
        Serialises the reports into a bytes object. If ReportIDs are used, then report must be specified
        :param report: The ReportID to serialise. Default: 0
        :param report_type: The report type to serialise. Default: ReportType.OUTPUT
        :return: bytes
        """
        if report_type is None:
            report_type = ReportType.OUTPUT
        if len(self._reports) == 0:
            raise ValueError("No reports have been created for {}".format(self.__class__.__name__))

        data = None
        if report_type == ReportType.INPUT:
            data = self._reports[report].inputs.serialize(report_type)
        if report_type == ReportType.OUTPUT:
            data = self._reports[report].outputs.serialize(report_type)
        if report_type == ReportType.FEATURE:
            data = self._reports[report].features.serialize(report_type)

        # Prepend the ReportID if not 0
        if report > 0:
            data.prepend(bytes([report]))
        return data.bytes

    def __init__(self, collection=None, timestamp=None):
        self._reports = {}  # type: _Dict[int, ReportGroup]
        self._collection = Collection(items=collection, allowed_usage_types=UsageType.COLLECTION_APPLICATION)
        # Create ReportGroups from the Report IDs found in the master Collection
        self._populate_report_types(self._collection)
        self._timestamp = timestamp

    @property
    def reports(self):
        """
        Returns a dictionary that maps report ids to collections
        :return:
        """
        return self._reports

    @property
    def all(self):
        """
        Returns the root collection, not bound to any report group
        :return:
        """
        return self._collection

    def _populate_report_types(self, collection: Collection, path=None):
        if path is None:
            path = []

        for item in collection.items:
            if isinstance(item, Collection):
                path.append(item)
                self._populate_report_types(item, path.copy())
                path.pop()
                continue

            # assume the item is a Report

            # Create a ReportGroup on a new Report ID
            if item.report_id not in self._reports.keys():
                self._reports[item.report_id] = ReportGroup()

            if item.report_type == ReportType.INPUT:
                self._collection_add_report(
                    self._reports[item.report_id].inputs,
                    path.copy(),
                    item
                )
            elif item.report_type == ReportType.OUTPUT:
                self._collection_add_report(
                    self._reports[item.report_id].outputs,
                    path.copy(),
                    item
                )
            elif item.report_type == ReportType.FEATURE:
                self._collection_add_report(
                    self._reports[item.report_id].features,
                    path.copy(),
                    item
                )

    def _collection_add_report(self, collection: Collection, path, report: Report):
        while len(path)>0:
            target = path.pop(0)
            try:
                collection = [item for item in collection.items if item.parent == target][0]
                continue
            except IndexError:
                break
        while len(path) >= 0 and collection.parent != target:
            # Create a derrived Collection
            new_collection = Collection(
                usage=target._usage,
                allowed_usage_types=target._usage_types,
                collection_type=target.collection_type,
                parent=target
            )
            collection.append(new_collection)
            collection = new_collection
            if len(path)>0:
                target = path.pop(0)

        collection.append(report)

    def __str__(self, index=0):
        result = "Device:"
        for report_id in self._reports.keys():
            result += "\n  Report 0x{:02X}:".format(report_id)
            if len(self._reports[report_id].inputs.items):
                result += "\n    Inputs"
                for collection in self._reports[report_id].inputs:
                    result += "\n" + collection.__str__(4)
            if len(self._reports[report_id].outputs.items):
                result += "\n    Outputs"
                for collection in self._reports[report_id].outputs:
                    result += "\n" + collection.__str__(4)
            if len(self._reports[report_id].features.items):
                result += "\n    Features"
                for collection in self._reports[report_id].features:
                    result += "\n" + collection.__str__(4)

        if self._timestamp is not None:
            result += f"\n{self._timestamp / 1e6:.2f}ms\n"
        else:
            result += "\n"

        return result
