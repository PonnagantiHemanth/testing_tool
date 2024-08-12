#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp.f9_fa.robustness
:brief: Validates HID++ 1.0 Manage Deactivatable Features with authentication (0xF9 & 0xFA) robustness
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/03/31
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pytestbox.receiver.hidpp.f9_fa.managedeactivatablefeaturesauth import \
    ReceiverManageDeactivatableFeaturesAuthTestCase
from pytestbox.shared.hidpp.managedeactivatablefeaturesauth.robustness import \
    SharedManageDeactivatableFeaturesAuthRobustnessTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ReceiverManageDeactivatableFeaturesAuthRobustnessTestCase(
        ReceiverManageDeactivatableFeaturesAuthTestCase, SharedManageDeactivatableFeaturesAuthRobustnessTestCase):
    """
    Validate the 'manage deactivatable features' mechanism (based on password authentication) robustness test cases
    with a receiver as a DUT
    """
    _disable_not_supported_bits_expected_error_codes = [Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE]
    _enable_no_opened_session_does_not_enable_expected_error_codes = [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE]
    _enable_no_opened_session_does_not_disable_expected_error_codes = [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE]
    _enable_not_supported_bits_expected_error_codes = [Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE]
    _enable_features_closes_session = [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE]
# end class ReceiverManageDeactivatableFeaturesAuthRobustnessTestCase
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
