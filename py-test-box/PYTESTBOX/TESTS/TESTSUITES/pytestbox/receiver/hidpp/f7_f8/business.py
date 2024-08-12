#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp.f7_f8.business
:brief: HID++ 1.0 ``PasswordAuthentication`` business test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.receiver.hidpp.f7_f8.passwordauthentication import ReceiverPasswordAuthenticationTestCase
from pytestbox.shared.hidpp.passwordauthentication.business import SharedPasswordAuthenticationBusinessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReceiverPasswordAuthenticationBusinessTestCase(SharedPasswordAuthenticationBusinessTestCase,
                                                     ReceiverPasswordAuthenticationTestCase):
    """
    Validate ``PasswordAuthentication`` business test cases
    """
# end class ReceiverPasswordAuthenticationBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
