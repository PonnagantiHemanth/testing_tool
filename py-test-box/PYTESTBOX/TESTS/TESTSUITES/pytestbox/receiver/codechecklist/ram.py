#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.codechecklist.ram
:brief: Device Ram tests
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/06/21
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.shared.codechecklist.ram import SharedRamTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ReceiverRamTestCase(SharedRamTestCase, ReceiverBaseTestCase):
    """
    Validate Ram Stack management
    """
# end class ReceiverRamTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
