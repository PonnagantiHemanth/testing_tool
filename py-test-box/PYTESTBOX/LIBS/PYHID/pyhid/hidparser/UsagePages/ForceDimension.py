#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package pyhid.hidparser.usagepages.ForceDimension
:brief:  HID parser Force Dimension usage page class
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


class ForceDimension(UsagePage):
    """
    Force Dimension Report Desc
    """
    @classmethod
    def _get_usage_page_index(cls):
        return 0xfffd
    # end def _get_usage_page_index

    USAGE_FD01 = Usage(0xFD01, UsageType.COLLECTION_APPLICATION)

# end class ForceDimension
