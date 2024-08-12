#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.receiver.hidpp20.common.feature_00D0_errorhandling
    :brief: Validates Receiver HID++ 2.0 Common feature 0x00D0
    :author: Stanislas Cottard
    :date: 2019/09/05
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.shared.hidpp20.common.feature_00D0_errorhandling import SharedDfuTestCaseErrorHandling
from pytestbox.base.dfuprocessing import ReceiverDfuTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DfuTestCaseErrorHandling(SharedDfuTestCaseErrorHandling, ReceiverDfuTestCase):
    """
    Validates DFU ErrorHandling TestCases
    """

# end class DfuTestCaseErrorHandling

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
