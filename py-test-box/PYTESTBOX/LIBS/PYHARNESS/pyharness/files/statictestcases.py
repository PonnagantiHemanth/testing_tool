#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.files.statictestcases

@brief Classes handling the static analysis result file format

@author christophe.roquebert

@date   2018/03/17
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class StaticFile(object):
    '''
    Represents the contents of a static file.
    '''

    def __init__(self, path=None):
        '''
        Constructor.

        @option path [in] (str) Path to the static file.
        '''
        self._path     = path
        self._testCases = {}
    # end def __init__

    def load(self, path=None):
        '''
        Loads the file from the path.

        @option path [in] (str) Path to the file to load

        @return The TestCases, as a dict<testId, tuple<testCaseId,author,comment,reference>>
        '''

        if (path is None):
            path = self._path
        # end if

        with open(self._path, "r") as inputFile:
            lines = inputFile.read()
        # end with

        return self.loadFromString(lines)
    # end def load

    def loadFromString(self, contents):
        '''
        Loads a TestCases file from a string

        @param  contents [in] (str) The file contents.

        @return The TestCases, as a dict<testId, tuple<testCaseId,author,comment,reference>>
        '''

        testId = None
        for line in [line.rstrip() for line in contents.split('\n')]:
            if (line.startswith('|')):
                testId = line[1:].strip()
            elif (line.startswith(' ')):
                testCaseId = None
                author     = None
                comment    = None

                line = line.lstrip()
                if '|' in line:
                    testCaseId, eol = line.split('|', 1)
                    if ('|' in eol):
                        author, comment = eol.split('|', 1)
                    else:
                        author = eol
                    # end if
                else:
                    testCaseId = line
                # end if
                testCases = self._testCases.setdefault(testId, [])
                testCases.append((testCaseId, author, comment))
            # end if
        # end for

        return self._testCases
    # end def loadFromString

    def saveToString(self, testCases = None):
        '''
        Saves the file to a string

        @option testCases [in] (dict<testId, tuple<testCaseId,author,comment>>) The TestCases

        @return (string) The file contents
        '''
        if (testCases is None):
            testCases = self._testCases
        # end if

        lines = []
        keys = list(testCases.keys())
        for key in sorted(keys):
            testCases = testCases[key]

            lines.append('|%s' % key)
            for testCaseId, author, comment in testCases:
                if (comment is not None):
                    line = ' %s|%s|%s' % (testCaseId, author, comment)
                elif (author is not None):
                    line = ' %s|%s' % (testCaseId, author)
                else:
                    line = ' %s' % (testCaseId,)
                # end if

                lines.append(line)
            # end for

            lines.append('')
        # end for

        return '\n'.join(lines)
    # end def saveToString

    def save(self, path      = None,
                   testCases = None):
        '''
        Saves the file to a string

        @option path     [in] (str) Path to the file to save.
        @option testCases [in] (dict<testId, tuple<testCaseId,author,comment>>) The TestCases
        '''
        if (path is None):
            path = self._path
        # end if

        with open(path, 'w+') as outputFile:
            outputFile.write(self.saveToString(testCases))
        # end with
    # end def save

    def update(self, values):
        '''
        Updates the dictionary with new values

        @param  values [in] (dict) A mapping testId -> tuple of TestCases
        '''
        self._testCases.update(values)
    # end def update
# end class StaticFile

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
