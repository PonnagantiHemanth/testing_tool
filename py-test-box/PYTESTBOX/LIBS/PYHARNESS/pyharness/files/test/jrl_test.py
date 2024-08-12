#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.files.test.jrl

@brief  Tests of the JrlFile class

@author christophe.roquebert

@date   2018/11/28
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path import join
from shutil import rmtree
from time import strptime
from unittest import TestCase

from pyharness.files.jrl import JrlFile
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class JrlFileTestCase(TestCase):
    '''
    Tests of the JrlFile class
    '''
    TEST_VECTORS = (("test.id",  "2007-01-02 01:02:03", "2007-01-02 04:05:06", "Failed", "Comment"),
                    ("test.id2", "2007-01-02 01:02:03", "2007-01-02 04:05:06", "Failed", "Comment"),
                    )

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

    def testJrlEntryAsString(self):
        '''
        Test the serialization/deserialization to/from string of the JrlEntry
        '''
        testIdLength = 79
        expectedValues = ("package.module.class.method.log".ljust(testIdLength) + " 1974-07-19 01:23:45 1974-10-01 02:34:56 state   message",
                          "package.module.class.method.log".ljust(testIdLength) + " 1974-07-19 01:23:45 1974-10-01 02:34:56 state",
                          "package.module.class.method.log".ljust(testIdLength) + " 1974-07-19 01:23:45 1974-10-01 02:34:56 ???????",
                          "package.module.class.method.log".ljust(testIdLength) + " 1974-07-19 01:23:45 ....-..-.. ..:..:.. ???????",)

        for expected in expectedValues:
            jrlEntry = JrlFile.JrlEntry.fromString(expected)
            obtained = jrlEntry.toString().strip()

            self.assertEqual(expected,
                             obtained,
                             "Invalid serialization/deserialization")
        # end for
    # end def testJrlEntryAsString

    def test_Load(self):
        '''
        Tests the loading of a simple file
        '''

        index = 0
        for testVector in self.TEST_VECTORS:
            inputFilePath = join(self.__tempDirPath, 'input.%d.jrl' % index)
            with open(inputFilePath, "w+") as inputFile:
                inputFile.write("%s %s %s %s %s" % testVector)
            # end with

            jrlFile = JrlFile.create(inputFilePath)
            testId, testStartDate, testStopDate, testState, testMessage = testVector
            testStartDate = strptime(testStartDate, "%Y-%m-%d %H:%M:%S")
            testStopDate  = strptime(testStopDate,  "%Y-%m-%d %H:%M:%S")

            jrlEntry = jrlFile.getLastEntry(testId)
            self.assertEqual(testId,
                             jrlEntry.getTestId(),
                             "Unexpected test id")

            self.assertEqual(testStartDate,
                             jrlEntry.getTestStartDate(),
                             "Unexpected test start date")

            self.assertEqual(testStopDate,
                             jrlEntry.getTestStopDate(),
                             "Unexpected test stop date")

            self.assertEqual(testState,
                             jrlEntry.getTestState(),
                             "Unexpected test state")

            self.assertEqual(testMessage,
                             jrlEntry.getTestMessage(),
                             "Unexpected test message")

            index += 1
        # end for
    # end def test_Load
# end class JrlFileTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
