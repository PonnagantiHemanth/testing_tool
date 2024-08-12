#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp.f9_fa.functionality
:brief: Validates HID++ 1.0 Manage Deactivatable Features with authentication (0xF9 & 0xFA) functionality
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/02/19
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.receiver.hidpp.f9_fa.managedeactivatablefeaturesauth import \
    ReceiverManageDeactivatableFeaturesAuthTestCase
from pytestbox.shared.hidpp.managedeactivatablefeaturesauth.functionality import \
    SharedManageDeactivatableFeaturesAuthFunctionalityTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ReceiverManageDeactivatableFeaturesAuthFunctionalityTestCase(
        ReceiverManageDeactivatableFeaturesAuthTestCase, SharedManageDeactivatableFeaturesAuthFunctionalityTestCase):
    """
    Validate the 'manage deactivatable features' mechanism (based on password authentication) functionality test cases
    with a receiver as a DUT
    """
# end class ReceiverManageDeactivatableFeaturesAuthFunctionalityTestCase
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
