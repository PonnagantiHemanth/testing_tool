#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.usb.descriptors
:brief: Validate USB descriptors receiver test cases
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/01/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.shared.usb.descriptors import SharedDescriptorsTestCases


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DescriptorsTestCases(SharedDescriptorsTestCases, ReceiverBaseTestCase):
    """
    Validate USB descriptors
    """
# end class DescriptorsTestCases

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
