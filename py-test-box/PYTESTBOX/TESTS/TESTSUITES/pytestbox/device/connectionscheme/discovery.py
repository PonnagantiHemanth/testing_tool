#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.device.connectionscheme.discovery
    :brief: Validates device discovery feature
    :author: Martin Cryonnet
    :date: 2020/04/27
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.shared.connectionscheme.discovery import SharedDiscoveryTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DiscoveryTestCase(SharedDiscoveryTestCase, DeviceBaseTestCase):
    """
    Discovery TestCases
    """
# end class DiscoveryTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
