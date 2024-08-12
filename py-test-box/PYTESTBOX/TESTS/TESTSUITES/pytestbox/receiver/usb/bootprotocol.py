#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.usb.bootprotocol
:brief: Validate USB Boot protocol receiver test cases
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/03/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.shared.usb.bootprotocol import SharedBootProtocolTestCases


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BootProtocolTestCases(SharedBootProtocolTestCases, ReceiverBaseTestCase):
    """
    Validate USB Boot Protocol Receiver Test Cases
    """
# end class BootProtocolTestCases

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
