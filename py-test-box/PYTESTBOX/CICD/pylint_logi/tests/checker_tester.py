#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Custom linter
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pylint_logi.tests.checker_tester
:brief: base unittest checker for custom pylint checkers
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/04/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import os
import sys
import unittest
from os import path as op
from sys import stdout

from pylint import lint
from pylint.reporters import CollectingReporter

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
VERBOSE = False

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
if op.basename(os.getcwd()) == "tests":
    # add pylint checkers to the syspath if running from the tests directory
    sys.path.append(op.abspath('../'))
# end if


class CheckerTester(unittest.TestCase):
    """
    Generic test class for custom pylint checkers
    """
    CHECKER_UNDER_TEST = None

    def setUp(self):
        # See ``TestCase.setUp``
        if op.basename(os.getcwd()) == "tests":
            self.test_data_root = op.abspath("pylint_test_data")
        else:
            self.test_data_root = op.abspath(r"PYTESTBOX/CICD/pylint_logi/tests/pylint_test_data")
        # end if

        if self.CHECKER_UNDER_TEST is not None:
            self.config = ",".join([name for (_, (_,name, _)) in self.CHECKER_UNDER_TEST.msgs.items()])
        else:
            self.config = None
        # end if
    # end def setUp

    def generic_test_linting(self, file, expected_messages):
        """
        verify that a given test has the expected error messages

        :param file: file to lint, relative to the test_data folder
        :type file: ``str``
        :param expected_messages: list of expected message to find, and which line they are to be found. additionally
            can add additional message, in which case the text has to be found into the
        :type expected_messages: ``list[tuple[str, int]|tuple[str, int, tuple[str]]]``

        :raise ``AssertionError``: if the linting doesn't match the expected messages
        """
        collecting_reporter = CollectingReporter()

        self.assertIsNotNone(self.config, "No checker chosen for this test")

        path = op.join(self.test_data_root, file)

        self.assertTrue(op.exists(path), f"reference file {path} doesn't exist")

        pylint_obs = ["--disable=all", f"--enable={self.config}", path]

        lint.Run(pylint_obs, exit=False, reporter=collecting_reporter)
        messages = collecting_reporter.messages

        if VERBOSE:
            stdout.write("\n".join(f"{x.symbol} = {x.line} [{x.msg}]" for x in messages) + "\n")
        # end if

        self.assertEqual(len(expected_messages),
                         len(messages),
                         "Wrong number of message collected")

        for (message, expected_message) in zip(messages, expected_messages):

            match expected_message:
                case (symbol, line):
                    expected_symbol = symbol
                    expected_line = line
                    expected_additional_messages = []
                    expected_excluded_message = []
                case (symbol, line, additional_messages):
                    expected_symbol = symbol
                    expected_line = line
                    expected_additional_messages = additional_messages
                    expected_excluded_message = []
                case (symbol, line, additional_messages, excluded_messages):
                    expected_symbol = symbol
                    expected_line = line
                    expected_additional_messages = additional_messages
                    expected_excluded_message = excluded_messages
                case _:
                    self.fail("Badly constructed test reference")
            # end match

            self.assertEqual(expected_symbol, message.symbol, f"Unexpected message id for message{message}")
            self.assertEqual(expected_line, message.line, f"Unexpected message line for message{message}")

            for additional_message in expected_additional_messages:
                match additional_message:
                    case (format, data):
                        expected_message = format % data
                    case direct_string:
                        expected_message = direct_string
                # end match

                self.assertIn(expected_message, message.msg)
            # end for

            for excluded_message in expected_excluded_message:
                match excluded_message:
                    case (format, data):
                        excluded_message = format % data
                    case direct_string:
                        excluded_message = direct_string
                # end match

                self.assertNotIn(excluded_message, message.msg)
            # end for
        # end for
    # end def generic_test_linting
# end class CheckerTester


# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
