#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.codechecklist.uicr
:brief: Receiver UICR tests
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/08/24
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.shared.codechecklist.uicr import SharedUICRTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ReceiverUICRTestCase(SharedUICRTestCase, ReceiverBaseTestCase):
    """
    Validate Receiver UICR registers
    """
# end class ReceiverUICRTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
