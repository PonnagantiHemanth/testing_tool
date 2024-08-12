#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.hid.common.feature_00D0_functionality
    :brief: Validates Device HID++ 2.0 Common feature 0x00D0
    :author: Stanislas Cottard
    :date: 2019/09/05
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.shared.hidpp20.common.feature_00D0_functionality import SharedDfuTestCaseFunctionality
from pytestbox.base.dfuprocessing import DeviceDfuTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DfuTestCaseFunctionality(SharedDfuTestCaseFunctionality, DeviceDfuTestCase):
    """
    Validates DFU Functionality TestCases
    """

# end class DfuTestCaseFunctionality

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
