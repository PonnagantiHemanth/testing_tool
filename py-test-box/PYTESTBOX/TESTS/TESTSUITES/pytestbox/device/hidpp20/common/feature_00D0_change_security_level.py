#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.hid.common.feature_00D0_change_security_level
    :brief: Validates Device HID++ 2.0 Common feature 0x00D0
    :author: Stanislas Cottard
    :date: 2019/09/05
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.shared.hidpp20.common.feature_00D0_change_security_level import SharedDfuTestCaseChangeSecurityLevel
from pytestbox.base.dfuprocessing import DeviceDfuTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DfuTestCaseChangeSecurityLevel(SharedDfuTestCaseChangeSecurityLevel, DeviceDfuTestCase):
    """
    Validates DFU TestCases that needs to change the DFU security level
    """

# end class DfuTestCaseChangeSecurityLevel

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
