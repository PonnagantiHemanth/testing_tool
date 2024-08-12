#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.hid.common.feature_00D0_interface
    :brief: Validates Device HID++ 2.0 Common feature 0x00D0
    :author: Stanislas Cottard
    :date: 2019/09/05
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.shared.hidpp20.common.feature_00D0_interface import SharedDfuTestCaseInterface
from pytestbox.base.dfuprocessing import DeviceDfuTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DfuTestCaseInterface(SharedDfuTestCaseInterface, DeviceDfuTestCase):
    """
    Validates DFU Interface TestCases
    """

# end class DfuTestCaseInterface

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
