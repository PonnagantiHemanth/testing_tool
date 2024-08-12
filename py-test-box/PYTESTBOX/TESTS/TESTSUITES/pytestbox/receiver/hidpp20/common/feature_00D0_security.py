#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.receiver.hidpp20.common.feature_00D0_security
    :brief: Validates Receiver HID++ 2.0 Common feature 0x00D0
    :author: Stanislas Cottard
    :date: 2019/10/07
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.shared.hidpp20.common.feature_00D0_security import SharedDfuTestCaseSecurity
from pytestbox.base.dfuprocessing import ReceiverDfuTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DfuTestCaseSecurity(SharedDfuTestCaseSecurity, ReceiverDfuTestCase):
    """
    Validates DFU Security TestCases
    """

# end class DfuTestCaseSecurity

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
