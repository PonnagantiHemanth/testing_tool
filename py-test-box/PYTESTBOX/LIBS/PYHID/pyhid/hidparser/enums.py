#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package pyhid.hidparser.enums

@brief  HID parser enums class

@author christophe Roquebert

@date   2019/01/24
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from array import array as _array
from pyhid.hidparser.helper import FlagEnum, EnumMask, Enum

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class ReportType(Enum):
    INPUT = 1
    OUTPUT = 2
    FEATURE = 3


class ReportFlags(FlagEnum):
    CONSTANT = 0x01
    VARIABLE = 0x02
    RELATIVE = 0x04
    WRAP = 0x08
    NON_LINEAR = 0x10
    NO_PREFERRED = 0x20
    NULL_STATE = 0x40
    # reserved = 0x80
    BUFFERED_BYTES = 0x100

    @classmethod
    def from_bytes(cls, data: _array):
        result = 0
        if data is None:
            return EnumMask(cls,result)
        if len(data)>0:
            result |= data[0]
        if len(data)>1:
            result |= data[1] << 8

        return EnumMask(cls, result)

    @classmethod
    def __repr_members__(cls, value):
        return [
            "Data" if not value & ReportFlags.CONSTANT.value else "Constant",
            "Array" if not value & ReportFlags.VARIABLE.value else "Variable",
            "Absolute" if not value & ReportFlags.RELATIVE.value else "Relative",
            "No Wrap" if not value & ReportFlags.WRAP.value else "Wrap",
            "Linear" if not value & ReportFlags.NON_LINEAR.value else "Non Linear",
            "Prefered State" if not value & ReportFlags.NO_PREFERRED.value else "No Prefered",
            "No Null position" if not value & ReportFlags.NULL_STATE.value else "Null state",
            "Bit Field" if not value & ReportFlags.BUFFERED_BYTES.value else "Buffered Bytes",
            ]


# TODO Support vendor defined functions
class CollectionType(Enum):
    PHYSICAL = 0
    APPLICATION = 1
    LOGICAL = 2
    REPORT = 3
    NAMED_ARRAY = 4
    USAGE_SWITCH = 5
    USAGE_MODIFIER = 6


class UnitSystem(Enum):
    NONE = 0x0
    SI_LINEAR = 0x01
    SI_ROTATION = 0x02
    ENGLISH_LINEAR = 0x03
    ENGLISH_ROTATION = 0x04
    VENDOR_DEFINED = 0x0F

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.name, self._name_.replace("_", " ").title())


# TODO Support printing out SI units ("cm", "mm", "km" etc...)
# TODO Support SI Linear, SI Rotation, English Linear and English Rotation
class UnitLength(Enum):
    NONE = 0
    CENTIMETERS = 1
    METERS = 3
    KILOMETERS = 6
    MILLIMETERS = -1
    MICROMETERS = -4
    NANOMETERS = -7


class UnitMass(Enum):
    NONE = 0
    GRAMS = 1
    KILOGRAMS = 4
    TON = 7
    MILLIGRAMS = -2
    MICROGRAMS = -5
    NANOGRAMS = -8
