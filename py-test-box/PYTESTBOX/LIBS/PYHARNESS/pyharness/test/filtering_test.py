#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.test.filteringtest

@brief Tests of the filtering module

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

from pyharness.filtering import ContainsOperator
from pyharness.filtering import FilteringProfile
from pyharness.filtering import LevelsAccessor
from pyharness.filtering import SimpleFilter
from pyharness.filtering import TestIdAccessor
from pyharness.test.manipulator_test import ManipulatorTestCase
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class SimpleFilterTestCase(ManipulatorTestCase):                                                                        # pylint:disable=R0901
    '''
    Tests of the Filter class, and its derived classes
    '''

    @classmethod
    def _getClass(cls):
        '''
        @copydoc pyharness.test.manipulatortest.ManipulatorTestCase._getClass
        '''
        return SimpleFilter
    # end def _getClass
# end class SimpleFilterTestCase

class FilteringProfileTestCase(TestCase):                                                                           # pylint:disable=R0901
    '''
    Tests of the FilteringProfile class, and its derived classes
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
        return FilteringProfile
    # end def _getClass

    def test_Construction(self):
        '''
        Tests the constructor
        '''
        clazz = self._getClass()
        instance = clazz('customId1', matchMethod=True)
        self.assertEqual(True,
                         instance.getMatchMethod(),
                         "Invalid match all")

        instance.setMatchMethod(False)
        self.assertEqual(False,
                         instance.getMatchMethod(),
                         "Invalid match all")

        instance = clazz('customId2', matchMethod=False)
        self.assertEqual(False,
                         instance.getMatchMethod(),
                         "Invalid match all")
        instance.setMatchMethod(True)
        self.assertEqual(True,
                         instance.getMatchMethod(),
                         "Invalid match all")
    # end def test_Construction

    def test_Compare(self):
        '''
        Tests the comparison method.
        '''

        clazz = self._getClass()

        instances = []
        for _ in range(2):
            profileId = 'profileId'
            filters   = [SimpleFilter(LevelsAccessor(), ContainsOperator(), "First"),
                         SimpleFilter(TestIdAccessor(), ContainsOperator(), "Second"),]
            matchMethod  = False

            instance = clazz(profileId, filters, matchMethod)
            instances.append(instance)
        # end for

        self.assertEqual(instances[0],
                         instances[1],
                         'Invalid comparison')

        instances = []
        for index in range(2):
            profileId = 'profileId'
            filters   = [SimpleFilter(LevelsAccessor(), ContainsOperator(), "First"),
                         SimpleFilter(TestIdAccessor(), ContainsOperator(), "Second"),]
            matchMethod  = False

            if (index == 0):
                profileId = 'profileIdModified'
            # end if
            instance = clazz(profileId, filters, matchMethod)
            instances.append(instance)
        # end for

        self.assertNotEqual(instances[0],
                            instances[1],
                            'Invalid comparison (sorters)')

        self.assertNotEqual(instances[0],
                            instances[1],
                            'Invalid comparison (sorters)')

        instances = []
        for index in range(2):
            profileId = 'profileId'
            filters   = [SimpleFilter(LevelsAccessor(), ContainsOperator(), "First"),
                         SimpleFilter(TestIdAccessor(), ContainsOperator(), "Second"),]
            matchMethod  = False

            if (index == 0):
                filters.reverse()
            # end if
            instance = clazz(profileId, filters, matchMethod)
            instances.append(instance)
        # end for

        self.assertNotEqual(instances[0],
                            instances[1],
                            'Invalid comparison (filters)')

        instances = []
        for index in range(2):
            profileId = 'profileId'
            filters   = [SimpleFilter(LevelsAccessor(), ContainsOperator(), "First"),
                         SimpleFilter(TestIdAccessor(), ContainsOperator(), "Second"),]
            matchMethod  = False

            if (index == 0):
                matchMethod = not matchMethod
            # end if
            instance = clazz(profileId, filters, matchMethod)
            instances.append(instance)
        # end for

        self.assertNotEqual(instances[0],
                            instances[1],
                            'Invalid comparison (matchMethod)')
    # end def test_Compare

    def test_Serialization(self):
        '''
        Tests the serialization to/from XML
        '''

        clazz = self._getClass()
        profileIdValues = ('profileId', 'profileIdModified')
        filtersValues   = ( [SimpleFilter(LevelsAccessor(), ContainsOperator(), "First"),
                             SimpleFilter(TestIdAccessor(), ContainsOperator(), "Second"),],
                            [SimpleFilter(TestIdAccessor(), ContainsOperator(), "Second"),
                             SimpleFilter(LevelsAccessor(), ContainsOperator(), "First"),])
        matchMethodValues  = (FilteringProfile.MATCH_ALL, FilteringProfile.MATCH_ONE, FilteringProfile.MATCH_ADVANCED)
        matchCodeValues    = ("True", "False")
        readOnlyValues  = (True, False)

        combinations = [(profileId, filters, matchMethod, matchCode, readOnly)
                            for profileId in profileIdValues
                            for filters in filtersValues
                            for matchMethod in matchMethodValues
                            for matchCode in matchCodeValues
                            for readOnly in readOnlyValues]

        for profileId, filters, matchMethod, matchCode, readOnly in combinations:


            inputFileName = 'serialization.xml'
            filePath    = join(self.__tempDirPath, inputFileName)

            instanceToWrite = clazz(profileId, filters, matchMethod, matchCode, readOnly)

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
# end class FilteringProfileTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
