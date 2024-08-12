#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pylibrary.tools.passwordfileparser
    :brief: Password file parser
    :author: Martin Cryonnet
    :date: 2020/11/17
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from enum import Enum
import re


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class PasswordFileParser:
    """
    Password file parser

    Parse a file containing passwords to enable features. If no filename is provided, default passwords are used.
    """
    class Accounts(Enum):
        """
        Accounts as defined in the password file
        """
        MANUFACTURING = "manufHidpp"
        COMPLIANCE = "complHidpp"
        GOTHARD = "gothard"
        GOTTHARD = GOTHARD
    # end class Accounts

    def __init__(self, filename=None):
        """
        Constructor
        :param filename: Full filename - OPTIONAL
        :type filename: ``str``
        """
        self._filename = filename
    # end def __init__

    def get_password(self, account):
        """
        Get password for given account

        :param account: Account
        :type account: ``PasswordFileParser.Accounts``

        :return: Password
        :rtype: ``str``
        """
        if self._filename is None:
            lines = ['manufHidpp:6162636465666768696A6B6C6D6E6F70\n',
                     'gothard:6162636465666768696A6B6C6D6E6F70\n',
                     'complHidpp:30313233343536373839414243444546']
        else:
            with open(self._filename) as file:
                lines = file.readlines()
            # end with
        return re.search(r':([0-9a-fA-F]+)', [line for line in lines if account.value in line][0])[1]
    # end def get_password
# end class PasswordFileParser


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
