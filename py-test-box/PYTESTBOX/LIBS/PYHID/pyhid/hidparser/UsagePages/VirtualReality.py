#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package pyhid.hidparser.usagepages.virtualreality

@brief  HID parser usage pages virtual reality class
        Built from https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf

@author christophe Roquebert

@date   2019/01/24
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidparser.UsagePage import UsagePage, Usage, UsageType

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class VirtualReality(UsagePage):

    @classmethod
    def _get_usage_page_index(cls):
        return 0x03

    BELT = Usage(0x01, UsageType.COLLECTION_APPLICATION)
    BODY_SUIT =  Usage(0x02, UsageType.COLLECTION_APPLICATION)
    FLEXOR = Usage(0x03, UsageType.COLLECTION_PHYSICAL)
    GLOVE = Usage(0x04, UsageType.COLLECTION_APPLICATION)
    HEAD_TRACKER = Usage(0x05, UsageType.COLLECTION_PHYSICAL)
    HEAD_MOUNTED_DISPLAY = Usage(0x06, UsageType.COLLECTION_APPLICATION)
    HAND_TRACKER = Usage(0x07, UsageType.COLLECTION_APPLICATION)
    OCULOMETER = Usage(0x08, UsageType.COLLECTION_APPLICATION)
    VEST = Usage(0x09, UsageType.COLLECTION_APPLICATION)
    ANIMATRONIC_DEVICE = Usage(0x0A, UsageType.COLLECTION_APPLICATION)

    STEREO_ENABLE = Usage(0x20, UsageType.CONTROL_ON_OFF)
    DISPLAY_ENABLE = Usage(0x21, UsageType.CONTROL_ON_OFF)
