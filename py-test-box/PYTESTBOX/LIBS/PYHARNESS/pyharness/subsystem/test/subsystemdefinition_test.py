#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.test.subsystemdefinitiontest

@brief Tests the definition of a subsystem.

@author christophe.roquebert

@date   2018/10/20
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.subsystem.subsystemdefinition import SubSystemDefinition
from random                                import randint
from unittest                              import TestCase
# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class SubSystemDefinitionTestCase(TestCase):
    '''
    Tests of the SubSystemDefinition class.
    '''

    @staticmethod
    def _createSubSystemDefinition(name      = None,
                                   parent    = None,
                                   doc       = None,
                                   children  = None,
                                   features  = None,
                                   locations = None):
        '''
        Creates a subsystem for test purposes

        @option name      [in] (object) name for the new test object
        @option parent    [in] (object) parent for the new test object
        @option doc       [in] (object) doc for the new test object
        @option children  [in] (object) children for the new test object
        @option features  [in] (object) features for the new test object
        @option locations [in] (object) location for the new test object

        @return A new instance of a test definition
        '''

        if (name is None):
            name = 'TestName'
        # end if

        if (parent is None):
            parent = SubSystemDefinition('TestParent')
        # end if

        if (doc is None):
            doc = 'TestDoc'
        # end if

        if (children is None):
            children = tuple()
        # end if

        if (features is None):
            features = tuple()
        # end if

        if (locations is None):
            locations = ('TestLocation',)
        # end if

        return SubSystemDefinition(name      = name,
                                   parent    = parent,
                                   doc       = doc,
                                   children  = children,
                                   features  = features,
                                   locations = locations)
    # end def _createSubSystemDefinition

    def _testAttribute(self, propertyName, valueGenerator = lambda: randint(1, 30000)):
        '''
        Tests the propertyName attribute

        @param propertyName  [in] (str) Name of the property
        @param valueGenerator [in] (callable) Generator for attribute values
        '''

        accessorSuffix = propertyName[0].upper() + propertyName[1:]
        getterName = 'get' + accessorSuffix
        setterName = 'set' + accessorSuffix

        # Constructor access
        value = valueGenerator()
        instance = self._createSubSystemDefinition(**{propertyName: value})
        self.assertEqual(value,
                         getattr(instance, propertyName),
                         'Invalid constructor initialization')

        # Property/getter access
        value = valueGenerator()
        instance = self._createSubSystemDefinition()
        setattr(instance, propertyName, value)
        self.assertEqual(value,
                         getattr(instance, getterName)(),
                         'Invalid value from property to getter')

        # Setter/property access
        value = valueGenerator()
        instance = self._createSubSystemDefinition()
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
                            lambda: SubSystemDefinition('Parent' + ''.join([chr(randint(ord('a'), ord('z'))) for _ in range(10)])))
    # end def testParent

    def testDoc(self):
        '''
        Tests the doc attribute
        '''
        self._testAttribute('doc')
    # end def testDoc

    def testFeatures(self):
        '''
        Tests the features attribute
        '''

        def generator():
            '''
            Generates a new element

            @return A new element
            '''
            result = [SubSystemDefinition.FeatureDefinition('Feature' + ''.join([chr(randint(ord('a'), ord('z'))) for _ in range(10)])) for __ in range(randint(1, 5))]
            result.append(SubSystemDefinition.FeatureDefinition('Enabled', type='boolean', default='true'))
            return sorted(result,
                          key = lambda x: x.name)
        # end def generator

        self._testAttribute('features', generator)
    # end def testFeatures

    def testLocations(self):
        '''
        Tests the locations attribute
        '''
        self._testAttribute('locations')
    # end def testLocations

    def testAddChild(self):
        '''
        Tests the addChild method
        '''
        parent = self._createSubSystemDefinition('Parent')
        child  = self._createSubSystemDefinition('Child')

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

    def testGetPath(self):
        '''
        Tests the addChild method
        '''
        parent = self._createSubSystemDefinition('Parent')
        child  = self._createSubSystemDefinition('Child')
        parent.addChild(child)

        self.assertEqual('Parent/Child',
                         child.getPath(),
                         'Invalid absolute path')
    # end def testGetPath

    def testEqual(self):
        '''
        Tests the __eq__ method
        '''
        element1 = self._createSubSystemDefinition('SubSystemName',
                                                   doc = 'SubSystemDoc',
                                                   features = [SubSystemDefinition.FeatureDefinition('FeatureName')])
        element2 = self._createSubSystemDefinition('SubSystemName',
                                                   doc = 'SubSystemDoc',
                                                   features = [SubSystemDefinition.FeatureDefinition('FeatureName')])

        self.assertEqual(element1,
                         element2,
                         'Invalid Equality')
    # end def testEqual
# end class SubSystemDefinitionTestCase

class FeatureDefinitionTestCase(TestCase):
    '''
    Tests of the SubSystemDefinition.FeatureDefinition class.
    '''

    @staticmethod
    def _createFeatureDefinition(name    = None,
                                 parent  = None,
                                 doc     = None,
                                 default = None,
                                 type    = None,                                                                        #@ReservedAssignment pylint:disable=W0622
                                 format  = None):                                                                       #@ReservedAssignment pylint:disable=W0622
        '''
        Creates a subsystem for test purposes

        @option name     [in] (object) name for the new test object
        @option parent   [in] (object) parent for the new test object
        @option doc      [in] (object) doc for the new test object
        @option default  [in] (object) default value for the new test object
        @option type     [in] (object) type for the new test object
        @option format   [in] (object) format for the new test object

        @return A new instance of a feature definition
        '''

        if (name is None):
            name = 'TestName'
        # end if

        if (parent is None):
            parent = SubSystemDefinition('TestParent')
        # end if

        if (doc is None):
            doc = 'TestDoc'
        # end if

        if (default is None):
            default = 'TestDefault'
        # end if

        if (type is None):
            type = 'string'                                                                                             #@ReservedAssignment
        # end if

        if (format is None):
            format = 'Test %s value'                                                                                    #@ReservedAssignment
        # end if

        return SubSystemDefinition.FeatureDefinition(name     = name,
                                                     parent   = parent,
                                                     doc      = doc,
                                                     default  = default,
                                                     type     = type,
                                                     format   = format)
    # end def _createFeatureDefinition

    def _testAttribute(self, propertyName,
                             valueGenerator = lambda: randint(1, 30000)):
        '''
        Tests the propertyName attribute

        @param  propertyName   [in] (str)     Name of the property
        @option valueGenerator [in] (callable) Generator for attribute values
        '''

        accessorSuffix = propertyName[0].upper() + propertyName[1:]
        getterName = 'get' + accessorSuffix
        setterName = 'set' + accessorSuffix

        # Constructor access
        value = valueGenerator()
        instance = self._createFeatureDefinition(**{propertyName: value})
        self.assertEqual(value,
                         getattr(instance, propertyName),
                         'Invalid constructor initialization')

        # Property/getter access
        value = valueGenerator()
        instance = self._createFeatureDefinition()
        setattr(instance, propertyName, value)
        self.assertEqual(value,
                         getattr(instance, getterName)(),
                         'Invalid value from property to getter')

        # Setter/property access
        value = valueGenerator()
        instance = self._createFeatureDefinition()
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
                            lambda: SubSystemDefinition('Parent' + ''.join([chr(randint(ord('a'), ord('z'))) for _ in range(10)])))
    # end def testParent

    def testDoc(self):
        '''
        Tests the doc attribute
        '''
        self._testAttribute('doc')
    # end def testDoc

    def testDefault(self):
        '''
        Tests the default attribute
        '''
        self._testAttribute('default')
    # end def testDefault

    def testType(self):
        '''
        Tests the type attribute
        '''
        self._testAttribute('type')
    # end def testType

    def testFormat(self):
        '''
        Tests the format attribute
        '''
        self._testAttribute('format')
    # end def testFormat

    def testEqual(self):
        '''
        Tests the __eq__ method
        '''
        element1 = self._createFeatureDefinition('FeatureName',
                                                 doc     = 'FeatureDoc',
                                                 default = 'FeatureDefault',
                                                 type    = 'FeatureType',
                                                 format  = 'FeatureFormat')
        element2 = self._createFeatureDefinition('FeatureName',
                                                 doc     = 'FeatureDoc',
                                                 default = 'FeatureDefault',
                                                 type    = 'FeatureType',
                                                 format  = 'FeatureFormat')

        self.assertEqual(element1,
                         element2,
                         'Invalid Equality')
    # end def testEqual
# end class FeatureDefinitionTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
