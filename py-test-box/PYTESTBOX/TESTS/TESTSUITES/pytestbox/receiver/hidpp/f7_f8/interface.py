#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp.f7_f8.interface
:brief: HID++ 1.0 ``PasswordAuthentication`` interface test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.receiver.hidpp.f7_f8.passwordauthentication import ReceiverPasswordAuthenticationTestCase
from pytestbox.shared.hidpp.passwordauthentication.interface import SharedPasswordAuthenticationInterfaceTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReceiverPasswordAuthenticationInterfaceTestCase(SharedPasswordAuthenticationInterfaceTestCase,
                                                      ReceiverPasswordAuthenticationTestCase):
    """
    Validate ``PasswordAuthentication`` interface test cases
    """
# end class ReceiverPasswordAuthenticationInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
