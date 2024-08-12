#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp.f9_fa.business
:brief: Validates HID++ 1.0 Manage Deactivatable Features with authentication (0xF9 & 0xFA) business
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/02/19
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.receiver.hidpp.f9_fa.managedeactivatablefeaturesauth import \
    ReceiverManageDeactivatableFeaturesAuthTestCase
from pytestbox.shared.hidpp.managedeactivatablefeaturesauth.business import \
    SharedManageDeactivatableFeaturesAuthBusinessTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ReceiverManageDeactivatableFeaturesAuthBusinessTestCase(ReceiverManageDeactivatableFeaturesAuthTestCase,
                                                              SharedManageDeactivatableFeaturesAuthBusinessTestCase):
    """
    Validate the 'manage deactivatable features' mechanism (based on password authentication) business test cases
    with a receiver as a DUT
    """
# end class ReceiverManageDeactivatableFeaturesAuthBusinessTestCase
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
