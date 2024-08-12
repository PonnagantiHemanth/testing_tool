#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp.f7_f8.errorhandling
:brief: HID++ 1.0 ``PasswordAuthentication`` error handling test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pytestbox.receiver.hidpp.f7_f8.passwordauthentication import ReceiverPasswordAuthenticationTestCase
from pytestbox.shared.hidpp.passwordauthentication.errorhandling import \
    SharedPasswordAuthenticationErrorHandlingTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReceiverPasswordAuthenticationErrorHandlingTestCase(SharedPasswordAuthenticationErrorHandlingTestCase,
                                                          ReceiverPasswordAuthenticationTestCase):
    """
    Validate ``PasswordAuthentication`` errorhandling test cases
    """
    _test_sending_password_without_started_session_expected_error_codes = [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE]
    _test_session_if_no_authentication_expected_error_code = [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE]
    _test_session_is_closed_when_device_is_reset_expected_error_codes = [Hidpp1ErrorCodes.ERR_INVALID_ADDRESS]
    _test_start_session_request_for_an_already_open_session_expected_error_codes = \
        [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE]
    _test_start_session_with_wrong_authentication_expected_error_codes = [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE]
    _test_start_session_with_wrong_name_expected_error_codes = [Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE]
# end class ReceiverPasswordAuthenticationErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
