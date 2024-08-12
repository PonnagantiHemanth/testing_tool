#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.files.test.statictestcases

@brief  Tests of the StaticFile class

@author christophe.roquebert

@date   2018/03/17
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path import join
from shutil import rmtree
from unittest import TestCase

from pyharness.files.statictestcases import StaticFile
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class StaticFileTestCase(TestCase):
    '''
    Tests of the StaticFile class
    '''
    TestedClass = StaticFile

    @classmethod
    def _createInstance(cls, path  = None):
        '''
        Create an instance of TestedClass

        @option path [in] (str) Path to the static file.

        @return (StaticFile) StaticFile instance
        '''
        return cls.TestedClass(path)
    # end def _createInstance

    def setUp(self):
        '''
        Create a temporary directory
        '''
        TestCase.setUp(self)

        self.__tempDirPath = mkdtemp("", "test_%s" % self.id())
    # end def setUp

    def tearDown(self):
        '''
        Cleans up the temporary directory
        '''
        rmtree(self.__tempDirPath, True)

        TestCase.tearDown(self)
    # end def tearDown

    def testLoadFromString(self):
        '''
        Loads the static contents from a string
        '''
        vectors = (('\n'.join(("|testId",
                               " testCase1",
                               " testCase2|author2",
                               " testCase3|author3|comment3")),
                    {"testId": [("testCase1", None, None),
                                ("testCase2", "author2", None),
                                ("testCase3", "author3", "comment3"),]}
                   ),
                   )
        for source, expected in vectors:
            staticFile = self._createInstance()
            obtained = staticFile.loadFromString(source)

            self.assertEqual(expected,
                             obtained,
                             "Invalid deserialization")
        # end for
    # end def testLoadFromString

    def testSaveLoad(self):
        '''
        Saves and loads contents to a file
        '''
        vectors = ({"testId": [("testCase1",  None,     None),
                               ("testCase2", "author2", None),
                               ("testCase3", "author3", "comment3"),]},
                   )

        for expected in vectors:
            staticFile = self._createInstance(join(self.__tempDirPath, 'static'))
            staticFile.save(testCases = expected)

            staticFile = self._createInstance(join(self.__tempDirPath, 'static'))
            obtained = staticFile.load()

            self.assertEqual(expected,
                             obtained,
                             "Invalid deserialization from save to load")
        # end for
    # end def testSaveLoad

    def testUpdate(self):
        '''
        Tests the update method
        '''
        testCases = {"testId": [("testCase1",  None,     None),
                               ("testCase2", "author2", None),
                               ("testCase3", "author3", "comment3"),]}
        staticFile = self._createInstance()
        staticFile.update(testCases)
        expected = "\n".join(('|testId',
                              ' testCase1',
                              ' testCase2|author2',
                              ' testCase3|author3|comment3',
                              ''))
        obtained = staticFile.saveToString()
        self.assertEqual(expected, obtained, 'Wrong TestCases update')
    # end def testUpdate

# end class StaticFileTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
