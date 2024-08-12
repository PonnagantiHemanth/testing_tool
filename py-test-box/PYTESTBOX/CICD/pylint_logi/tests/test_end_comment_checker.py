#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Custom linter
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pylint_logi.tests.test_end_comment_checker
:brief: unittest checker for end comment checker
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/04/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import sys
import unittest
from os import path as op

sys.path.append(op.abspath(__file__).split('pylint_logi')[0])

from pylint_logi.end_comment_checker import EndCommentChecker
from pylint_logi.end_comment_checker import MISSING_END_COMMENT_SYMBOL
from pylint_logi.end_comment_checker import WRONG_END_COMMENT_SYMBOL
from pylint_logi.end_comment_checker import END_COMMENT_TOO_EARLY_SYMBOL
from pylint_logi.tests.checker_tester import CheckerTester


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------


class EndCommentCheckerTest(CheckerTester):
    """
    Test class for the ``EndCommentChecker``
    """
    CHECKER_UNDER_TEST = EndCommentChecker

    def test_no_error_no_hierarchy(self):
        """
        test simple cases without errors
        """

        self.generic_test_linting(
            "end-comment/no-error-no-hierarchy.py",
            [])
    # end def test_no_error_no_hierarchy

    def test_no_end_no_hierarchy(self):
        """
        test simple cases without any end comment
        """

        self.generic_test_linting(
            "end-comment/no-comments-no-hierarchy.py",
            [
                (MISSING_END_COMMENT_SYMBOL, 6),
                (MISSING_END_COMMENT_SYMBOL, 12),
                (MISSING_END_COMMENT_SYMBOL, 17),
                (MISSING_END_COMMENT_SYMBOL, 22),
                (MISSING_END_COMMENT_SYMBOL, 27),
                (MISSING_END_COMMENT_SYMBOL, 32),
                (MISSING_END_COMMENT_SYMBOL, 37),
                (MISSING_END_COMMENT_SYMBOL, 42),
            ])
    # end def test_no_end_no_hierarchy

    def test_all_error_no_hierarchy(self):
        """
        test simple cases with all end comments being of a wrong type
        """

        self.generic_test_linting(
            "end-comment/all-error-no-hierarchy.py",
            [
                (WRONG_END_COMMENT_SYMBOL, 5),
                (WRONG_END_COMMENT_SYMBOL, 9),
                (WRONG_END_COMMENT_SYMBOL, 13),
                (WRONG_END_COMMENT_SYMBOL, 17),
                (WRONG_END_COMMENT_SYMBOL, 21),
                (WRONG_END_COMMENT_SYMBOL, 25),
                (WRONG_END_COMMENT_SYMBOL, 29),
                (WRONG_END_COMMENT_SYMBOL, 33),
            ])
    # end def test_all_error_no_hierarchy

    def test_all_error_name_end_no_hierarchy(self):
        """
        test simple cases with all string with a name having the wrong name
        """

        self.generic_test_linting(
            "end-comment/all-name-error-no-hierarchy.py",
            [
                (WRONG_END_COMMENT_SYMBOL, 5),
                (WRONG_END_COMMENT_SYMBOL, 9),
                (WRONG_END_COMMENT_SYMBOL, 13),
                (WRONG_END_COMMENT_SYMBOL, 17),
            ])
    # end def test_all_error_name_end_no_hierarchy

    def test_no_error_hierarchy(self):
        """
        test hierarchical cases without errors
        """

        self.generic_test_linting(
            "end-comment/no-error-hierarchy.py",
            [])
    # end def test_no_error_hierarchy

    def test_all_error_hierarchy(self):
        """
        test hierarchical cases with all end comments being of a wrong type
        """
        self.generic_test_linting(
            "end-comment/all-error-hierarchy.py",
            [
                (WRONG_END_COMMENT_SYMBOL, 9),
                (WRONG_END_COMMENT_SYMBOL, 13),
                (WRONG_END_COMMENT_SYMBOL, 14),
                (WRONG_END_COMMENT_SYMBOL, 15),
                (WRONG_END_COMMENT_SYMBOL, 16),
                (WRONG_END_COMMENT_SYMBOL, 21),
                (WRONG_END_COMMENT_SYMBOL, 22),
                (WRONG_END_COMMENT_SYMBOL, 27),
                (WRONG_END_COMMENT_SYMBOL, 36),
                (WRONG_END_COMMENT_SYMBOL, 37),
                (WRONG_END_COMMENT_SYMBOL, 38),
            ])
    # end def test_all_error_hierarchy

    def test_no_comments_hierarchy(self):
        """
        test hierarchical cases with no comments

        Note: this tests the current behaviour, which for this case should
            be improved as we miss some messages due to loosing synch
        """

        self.generic_test_linting(
            "end-comment/no-comments-hierarchy.py",
            [
                (MISSING_END_COMMENT_SYMBOL, 10),
                (MISSING_END_COMMENT_SYMBOL, 13),
                (MISSING_END_COMMENT_SYMBOL, 13), # the new mechanism mention the ``if`` independently
                (MISSING_END_COMMENT_SYMBOL, 17),
                (MISSING_END_COMMENT_SYMBOL, 18),
                # (MISSING_END_COMMENT_SYMBOL, 21), # this detection fails due to synch loss
                (MISSING_END_COMMENT_SYMBOL, 28),
            ])
    # end def test_no_comments_hierarchy

    def test_allowed_edge_case_above_elif_except(self):
        """
        Test a scenario where a comment is allowed above multiple elif or except blocks.
        """

        self.generic_test_linting(
            "end-comment/allowed-edge-case-above-elif-except.py",
            [])
    # end def test_allowed_edge_case_above_elif_except

    def test_end_if_before_end(self):
        """
        test hierarchical where the end comment arrives before the end of the block
        """

        self.generic_test_linting(
            "end-comment/end_if_before_end.py",
            [
                (END_COMMENT_TOO_EARLY_SYMBOL, 6),
                (END_COMMENT_TOO_EARLY_SYMBOL, 18),
                (END_COMMENT_TOO_EARLY_SYMBOL, 29),
            ])
    # end def test_end_if_before_end
# end class EndCommentCheckerTest


if __name__ == '__main__':
    unittest.main()
# end if

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
