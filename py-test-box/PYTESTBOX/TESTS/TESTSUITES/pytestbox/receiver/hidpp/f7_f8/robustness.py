#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp.f7_f8.robustness
:brief: HID++ 1.0 ``PasswordAuthentication`` robustness test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pytestbox.receiver.hidpp.f7_f8.passwordauthentication import ReceiverPasswordAuthenticationTestCase
from pytestbox.shared.hidpp.passwordauthentication.robustness import SharedPasswordAuthenticationRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReceiverPasswordAuthenticationRobustnessTestCase(SharedPasswordAuthenticationRobustnessTestCase,
                                                       ReceiverPasswordAuthenticationTestCase):
    """
    Validate ``PasswordAuthentication`` robustness test cases
    """
    _test_service_is_closed_when_underlying_transport_channel_is_terminated_err_codes = \
        [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE]
# end ReceiverPasswordAuthenticationRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
