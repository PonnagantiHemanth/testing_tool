#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp20.important.feature_0001
:brief: Recerver HID++ 2.0 FeatureSet Important Package
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/12/03
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.base.bootloadertest import ReceiverBootloaderTestCase
from pytestbox.shared.hidpp20.important.feature_0001 import SharedIFeatureSetTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class IFeatureSetTestCase(SharedIFeatureSetTestCase, ReceiverBootloaderTestCase):
    """
    Validate Receiver Important Feature Set TestCases in Bootloader mode
    """
# end class IFeatureSetTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
