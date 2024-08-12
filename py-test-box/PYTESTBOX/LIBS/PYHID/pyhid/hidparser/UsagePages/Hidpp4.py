#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package pyhid.hidparser.usagepages.hidpp4

@brief  HID parser usage pages hidpp vendor specific class

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


class Hidpp4(UsagePage):
    @classmethod
    def _get_usage_page_index(cls):
        return 0xff01
    # end def _get_usage_page_index

    HIDPP_MODE_SHORT = Usage(0x01, UsageType.COLLECTION_APPLICATION)
    HIDPP_MODE_LONG = Usage(0x02, UsageType.COLLECTION_APPLICATION)
    HIDPP_MODE_VERY_LONG = Usage(0x04, UsageType.COLLECTION_APPLICATION)

    HIDPP2_MODE_41= Usage(0x41, UsageType.COLLECTION_APPLICATION)
    HIDPP2_MODE_42 = Usage(0x42, UsageType.COLLECTION_APPLICATION)

# end class Hidpp4
