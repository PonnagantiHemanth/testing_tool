#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.codechecklist.ram
:brief: Device Ram tests
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/06/21
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.shared.codechecklist.ram import SharedRamTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceRamTestCase(SharedRamTestCase, DeviceBaseTestCase):
    """
    Validate Ram management
    """
# end class DeviceRamTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
