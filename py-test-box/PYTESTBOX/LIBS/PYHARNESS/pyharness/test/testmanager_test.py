#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.test.testmanager

@brief  Testing of TestManager

@author christophe Roquebert

@date   2018/06/08
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.arguments                 import KeywordArguments
from pyharness.testmanager               import CollectListener
from pyharness.testmanager               import LocalTestManager
from pyharness.testmanager               import TestDescriptor
from pyharness.testmanager               import TestManager
from pyharness.testmanager               import VersionDescriptor
from unittest                           import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class TestDescriptorTestCase(TestCase):
    '''
    Testing class for TestDescriptor
    '''

    Descriptor = TestDescriptor

    @classmethod
    def _createDescriptor(cls, testId   = 'testDefault'):
        '''
        Create a Descriptor instance

        @option testId [in] (string) Test identifier

        @return (object) Descriptor instance
        '''
        return cls.Descriptor(testId)

    # end def _createDescriptor

    def testGetType(self):
        '''
        Tests getType method
        '''
        descriptor = self._createDescriptor()

        self.assertEqual(self.Descriptor.TYPE_UNKNOWN,
                         descriptor.getType(),
                         'Wrong Type value')

    # end def testGetType

    def testGetSetParent(self):
        '''
        Tests getParent and setParent methods
        '''
        descriptor = self._createDescriptor('testChild')
        parentDescriptor = self._createDescriptor('testParent')

        self.assertIsNone(descriptor.getParent(),
                          'Wrong parent value')

        descriptor.setParent(parentDescriptor)

        self.assertEqual(parentDescriptor,
                         descriptor.getParent(),
                         'Wrong Parent value')

    # end def testGetSetParent

    def testGetSetState(self):
        '''
        Tests getState and setState methods
        '''
        descriptor = self._createDescriptor('testChild')
        parentDescriptor = self._createDescriptor('testParent')
        descriptor.setParent(parentDescriptor)

        self.assertEqual(self.Descriptor.STATE_UNKNOWN,
                         descriptor.getState(),
                         'Wrong state value')

        descriptor.setState(self.Descriptor.STATE_SUCCESS)

        self.assertEqual(self.Descriptor.STATE_SUCCESS,
                         descriptor.getState(),
                         'Wrong state value')

        self.assertEqual(self.Descriptor.STATE_SUCCESS,
                         parentDescriptor.getState(),
                         'Wrong state value')

    # end def testGetSetState

    def testUpdateState(self):
        '''
        Tests updateState method
        '''
        descriptor = self._createDescriptor()
        childDescriptor1 = self._createDescriptor()
        childDescriptor2 = self._createDescriptor()

        descriptor.setState(self.Descriptor.STATE_ERROR)
        childDescriptor1.setState(self.Descriptor.STATE_MISSING)
        childDescriptor2.setState(self.Descriptor.STATE_RUNNING)

        descriptor.addChild(childDescriptor1)
        descriptor.addChild(childDescriptor2)

        descriptor.updateState(None)

        self.assertEqual(self.Descriptor.STATE_RUNNING,
                         descriptor.getState(),
                         'Wrong state update')

        descriptor.setState(self.Descriptor.STATE_SUCCESS)
        descriptor.updateState(self.Descriptor.STATE_SUCCESS)

        self.assertEqual(self.Descriptor.STATE_SUCCESS,
                         descriptor.getState(),
                         'Wrong state update')

    # end def testUpdateState

    def testAddGetRemoveChild(self):
        '''
        Tests addChild, getChildren and removeChild methods
        '''
        descriptor = self._createDescriptor()
        childDescriptor1 = self._createDescriptor()
        childDescriptor2 = self._createDescriptor()

        self.assertEqual(tuple(),
                         descriptor.getChildren(),
                         'Wrong children list')

        descriptor.addChild(childDescriptor1)
        descriptor.addChild(childDescriptor2)

        self.assertEqual((childDescriptor1, childDescriptor2),
                         descriptor.getChildren(),
                         'Wrong children list')

        self.assertEqual(descriptor,
                         childDescriptor1.getParent(),
                         'Wrong parent reference')

        self.assertEqual(descriptor,
                         childDescriptor2.getParent(),
                         'Wrong parent reference')

        descriptor.removeChild(childDescriptor1)

        self.assertEqual((childDescriptor2,),
                         descriptor.getChildren(),
                         'Wrong children list')

        self.assertIsNone(childDescriptor1.getParent(),
                          'Wrong parent reference')

        self.assertEqual(descriptor,
                         childDescriptor2.getParent(),
                         'Wrong parent reference')

    # end def testAddGetRemoveChild

    def testToStringRepr(self):
        '''
        Tests __toString, __str__ and __repr__ methods
        '''
        parentId = 'testParentId'
        childId1 = 'testChildId1'
        childId2 = 'testChildId2'
        descriptor = self._createDescriptor(parentId)
        childDescriptor1 = self._createDescriptor(childId1)
        childDescriptor2 = self._createDescriptor(childId2)

        descriptor.addChild(childDescriptor1)
        descriptor.addChild(childDescriptor2)

        expected = '\n'.join((parentId,
                              "   " + childId1,
                              "   " + childId2,
                              ))

        self.assertEqual(expected,
                         str(descriptor),
                         'Wrong string representation')

        self.assertEqual(expected,
                         descriptor.__repr__(),
                         'Wrong string representation')

    # end def testToStringRepr

    def testDeepClone(self):
        '''
        Tests deepClone method
        '''
        parentId = 'testParentId'
        childId1 = 'testChildId1'
        childId2 = 'testChildId2'
        descriptor = self._createDescriptor(parentId)
        childDescriptor1 = self._createDescriptor(childId1)
        childDescriptor2 = self._createDescriptor(childId2)

        descriptor.setState(self.Descriptor.STATE_RUNNING)
        descriptor.addChild(childDescriptor1)
        descriptor.addChild(childDescriptor2)

        descriptor2 = descriptor.deepClone()

        self.assertEqual(str(descriptor),
                         str(descriptor2),
                         'Wrong cloning result')

        self.assertEqual(descriptor.getState(),
                         descriptor2.getState(),
                         'Wrong cloning result')

    # end def testDeepClone

# end class TestDescriptorTestCase

class VersionDescriptorTestCase(TestCase):
    '''
    Testing class for VersionDescriptor
    '''

    Descriptor = VersionDescriptor

    @classmethod
    def _createDescriptor(cls, name = 'version'):
        '''
        Create a Descriptor instance

        @option name [in] (string) Name of the version

        @return (object) Descriptor instance
        '''
        return cls.Descriptor(name)

    # end def _createDescriptor

    def testFlatten(self):
        '''
        Tests flatten method
        '''
        name = 'myName'
        childName1 = 'child1'
        childName2 = 'child2'
        descriptor = self._createDescriptor(name)
        childDescriptor1 = self._createDescriptor(childName1)
        childDescriptor2 = self._createDescriptor(childName2)

        self.assertEqual([name,],
                         descriptor.flatten(),
                         'Wrong flatten result')

        descriptor.children = [childDescriptor1, childDescriptor2]

        self.assertEqual([name + '/' + childName1, name + '/' + childName2],
                         descriptor.flatten(),
                         'Wrong flatten result')

    # end def testFlatten

    def testStr(self):
        '''
        Tests __str__ method
        '''
        name = 'myName'
        descriptor = self._createDescriptor(name)

        self.assertEqual(name,
                         str(descriptor),
                         'Wrong String representation')

    # end def testStr

# end class VersionDescriptorTestCase

class CollectListenerTestCase(TestCase):
    '''
    Tests CollectListener class
    '''

    Listener    = CollectListener
    Descriptor  = TestDescriptor

    @classmethod
    def _createListener(cls):
        '''
        Create a Listener instance

        @return (TestListener) Listenenr instance
        '''
        return cls.Listener()
    # end def _createListener

    @classmethod
    def _createDescriptor(cls, testId   = 'testDefault'):
        '''
        Create a Descriptor instance

        @option testId [in] (string) Test identifier

        @return (object) Descriptor instance
        '''
        return cls.Descriptor(testId)

    # end def _createDescriptor

    def testStartStopTest(self):
        '''
        Tests startTest and stopTest methods
        '''
        listener = self._createListener()

        listener.startTest(self)

        descriptor = self._createDescriptor(self.id())

        self.assertEqual(str(descriptor),
                         str(listener.descriptorStack[1]),
                         'Wrong descriptor created')

        listener.stopTest(self)

        self.assertEqual(1,
                         len(listener.descriptorStack),
                         'Wrong stopping')

    # end def testStartStopTest

# end class CollectListenerTestCase

class TestManagerTestCase(TestCase):
    '''
    Tests TestManager class
    '''

    Manager = TestManager

    @classmethod
    def _createManager(cls, kwArgs = None):
        '''
        Create a TestManager instance

        @option kwArgs [in] (dict) Keywords arguments

        @return (TestManager) TestManager instance
        '''
        if (kwArgs is None):
            kwArgs = KeywordArguments.DEFAULT_ARGUMENTS.copy()
        # end if

        return cls.Manager(kwArgs)

    # end def _createManager

    def testNotImplemented(self):
        '''
        Tests not implemented methods
        '''
        manager = self._createManager()

        self.assertRaises(NotImplementedError,
                          manager.getSubSystemDefinitionAndInstantiations)

        self.assertRaises(NotImplementedError,
                          manager.hasTestDescriptor,
                          self.id())

        self.assertRaises(NotImplementedError,
                          manager.getTestDescriptor,
                          self.id())

        self.assertRaises(NotImplementedError,
                          manager.getTestState,
                          self.id())

        self.assertRaises(NotImplementedError,
                          manager.getTestStates,
                          (self.id(), self.id()))

        self.assertRaises(NotImplementedError,
                          manager.getTestHistory,
                          self.id())

        self.assertRaises(NotImplementedError,
                          manager.getStaticTestCases,
                          self.id())

        self.assertRaises(NotImplementedError,
                          manager.getTestLogPath,
                          self.id())

        self.assertRaises(NotImplementedError,
                          manager.getTestLog,
                          self.id())

        self.assertRaises(NotImplementedError,
                          manager.getTestSourceFile,
                          self.id())

        self.assertRaises(NotImplementedError,
                          manager.getTestSourceLine,
                          self.id())

        self.assertRaises(NotImplementedError,
                          manager.setSelectedConfig,
                          'product', 'variant', 'target', 'mode')

        self.assertRaises(NotImplementedError,
                          manager.getAvailableModes)

        self.assertRaises(NotImplementedError,
                          manager.getSelectedMode)

        self.assertRaises(NotImplementedError,
                          manager.setSelectedMode,
                          'mode')

        self.assertRaises(NotImplementedError,
                          manager.getAvailableProducts)

        self.assertRaises(NotImplementedError,
                          manager.getSelectedProduct)

        self.assertRaises(NotImplementedError,
                          manager.setSelectedProduct,
                          'product')

        self.assertRaises(NotImplementedError,
                          manager.getAvailableVariants)

        self.assertRaises(NotImplementedError,
                          manager.getSelectedVariant)

        self.assertRaises(NotImplementedError,
                          manager.setSelectedVariant,
                          'variant')

        self.assertRaises(NotImplementedError,
                          manager.getSelectedTarget)

        self.assertRaises(NotImplementedError,
                          manager.setSelectedTarget,
                          'target')

        self.assertRaises(NotImplementedError,
                          manager.getAvailableLevels,
                          self.id())

        self.assertRaises(NotImplementedError,
                          manager.resetTests,
                          (self.id(), self.id()))

        self.assertRaises(NotImplementedError,
                          manager.run,
                          (self.id(), self.id()))

        self.assertRaises(NotImplementedError,
                          manager.pause)

        self.assertRaises(NotImplementedError,
                          manager.stop)

        self.assertRaises(NotImplementedError,
                          manager.resume)

    # end def testNotImplemented

    def testClearCache(self):
        '''
        Tests clearCache method
        '''
        manager = self._createManager()

        manager.descriptorCache = {'element': 'value'}

        manager.clearCache()

        self.assertEqual({},
                         manager.descriptorCache,
                         'Wrong descriptorCache value')

    # end def testClearCache

# end class TestManagerTestCase

class LocalTestManagerTestCase(TestManagerTestCase):
    '''
    Tests LocalTestManager class
    '''

    Manager = LocalTestManager

    def testNotImplemented(self):
        '''
        copydoc pyharness.test.testmanager.TestManagerTestCase.testNotImplemented
        '''
        pass
    # end def testNotImplemented

# end class LocalTestManagerTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
