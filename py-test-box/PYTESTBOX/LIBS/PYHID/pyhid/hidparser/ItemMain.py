#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package pyhid.hidparser.itemmain

@brief  HID parser main item class

@author christophe Roquebert

@date   2019/01/24
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidparser.Item import ItemType, Item
from pyhid.hidparser.enums import CollectionType, ReportFlags, ReportType
from pyhid.hidparser.DeviceBuilder import DeviceBuilder

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class InputItem(Item):
    flags = None # type: ReportFlags

    def visit(self, descriptor: DeviceBuilder):
        descriptor.add_report(ReportType.INPUT, self.flags)

    @classmethod
    def _get_tag(cls):
        return 0x80

    @classmethod
    def _get_type(cls):
        return ItemType.MAIN

    def __init__(self, **kwargs):
        super(InputItem, self).__init__(**kwargs)

        self.flags = ReportFlags.from_bytes(self.data)

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self.flags)


class OutputItem(Item):
    flags = None

    def visit(self, descriptor: DeviceBuilder):
        descriptor.add_report(ReportType.OUTPUT, self.flags)

    @classmethod
    def _get_tag(cls):
        return 0x90

    @classmethod
    def _get_type(cls):
        return ItemType.MAIN

    def __init__(self, **kwargs):
        super(OutputItem, self).__init__(**kwargs)

        self.flags = ReportFlags.from_bytes(self.data)

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self.flags)


class FeatureItem(Item):
    flags = None

    def visit(self, descriptor: DeviceBuilder):
        descriptor.add_report(ReportType.FEATURE, self.flags)

    @classmethod
    def _get_tag(cls):
        return 0xB0

    @classmethod
    def _get_type(cls):
        return ItemType.MAIN

    def __init__(self, **kwargs):
        super(FeatureItem, self).__init__(**kwargs)

        self.flags = ReportFlags.from_bytes(self.data)

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self.flags)


class CollectionItem(Item):
    collection = None

    @classmethod
    def _get_tag(cls):
        return 0xA0

    @classmethod
    def _get_type(cls):
        return ItemType.MAIN

    def visit(self, descriptor: DeviceBuilder):
        if not isinstance(self.collection, CollectionType):
            raise ValueError("CollectionItem does not have a valid collection set")
        descriptor.push_collection(self.collection)

    def __init__(self, **kwargs):
        super(CollectionItem, self).__init__(**kwargs)

        if self.data is None or len(self.data) != 1:
            raise ValueError("Collection must contain one byte of data")
        self.collection = CollectionType(self.data[0])

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.collection)


class EndCollectionItem(Item):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.pop_collection()

    @classmethod
    def _get_tag(cls):
        return 0xC0

    @classmethod
    def _get_type(cls):
        return ItemType.MAIN
