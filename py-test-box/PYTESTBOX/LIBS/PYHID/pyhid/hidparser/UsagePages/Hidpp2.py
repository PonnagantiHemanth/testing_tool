#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidparser.usagepages.hidpp2
:brief: HID parser usage pages hidpp vendor specific class
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2019/01/31
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
class Hidpp2(UsagePage):

    @classmethod
    def _get_usage_page_index(cls):
        return 0xff43
    # end def _get_usage_page_index

    HIDPP2_MODE_SHORT = Usage(0x01, UsageType.COLLECTION_APPLICATION)
    HIDPP2_MODE_LONG = Usage(0x02, UsageType.COLLECTION_APPLICATION)
    HIDPP2_MODE_VERY_LONG = Usage(0x04, UsageType.COLLECTION_APPLICATION)
    VLP_MODE_NORMAL = Usage(0x08, UsageType.COLLECTION_APPLICATION)
    VLP_MODE_EXTENDED = Usage(0x10, UsageType.COLLECTION_APPLICATION)

    # The 2 bytes format matches this structure:
    #   supported, defined == (((supported) << 8) | (defined))

    # HIDPP_LONG_MSG , HIDPP_LONG_MSG == 0x0202
    HIDPP2_MODE_0202 = Usage(0x0202, UsageType.COLLECTION_APPLICATION)

    # HIDPP_SHORT_MSG | HIDPP_LONG_MSG, HIDPP_SHORT_MSG == 0x0301
    HIDPP2_MODE_0301 = Usage(0x0301, UsageType.COLLECTION_APPLICATION)
    # HIDPP_SHORT_MSG | HIDPP_LONG_MSG, HIDPP_LONG_MSG == 0x0302
    HIDPP2_MODE_0302 = Usage(0x0302, UsageType.COLLECTION_APPLICATION)

    # HIDPP_LONG_MSG | HIDPP_VERY_LONG_MSG, HIDPP_LONG_MSG == 0x0602
    HIDPP2_MODE_0602 = Usage(0x0602, UsageType.COLLECTION_APPLICATION)
    # HIDPP_LONG_MSG | HIDPP_VERY_LONG_MSG, HIDPP_VERY_LONG_MSG == 0x0604
    HIDPP2_MODE_0604 = Usage(0x0604, UsageType.COLLECTION_APPLICATION)

    # HIDPP_SHORT_MSG | HIDPP_LONG_MSG | HIDPP_VERY_LONG_MSG, HIDPP_SHORT_MSG == 0x0701
    HIDPP2_MODE_0701 = Usage(0x0701, UsageType.COLLECTION_APPLICATION)
    # HIDPP_SHORT_MSG | HIDPP_LONG_MSG | HIDPP_VERY_LONG_MSG, HIDPP_LONG_MSG == 0x0702
    HIDPP2_MODE_0702 = Usage(0x0702, UsageType.COLLECTION_APPLICATION)
    # HIDPP_SHORT_MSG | HIDPP_LONG_MSG | HIDPP_VERY_LONG_MSG, HIDPP_VERY_LONG_MSG == 0x0704
    HIDPP2_MODE_0704 = Usage(0x0704, UsageType.COLLECTION_APPLICATION)

    # VLP
    VLP_MODE_1A02 = Usage(0x1A02, UsageType.COLLECTION_APPLICATION)
    VLP_MODE_1A08 = Usage(0x1A08, UsageType.COLLECTION_APPLICATION)
    VLP_MODE_1A10 = Usage(0x1A10, UsageType.COLLECTION_APPLICATION)
# end class Hidpp2

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
