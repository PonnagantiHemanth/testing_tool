#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
""" @package autotests.newfeatures.strings

@brief Auto Test of strings manipulation

@author christophe.roquebert

@date   2018/09/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.core import TestCase
import decimal

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------


class TestStringMethods(TestCase):
    """ The unittest module provides a rich set of tools for constructing 
        and running autotests. This section demonstrates that a small subset 
        of the tools suffice to meet the needs of most users. """

    def test_upper(self):
        """ test upper() string methods """
        self.assertEqual('foo'.upper(), 'FOO')
    # end def test_upper

    def test_isupper(self):
        """ test isupper() string methods """
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())
    # end def test_isupper

    def test_split(self):
        """ test split() string methods """
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        self.assertRaises(TypeError, s.split, 2)
    # end def test_split
    
    # PEP 498: Formatted string literals
    def test_formattedStringLiterals(self):
        """ Formatted string literals are prefixed with 'f' 
            and are similar to the format strings accepted 
            by str.format(). 
            They contain replacement fields surrounded by curly braces. 
            The replacement fields are expressions, which are evaluated 
            at run time, and then formatted using the format() protocol: """
        name = "Fred"
        result = f"He said his name is {name}."
        self.assertEqual('He said his name is Fred.', result)
        width = 10
        precision = 4
        value = decimal.Decimal("12.34567")
        result2 = f"result: {value:{width}.{precision}}"  # nested fields
        self.assertEqual('result:      12.35', result2)
    # end def test_formattedStringLiterals
    
# end class TestStringMethods  
         
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
