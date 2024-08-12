#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.codechecklist.uicr
:brief: Device UICR tests
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/08/24
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.shared.codechecklist.uicr import SharedUICRTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceUICRTestCase(SharedUICRTestCase, DeviceBaseTestCase):
    """
    Validate Device UICR registers
    """
# end class DeviceUICRTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
