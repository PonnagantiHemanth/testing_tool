#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidparser.usagepages.keydisplay
:brief: HID parser usage pages key display class
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: :2023/06/21
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidparser.UsagePage import Usage
from pyhid.hidparser.UsagePage import UsageType
from pyhid.hidparser.UsagePage import UsagePage


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KeyDisplay(UsagePage):
    @classmethod
    def _get_usage_page_index(cls):
        return 0xff40
    # end def _get_usage_page_index

    FEATURE = Usage(0x01, UsageType.COLLECTION_APPLICATION)
# end class KeyDisplay
