#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.files.dynamic

@brief  Classes handling the TESTCASES/*.dynamic file format

@author christophe.roquebert

@date   2018/12/09
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path                  import abspath
from pylibrary.tools.threadutils        import synchronized
from os                                 import R_OK
from os                                 import access

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DynamicFile(object):
    '''
    File handler for the @c dynamic file, generated in the results
    directory.

    It provides a means to remove all validated TestCases for a test id, and
    then add each validated TestCases to the file.
    '''

    NEWTESTMARKER = "|"

    def __init__(self, dynamicPath):
        '''
        Constructor

        @param  dynamicPath [in] (str) Path to the testCases/dynamic file
        '''
        self._testcases = {}
        self._dynamicPath = dynamicPath
    # end def __init__

    def load(self, dynamicPath = None):
        '''
        Loads the dynamic file

        @option dynamicPath [in] (str) The path to the file to load.
        '''

        if (dynamicPath is None):
            dynamicPath = self._dynamicPath
        # end if

        if (access(dynamicPath, R_OK)):
            with open(dynamicPath, "r+") as testCasesFile:
                testCasesLines = testCasesFile.readlines()

                currentTestId = None
                for testCasesLine in testCasesLines:
                    if (testCasesLine.startswith(self.NEWTESTMARKER)):
                        currentTestId = testCasesLine.strip("\n|")
                        self._testcases.setdefault(currentTestId, set())
                    else:
                        testCasesLine = testCasesLine.strip(" \n")
                        if (    (len(testCasesLine) > 0)
                            and (currentTestId is not None)):
                            testCases = self._testcases[currentTestId]

                            # Split the line on double-pipes
                            elements = testCasesLine.split('||', 2)
                            testCase = elements[0]
                            author = len(elements) > 1 and elements[1] or None
                            comment = len(elements) > 2 and elements[2] or None

                            testCases.add((testCase, author, comment))
                        # end if
                    # end if
                # end for
            # end with
        # end if
    # end def load

    def removeTestCases(self, testId):
        '''
        Removes all the testCases from the dynamic file for the specified test id.

        @param  testId [in] (str) Id of the test to modify
        '''
        self._testcases[testId] = None
        del self._testcases[testId]
    # end def removeTestCases

    def addTestCase(self, testId,
                          testCase,
                          author  = None,
                          comment = None):
        '''
        Adds a TestCase in the dynamic file for the specified test id.

        @param  testId    [in] (str) Id of the test to modify
        @param  testCase  [in] (str) TestCase to add
        @param  author    [in] (str) The operator for this TestCase (optional)
        @param  comment   [in] (str) The comment entered by the operator for this testCase
        '''
        testCasesList = self._testcases.setdefault(testId, set())
        testCasesList.add((testCase, author, comment))
    # end def addTestCase

    def getTestCases(self, testId):
        '''
        Obtains the list of testCases for the specified test id.

        @param  testId    [in] (str) Id of the test to obtain

        @return A set(tuple(testCaseId, author, comment))
        '''
        return self._testcases.setdefault(testId, set())
    # end def getTestCases

    def save(self, dynamicPath=None):
        '''
        Saves the file to the specified path.

        @option dynamicPath [in] (str) Path to the file to modify.
        '''

        if (dynamicPath is None):
            dynamicPath = self._dynamicPath
        # end if

        with open(dynamicPath, "w+") as testCasesFile:
            for testId in self._testcases.keys():
                testCasesFile.write("%s%s\n" % (self.NEWTESTMARKER, testId))
                testCases = self._testcases[testId]
                for testCase, author, comment in testCases:
                    if (    (author is None)
                        and (comment is None)):
                        txt = ""

                    else:
                        txt = "||%s||%s" % (author, comment)
                    # end if
                    testCasesFile.write(" %s%s\n" % (testCase, txt))
                # end for
            # end for
        # end with
    # end def save

    DYNAMIC_FILE_CACHE = {}

    @classmethod
    @synchronized
    def create(cls, dynamicPath,
                    erase = False):
        '''
        Creates or obtain a cached instance of a DynamicFile, on the specified path.

        @param  dynamicPath [in] (str) The path to the dynamic file.
        @option erase       [in] (bool) Whether to erase the file or not

        @return (DynamicFile) An instance of the DynamicFile
        '''
        key = abspath(dynamicPath)
        if (    (not erase)
            and (key in cls.DYNAMIC_FILE_CACHE)):
            result = cls.DYNAMIC_FILE_CACHE[key]
        else:
            if (erase):
                open(key, "w").close()
            # end if

            result = cls(key)
            result.load()
            cls.DYNAMIC_FILE_CACHE[key] = result
        # end if

        return result
    # end def create
# end class DynamicFile

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
