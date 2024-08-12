#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: method_test_exception_no_error
:brief: sample file where method has exceptions raised by rest methods
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
        self.assertTrue(on, "test failed")
    # end def _generic_method

    def test_method(self):
        """
        Test method
        """
        self._generic_method(True)
        self.assertTrue(True, "test failed")
    # end def test_method
# end class TestClass
