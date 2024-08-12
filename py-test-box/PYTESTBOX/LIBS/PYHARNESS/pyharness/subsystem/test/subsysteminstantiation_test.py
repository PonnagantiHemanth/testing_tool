#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.test.subsysteminstantiationtest

@brief  Tests the instantiation of a subsystem.

@author christophe.roquebert

@date   2018/10/20
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.subsystem.subsysteminstantiation import SubSystemInstantiation
from random                                   import randint
from unittest                                 import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class SubSystemInstantiationTestCase(TestCase):
    '''
    Tests of the SubSystemInstantiation class.
    '''

    @staticmethod
    def _createSubSystemInstantiation(path     = None,
                                      parent   = None,
                                      children = None,
                                      features = None):
        '''
        Creates a subsystem for test purposes

        @option path     [in] (object) path for the new test object
        @option parent   [in] (object) parent for the new test object
        @option children [in] (object) children for the new test object
        @option features [in] (object) features for the new test object

        @return A new instance of a test instantiation
        '''
        if (path is None):
            path = 'TestPath'
        # end if

        if (parent is None):
            parent = SubSystemInstantiation('TestParent')
        # end if

        if (children is None):
            children = tuple()
        # end if

        if (features is None):
            features = tuple()
        # end if

        return SubSystemInstantiation(path     = path,
                                      parent   = parent,
                                      children = children,
                                      features = features)
    # end def _createSubSystemInstantiation

    def _testAttribute(self, propertyName, valueGenerator = lambda: randint(1, 30000)):
        '''
        Tests the propertyName attribute

        @param  propertyName   [in] (str)      Name of the property
        @option valueGenerator [in] (callable) Generator for attribute values
        '''

        accessorSuffix = propertyName[0].upper() + propertyName[1:]
        getterName = 'get%s' % accessorSuffix
        setterName = 'set%s' % accessorSuffix

        # Constructor access
        value = valueGenerator()
        instance = self._createSubSystemInstantiation(**{propertyName: value})
        self.assertEqual(value,
                         getattr(instance, propertyName),
                         'Invalid constructor initialization')

        # Property/getter access
        value = valueGenerator()
        instance = self._createSubSystemInstantiation()
        setattr(instance, propertyName, value)
        self.assertEqual(value,
                         getattr(instance, getterName)(),
                         'Invalid value from property to getter')

        # Setter/property access
        value = valueGenerator()
        instance = self._createSubSystemInstantiation()
        getattr(instance, setterName)(value)
        self.assertEqual(value,
                         getattr(instance, propertyName),
                         'Invalid value from setter to property')
    # end def _testAttribute

    def testPath(self):
        '''
        Tests the path attribute
        '''
        self._testAttribute('path')
    # end def testPath

    def testParent(self):
        '''
        Tests the parent attribute
        '''
        self._testAttribute('parent',
                            lambda: SubSystemInstantiation('Parent' + ''.join([chr(randint(ord('a'), ord('z'))) for _ in range(10)])))
    # end def testParent

    def testFeatures(self):
        '''
        Tests the features attribute
        '''
        self._testAttribute('features',
                            lambda: sorted([SubSystemInstantiation.FeatureInstantiation('Feature' + ''.join([chr(randint(ord('a'), ord('z'))) for _ in range(10)])) for __ in range(randint(1, 5))],
                                           key = lambda x: x.name))
    # end def testFeatures

    def testAddChild(self):
        '''
        Tests the addChild method
        '''
        parent = self._createSubSystemInstantiation('Parent')
        child  = self._createSubSystemInstantiation('Child')

        self.assertEqual(None,
                         child.getParent(),
                         'Non-None parent')
        self.assertNotEqual(parent,
                            child.getParent(),
                            'Invalid parent')

        parent.addChild(child)

        self.assertEqual(parent,
                         child.getParent(),
                         'Non-None parent')
    # end def testAddChild

    def testEqual(self):
        '''
        Tests the __eq__ method
        '''
        element1 = self._createSubSystemInstantiation('SubSystemName',
                                                      features = [SubSystemInstantiation.FeatureInstantiation('FeatureName')])
        element2 = self._createSubSystemInstantiation('SubSystemName',
                                                      features = [SubSystemInstantiation.FeatureInstantiation('FeatureName')])

        self.assertEqual(element1,
                         element2,
                         'Invalid Equality')
    # end def testEqual
# end class SubSystemInstantiationTestCase

class FeatureInstantiationTestCase(TestCase):
    '''
    Tests of the SubSystemInstantiation.FeatureInstantiation class.
    '''

    @staticmethod
    def _createFeatureInstantiation(name    = None,
                                    parent  = None,
                                    value   = None,
                                    ):
        '''
        Creates a subsystem for test purposes

        @option name     [in] (object) name for the new test object
        @option parent   [in] (object) parent for the new test object
        @option value    [in] (str) value for the new test object

        @return A new instance of a feature instantiation
        '''

        if (name is None):
            name = 'TestName'
        # end if

        if (parent is None):
            parent = SubSystemInstantiation('TestParent')
        # end if

        if (value is None):
            value = SubSystemInstantiation('TestValue')
        # end if

        return SubSystemInstantiation.FeatureInstantiation(name   = name,
                                                           parent = parent,
                                                           value  = value,
                                                           )
    # end def _createFeatureInstantiation

    def _testAttribute(self, propertyName, valueGenerator = lambda: randint(1, 30000)):
        '''
        Tests the propertyName attribute

        @param  propertyName   [in] (str)      Name of the property
        @option valueGenerator [in] (callable) Generator for attribute values
        '''

        accessorSuffix = propertyName[0].upper() + propertyName[1:]
        getterName = 'get' + accessorSuffix
        setterName = 'set' + accessorSuffix

        # Constructor access
        value = valueGenerator()
        instance = self._createFeatureInstantiation(**{propertyName: value})
        self.assertEqual(value,
                         getattr(instance, propertyName),
                         'Invalid constructor initialization')

        # Property/getter access
        value = valueGenerator()
        instance = self._createFeatureInstantiation()
        setattr(instance, propertyName, value)
        self.assertEqual(value,
                         getattr(instance, getterName)(),
                         'Invalid value from property to getter')

        # Setter/property access
        value = valueGenerator()
        instance = self._createFeatureInstantiation()
        getattr(instance, setterName)(value)
        self.assertEqual(value,
                         getattr(instance, propertyName),
                         'Invalid value from setter to property')
    # end def _testAttribute

    def testName(self):
        '''
        Tests the name attribute
        '''
        self._testAttribute('name')
    # end def testName

    def testParent(self):
        '''
        Tests the parent attribute
        '''
        self._testAttribute('parent',
                            lambda: SubSystemInstantiation('Parent' + ''.join([chr(randint(ord('a'), ord('z'))) for _ in range(10)])))
    # end def testParent

    def testValue(self):
        '''
        Tests the value attribute
        '''
        self._testAttribute('value')
    # end def testValue

    def testEqual(self):
        '''
        Tests the __eq__ method
        '''
        element1 = self._createFeatureInstantiation('FeatureName',
                                                    value     = 'FeatureValue')
        element2 = self._createFeatureInstantiation('FeatureName',
                                                    value     = 'FeatureValue')

        self.assertEqual(element1,
                         element2,
                         'Invalid Equality')
    # end def testEqual
# end class FeatureInstantiationTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
