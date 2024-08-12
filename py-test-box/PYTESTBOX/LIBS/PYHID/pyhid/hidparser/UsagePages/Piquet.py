#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package pyhid.hidparser.usagepages.Piquet
:brief:  HID parser Piquet usage page class
:author: christophe Roquebert
:date:   2021/02/23
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidparser.UsagePage import Usage, UsageType, UsagePage

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class Piquet(UsagePage):
    """
    Piquet Report Desc
    """
    @classmethod
    def _get_usage_page_index(cls):
        return 0xff09
    # end def _get_usage_page_index

    USAGE_01 = Usage(0x01, UsageType.DATA_DYNAMIC_VALUE)
    USAGE_02 = Usage(0x02, UsageType.DATA_DYNAMIC_VALUE)
    USAGE_03 = Usage(0x03, UsageType.DATA_DYNAMIC_VALUE)
# end class Piquet
