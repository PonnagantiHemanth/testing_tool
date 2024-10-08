#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package pyhid.hidparser.devicebuilder

@brief  HID parser device builder class

@author christophe Roquebert

@date   2019/01/24
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import copy as _copy
from pyhid.hidparser.enums import CollectionType, ReportFlags, EnumMask, ReportType
from pyhid.hidparser.UsagePage import UsagePage, Usage, UsageType, UsageRange
from pyhid.hidparser.Device import Device, Report, ReportGroup, Collection
from pyhid.hidparser.helper import ValueRange

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class DeviceBuilder:
    def __init__(self):
        self._state_stack = []

        # Global Items
        self.usage_page = None
        self.unit = None
        self.unit_exponent = 1

        self.report_id = 0
        self.report_size = 0
        self.report_count = 0
        self.logical_range = ValueRange()
        self.physical_range = ValueRange()

        # Local Items
        self._usages = []
        self._last_usage = None

        self.designators = range(0)
        self.strings = range(0)

        self._collection = Collection(allowed_usage_types=UsageType.COLLECTION_APPLICATION)
        self._current_collection = self._collection

    def add_report(self, report_type: ReportType, flags):
        usages = []
        if not flags & ReportFlags.CONSTANT or len(self._usages):
            if len(self._usages) == 0:
                usages = [self._last_usage]*self.report_count
            else:
                while len(self._usages) > 0 and len(usages) < self.report_count:
                    usage = self._usages.pop(0)
                    self._last_usage = usage
                    usages.extend(usage.get_range() if isinstance(usage, UsageRange) else [usage])

        designators = range(0)
        if len(self.designators) > 0:
            designator_diff =  len(self.designators) - self.report_count
            assert designator_diff >= 0, "Too few designators for report"
            designators = self.designators[0:-designator_diff]
            self.designators = self.designators[designator_diff + 1:]

        strings = range(0)
        if len(self.strings) > 0:
            strings_diff = len(self.strings) - self.report_count
            assert strings_diff >= 0, "Too few strings for report"
            strings = self.strings[0:-strings_diff]
            self.strings = self.strings[strings_diff + 1:]

        self._current_collection.append(Report(
            report_id=self.report_id,
            report_type=report_type,
            usages=usages,
            designators=designators,
            strings=strings,
            size=self.report_size,
            count=self.report_count,
            logical_range=_copy.copy(self.logical_range) if self.logical_range != ValueRange() else None,
            physical_range=_copy.copy(self.physical_range) if self.physical_range != ValueRange() else None,
            unit=self.unit,
            exponent=self.unit_exponent,
            flags=flags
        ))

    def set_report_id(self, report_id: int):
        self.report_id = report_id

    def set_designator_range(self, minimum=None, maximum=None):
        if minimum is None:
            minimum = self.designators.start
        if maximum is None:
            maximum = self.designators.stop - 1 # Subtract one, so the output range generator is inclusive from start to stop
        self.designators = range(minimum, maximum + 1)

    def set_string_range(self, minimum=None, maximum=None):
        if minimum is None:
            minimum = self.strings.start
        if maximum is None:
            maximum = self.strings.stop - 1  # Subtract one, so the output range generator is inclusive from start to stop
        self.strings = range(minimum, maximum + 1)

    def set_usage_range(self, minimum=None, maximum=None):
        usage = self._usages[len(self._usages)-1] if len(self._usages) else None
        if usage is None or not isinstance(usage, UsageRange):
            usage = UsageRange(self.usage_page)
            self._usages.append(usage)

        if minimum is not None:
            usage.minimum = minimum
        if maximum is not None:
            usage.maximum = maximum

    def set_logical_range(self, minimum = None, maximum = None):
        if minimum is not None:
            self.logical_range.minimum = minimum

        if maximum is not None:
            self.logical_range.maximum = maximum

    def set_physical_range(self, minimum=None, maximum=None):
        if minimum is not None:
            self.physical_range.minimum = minimum

        if maximum is not None:
            self.physical_range.maximum = maximum

    def add_usage(self, usage):
        if isinstance(usage, Usage):
            self._usages.append(usage)
        elif isinstance(usage, UsagePage):
            self._usages.append(usage.value)
        else:
            usage_page = self.usage_page if (usage & ~0xFFFF) == 0 else UsagePage.find_usage_page((usage & ~0xFFFF) >> 16)
            if usage_page is None:
                raise ValueError("Invalid usage page")
            self._usages.append(usage_page.get_usage(usage & 0xFFFF))

    def set_usage_page(self, usage_page: UsagePage.__class__):
        self.usage_page = usage_page
        self._usages.clear()

    def push_collection(self, collection: CollectionType):
        try:
            usage = self._usages.pop(0)
        except IndexError:
            usage = None
        collection_element = Collection(
            usage=usage,
            parent=self._current_collection,
            collection_type=collection
        )
        self._current_collection.append(collection_element)
        self._current_collection = collection_element

        self._usages.clear()
        return self

    def pop_collection(self):
        if self._current_collection.parent is None:
            raise RuntimeError("Can not pop collection state")
        self._current_collection = self._current_collection.parent

        self._usages.clear()
        return self

    def push(self):
        """
        Pushes the state of all the global items onto the stack
        """
        global_items = (
            "usage_page", "unit","unit_exponent", "report_id",
            "report_size", "report_count", "logical_range", "physical_range"
        )
        state = _copy.deepcopy({k:v for k,v in self.__dict__.items() if k in global_items})
        self._state_stack.append(state)
        return self

    def pop(self):
        """
        Pops and restores the global item states from the stack
        """
        if len(self._state_stack) > 0:
            state = self._state_stack.pop()
            self.__dict__.update(state)
        return self

    def build(self, timestamp=None):
        return Device(self._collection.items, timestamp)
