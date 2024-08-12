#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: edge_case_assert_self_assert_equal
:brief: sample file where method has exceptions raised by test methods and an assert, edge case that triggered a bug
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/06/17
"""
from unittest import TestCase


class TestClass(TestCase):
    """
    Doc string sample test class
    """

    def _generic_method(self, on):
        """
        Generic method

        :param on: a parameter
        :type on: ``bool``

        :raise ``AssertionError``: on test failure
        """
        assert on, "test failed"
        self.assertTrue(on, "test failed")
    # end def _generic_method
# end class TestClass
