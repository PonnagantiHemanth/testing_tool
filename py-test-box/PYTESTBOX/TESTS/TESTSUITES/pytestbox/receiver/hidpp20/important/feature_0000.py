#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp20.important.feature_0000
:brief: Recerver HID++ 2.0 IRoot Important Package
:author: Christophe Roquebert
:date: 2018/12/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.shared.hidpp20.important.feature_0000 import SharedIRootTestCase
from pytestbox.base.bootloadertest import ReceiverBootloaderTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class IRootTestCase(SharedIRootTestCase, ReceiverBootloaderTestCase):
    """
    Validate Receiver Important Root TestCases
    """
# end class IRootTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
