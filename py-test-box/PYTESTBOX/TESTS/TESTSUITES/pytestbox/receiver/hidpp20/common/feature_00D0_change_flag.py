#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.receiver.hidpp20.common.feature_00D0_change_flag
    :brief: Validates Receiver HID++ 2.0 Common feature 0x00D0
    :author: Stanislas Cottard
    :date: 2019/09/05
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.shared.hidpp20.common.feature_00D0_change_flag import SharedDfuTestCaseChangeFlag
from pytestbox.base.dfuprocessing import ReceiverDfuTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DfuTestCaseChangeFlag(SharedDfuTestCaseChangeFlag, ReceiverDfuTestCase):
    """
    Validates DFU TestCases that needs to change the DFU flag
    """

# end class DfuTestCaseChangeFlag

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
