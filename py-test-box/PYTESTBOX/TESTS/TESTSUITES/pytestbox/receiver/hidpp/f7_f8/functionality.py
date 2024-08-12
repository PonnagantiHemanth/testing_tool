#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp.f7_f8.functionality
:brief: HID++ 1.0 ``PasswordAuthentication`` functionality test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.receiver.hidpp.f7_f8.passwordauthentication import ReceiverPasswordAuthenticationTestCase
from pytestbox.shared.hidpp.passwordauthentication.functionality import \
    SharedPasswordAuthenticationFunctionalityTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReceiverPasswordAuthenticationFunctionalityTestCase(SharedPasswordAuthenticationFunctionalityTestCase,
                                                          ReceiverPasswordAuthenticationTestCase):
    """
    Validate ``PasswordAuthentication`` functionality test cases
    """
# end class ReceiverPasswordAuthenticationFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
