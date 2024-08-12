#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.test.subsystemcomposite

@brief  Testing fo Composite definition for all SubSystem classes

@author christophe Roquebert

@date   2018/06/06
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.subsystem.subsystemcomposite   import SubSystemComposite
from unittest                               import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class SubSystemStub(object):
    '''
    SubSystem stub class
    '''
# end class SubSystemStub

class SubSystemCompositeStub(SubSystemComposite):
    '''
    SubSystemComposite Stub
    '''
    ClassReference = SubSystemStub
# end class SubSystemCompositeStub

class SubSystemCompositeTestCase(TestCase):
    '''
    Testing class for SubSystemComposite
    '''

    Composite       = SubSystemCompositeStub
    SubSystemStub   = SubSystemStub

    @classmethod
    def _createComposite(cls):
        '''
        Create a composite instance

        @return (SubSystemComposite) SubSystemComposite instance
        '''
        return cls.Composite()
    # end def _createComposite

    def testAdd(self):
        '''
        Tests the add method
        '''
        child = self.SubSystemStub()
        composite = self._createComposite()

        composite.add(child)

        self.assertEqual(child,
                         composite.getChild(0),
                         'Wrong child added')

    # end def testAdd

    def testAdd_WrongType(self):
        '''
        Tests add method with a wrong type parameter
        '''
        composite = self._createComposite()

        self.assertRaises(TypeError,
                          composite.add,
                          0)

        self.assertRaises(TypeError,
                          composite.add,
                          '0')

        self.assertRaises(TypeError,
                          composite.add,
                          [0, 1])

    # end def testAdd_WrongType

    def testRemove(self):
        '''
        Tests remove method
        '''
        child1 = self.SubSystemStub()
        child2 = self.SubSystemStub()
        composite = self._createComposite()

        composite.add(child1)
        composite.add(child2)

        composite.remove(child1)

        self.assertEqual(child2,
                         composite.getChild(0),
                         'Wrong child removed')

    # end def testRemove

    def testRemove_WrongIndex(self):
        '''
        Tests remove method with unknown child parameter
        '''
        child1 = self.SubSystemStub()
        child2 = self.SubSystemStub()
        child3 = self.SubSystemStub()
        composite = self._createComposite()

        composite.add(child1)
        composite.add(child2)

        self.assertRaises(IndexError,
                          composite.remove,
                          child3)

    # end def testRemove_WrongIndex

    def testGetChild(self):
        '''
        Tests getChild method
        '''
        child1 = self.SubSystemStub()
        child2 = self.SubSystemStub()
        composite = self._createComposite()

        composite.add(child1)
        composite.add(child2)

        self.assertEqual(child1,
                         composite.getChild(0),
                         'Wrong child returned')

        self.assertEqual(child2,
                         composite.getChild(1),
                         'Wrong child returned')

    # end def testGetChild

# end class SubSystemCompositeTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
