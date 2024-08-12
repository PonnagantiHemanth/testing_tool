#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.hid.common.feature_00D0_robustness
    :brief: Validates Device HID++ 2.0 Common feature 0x00D0
    :author: Stanislas Cottard
    :date: 2019/09/05
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.shared.hidpp20.common.feature_00D0_robustness import SharedDfuTestCaseRobustness
from pytestbox.base.dfuprocessing import DeviceDfuTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DfuTestCaseRobustness(SharedDfuTestCaseRobustness, DeviceDfuTestCase):
    """
    Validates DFU Robustness TestCases
    """

# end class DfuTestCaseRobustness

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
