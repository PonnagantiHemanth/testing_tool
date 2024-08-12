#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
""" @package autotests.newfeatures.literals

@brief Auto Test of numerical literals

@author christophe.roquebert

@date   2018/09/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.core             import TestCase
from pylibrary.tools.hexlist    import HexList
from pylibrary.tools.numeral    import Numeral

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------


class TestLiteralsMethods(TestCase):
    """ The unittest module provides a rich set of tools for constructing 
        and running autotests. This section demonstrates that a small subset 
        of the tools suffice to meet the needs of most users. """
    
    # PEP 515: Underscores in Numeric Literals
    def test_numericLiterals(self):
        """ test the ability to use underscores in numeric literals 
            for improved readability. """
        result = 1_000_000_000_000_000
        self.assertEqual(1000000000000000, result)
        result2 = 0x_FF_FF_FF_FF
        self.assertEqual(4294967295, result2)
        self.assertEqual(HexList('FFFFFFFF'), HexList(Numeral(result2)))
        
        # The string formatting language also now has support for the '_' option 
        # to signal the use of an underscore for a thousands separator for 
        # floating point presentation types and for integer presentation type 'd'. 
        result3 = '{:_}'.format(1000000)
        self.assertEqual('1_000_000', result3)
        # For integer presentation types 'b', 'o', 'x', and 'X', underscores will be 
        # inserted every 4 digits:
        result4 = '{:_x}'.format(0xFFFFFFFF)
        self.assertEqual('ffff_ffff', result4)
    # end def test_numericLiterals
    
# end class TestStringMethods  
         
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
