#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package pyhid.hidparser.usagepages.hidpp

@brief  HID parser usage pages hidpp class

@author christophe Roquebert

@date   2019/01/24
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidparser.UsagePage import Usage, UsageType, UsagePage

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class Hidpp(UsagePage):
    """
    HID++ Report Desc
    """
    @classmethod
    def _get_usage_page_index(cls):
        return 0xff00
    # end def _get_usage_page_index

    HIDPP_MODE_00 = Usage(0x00, UsageType.DATA_DYNAMIC_VALUE)
    HIDPP_MODE_SHORT = Usage(0x01, UsageType.COLLECTION_APPLICATION)
    HIDPP_MODE_LONG = Usage(0x02, UsageType.COLLECTION_APPLICATION)
    HIDPP_MODE_VERY_LONG = Usage(0x04, UsageType.COLLECTION_APPLICATION)

    HIDPP_MODE_20 = Usage(0x20, UsageType.DATA_DYNAMIC_VALUE)
    HIDPP_MODE_21 = Usage(0x21, UsageType.DATA_DYNAMIC_VALUE)
    HIDPP_MODE_22 = Usage(0x22, UsageType.DATA_DYNAMIC_VALUE)

    HIDPP_MODE_41 = Usage(0x41, UsageType.COLLECTION_APPLICATION)
    HIDPP_MODE_42 = Usage(0x42, UsageType.COLLECTION_APPLICATION)

    DEVICE_CERTIFICATION_STATUS = Usage(0xC5, UsageType.COLLECTION_APPLICATION)

    NVIDIA_EXTENSION = Usage(0xF1, UsageType.COLLECTION_APPLICATION)
    HIDPP_MODE_F2 = Usage(0xF2, UsageType.COLLECTION_APPLICATION)
# end class Hidpp
