#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidparser.usagepages.logireport
:brief: HID parser usage pages hidpp vendor specific class
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: :2022/07/05
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidparser.UsagePage import Usage
from pyhid.hidparser.UsagePage import UsagePage
from pyhid.hidparser.UsagePage import UsageType


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class LogiReport(UsagePage):
    @classmethod
    def _get_usage_page_index(cls):
        return 0xff47
    # end def _get_usage_page_index

    FEATURE = Usage(0x01, UsageType.COLLECTION_APPLICATION)
# end class LogiReport
