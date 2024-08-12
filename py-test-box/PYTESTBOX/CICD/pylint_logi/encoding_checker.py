#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pylint_logi.encoding_checker
:brief: Custom pylint checker for the file encoding
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/07/25
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from astroid import nodes
from pylint.checkers import BaseRawFileChecker

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------


class EncodingChecker(BaseRawFileChecker):
    """
    Check the file encoding
    """

    BASE_ID = "56" # Arbitrary number for the checker ID, chosent to be unique in the range available to custom checkers

    name = "encoding_checker"

    INVALID_ENCODING = 'invalid-encoding'

    msgs = {
        'F%s01' % BASE_ID: (
            'Invalid encoding: %s',
            INVALID_ENCODING,
            'The file encoding is not valid. Please use UTF-8.'
        )
    }

    def process_module(self, node: nodes.Module):
        """
        Process the module node

        :param node: the module node
        :type node: ``astroid.nodes.Module``
        """
        if node.file_encoding != "utf-8":
            self.add_message(self.INVALID_ENCODING, node=node, args=node.file_encoding)
        # end if
    # end def process_module
# end class EncodingChecker


def register(linter):
    """
    Register the checker

    :param linter: the linter
    :type linter: ``pylint.lint.PyLinter``
    """
    linter.register_checker(EncodingChecker(linter))
# end def register

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
