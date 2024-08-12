#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidparser
:brief: HID parser class
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2019/01/24
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidparser.Item import Item
from pyhid.hidparser.Item import ItemType
from pyhid.hidparser.ItemMain import *
from pyhid.hidparser.ItemGlobal import *
from pyhid.hidparser.ItemLocal import *
from pyhid.hidparser.DeviceBuilder import DeviceBuilder
from pyhid.hidparser.Device import Collection
from pyhid.hidparser.Device import Device
from pyhid.hidparser.Device import Report
from pyhid.hidparser.Device import ReportGroup
from pyhid.hidparser.UsagePage import Usage
from pyhid.hidparser.UsagePage import UsagePage
from pyhid.hidparser.UsagePage import UsageRange
from pyhid.hidparser.UsagePage import UsageType
import pyhid.hidparser.UsagePages


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
def parse(data, timestamp=None):
    """
    Create Item list from data

    :param data: Data to parse
    :type data: `bytes``
    :param timestamp: Timestamp of the data
    :type timestamp: ``int``

    @return (Device) device object listing the collections extracted from data
    """
    items = get_items(data)

    descriptor_builder = DeviceBuilder()
    for item in items:
        item.visit(descriptor_builder)

    return descriptor_builder.build(timestamp=timestamp)
# end def parse


def get_items(data):
    """
    Create Item list from data

    @param  data    [in] (byte array) Data to parse

    @return (UsagePageItem List) List of UsagePageItem element
    """
    import array

    if isinstance(data, bytes):
        data = array.array('B', bytearray.fromhex(data.decode('utf-8')))

    # grab the next len bytes and return an array from the iterator
    get_bytes = lambda it, len: [next(it) for x in range(len)]

    byte_iter = iter(data)
    while True:
        try:
            item = next(byte_iter)
            # Check if the item is "Long"
            if item == 0xFE:
                size = next(byte_iter)
                tag = next(byte_iter)
                if tag not in range(0xF0, 0xFF):
                    raise ValueError("Long Items are only supported by Vender defined tags as of Version 1.11")
                # Yield a long item, There are no tags defined in HID as of Version 1.11
                yield Item(tag=tag, data=get_bytes(byte_iter, size), long=True)

            # Short item's size is the first two bits (eitehr 0,1,2 or 4)
            size = item & 0x03
            if size == 3:
                size = 4

            # Get the item tag type from bits 3 - 2
            item_type = ItemType(item & 0x0C)
            if item_type == ItemType.RESERVED:
                raise ValueError("Invalid bType in short item")

            yield Item.create(tag=item & 0xFC, data=get_bytes(byte_iter, size))

        except StopIteration:
            break
    pass
# end def get_items

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
