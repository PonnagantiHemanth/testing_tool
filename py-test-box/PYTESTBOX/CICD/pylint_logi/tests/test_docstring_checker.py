#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Custom linter
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pylint_logi.tests.test_docstring_checker
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

from pylint_logi.docstring_checker import LogiDocstringChecker
from pylint_logi.tests.checker_tester import CheckerTester


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------


class DocstringCheckerTest(CheckerTester):
    """
    Test cases to check the docstring linting checker
    """
    CHECKER_UNDER_TEST = LogiDocstringChecker

    def test_class_inherited_inner_class(self):
        """
        verify when the class has an inner class that inherits from another class
        """

        self.generic_test_linting(
            "docstring/class_inherited_inner_class.py",
            [])
    # end def test_class_inherited_inner_class

    def test_edge_case_assert_self_assert_equal(self):
        """
        verify when the method has an assert and a self.assert... statement
        """

        self.generic_test_linting(
            "docstring/edge_case_assert_self_assert_equal.py",
            [])
    # end def test_edge_case_assert_self_assert_equal

    def test_edge_case_raise_e(self):
        """
        verify when the method has a raise with an exception
        """

        self.generic_test_linting(
            "docstring/edge_case_raise_e.py",
            [])
    # end def test_edge_case_raise_e
    
    def test_edge_case_reraise_raise(self):
        """
        verify when the method has a reraise with an exception
        """

        self.generic_test_linting(
            "docstring/edge_case_reraise_raise.py",
            [])
    # end def test_edge_case_reraise_raise

    def test_edge_case_refered_multi_line_definition(self):
        """
        verify when the method has a reference after a multi line definition
        """

        self.generic_test_linting(
            "docstring/edge_case_referred_multi_line_definition.py",
            [])
    # end def test_edge_case_refered_multi_line_definition

    def test_init_with_brief(self):
        """
        verify when there is a brief on init method
        """
        self.generic_test_linting(
            "docstring/init_with_brief.py",
            [
                (LogiDocstringChecker.INIT_BRIEF, 14),  # class TestClassBase
                (LogiDocstringChecker.INIT_BRIEF, 27),  # class TestInitWithParam
            ])
    # end def test_init_with_brief

    def test_init_with_return(self):
        """
        Verify when the inits have return description
        """
        self.generic_test_linting(
            "docstring/init_with_return.py",
            [
                (LogiDocstringChecker.INIT_WITH_RETURN, 15,),
                (LogiDocstringChecker.INIT_WITH_RETURN, 30,),
                (LogiDocstringChecker.INIT_WITH_RETURN, 43,),
                (LogiDocstringChecker.INIT_WITH_RETURN, 57,),
            ]
        )
    # end def test_init_with_return

    def test_magic_method_ignore(self):
        """
        Verify when the magic methods are not filled
        """

        self.generic_test_linting(
            "docstring/magic_method_ignore.py",
            [])
    # end def test_magic_method_ignore

    def test_method_duplicate_a_param(self):
        """
        Verify when the methods have a whole parameter duplicated
        """
        self.generic_test_linting(
            "docstring/method_duplicate_a_param.py",
            [
                (LogiDocstringChecker.DUPLICATED_PARAM, 15,
                 ((LogiDocstringChecker.TXT_PARAM, "a"),),
                 ((LogiDocstringChecker.TXT_PARAM, "b"), (LogiDocstringChecker.TXT_PARAM, "c"),)),
                (LogiDocstringChecker.DUPLICATED_PARAM, 31,
                 ((LogiDocstringChecker.TXT_PARAM, "a"),),
                 ((LogiDocstringChecker.TXT_PARAM, "b"), (LogiDocstringChecker.TXT_PARAM, "c"),)),
                (LogiDocstringChecker.DUPLICATED_PARAM, 57,
                 ((LogiDocstringChecker.TXT_PARAM, "a"),),
                 ((LogiDocstringChecker.TXT_PARAM, "b"), (LogiDocstringChecker.TXT_PARAM, "c"),)),
                (LogiDocstringChecker.DUPLICATED_PARAM, 74,
                 ((LogiDocstringChecker.TXT_PARAM, "a"),),
                 ((LogiDocstringChecker.TXT_PARAM, "b"), (LogiDocstringChecker.TXT_PARAM, "c"),)),
                (LogiDocstringChecker.DUPLICATED_PARAM, 102,
                 ((LogiDocstringChecker.TXT_PARAM, "a"),),
                 ((LogiDocstringChecker.TXT_PARAM, "b"), (LogiDocstringChecker.TXT_PARAM, "c"),)),

                (LogiDocstringChecker.DUPLICATED_PARAM, 119,
                 ((LogiDocstringChecker.TXT_PARAM, "sample"),))
            ])
    # end def test_method_duplicate_a_param

    def test_method_duplicate_a_type(self):
        """
        Verify when the methods have only the type of parameter duplicated
        """
        self.generic_test_linting(
            "docstring/method_duplicate_a_type.py",
            [

                (LogiDocstringChecker.DUPLICATED_TYPE, 15,
                 ((LogiDocstringChecker.TXT_TYPE, "a"),),
                 ((LogiDocstringChecker.TXT_TYPE, "b"), (LogiDocstringChecker.TXT_TYPE, "c"),)),
                (LogiDocstringChecker.DUPLICATED_TYPE, 30,
                 ((LogiDocstringChecker.TXT_TYPE, "a"),),
                 ((LogiDocstringChecker.TXT_TYPE, "b"), (LogiDocstringChecker.TXT_TYPE, "c"),)),
                (LogiDocstringChecker.DUPLICATED_TYPE, 55,
                 ((LogiDocstringChecker.TXT_TYPE, "a"),),
                 ((LogiDocstringChecker.TXT_TYPE, "b"), (LogiDocstringChecker.TXT_TYPE, "c"),)),
                (LogiDocstringChecker.DUPLICATED_TYPE, 71,
                 ((LogiDocstringChecker.TXT_TYPE, "a"),),
                 ((LogiDocstringChecker.TXT_TYPE, "b"), (LogiDocstringChecker.TXT_TYPE, "c"),)),
                (LogiDocstringChecker.DUPLICATED_TYPE, 98,
                 ((LogiDocstringChecker.TXT_TYPE, "a"),),
                 ((LogiDocstringChecker.TXT_TYPE, "b"), (LogiDocstringChecker.TXT_TYPE, "c"),)),

                (LogiDocstringChecker.DUPLICATED_TYPE, 114,
                 ((LogiDocstringChecker.TXT_TYPE, "sample"),),),
            ])
    # end def test_method_duplicate_a_type

    def test_method_duplicated_return_rtype(self):
        """
        Verify when the methods duplicated return and rtype fields
        """
        self.generic_test_linting(
            "docstring/method_duplicated_return_rtype.py",
            [
                (LogiDocstringChecker.DUPLICATED_RETURN, 15,),
                (LogiDocstringChecker.DUPLICATED_RETURN, 27,),
                (LogiDocstringChecker.DUPLICATED_RETURN, 53,),
                (LogiDocstringChecker.DUPLICATED_RETURN, 65,),
            ])
    # end def test_method_duplicated_return_rtype

    def test_method_duplicated_rtype(self):
        """
        Verify when the methods duplicated rtype fields
        """
        self.generic_test_linting(
            "docstring/method_duplicated_rtype.py",
            [
                (LogiDocstringChecker.DUPLICATED_RTYPE, 15,),
                (LogiDocstringChecker.DUPLICATED_RTYPE, 26,),
                (LogiDocstringChecker.DUPLICATED_RTYPE, 51,),
                (LogiDocstringChecker.DUPLICATED_RTYPE, 62,),
            ])
    # end def test_method_duplicated_rtype

    def test_method_generator_no_error(self):
        """
        Verify when generator methods have no errors
        """
        self.generic_test_linting(
            "docstring/method_generator_no_error.py",
            [])
    # end def test_method_generator_no_error

    def test_method_inner_method_return(self):
        """
        Verify when the methods have inner methods with return
        """
        self.generic_test_linting(
            "docstring/method_inner_method_return.py",
            [])
    # end def test_method_inner_method_return

    def test_method_missing_raise(self):
        """
        Verify when the methods lack raise in the docstring
        """
        self.generic_test_linting(
            "docstring/method_missing_raise.py",
            [
                (LogiDocstringChecker.RAISE_MISSING, 9,),
            ])
    # end def test_method_missing_raise

    def test_method_missing_return_briefs(self):
        """
        Verify when the methods lack return and rtype briefs
        """
        self.generic_test_linting(
            "docstring/method_missing_return_briefs.py",
            [
                (LogiDocstringChecker.MISSING_RETURN_BRIEF, 15,),
                (LogiDocstringChecker.MISSING_RTYPE_BRIEF, 15,),
                (LogiDocstringChecker.MISSING_RETURN_BRIEF, 25,),
                (LogiDocstringChecker.MISSING_RTYPE_BRIEF, 25,),
                (LogiDocstringChecker.MISSING_RETURN_BRIEF, 49,),
                (LogiDocstringChecker.MISSING_RTYPE_BRIEF, 49,),
                (LogiDocstringChecker.MISSING_RETURN_BRIEF, 59,),
                (LogiDocstringChecker.MISSING_RTYPE_BRIEF, 59,),
            ])
    # end def test_method_missing_return_briefs

    def test_method_missing_return_type(self):
        """
        Verify when the methods lack rtype fields
        """
        self.generic_test_linting(
            "docstring/method_missing_return_type.py",
            [
                (LogiDocstringChecker.MISSING_RTYPE, 15,),
                (LogiDocstringChecker.MISSING_RTYPE, 24,),
                (LogiDocstringChecker.MISSING_RTYPE, 47,),
                (LogiDocstringChecker.MISSING_RTYPE, 56,),
            ])
    # end def test_method_missing_return_type

    def test_method_no_brief(self):
        """
        Verify when the methods don't have a brief
        """
        self.generic_test_linting(
            "docstring/method_no_brief.py",
            [

                (LogiDocstringChecker.METHOD_BRIEF, 19),
                (LogiDocstringChecker.METHOD_BRIEF, 26),
                (LogiDocstringChecker.METHOD_BRIEF, 38),
                (LogiDocstringChecker.METHOD_BRIEF, 47),
                (LogiDocstringChecker.METHOD_BRIEF, 71),
                (LogiDocstringChecker.METHOD_BRIEF, 78),
                (LogiDocstringChecker.METHOD_BRIEF, 92),
                (LogiDocstringChecker.METHOD_BRIEF, 103),
            ])
    # end def test_method_no_brief

    def test_method_no_param_type(self):
        """
        Verify when the methods don't have param and type field
        """
        self.generic_test_linting(
            "docstring/method_no_param_type.py",
            [

                (LogiDocstringChecker.MISSING_PARAM, 14,
                 ((LogiDocstringChecker.TXT_PARAM, "a"),
                  (LogiDocstringChecker.TXT_PARAM, "b"),
                  (LogiDocstringChecker.TXT_PARAM, "c"),
                  )),
                (LogiDocstringChecker.MISSING_PARAM, 21,
                 ((LogiDocstringChecker.TXT_PARAM, "a"),
                  (LogiDocstringChecker.TXT_PARAM, "b"),
                  (LogiDocstringChecker.TXT_PARAM, "c"),
                  )),
                (LogiDocstringChecker.MISSING_PARAM, 37,
                 ((LogiDocstringChecker.TXT_PARAM, "a"),
                  (LogiDocstringChecker.TXT_PARAM, "b"),
                  (LogiDocstringChecker.TXT_PARAM, "c"),
                  )),
                (LogiDocstringChecker.MISSING_PARAM, 45,
                 ((LogiDocstringChecker.TXT_PARAM, "a"),
                  (LogiDocstringChecker.TXT_PARAM, "b"),
                  (LogiDocstringChecker.TXT_PARAM, "c"),
                  )),
                (LogiDocstringChecker.MISSING_PARAM, 64,
                 ((LogiDocstringChecker.TXT_PARAM, "a"),
                  (LogiDocstringChecker.TXT_PARAM, "b"),
                  (LogiDocstringChecker.TXT_PARAM, "c"),
                  )),

                (LogiDocstringChecker.MISSING_PARAM, 73,
                 ((LogiDocstringChecker.TXT_PARAM, "sample"),
                  )),
            ])
    # end def test_method_no_param_type

    def test_method_no_param_type_brief(self):
        """
        Verify when the methods don't have param and type description
        """
        self.generic_test_linting(
            "docstring/method_no_param_type_brief.py",
            [

                (LogiDocstringChecker.MISSING_PARAM_BRIEF, 15,
                 ("*a", "*b", "*c")),
                (LogiDocstringChecker.MISSING_TYPE_BRIEF, 15,
                 ("*a", "*b", "*c")),
                (LogiDocstringChecker.MISSING_PARAM_BRIEF, 29,
                 ("*a", "*b", "*c")),
                (LogiDocstringChecker.MISSING_TYPE_BRIEF, 29,
                 ("*a", "*b", "*c")),
                (LogiDocstringChecker.MISSING_PARAM_BRIEF, 53,
                 ("*a", "*b", "*c")),
                (LogiDocstringChecker.MISSING_TYPE_BRIEF, 53,
                 ("*a", "*b", "*c")),
                (LogiDocstringChecker.MISSING_PARAM_BRIEF, 68,
                 ("*a", "*b", "*c")),
                (LogiDocstringChecker.MISSING_TYPE_BRIEF, 68,
                 ("*a", "*b", "*c")),
                (LogiDocstringChecker.MISSING_PARAM_BRIEF, 94,
                 ("*a", "*b", "*c")),
                (LogiDocstringChecker.MISSING_TYPE_BRIEF, 94,
                 ("*a", "*b", "*c")),
                (LogiDocstringChecker.MISSING_PARAM_BRIEF, 109,
                 ("sample",)),
                (LogiDocstringChecker.MISSING_TYPE_BRIEF, 109,
                 ("sample",)),
            ])
    # end def test_method_no_param_type_brief

    def test_method_no_return(self):
        """
        Verify when the methods lack return and rtype fields
        """
        self.generic_test_linting(
            "docstring/method_no_return.py",
            [
                # missing returns when a NotImplementedError present can't be checked by the linter as it lacks context
                (LogiDocstringChecker.MISSING_RETURN, 43,),
                (LogiDocstringChecker.MISSING_RETURN, 50,),
            ])
    # end def test_method_no_return

    def test_method_no_type(self):
        """
        Verify when the methods don't have type field
        """
        self.generic_test_linting(
            "docstring/method_no_type.py",
            [

                (LogiDocstringChecker.MISSING_TYPE, 15,
                 ((LogiDocstringChecker.TXT_TYPE, "a"),
                  (LogiDocstringChecker.TXT_TYPE, "b"),
                  (LogiDocstringChecker.TXT_TYPE, "c"),
                  )),
                (LogiDocstringChecker.MISSING_TYPE, 26,
                 ((LogiDocstringChecker.TXT_TYPE, "a"),
                  (LogiDocstringChecker.TXT_TYPE, "b"),
                  (LogiDocstringChecker.TXT_TYPE, "c"),
                  )),
                (LogiDocstringChecker.MISSING_TYPE, 47,
                 ((LogiDocstringChecker.TXT_TYPE, "a"),
                  (LogiDocstringChecker.TXT_TYPE, "b"),
                  (LogiDocstringChecker.TXT_TYPE, "c"),
                  )),
                (LogiDocstringChecker.MISSING_TYPE, 58,
                 ((LogiDocstringChecker.TXT_TYPE, "a"),
                  (LogiDocstringChecker.TXT_TYPE, "b"),
                  (LogiDocstringChecker.TXT_TYPE, "c"),
                  )),
                (LogiDocstringChecker.MISSING_TYPE, 81,
                 ((LogiDocstringChecker.TXT_TYPE, "a"),
                  (LogiDocstringChecker.TXT_TYPE, "b"),
                  (LogiDocstringChecker.TXT_TYPE, "c"),
                  )),
                (LogiDocstringChecker.MISSING_TYPE, 94,
                 ((LogiDocstringChecker.TXT_TYPE, "sample"),
                  )),
            ])
    # end def test_method_no_type

    def test_method_raise_deep_in_tree(self):
        """
        Verify when the methods have the raise statements in side branches of the branching tree, without error
        """
        self.generic_test_linting("docstring/method_raise_deep_in_tree.py",
                                  [])
    # end def test_method_raise_deep_in_tree

    def test_method_param_wrong_order(self):
        """
        Verify when the methods don't have param and type description
        """
        self.generic_test_linting(
            "docstring/method_wrong_order_param.py",
            [

                (LogiDocstringChecker.ORDER_PARAM, 15,
                 ("*a", "*c"), ("*b",)),
                (LogiDocstringChecker.ORDER_PARAM, 29,
                 ("*a", "*c"), ("*b",)),
                (LogiDocstringChecker.ORDER_PARAM, 53,
                 ("*a", "*c"), ("*b",)),
                (LogiDocstringChecker.ORDER_PARAM, 68,
                 ("*a", "*c"), ("*b",)),
                (LogiDocstringChecker.ORDER_PARAM, 95,
                 ("*a", "*c"), ("*b",)),
            ])
    # end def test_method_param_wrong_order

    def test_method_self_in_param(self):
        """
        Verify when the methods have description of self parameter
        """
        self.generic_test_linting(
            "docstring/method_self_in_param.py",
            [
                (LogiDocstringChecker.PARAM_UNNEEDED_DESCRIPTION, 15,
                 ("self",)),
                (LogiDocstringChecker.PARAM_UNNEEDED_DESCRIPTION, 23,
                 ("self",)),
                (LogiDocstringChecker.PARAM_UNNEEDED_DESCRIPTION, 33,
                 ("self",)),
                (LogiDocstringChecker.PARAM_UNNEEDED_DESCRIPTION, 49,
                 ("self",)),
                (LogiDocstringChecker.PARAM_UNNEEDED_DESCRIPTION, 61,
                 ("self",)),
                (LogiDocstringChecker.PARAM_UNNEEDED_DESCRIPTION, 87,
                 ("self",)),
                (LogiDocstringChecker.PARAM_UNNEEDED_DESCRIPTION, 95,
                 ("self",)),
                (LogiDocstringChecker.PARAM_UNNEEDED_DESCRIPTION, 106,
                 ("self",)),
                (LogiDocstringChecker.PARAM_UNNEEDED_DESCRIPTION, 123,
                 ("self",)),
                (LogiDocstringChecker.PARAM_UNNEEDED_DESCRIPTION, 137,
                 ("self",)),
                (LogiDocstringChecker.PARAM_UNNEEDED_DESCRIPTION, 166,
                 ("self",)),
            ])
    # end def test_method_self_in_param

    def test_method_test_exception_no_error(self):
        """
        Verify when the methods have exceptions raised by rest methods
        """
        self.generic_test_linting(
            "docstring/method_test_exception_no_error.py",
            [])
    # end def test_method_test_exception_no_error

    def test_method_test_exception_no_raise(self):
        """
        Verify when the methods have exceptions raised by rest methods
        """
        self.generic_test_linting(
            "docstring/method_test_exception_no_raise.py",
            [(LogiDocstringChecker.RAISE_MISSING, 17,),])
    # end def test_method_test_exception_no_raise


    def test_method_type_bottom(self):
        """
        Verify when the methods don't have param and type description
        """
        self.generic_test_linting(
            "docstring/method_type_bottom.py",
            [

                (LogiDocstringChecker.ORDER_TYPE, 15,
                 ("*a", "*b", "*c")),
                (LogiDocstringChecker.ORDER_TYPE, 29,
                 ("*a", "*b", "*c")),
                (LogiDocstringChecker.ORDER_TYPE, 53,
                 ("*a", "*b", "*c")),
                (LogiDocstringChecker.ORDER_TYPE, 68,
                 ("*a", "*b", "*c")),
                (LogiDocstringChecker.ORDER_TYPE, 95,
                 ("*a", "*b", "*c")),
            ])
    # end def test_method_type_bottom

    def test_method_unknown_params(self):
        """
        Verify when the methods have unknown parameters
        """
        self.generic_test_linting(
            "docstring/method_unknown_params.py",
            [
                (LogiDocstringChecker.UNKNOWN_PARAM, 14,
                 ((LogiDocstringChecker.TXT_PARAM, "not_in_prototype"),)),
                (LogiDocstringChecker.UNKNOWN_PARAM, 24,
                 ((LogiDocstringChecker.TXT_PARAM, "not_in_prototype"),)),
                (LogiDocstringChecker.UNKNOWN_PARAM, 40,
                 ((LogiDocstringChecker.TXT_PARAM, "not_in_prototype"),)),
                (LogiDocstringChecker.UNKNOWN_PARAM, 53,
                 ((LogiDocstringChecker.TXT_PARAM, "not_in_prototype"),)),
                (LogiDocstringChecker.UNKNOWN_PARAM, 79,
                 ((LogiDocstringChecker.TXT_PARAM, "not_in_prototype"),)),
                (LogiDocstringChecker.UNKNOWN_PARAM, 87,
                 ((LogiDocstringChecker.TXT_PARAM, "not_in_prototype"),)),
                (LogiDocstringChecker.UNKNOWN_PARAM, 97,
                 ((LogiDocstringChecker.TXT_PARAM, "not_in_prototype"),)),
                (LogiDocstringChecker.UNKNOWN_PARAM, 113,
                 ((LogiDocstringChecker.TXT_PARAM, "not_in_prototype"),)),
                (LogiDocstringChecker.UNKNOWN_PARAM, 126,
                 ((LogiDocstringChecker.TXT_PARAM, "not_in_prototype"),)),
                (LogiDocstringChecker.UNKNOWN_PARAM, 154,
                 ((LogiDocstringChecker.TXT_PARAM, "not_in_prototype"),)),
                (LogiDocstringChecker.UNKNOWN_PARAM, 172,
                 ((LogiDocstringChecker.TXT_PARAM, "not_in_prototype"),)),
                (LogiDocstringChecker.UNKNOWN_PARAM, 186,
                 ((LogiDocstringChecker.TXT_PARAM, "not_in_prototype"),)),
                (LogiDocstringChecker.UNKNOWN_PARAM, 202,
                 ((LogiDocstringChecker.TXT_PARAM, "not_in_prototype"),)),
            ])
    # end def test_method_unknown_params

    def test_method_wrong_code_content_quotes(self):
        """
        Verify when the methods have the wrong type of quote around code elements
        """

        self.generic_test_linting(
            "docstring/wrong_code_content_quotes.py",
            [
                (LogiDocstringChecker.TYPE_HINT_FORMAT_ERROR, 15,
                 ((LogiDocstringChecker.TXT_TYPE, "a"),
                  (LogiDocstringChecker.TXT_TYPE, "b"),
                  (LogiDocstringChecker.TXT_TYPE, "c"),),
                 ),
                (LogiDocstringChecker.RTYPE_FORMAT_ERROR, 29,),
                (LogiDocstringChecker.TYPE_HINT_FORMAT_ERROR, 39,
                 ((LogiDocstringChecker.TXT_TYPE, "a"),
                  (LogiDocstringChecker.TXT_TYPE, "b"),
                  (LogiDocstringChecker.TXT_TYPE, "c"),),
                 ),
                (LogiDocstringChecker.RTYPE_FORMAT_ERROR, 39,),
                (LogiDocstringChecker.TYPE_HINT_FORMAT_ERROR, 63,
                 ((LogiDocstringChecker.TXT_TYPE, "a"),
                  (LogiDocstringChecker.TXT_TYPE, "b"),
                  (LogiDocstringChecker.TXT_TYPE, "c"),),
                 ),
                (LogiDocstringChecker.RTYPE_FORMAT_ERROR, 78,),

                (LogiDocstringChecker.TYPE_HINT_FORMAT_ERROR, 90,
                 ((LogiDocstringChecker.TXT_TYPE, "a"),
                  (LogiDocstringChecker.TXT_TYPE, "b"),
                  (LogiDocstringChecker.TXT_TYPE, "c"),),
                 ),
                (LogiDocstringChecker.RTYPE_FORMAT_ERROR, 90,),
                (LogiDocstringChecker.NO_DOCSTRING, 112),
                (LogiDocstringChecker.NO_DOCSTRING, 115),
                (LogiDocstringChecker.NO_DOCSTRING, 121),
                (LogiDocstringChecker.NO_DOCSTRING, 127),
                (LogiDocstringChecker.NO_DOCSTRING, 133),

                (LogiDocstringChecker.TYPE_HINT_FORMAT_ERROR, 146,
                 ((LogiDocstringChecker.TXT_TYPE, "a"),
                  (LogiDocstringChecker.TXT_TYPE, "b"),
                  (LogiDocstringChecker.TXT_TYPE, "c"),),
                 ),
                (LogiDocstringChecker.TYPE_HINT_FORMAT_ERROR, 162,
                 ((LogiDocstringChecker.TXT_TYPE, "sample"),),
                 ),

                (LogiDocstringChecker.TYPE_HINT_FORMAT_ERROR, 175,
                 ((LogiDocstringChecker.TXT_TYPE, "list_parameter"),
                  (LogiDocstringChecker.TXT_TYPE, "tuple_parameter"),)
                 ),

                (LogiDocstringChecker.TYPE_HINT_FORMAT_ERROR, 187,
                 ((LogiDocstringChecker.TXT_TYPE, "on"),),
                 ),

                (LogiDocstringChecker.RAISE_FORMAT, 187),
            ])
    # end def test_method_wrong_code_content_quotes

    def test_module_brief_multiline(self):
        """
        verify when there is multiple lines in the brief
        """
        self.generic_test_linting(
            "docstring/module_brief_multiline.py",
            []
        )
    # end def test_module_brief_multiline

    def test_module_tool_no_errors(self):
        """
        Verify a case without errors but with a tool generation tag
        """

        self.generic_test_linting(
            "docstring/module_tool_no_error.py",
            [])
    # end def test_module_tool_no_errors

    def test_module_two_authors(self):
        """
        verify when there are two authors in the module brief
        """
        self.generic_test_linting(
            "docstring/module_two_authors.py",
            [])
    # end def test_module_two_authors


    def test_module_wrong_file(self):
        """
        verify when there isn't line break to start with
        """
        self.generic_test_linting(
            "docstring/module_wrong_file.py",
            [
                (LogiDocstringChecker.MODULE_FORMAT, 1, (LogiDocstringChecker.TXT_MODULE_PATH_PACKAGE,)),  # module
            ])
    # end def test_module_wrong_file

    def test_module_wrong_format(self):
        """
        verify when the fields aren't in the right order
        """
        self.generic_test_linting(
            "docstring/module_wrong_format.py",
            [
                (LogiDocstringChecker.MODULE_FORMAT, 1, (LogiDocstringChecker.TXT_MODULE_FORMAT_PACKAGE,
                                                         LogiDocstringChecker.TXT_MODULE_FORMAT_AUTHOR,
                                                         LogiDocstringChecker.TXT_MODULE_FORMAT_DATE)),  # module
            ])
    # end def test_module_wrong_format

    def test_module_wrong_order(self):
        """
        verify when the fields aren't in the right order
        """
        self.generic_test_linting(
            "docstring/module_wrong_order.py",
            [
                (LogiDocstringChecker.MODULE_FORMAT, 1, (LogiDocstringChecker.TXT_MODULE_PLACE_PACKAGE,
                                                         LogiDocstringChecker.TXT_MODULE_PLACE_BRIEF,
                                                         LogiDocstringChecker.TXT_MODULE_PLACE_AUTHOR,
                                                         LogiDocstringChecker.TXT_MODULE_PLACE_DATE)),  # module
            ])
    # end def test_module_wrong_order

    def test_module_wrong_start(self):
        """
        verify when there isn't line break to start a docstring
        """
        self.generic_test_linting(
            "docstring/format_wrong_start.py",
            [
                (LogiDocstringChecker.MODULE_FORMAT, 1, (LogiDocstringChecker.TXT_DOCSTRING_START,)),  # module

                (LogiDocstringChecker.CLASS_FORMAT, 9, (LogiDocstringChecker.TXT_DOCSTRING_START,)),  # TestClassBase

                (LogiDocstringChecker.METHOD_FORMAT, 16, (LogiDocstringChecker.TXT_DOCSTRING_START,)),
                (LogiDocstringChecker.METHOD_FORMAT, 21, (LogiDocstringChecker.TXT_DOCSTRING_START,)),
                (LogiDocstringChecker.METHOD_FORMAT, 34, (LogiDocstringChecker.TXT_DOCSTRING_START,)),
                (LogiDocstringChecker.METHOD_FORMAT, 43, (LogiDocstringChecker.TXT_DOCSTRING_START,)),

                (LogiDocstringChecker.CLASS_FORMAT, 58, (LogiDocstringChecker.TXT_DOCSTRING_START,)),  # TestOverrideRepeatDocs

                (LogiDocstringChecker.METHOD_FORMAT, 66, (LogiDocstringChecker.TXT_DOCSTRING_START,)),
                (LogiDocstringChecker.METHOD_FORMAT, 73, (LogiDocstringChecker.TXT_DOCSTRING_START,)),
                (LogiDocstringChecker.METHOD_FORMAT, 87, (LogiDocstringChecker.TXT_DOCSTRING_START,)),
                (LogiDocstringChecker.METHOD_FORMAT, 98, (LogiDocstringChecker.TXT_DOCSTRING_START,)),

                (LogiDocstringChecker.CLASS_FORMAT, 120, (LogiDocstringChecker.TXT_DOCSTRING_START,)),  # TestInitWithParam

                (LogiDocstringChecker.INIT_FORMAT, 123, (LogiDocstringChecker.TXT_DOCSTRING_START,)),

            ])
    # end def test_module_wrong_start

    def test_no_documentation(self):
        """
        verify when there isn't any doc strings or reference comment
        """

        self.generic_test_linting(
            "docstring/nothing.py",
            [

                (LogiDocstringChecker.NO_DOCSTRING, 1),  # module

                (LogiDocstringChecker.NO_DOCSTRING, 4),  # class TestClassBase

                (LogiDocstringChecker.NO_DOCSTRING, 10),
                (LogiDocstringChecker.NO_DOCSTRING, 14),
                (LogiDocstringChecker.NO_DOCSTRING, 18),
                (LogiDocstringChecker.NO_DOCSTRING, 22),

                (LogiDocstringChecker.NO_DOCSTRING, 28),  # class TestOverride

                (LogiDocstringChecker.NO_DOCSTRING, 34),
                (LogiDocstringChecker.NO_DOCSTRING, 38),
                (LogiDocstringChecker.NO_DOCSTRING, 42),
                (LogiDocstringChecker.NO_DOCSTRING, 46),

                (LogiDocstringChecker.NO_DOCSTRING, 53),  # class TestInitWithParam

                (LogiDocstringChecker.NO_DOCSTRING, 54),

            ])
    # end def test_no_documentation

    def test_no_error(self):
        """
        Verify simple cases without errors
        """

        self.generic_test_linting(
            "docstring/no_error.py",
            [])
    # end def test_no_error

    def test_optional_tag_multi_line(self):
        """
        verify when the optional tag is at multiple position on the param brief
        """
        self.generic_test_linting(
            "docstring/optional_tag_multi_line.py",
            [])
    # end def test_optional_tag_multi_line

    def test_wrong_quote(self):
        """
        verify when the wrong quotation style is used
        """

        self.generic_test_linting(
            "docstring/wrong_quote.py",
            [

                (LogiDocstringChecker.WRONG_QUOTE, 1),  # module

                (LogiDocstringChecker.WRONG_QUOTE, 10),  # class TestClassBase

                (LogiDocstringChecker.WRONG_QUOTE, 19),
                (LogiDocstringChecker.WRONG_QUOTE, 26),
                (LogiDocstringChecker.WRONG_QUOTE, 40),
                (LogiDocstringChecker.WRONG_QUOTE, 51),

                (LogiDocstringChecker.WRONG_QUOTE, 67),  # class TestOverride\

                (LogiDocstringChecker.WRONG_QUOTE, 76),
                (LogiDocstringChecker.WRONG_QUOTE, 84),
                (LogiDocstringChecker.WRONG_QUOTE, 99),
                (LogiDocstringChecker.WRONG_QUOTE, 111),

                (LogiDocstringChecker.WRONG_QUOTE, 133),  # class TestInitWithParam

                (LogiDocstringChecker.WRONG_QUOTE, 138),
            ])
    # end def test_wrong_quote
# end class DocstringCheckerTest


if __name__ == '__main__':
    unittest.main()
# end if

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
