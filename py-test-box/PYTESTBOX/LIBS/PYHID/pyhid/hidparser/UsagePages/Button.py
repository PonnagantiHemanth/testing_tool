#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package pyhid.hidparser.usagepages.button

@brief  HID parser usage pages button class

@author christophe Roquebert

@date   2019/01/24
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidparser.UsagePage import UsagePage, UsageType, Usage

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class Button(UsagePage):

    @classmethod
    def get_usage(cls, value):
        try:
            return cls._value2member_map_[value]
        except KeyError:
            return Button(value)
        # end try
    # end def get_usage

    @classmethod
    def _get_usage_page_index(cls):
        return 0x09
    # end def _get_usage_page_index

    NO_BUTTON_PRESSED = Usage(0x00, UsageType.DATA_SELECTOR)  # Sel
    BUTTON_1 = Usage(0x01, UsageType.DATA_SELECTOR)  # Sel
    BUTTON_2 = Usage(0x02, UsageType.DATA_SELECTOR)  # Sel
    BUTTON_3 = Usage(0x03, UsageType.DATA_SELECTOR)  # Sel
    BUTTON_4 = Usage(0x04, UsageType.DATA_SELECTOR)  # Sel
    BUTTON_5 = Usage(0x05, UsageType.DATA_SELECTOR)  # Sel
    BUTTON_6 = Usage(0x06, UsageType.DATA_SELECTOR)  # Sel
    BUTTON_7 = Usage(0x07, UsageType.DATA_SELECTOR)  # Sel
    BUTTON_8 = Usage(0x08, UsageType.DATA_SELECTOR)  # Sel
    BUTTON_9 = Usage(0x09, UsageType.DATA_SELECTOR)  # Sel
    BUTTON_10 = Usage(0x10, UsageType.DATA_SELECTOR)  # Sel
# end class Button


# Because Enum overrides the __new__ method in teh metaclass, so, it's getting overridden externally
def _create_button_usage(cls, value):
    if isinstance(value, Usage):
        return super(Button, cls).__new__(cls, value)
    if (value & ~0xFFFF) > 0:
        raise ValueError()
    button = Usage(value, [
        UsageType.DATA_SELECTOR,
        UsageType.CONTROL_ON_OFF,
        UsageType.CONTROL_MOMENTARY,
        UsageType.CONTROL_ONE_SHOT
    ])
    button_enum = object.__new__(cls)
    button_enum._value_ = button
    button_enum._name_ = "BUTTON{}".format(value)
    button_enum.__objclass__ = cls
    button_enum.__init__(button)
    cls._member_names_.append(button_enum._name_)
    cls._member_map_[button_enum._name_] = button_enum
    cls._value2member_map_[value] = button_enum
    return button_enum


setattr(Button, "__new__", _create_button_usage)
