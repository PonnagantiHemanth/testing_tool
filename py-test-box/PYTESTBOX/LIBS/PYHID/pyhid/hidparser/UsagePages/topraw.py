#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidparser.usagepages.topraw
:brief: HID parser usage pages top raw layout Google vendor specific class
        cf WWCB Keyboard HID Report Descriptor:
        https://drive.google.com/file/d/1r1kNfd4ZL9kt9njqCvX6C5ANZbArblWx/view
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/09/09
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidparser.UsagePage import Usage, UsageType, UsagePage


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class TopRaw(UsagePage):
    """
    Top Row Layout Feature usage page
    """
    @classmethod
    def _get_usage_page_index(cls):
        """
        Google vendor specific usage page index
        """
        return 0xffd1
    # end def _get_usage_page_index

    TOP_RAW_01 = Usage(0x01, UsageType.CONTROL_LINEAR)
    TOP_RAW_02 = Usage(0x02, UsageType.CONTROL_LINEAR)
    TOP_RAW_03 = Usage(0x03, UsageType.CONTROL_LINEAR)
    TOP_RAW_04 = Usage(0x04, UsageType.CONTROL_LINEAR)
    TOP_RAW_05 = Usage(0x05, UsageType.CONTROL_LINEAR)
    TOP_RAW_06 = Usage(0x06, UsageType.CONTROL_LINEAR)
    TOP_RAW_07 = Usage(0x07, UsageType.CONTROL_LINEAR)
    TOP_RAW_08 = Usage(0x08, UsageType.CONTROL_LINEAR)
    TOP_RAW_09 = Usage(0x09, UsageType.CONTROL_LINEAR)
    TOP_RAW_10 = Usage(0x10, UsageType.CONTROL_LINEAR)
    TOP_RAW_11 = Usage(0x11, UsageType.CONTROL_LINEAR)
    TOP_RAW_12 = Usage(0x12, UsageType.CONTROL_LINEAR)
    TOP_RAW_13 = Usage(0x13, UsageType.CONTROL_LINEAR)
    TOP_RAW_14 = Usage(0x14, UsageType.CONTROL_LINEAR)
    TOP_RAW_15 = Usage(0x15, UsageType.CONTROL_LINEAR)
    TOP_RAW_16 = Usage(0x16, UsageType.CONTROL_LINEAR)
    TOP_RAW_17 = Usage(0x17, UsageType.CONTROL_LINEAR)
    TOP_RAW_18 = Usage(0x18, UsageType.CONTROL_LINEAR)
    TOP_RAW_19 = Usage(0x19, UsageType.CONTROL_LINEAR)
# end class TopRaw

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
