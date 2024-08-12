#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.usb.descriptors
:brief: Validate USB descriptors test cases
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/01/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import LogitechProtocol
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.shared.usb.descriptors import SharedDescriptorsTestCases


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DescriptorsTestCases(SharedDescriptorsTestCases, DeviceBaseTestCase):
    """
    USB descriptors Device Test Cases
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.USB

# end class DescriptorsTestCases

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
