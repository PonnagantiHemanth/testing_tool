#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package pyhid.hidparser.usagepages.PS4
:brief:  HID parser PS4 usage page class
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


class PS4(UsagePage):
    """
    PS4 Report Desc
    """
    @classmethod
    def _get_usage_page_index(cls):
        return 0xfff0
    # end def _get_usage_page_index

    USAGE_40 = Usage(0x40, UsageType.COLLECTION_APPLICATION)
# end class PS4
