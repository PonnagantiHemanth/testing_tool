#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.usb.bootprotocol
:brief: Validate USB Boot protocol test cases
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/03/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.shared.usb.bootprotocol import SharedBootProtocolTestCases


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BootProtocolTestCases(SharedBootProtocolTestCases, DeviceBaseTestCase):
    """
    Validate USB Boot Protocol Device Test Cases
    """
# end class BootProtocolTestCases

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
