#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.test.checks

@brief  Testing module for checks

@author christophe Roquebert

@date   2018/06/03
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from unittest                           import TestCase

from pylibrary.tools.checks            import checkCallable
from pylibrary.tools.checks            import checkType


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class TestClass(object):
    '''
    Testing class for checkType
    '''
    def __init__(self, types = None):
        '''
        Constructor

        @option types [in] (type,tuple) Available types
        '''
        self.types = types
    # end def __init__

    def testCheckType(self, param):
        '''
        Tests parameter type

        @param  param [in] (str) String parameter

        @return (bool) True if @c param is of expected type
        '''
        try:
            checkType(param, self.types)
            result = True
        except TypeError:
            result = False
        except:
            raise
        # end try
        return result
    # end def testCheckType

    @staticmethod
    def testCheckCallable(param):
        '''
        Tests string parameter type

        @param  param [in] (str) String parameter

        @return (bool) True if @c param is of expected type
        '''
        try:
            checkCallable(param)
            result = True
        except TypeError:
            result = False
        except:
            raise
        # end try
        return result
    # end def testCheckCallable
# end class TestClass

class CheckTypeTestCase(TestCase):
    '''
    Testing of checkType
    '''
    RefClass = TestClass

    @classmethod
    def _createInstance(cls, types = None):
        '''
        Create an instance of checkType testing class

        @option types [in] (type,tuple) Available types

        @return (object) instance of checkType testing class
        '''
        return cls.RefClass(types)
    # end def _createInstance

    def testCheckType(self):
        '''
        Tests checkType method
        '''
        instance = self._createInstance(str)
        self.assertTrue(instance.testCheckType('1'))
        self.assertFalse(instance.testCheckType(1))
        self.assertFalse(instance.testCheckType([1, ]))
        self.assertFalse(instance.testCheckType((1, )))
    # end def testCheckType

    def testCheckType_WrongTypes(self):
        '''
        Tests checkType with wrong @c types type
        '''
        instance = self._createInstance(1)
        self.assertRaises(TypeError, instance.testCheckType(1))
    # end def testCheckType_WrongTypes

    def testCheckCallable(self):
        '''
        Tests checkCallable method
        '''
        instance = self._createInstance()
        self.assertTrue(instance.testCheckCallable(lambda: True))
        self.assertFalse(instance.testCheckCallable('1'))
        self.assertFalse(instance.testCheckCallable(1))
        self.assertFalse(instance.testCheckCallable([1, ]))
        self.assertFalse(instance.testCheckCallable((1, )))
    # end def testCheckCallable
# end class CheckTypeTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
