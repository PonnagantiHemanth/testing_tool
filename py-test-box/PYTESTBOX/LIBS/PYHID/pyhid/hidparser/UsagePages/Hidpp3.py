#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package pyhid.hidparser.usagepages.hidpp2

@brief  HID parser usage pages hidpp vendor specific class

@author christophe Roquebert

@date   2019/01/31
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidparser.UsagePage import Usage, UsageType, UsagePage

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class Hidpp3(UsagePage):
    @classmethod
    def _get_usage_page_index(cls):
        return 0xffBC
    # end def _get_usage_page_index

    HIDPP3_MODE_88 = Usage(0x88, UsageType.COLLECTION_APPLICATION)

# end class Hidpp3
