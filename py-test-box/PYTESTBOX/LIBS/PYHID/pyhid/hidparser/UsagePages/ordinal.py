#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidparser.usagepages.ordinal
:brief: HID parser Ordinal usage page class
        cf https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf
        section 13 Ordinal Page (0x0A)
:author: Christophe Roquebert <croquebert@logitech.com>
:date: :2023/01/24
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
class Ordinal(UsagePage):
    @classmethod
    def _get_usage_page_index(cls):
        return 0x0A
    # end def _get_usage_page_index

    # UM: The Usage Modifier usage type identifies a usage applied to a logical collection.
    UNDEFINED = Usage(0x00, UsageType.COLLECTION_USAGE_MODIFIER)  # UM
    INSTANCE_1 = Usage(0x01, UsageType.COLLECTION_USAGE_MODIFIER)  # UM
    INSTANCE_2 = Usage(0x02, UsageType.COLLECTION_USAGE_MODIFIER)  # UM
    INSTANCE_3 = Usage(0x03, UsageType.COLLECTION_USAGE_MODIFIER)  # UM
    INSTANCE_4 = Usage(0x04, UsageType.COLLECTION_USAGE_MODIFIER)  # UM
    INSTANCE_5 = Usage(0x05, UsageType.COLLECTION_USAGE_MODIFIER)  # UM
    INSTANCE_6 = Usage(0x06, UsageType.COLLECTION_USAGE_MODIFIER)  # UM
    INSTANCE_7 = Usage(0x07, UsageType.COLLECTION_USAGE_MODIFIER)  # UM
    INSTANCE_8 = Usage(0x08, UsageType.COLLECTION_USAGE_MODIFIER)  # UM
    INSTANCE_9 = Usage(0x09, UsageType.COLLECTION_USAGE_MODIFIER)  # UM
    INSTANCE_10 = Usage(0x0A, UsageType.COLLECTION_USAGE_MODIFIER)  # UM
    INSTANCE_11 = Usage(0x0B, UsageType.COLLECTION_USAGE_MODIFIER)  # UM
    INSTANCE_12 = Usage(0x0C, UsageType.COLLECTION_USAGE_MODIFIER)  # UM
    INSTANCE_13 = Usage(0x0D, UsageType.COLLECTION_USAGE_MODIFIER)  # UM
    INSTANCE_14 = Usage(0x0E, UsageType.COLLECTION_USAGE_MODIFIER)  # UM
    INSTANCE_15 = Usage(0x0F, UsageType.COLLECTION_USAGE_MODIFIER)  # UM
    INSTANCE_16 = Usage(0x10, UsageType.COLLECTION_USAGE_MODIFIER)  # UM
# end class Ordinal

# ------------------------------------------------------------------------------
# End of file
# ------------------------------------------------------------------------------
