#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.test.stringutils

@brief  StringUtils testing module

@author christophe Roquebert

@date   2018/06/06
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from unittest                           import TestCase

from pylibrary.tools.hexlist            import HexList
from pyharness.subsystem.stringutils      import StringUtils


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class StringUtilsTestCase(TestCase):
    '''
    StringUtils testing class
    '''
    def testStringToPython(self):
        '''
        Tests stringToPython method
        '''
        self.assertEqual('value',
                         StringUtils.stringToPython('value', 'string'),
                         'Wrong conversion result')

        self.assertTrue(StringUtils.stringToPython('true', 'boolean'),
                        'Wrong conversion result')

        self.assertFalse(StringUtils.stringToPython('false', 'boolean'),
                         'Wrong conversion result')

        self.assertEqual(42465,
                         StringUtils.stringToPython('0xA5E1', 'int'),
                         'Wrong conversion result')

        self.assertEqual(1.2,
                         StringUtils.stringToPython('1.2', 'float'),
                         'Wrong conversion result')

        self.assertEqual(HexList('A5 E1'),
                         StringUtils.stringToPython('A5E1', 'hexlist'),
                         'Wrong conversion result')

        self.assertIsNone(StringUtils.stringToPython('none', 'auto'),
                          'Wrong conversion result')

        self.assertIsNone(StringUtils.stringToPython(None, 'auto'),
                          'Wrong conversion result')

        self.assertEqual('{A5E1}',
                         StringUtils.stringToPython('{A5E1}', 'auto'),
                         'Wrong conversion result')

    # end def testStringToPython

    def testPythonToString(self):
        '''
        Tests pythonToString method
        '''
        self.assertEqual('value',
                         StringUtils.pythonToString('value', 'string'),
                         'Wrong conversion result')

        self.assertEqual('true',
                         StringUtils.pythonToString(True, 'boolean'),
                         'Wrong conversion result')

        self.assertEqual('false',
                         StringUtils.pythonToString(False, 'boolean'),
                         'Wrong conversion result')

        self.assertEqual('42465',
                         StringUtils.pythonToString(42465, 'int'),
                         'Wrong conversion result')

        self.assertEqual('1.2',
                         StringUtils.pythonToString(1.2, 'float'),
                         'Wrong conversion result')

        self.assertEqual('A5E1',
                         StringUtils.pythonToString(HexList('A5 E1'), 'hexlist'),
                         'Wrong conversion result')

        self.assertEqual('none',
                         StringUtils.pythonToString(None, 'auto'),
                         'Wrong conversion result')

    # end def testPythonToString

    def testPythonToString_WrongType(self):
        '''
        Tests pythonToString method with wrong parameters
        '''
        self.assertRaises(ValueError,
                          StringUtils.pythonToString,
                          ['list', 'list'], 'auto')
    # end def testPythonToString_WrongType

    def testPythonToRepr(self):
        '''
        Tests pythonToRepr method
        '''
        self.assertEqual("'value'",
                         StringUtils.pythonToRepr('value', 'string'),
                         'Wrong representation result')

        self.assertEqual('True',
                         StringUtils.pythonToRepr(True, 'boolean'),
                         'Wrong representation result')

        self.assertEqual('False',
                         StringUtils.pythonToRepr(False, 'boolean'),
                         'Wrong representation result')

        self.assertEqual('42465',
                         StringUtils.pythonToRepr(42465, 'int'),
                         'Wrong representation result')

        self.assertEqual('1.2',
                         StringUtils.pythonToRepr(1.2, 'float'),
                         'Wrong representation result')

        self.assertEqual("HexList('A5E1')",
                         StringUtils.pythonToRepr(HexList('A5 E1'), 'hexlist'),
                         'Wrong representation result')

        self.assertEqual('None',
                         StringUtils.pythonToRepr(None, 'auto'),
                         'Wrong representation result')

    # end def testPythonToRepr

    def testPythonToRepr_WrongType(self):
        '''
        Tests pythonToRepr method with wrong parameters
        '''
        self.assertRaises(ValueError,
                          StringUtils.pythonToRepr,
                          ['list', 'list'], 'auto')
    # end def testPythonToRepr_WrongType

    def testStringToRepr(self):
        '''
        Tests stringToRepr method
        '''
        self.assertEqual("'value'",
                         StringUtils.stringToRepr('value', 'string'),
                         'Wrong representation result')

        self.assertEqual('True',
                         StringUtils.stringToRepr('true', 'boolean'),
                         'Wrong representation result')

        self.assertEqual('False',
                         StringUtils.stringToRepr('false', 'boolean'),
                         'Wrong representation result')

        self.assertEqual('42465',
                         StringUtils.stringToRepr('42465', 'int'),
                         'Wrong representation result')

        self.assertEqual('1.2',
                         StringUtils.stringToRepr('1.2', 'float'),
                         'Wrong representation result')

        self.assertEqual("HexList('A5E1')",
                         StringUtils.stringToRepr('A5E1', 'hexlist'),
                         'Wrong representation result')

        self.assertEqual("'none'",
                         StringUtils.stringToRepr('none', 'auto'),
                         'Wrong representation result')

    # end def testStringToRepr

    def testStringToRepr_WrongType(self):
        '''
        Tests stringToRepr method with wrong parameters
        '''
        self.assertRaises(ValueError,
                          StringUtils.stringToRepr,
                          ['list', 'list'], 'auto')
    # end def testStringToRepr_WrongType

# end class StringUtilsTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
