#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.test.sortingtest

@brief Tests of the sorting module

@author christophe.roquebert

@date   2018/09/27
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path import join
from shutil import rmtree
from unittest import TestCase
from xml.dom import minidom

from pyharness.core import TestAccess
from pyharness.manipulator import ContainsOperator
from pyharness.manipulator import LevelsAccessor
from pyharness.manipulator import NilAccessor
from pyharness.manipulator import NilOperator
from pyharness.manipulator import TestIdAccessor
from pyharness.sorting import SimpleSorter
from pyharness.sorting import Sorter
from pyharness.sorting import SortingProfile
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class SorterTestCase(TestCase):                                                                                     # pylint:disable=R0901
    '''
    Tests of the Sorting class, and its derived classes
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
        return Sorter
    # end def _getClass

    def test_Construction(self):
        '''
        Tests the constructor
        '''
        clazz = self._getClass()
        instance = clazz(True)
        self.assertEqual(True,
                         instance.isReversed(),
                         "Invalid reversed state")

        instance.setReversed(False)
        self.assertEqual(False,
                         instance.isReversed(),
                         "Invalid reversed state")

        instance = clazz(False)
        self.assertEqual(False,
                         instance.isReversed(),
                         "Invalid reversed state")
        instance.setReversed(True)
        self.assertEqual(True,
                         instance.isReversed(),
                         "Invalid reversed state")
    # end def test_Construction

    def test_Serialization(self):
        '''
        Tests the serialization to/from XML
        '''

        clazz = self._getClass()

        reverseValues = [True, False]
        combinations = [reverse for reverse in reverseValues]

        for reverse in combinations :

            inputFileName = 'serialization.xml'
            filePath    = join(self._tempDirPath, inputFileName)

            instanceToWrite = clazz(reverse)

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
# end class SorterTestCase

class SimpleSorterTestCase(SorterTestCase):                                                                             # pylint:disable=R0901
    '''
    Tests of the SimpleSorter class
    '''

    @classmethod
    def _getClass(cls):
        '''
        @copydoc pyharness.test.sortingtest.SorterTestCase._getClass
        '''
        return SimpleSorter
    # end def _getClass

    def test_Serialization(self):
        '''
        Tests the serialization to/from XML
        '''

        clazz = self._getClass()

        reverseValues  = [True, False]
        accessorValues = [NilAccessor(), TestIdAccessor(), LevelsAccessor()]
        operatorValues = [NilOperator(), ContainsOperator()]
        combinations   = [(reverse, accessor, operator)
                              for reverse in reverseValues
                              for accessor in accessorValues
                              for operator in operatorValues]

        for reverse, accessor, operator in combinations :

            inputFileName = 'serialization.xml'
            filePath    = join(self._tempDirPath, inputFileName)

            instanceToWrite = clazz(reverse, accessor, operator)

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

    def test_Sorting_Nil(self):
        '''
        Tests the comparison for the Nil operator
        '''

        #          testAccess, value
        testAccess1 = TestAccess('testId',  "1", tuple(), tuple())
        testAccess2 = TestAccess('testId2', "2", tuple(), tuple())

        clazz = self._getClass()
        instance = clazz(False, NilAccessor(), NilOperator())

        self.assertEqual(0,
                         instance(testAccess1, testAccess2),
                         "Invalid comparison")
    # end def test_Sorting_Nil

    def test_Sorting_TestId(self):
        '''
        Tests the comparison for the Nil operator
        '''

        #          testAccess, value
        testAccess1 = TestAccess('testId',  "1", tuple(), tuple())
        testAccess2 = TestAccess('testId2', "2", tuple(), tuple())

        clazz = self._getClass()

        values = ((True, 1),
                  (False, -1))

        for reverse, expected in values:
            instance = clazz(reverse, TestIdAccessor(), NilOperator())

            self.assertEqual(expected,
                             instance(testAccess1, testAccess2),
                             "Invalid comparison")
        # end for
    # end def test_Sorting_TestId

    def test_Sorting_Level(self):
        '''
        Tests the comparison for the Nil operator
        '''

        #          testAccess, value
        testAccess1 = TestAccess('testId',  "2", tuple(), tuple())
        testAccess2 = TestAccess('testId2', "1", tuple(), tuple())

        clazz = self._getClass()

        values = ((True, -1),
                  (False, 1))

        for reverse, expected in values:
            instance = clazz(reverse, LevelsAccessor(), NilOperator())

            self.assertEqual(expected,
                             instance(testAccess1, testAccess2),
                             "Invalid comparison")
        # end for
    # end def test_Sorting_Level
# end class SimpleSorterTestCase

class SortingProfileTestCase(TestCase):                                                                             # pylint:disable=R0901
    '''
    Tests of the SortingProfile class, and its derived classes
    '''

    def setUp(self):
        '''
        Creates a temporary directory
        '''
        TestCase.setUp(self)

        # Create a convenient hierarchy
        self.__tempDirPath = mkdtemp("", "test_%s" % self.id())
    # end def setUp

    def tearDown(self):
        '''
        Cleans up the temporary directory
        '''
        rmtree(self.__tempDirPath, True)

        TestCase.tearDown(self)
    # end def tearDown

    @classmethod
    def _getClass(cls):
        '''
        Obtains the class under test.

        @return The class under test.
        '''
        return SortingProfile
    # end def _getClass

    def test_Compare(self):
        '''
        Tests the comparison method.
        '''

        clazz = self._getClass()

        instances = []
        for _ in range(2):
            profileId = 'profileId'
            sorters   = [SimpleSorter(False, TestIdAccessor(), NilOperator()), SimpleSorter(False, LevelsAccessor(), NilOperator())]

            instance = clazz(profileId, sorters)
            instances.append(instance)
        # end for

        self.assertEqual(instances[0],
                         instances[1],
                         'Invalid comparison')

        instances = []
        for index in range(2):
            profileId = 'profileId'
            sorters   = [SimpleSorter(False, TestIdAccessor(), NilOperator()), SimpleSorter(False, LevelsAccessor(), NilOperator())]

            if (index == 0):
                profileId = 'profileIdModified'
            # end if
            instance = clazz(profileId, sorters)
            instances.append(instance)
        # end for

        self.assertNotEqual(instances[0],
                            instances[1],
                            'Invalid comparison (sorters)')

        instances = []
        for index in range(2):
            profileId = 'profileId'
            sorters   = [SimpleSorter(False, TestIdAccessor(), NilOperator()), SimpleSorter(False, LevelsAccessor(), NilOperator())]

            if (index == 0):
                sorters.reverse()
            # end if
            instance = clazz(profileId, sorters)
            instances.append(instance)
        # end for

        self.assertNotEqual(instances[0],
                            instances[1],
                            'Invalid comparison (sorters)')
    # end def test_Compare

    def test_Serialization(self):
        '''
        Tests the serialization to/from XML
        '''

        clazz = self._getClass()
        profileIdValues = ('profileId', 'profileIdModified')
        sortersValues   = ( [SimpleSorter(False, TestIdAccessor(), NilOperator()), SimpleSorter(False, LevelsAccessor(), NilOperator())],
                            [SimpleSorter(False, LevelsAccessor(), NilOperator()), SimpleSorter(False, TestIdAccessor(), NilOperator())], )
        readOnlyValues  = (True, False)

        combinations = [(profileId, sorters, readOnly)
                            for profileId in profileIdValues
                            for sorters in sortersValues
                            for readOnly in readOnlyValues]

        for profileId, sorters, readOnly in combinations:

            inputFileName = 'serialization.xml'
            filePath    = join(self.__tempDirPath, inputFileName)

            instanceToWrite = clazz(profileId, sorters, readOnly)

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
# end class SortingProfileTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
