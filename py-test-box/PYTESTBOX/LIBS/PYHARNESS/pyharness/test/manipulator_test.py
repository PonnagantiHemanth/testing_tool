#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.test.manipulatortest

@brief  Tests of the manipulator module

@author christophe.roquebert

@date   2018/10/15
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path import join
from shutil import rmtree
from unittest import TestCase
from xml.dom import minidom

from pyharness.core import TestAccess
from pyharness.manipulator import Accessor
from pyharness.manipulator import ContainsOperator
from pyharness.manipulator import DurationAccessor
from pyharness.manipulator import EndsWithOperator
from pyharness.manipulator import ImplementedTestCasesAccessor
from pyharness.manipulator import IsGreaterThanOperator
from pyharness.manipulator import IsLessThanOperator
from pyharness.manipulator import LevelsAccessor
from pyharness.manipulator import Manipulator
from pyharness.manipulator import NilAccessor
from pyharness.manipulator import NilOperator
from pyharness.manipulator import Operator
from pyharness.manipulator import StartsWithOperator
from pyharness.manipulator import TestIdAccessor
from pyharness.testmanager import TestDescriptor
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class AbstractOperatorTestCase(TestCase):                                                                                       # pylint:disable=R0901
    '''
    Tests of the Operator class.
    '''

    def setUp(self):
        '''
        Creates a temporary directory
        '''
        TestCase.setUp(self)

        # Create a convenient hierarchy
        self._tempDirPath = mkdtemp("", "test_%s" % self.id())
    # end def setUp

    def tearDown(self):
        '''
        Cleans up the temporary directory
        '''
        rmtree(self._tempDirPath, True)

        TestCase.tearDown(self)
    # end def tearDown

    @classmethod
    def isVirtual(cls):
        '''
        Tests whether the current instance is a virtual test or not.

        @return (bool) Whether the current instance is virtual.
        '''
        return cls.__name__.startswith('Abstract')
    # end def isVirtual

    @classmethod
    def _getClass(cls):
        '''
        Obtains the class under test.

        @return The class under test.
        '''
        return Operator
    # end def _getClass

    def test_Compare(self):
        '''
        Tests the comparison method.
        '''

        clazz = self._getClass()
        expected = clazz()
        obtained = clazz()

        self.assertEqual(expected,
                         obtained,
                         'Invalid comparison')
    # end def test_Compare

    def test_Serialization(self):
        '''
        Tests the serialization to/from XML
        '''

        clazz = self._getClass()

        inputFileName = 'serialization.xml'
        filePath    = join(self._tempDirPath, inputFileName)

        instanceToWrite = clazz()

        xmlDoc = minidom.parseString("<root/>")
        rootElement = xmlDoc.firstChild

        instanceToWrite.toElement(rootElement)

        with open(filePath, "w+") as fileToWrite:
            xmlDoc.writexml(fileToWrite, indent="  ")
        # end with


        xmlDoc = minidom.parse(filePath)
        element = xmlDoc.firstChild.getElementsByTagName(clazz.XML_TAG)[0]

        instanceToRead = clazz.fromElement(element)

        self.assertEqual(instanceToWrite,
                         instanceToRead,
                         "Inconsistent profiles from serialization to deserialization")
    # end def test_Serialization

    def test_accept(self):
        '''
        Test the acceptation method
        '''
        if (not self.isVirtual()):
            raise NotImplementedError
        # end if
    # end def test_accept

# end class AbstractOperatorTestCase

class ContainsOperatorTestCase(TestCase):                                                                           # pylint:disable=R0901
    '''
    Tests of the Operator class.
    '''

    @classmethod
    def _getClass(cls):
        '''
        Obtains the class under test.

        @return The class under test.
        '''
        return ContainsOperator
    # end def _getClass

    def test_accept(self):
        '''
        Test the acceptation method
        '''

        clazz = self._getClass()
        #          (element, container, result)
        vectors = ( ('test', 'thisisatest',         True),
                    ('test', 'thisisnotone',        False),
                    (1,      (1, 2, 3, 4),             True),
                    ('1',    ('1', '2', '3', '4'),     True),
                    ('1',    ('11', '12', '31', '41'), False),
                    )

        instance = clazz()
        for value, entry, result in vectors:
            self.assertEqual(result,
                             instance(entry, value),
                             "Unexpected acceptation for %s" % (clazz.__name__))
        # end for
    # end def test_accept
# end class ContainsOperatorTestCase

class EndsWithOperatorTestCase(TestCase):                                                                           # pylint:disable=R0901
    '''
    Tests of the Operator class.
    '''

    @classmethod
    def _getClass(cls):
        '''
        Obtains the class under test.

        @return The class under test.
        '''
        return EndsWithOperator
    # end def _getClass

    def test_accept(self):
        '''
        Test the acceptation method
        '''

        clazz = self._getClass()
        #          (element, container, result)
        vectors = ( ('test', 'thisisatest',         True),
                    ('test', 'testisnotthere',      False),
                    ('test', 'atestisone',          False),
                    )

        instance = clazz()
        for value, entry, result in vectors:
            self.assertEqual(result,
                             instance(entry, value),
                             "Unexpected acceptation for %s" % (clazz.__name__))
        # end for
    # end def test_accept
# end class EndsWithOperatorTestCase

class StartsWithOperatorTestCase(TestCase):                                                                         # pylint:disable=R0901
    '''
    Tests of the Operator class.
    '''

    @classmethod
    def _getClass(cls):
        '''
        Obtains the class under test.

        @return The class under test.
        '''
        return StartsWithOperator
    # end def _getClass

    def test_accept(self):
        '''
        Test the acceptation method
        '''

        clazz = self._getClass()
        #          (element, container, result)
        vectors = ( ('test', 'thisisatest',         False),
                    ('test', 'testisnotthere',      True),
                    ('test', 'atestisone',          False),
                    )

        instance = clazz()
        for value, entry, result in vectors:
            self.assertEqual(result,
                             instance(entry, value),
                             "Unexpected acceptation for %s" % (clazz.__name__))
        # end for
    # end def test_accept
# end class StartsWithOperatorTestCase

class IsLessThanOperatorTestCase(TestCase):                                                                         # pylint:disable=R0901
    '''
    Tests of the LesThanOperator class.
    '''

    @classmethod
    def _getClass(cls):
        '''
        Obtains the class under test.

        @return The class under test.
        '''
        return IsLessThanOperator
    # end def _getClass

    def test_accept(self):
        '''
        Test the acceptation method
        '''

        clazz = self._getClass()
        #          (element, container, result)
        vectors = ( (1, 2,       True),
                    (2, 1,       False),
                    (None, 1,    False),
                    (1, None,    False),
                    (None, None, False),
                    )

        instance = clazz()
        for entry, value, result in vectors:
            self.assertEqual(result,
                             instance(entry, value),
                             "Unexpected acceptation for %s(%s, %s)" % (clazz.__name__, value, entry))
        # end for
    # end def test_accept
# end class IsLessThanOperatorTestCase

class IsGreaterThanOperatorTestCase(TestCase):                                                                      # pylint:disable=R0901
    '''
    Tests of the GreaterThanOperator class.
    '''

    @classmethod
    def _getClass(cls):
        '''
        Obtains the class under test.

        @return The class under test.
        '''
        return IsGreaterThanOperator
    # end def _getClass

    def test_accept(self):
        '''
        Test the acceptation method
        '''

        clazz = self._getClass()
        #          (element, container, result)
        vectors = ( (1, 2,       False),
                    (2, 1,       True),
                    (None, 1,    False),
                    (1, None,    False),
                    (None, None, False),
                    )

        instance = clazz()
        for entry, value, result in vectors:
            self.assertEqual(result,
                             instance(entry, value),
                             "Unexpected acceptation for %s" % (clazz.__name__))
        # end for
    # end def test_accept
# end class IsGreaterThanOperatorTestCase

class AbstractAccessorTestCase(TestCase):                                                                                   # pylint:disable=R0901
    '''
    Tests of the Operator class.
    '''

    def setUp(self):
        '''
        Creates a temporary directory
        '''
        TestCase.setUp(self)

        # Create a convenient hierarchy
        self._tempDirPath = mkdtemp("", "test_%s" % self.id())
    # end def setUp

    def tearDown(self):
        '''
        Cleans up the temporary directory
        '''
        rmtree(self._tempDirPath, True)

        TestCase.tearDown(self)
    # end def tearDown

    @classmethod
    def isVirtual(cls):
        '''
        Tests whether the current instance is a virtual test or not.

        @return (bool) Whether the current instance is virtual.
        '''
        return cls.__name__.startswith('Abstract')
    # end def isVirtual

    @classmethod
    def _getClass(cls):
        '''
        Obtains the class under test.

        @return The class under test.
        '''
        return Accessor
    # end def _getClass

    def test_Compare(self):
        '''
        Tests the comparison method.
        '''

        clazz = self._getClass()
        expected = clazz()
        obtained = clazz()

        self.assertEqual(expected,
                         obtained,
                         'Invalid comparison')
    # end def test_Compare

    def test_Serialization(self):
        '''
        Tests the serialization to/from XML
        '''

        clazz = self._getClass()

        inputFileName = 'serialization.xml'
        filePath    = join(self._tempDirPath, inputFileName)

        instanceToWrite = clazz()

        xmlDoc = minidom.parseString("<root/>")
        rootElement = xmlDoc.firstChild

        instanceToWrite.toElement(rootElement)

        with open(filePath, "w+") as fileToWrite:
            xmlDoc.writexml(fileToWrite, indent="  ")
        # end with


        xmlDoc = minidom.parse(filePath)
        element = xmlDoc.firstChild.getElementsByTagName(clazz.XML_TAG)[0]

        instanceToRead = clazz.fromElement(element)

        self.assertEqual(instanceToWrite,
                         instanceToRead,
                         "Inconsistent profiles from serialization to deserialization")
    # end def test_Serialization

    def test_GetValue(self):
        '''
        Tests the getValue method of the Accessor class.
        '''
        if (not self.isVirtual()):
            raise NotImplementedError
        # end if
    # end def test_GetValue
# end class AbstractAccessorTestCase

class TestIdAccessorTestCase(AbstractAccessorTestCase):                                                                         # pylint:disable=R0901
    '''
    Tests of the Operator class.
    '''

    @classmethod
    def _getClass(cls):
        '''
        @copydoc pyharness.test.manipulatortest.AbstractAccessorTestCase._getClass
        '''
        return TestIdAccessor
    # end def _getClass

    def test_GetValue(self):
        '''
        Tests the getValue method of the Accessor class.
        '''
        clazz = self._getClass()

        instance = clazz()

        #          testAccess, value
        vectors = ( (TestAccess('testId',  None, tuple(), tuple()), 'testId'),
                    (TestAccess('testId2', None, tuple(), tuple()), 'testId2'),
                    )


        for testAccess, testId in vectors:
            self.assertEqual(testId,
                             instance(testAccess),
                             "Invalid value for accessor %s" % (clazz.__name__))
        # end for
    # end def test_GetValue
# end class TestIdAccessorTestCase

class DurationAccessorTestCase(AbstractAccessorTestCase):                                                                       # pylint:disable=R0901
    '''
    Tests of the DurationAccessor class.
    '''

    @classmethod
    def _getClass(cls):
        '''
        @copydoc pyharness.test.manipulatortest.AbstractAccessorTestCase._getClass
        '''
        return DurationAccessor
    # end def _getClass

    def test_GetValue(self):
        '''
        Tests the getValue method of the Accessor class.
        '''
        clazz = self._getClass()

        instance = clazz()

        #          testAccess, value
        vectors = ( (TestAccess('testId',  None, ((TestDescriptor.STATE_ERROR,
                                                   (2008, 3, 10, 13, 56, 39, 0, 70, -1),
                                                   (2008, 3, 10, 13, 56, 44, 0, 70, -1),
                                                   "Error",),
                                                  (TestDescriptor.STATE_SUCCESS,
                                                   (2008, 3, 10, 13, 56, 39, 0, 70, -1),
                                                   (2008, 3, 10, 13, 56, 49, 0, 70, -1),
                                                   "No comment",),), ('TESTCASE_1',)), 10),
                    (TestAccess('testId2', None, tuple(), tuple()), None),
                    )


        for testAccess, duration in vectors:
            self.assertEqual(duration,
                             instance(testAccess),
                             "Invalid value for accessor %s" % (clazz.__name__))
        # end for
    # end def test_GetValue
# end class DurationAccessorTestCase

class LevelsAccessorTestCase(AbstractAccessorTestCase):                                                                         # pylint:disable=R0901
    '''
    Tests of the LevelsAccessor class.
    '''

    @classmethod
    def _getClass(cls):
        '''
        @copydoc pyharness.test.manipulatortest.AbstractAccessorTestCase._getClass
        '''
        return LevelsAccessor
    # end def _getClass

    def test_GetValue(self):
        '''
        Tests the getValue method of the Accessor class.
        '''
        clazz = self._getClass()

        instance = clazz()

        #          testAccess, value
        vectors = ( (TestAccess('testId',  ('level1', 'level2'), tuple(), ('TESTCASE_1',)),  ('level1', 'level2')),
                    (TestAccess('testId2', tuple(),              tuple(), ('TESTCASE_2',)),               tuple()),
                    )


        for testAccess, expected in vectors:
            self.assertEqual(expected,
                             instance(testAccess),
                             "Invalid value for accessor %s" % (clazz.__name__))
        # end for
    # end def test_GetValue
# end class LevelsAccessorTestCase

class ImplementedTestCasesAccessorTestCase(AbstractAccessorTestCase):                                                            # pylint:disable=R0901
    '''
    Tests of the ImplementedTestCasesAccessor class.
    '''

    @classmethod
    def _getClass(cls):
        '''
        @copydoc pyharness.test.manipulatortest.AbstractAccessorTestCase._getClass
        '''
        return ImplementedTestCasesAccessor
    # end def _getClass

    def test_GetValue(self):
        '''
        Tests the getValue method of the Accessor class.
        '''
        clazz = self._getClass()

        instance = clazz()

        #          testAccess, value
        vectors = ( (TestAccess('testId',  ('level1', 'level2'), tuple(),           tuple()),               tuple()),
                    (TestAccess('testId2', tuple(),              tuple(),  ('TESTCASE_ID',)),      ('TESTCASE_ID',)),
                    )


        for testAccess, expected in vectors:
            self.assertEqual(expected,
                             instance(testAccess),
                             "Invalid value for accessor %s" % (clazz.__name__))
        # end for
    # end def test_GetValue
# end class ImplementedTestCasesAccessorTestCase

class ManipulatorTestCase(TestCase):                                                                                    # pylint:disable=R0901
    '''
    Tests of the Filter class, and its derived classes
    '''

    def setUp(self):
        '''
        Creates a temporary directory
        '''
        TestCase.setUp(self)

        # Create a convenient hierarchy
        self._tempDirPath = mkdtemp("", "test_%s" % self.id())
    # end def setUp

    def tearDown(self):
        '''
        Cleans up the temporary directory
        '''
        rmtree(self._tempDirPath, True)

        TestCase.tearDown(self)
    # end def tearDown

    @classmethod
    def _getClass(cls):
        '''
        Obtains the class under test.

        @return The class under test.
        '''
        return Manipulator
    # end def _getClass

    def test_Construction(self):
        '''
        Tests the constructor
        '''
        clazz = self._getClass()

        accessorValues = [NilAccessor(), TestIdAccessor(), LevelsAccessor()]
        operatorValues = [NilOperator(), ContainsOperator()]
        values         = [None, 1, "3"]

        combinations = [(accessor, operator, value)
                            for accessor in accessorValues
                            for operator in operatorValues
                            for value in values]

        for accessor, operator, value in combinations:

            instance = clazz(accessor=accessor, operator=operator, value=value)

            self.assertEqual(accessor,
                             instance.getAccessor(),
                             "Bad accessor")
            self.assertEqual(operator,
                             instance.getOperator(),
                             "Bad operator")
            self.assertEqual(value,
                             instance.getValue(),
                             "Bad value")
        # end for

    # end def test_Construction

    def test_Serialization(self):
        '''
        Tests the serialization to/from XML
        '''

        clazz = self._getClass()

        accessorValues = [NilAccessor(), TestIdAccessor(), LevelsAccessor()]
        operatorValues = [NilOperator(), ContainsOperator()]
        values         = [None, "test", "3"]

        combinations = [(accessor, operator, value)
                            for accessor in accessorValues
                            for operator in operatorValues
                            for value in values]

        inputFileName = 'serialization.xml'
        filePath    = join(self._tempDirPath, inputFileName)

        for accessor, operator, value in combinations:
            instanceToWrite = clazz(accessor=accessor, operator=operator, value=value)

            xmlDoc = minidom.parseString("<root/>")
            rootElement = xmlDoc.firstChild

            instanceToWrite.toElement(rootElement)

            with open(filePath, "w+") as fileToWrite:
                xmlDoc.writexml(fileToWrite, indent="  ")
            # end with


            xmlDoc = minidom.parse(filePath)
            element = xmlDoc.firstChild.getElementsByTagName(clazz.XML_TAG)[0]

            instanceToRead = clazz.fromElement(element)

            self.assertEqual(instanceToWrite,
                             instanceToRead,
                             "Inconsistent profiles from serialization to deserialization")
        # end for
    # end def test_Serialization
# end class ManipulatorTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
