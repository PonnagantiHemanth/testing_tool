#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.files.jrl

@brief  Classes handling the Journal.jrl file format.

@author christophe.roquebert

@date   2018/11/28
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path                            import abspath
from pylibrary.tools.threadutils        import synchronized
from os                                 import F_OK
from os                                 import R_OK
from os                                 import access
from os                                 import makedirs
from os.path                            import dirname
from threading                          import RLock
from time                               import localtime
from time                               import strftime
from time                               import strptime

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class JrlFile(object):
    '''
    An image of a Journal file.

    This clas is able to read, write and update the contents of a .jrl file.
    '''
    SYNCHRONIZATION_LOCK = RLock()

    class JrlComment(object):
        '''
        A comment entry in the JRL file

        This is made of:
        - A comment character ('#')
        - A space character (' ')
        - Some text without newlines
        '''

        LINE_LENGTH   = 200

        def __init__(self, text=""):
            '''
            Constructor

            @param  text [in] (str) The default text for this comment
            '''

            self._text = text
            self.dirty = False
        # end def __init__

        @classmethod
        def fromString(cls, line):
            '''
            Parses a JrlComment from a string

            @param  line [in] (str) The string to parse
            @return A new JrlComment
            '''
            result = cls()
            result.setText(line[1:].strip())

            return result
        # end def fromString

        def toString(self):
            '''
            Converts the current object to a string.

            @return (str) The current object, as a string.
            '''
            result = "# %s" % (self._text)

            # Pad the string up to LINE_LENGTH characters
            if len(result) > self.LINE_LENGTH:
                result = result[:self.LINE_LENGTH]
            else:
                result = result.ljust(self.LINE_LENGTH)
            # end if

            return result
        # end def toString

        def setText(self, text):
            '''
            Sets the comment text

            @param  text [in] (str) The text to set
            '''
            self._text = text
            self.dirty = True
        # end def setText

        def getText(self):
            '''
            Obtains the comment text

            @return (str) The comment text
            '''
            return self._text
        # end def getText

        __repr__ = toString
        __str__  = toString
    # end class JrlComment

    class JrlEntry(object):
        '''
        An entry in the JRL file.

        This is made of:
        - A test id (string)
        - A test start date
        - A test stop date
        - A test result
        - A test detail
        '''

        TIME_FORMAT   = "%Y-%m-%d %H:%M:%S"
        LINE_LENGTH   = 200
        TESTID_LENGTH = 79

        STATE_SUCCESS = "Ok"
        STATE_ERROR   = "Error"
        STATE_FAILURE = "Failed"

        def __init__(self, testId,
                           testStartDate,
                           testStopDate = None,
                           testState    = None,
                           testMessage  = None):
            '''
            Constructor

            @param  testId        [in] (str) The test id
            @param  testStartDate [in] (long)   The start date of the test.
            @param  testStopDate  [in] (long)   The stop date of the test (may be None if unknown)
            @param  testState     [in] (str) The test result (may be None if unknown)
            @param  testMessage   [in] (str) The test message (may be None if unknown)
            '''
            self.testId         = testId
            self._testStartDate = testStartDate
            self._testStopDate  = testStopDate
            self._testState     = testState
            self._testMessage   = testMessage

            self.dirty         = True
        # end def __init__

        def getTestStartDate(self):
            '''
            Obtains the testStartDate

            @return the testStartDate
            '''
            return self._testStartDate
        # end def getTestStartDate

        def setTestStartDate(self, testStartDate):
            '''
            Sets the testStartDate
            @param  testStartDate [in] (float) The testStartDate
            '''
            self.dirty         = True
            self._testStartDate = testStartDate
        # end def setTestStartDate

        def getTestStopDate(self):
            '''
            Obtains the testStopDate

            @return the testStopDate
            '''
            return self._testStopDate
        # end def getTestStopDate

        def setTestStopDate(self, testStopDate):
            '''
            Sets the testStopDate
            @param  testStopDate [in] (float) The testStopDate
            '''
            self.dirty         = True
            self._testStopDate = testStopDate
        # end def setTestStopDate

        def getTestState(self):
            '''
            Obtains the testState

            @return the testState
            '''
            return self._testState
        # end def getTestState

        def setTestState(self, testState):
            '''
            Sets the testState
            @param  testState [in] (str) The testState
            '''
            self.dirty         = True
            self._testState = testState
        # end def setTestState

        def getTestId(self):
            '''
            Obtains the testId

            @return the testId
            '''
            return self.testId
        # end def getTestId

        def setTestId(self, testId):
            '''
            Sets the testId

            @param  testId [in] (str) the testId
            '''
            self.dirty  = True
            self.testId = testId
        # end def setTestId

        def getTestMessage(self):
            '''
            Obtains the testMessage

            @return the testMessage
            '''
            return self._testMessage
        # end def getTestMessage

        def setTestMessage(self, testMessage):
            '''
            Sets the testMessage
            @param  testMessage [in] (str) The testMessage
            '''
            self.dirty         = True
            self._testMessage = testMessage
        # end def setTestMessage

        @classmethod
        def fromString(cls, value):
            '''
            Parses a journal entry from a string.
            The string must have the format:
            @code
            <test id> <start date> <stop date> <result> <message>
            @endcode

            @param  value [in] (str) The line to read from.
            @return The new journal line instance
            '''
            # Split the words of the line
            values = value.split(None, 6)
            nbElements = len(values)

            # Extract the test id
            testId        = values[0]
            if (testId.endswith('.log')):
                testId = testId[:-4]
            # end if

            # Extract the test start date
            testStartDate = None
            if (nbElements > 2):
                try:
                    testStartDate = strptime(values[1] + " " + values[2],
                                         "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    pass
                # end try
            # end if

            # Extract optional elements (that may be absent if the test was aborted
            testStopDate = None
            testState    = None
            testMessage  = None

            # Extract the test stop date.
            if (nbElements > 4):
                try:
                    testStopDate = strptime(values[3] + " " + values[4],
                                           "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    testStopDate = None
                # end try
            # end if

            # Extract the test state
            if (nbElements > 5):
                testState = values[5]

                # Extract the test message
                if (nbElements > 6):
                    testMessage = values[6]
                # end if
            # end if

            return cls(testId, testStartDate, testStopDate, testState, testMessage)
        # end def fromString

        def toString(self):
            '''
            Converts the current object to a line, suitable for logging in a jrl file.

            @return The current object, as a string.
            '''

            result = "%(testId)s %(testStartDate)s %(testStopDate)s %(testState)s %(testMessage)s" % \
                {'testId':        (self.testId + '.log').ljust(self.TESTID_LENGTH),
                 'testStartDate': self._testStartDate and strftime(self.TIME_FORMAT, self._testStartDate) or "....-..-.. ..:..:..",
                 'testStopDate':  self._testStopDate  and strftime(self.TIME_FORMAT, self._testStopDate)  or "....-..-.. ..:..:..",
                 'testState':     self._testState and self._testState.ljust(7) or "???????",
                 'testMessage':   self._testMessage or "",
                 }

            # Pad the string up to LINE_LENGTH characters
            if len(result) > self.LINE_LENGTH:
                result = result[:self.LINE_LENGTH]
            else:
                result = result.ljust(self.LINE_LENGTH)
            # end if

            return result
        # end def toString

        __str__ = toString
        __repr__ = toString
    # end class JrlEntry

    def __init__(self, filePath):
        '''
        Constructor.

        @param  filePath [in] (str) The path to the .jrl file
        '''
        self._entries      = []
        self._entriesCache = {}

        self._jrlPath = filePath

        if (not access(self._jrlPath, R_OK)):
            jrlDirPath = dirname(self._jrlPath)
            if (not access(jrlDirPath, F_OK)):
                makedirs(jrlDirPath)
            # end if

            self._createBlankFile(self._jrlPath)
        # end if

        self._loadJrlEntries(self._jrlPath)
    # end def __init__

    @classmethod
    def _createBlankFile(cls, filePath):
        '''
        Creates a blank JrlFile, with its header

        @param  filePath [in] (str) Path to the file to create
        '''
        with open(filePath, "w+b") as jrlFile:

            comments = ('========================================================',
                        'File name: Journal.jrl',
                        '========================================================',
                        )
            lines = [(cls.JrlComment(comment).toString()+'\n').encode('utf-8') for comment in comments]
            jrlFile.writelines(lines)
        # end with
    # end def _createBlankFile

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def _loadJrlEntries(self, path):
        '''
        Loads the JrlEntry instances from a text file

        @param  path [in] (str) The path to the journal.jrl file
        '''

        entries      = []
        entriesCache = {}
        if (access(path, R_OK)):
            with open(path, "r+") as jrlFile:
                lines = jrlFile.readlines()
            # end with

            for line in lines:
                line = line.strip()
                if (len(line) > 0):
                    if (line[0] == '#'):
                        jrlEntry = self.JrlComment.fromString(line)
                    else:
                        jrlEntry = self.JrlEntry.fromString(line)
                        entriesCache.setdefault(jrlEntry.getTestId(), []).append(jrlEntry)
                    # end if
                    entries.append(jrlEntry)
                # end if
            # end for
        # end if

        self._entries      = entries
        self._entriesCache = entriesCache
    # end def _loadJrlEntries

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def _saveJrlEntries(self, path):
        '''
        Saves the JrlEntry instances to a text file.

        This uses the dirty flags of the JrlEntries to only writes JrlEntries that have actually been modified.

        @param  path [in] (str) The path to the journal.jrl file to replace
        '''

        offset = 0
        with open(path, "r+b") as jrlFile:
            for jrlEntry in self._entries:
                if (jrlEntry.dirty):
                    jrlFile.seek(offset)
                    jrlFile.write(jrlEntry.toString().encode('utf8'))
                    jrlFile.write(b'\n')
                    jrlFile.seek(0, 2)
                    jrlEntry.dirty = False
                # end if

                offset += jrlEntry.LINE_LENGTH + 1
            # end for
        # end with
    # end def _saveJrlEntries

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def createEntry(self, testId, testStartTime=None):
        '''
        Creates a new entry for the testId, and use it as the active one.

        @param  testId        [in] (str) The test Id identifying the entry
        @option testStartTime [in] (float) The test start time, usually localTime

        @return (JrlFile.JrlEntry) The newly created entry
        '''
        jrlEntry = self.JrlEntry(testId, testStartTime)
        self._entries.append(jrlEntry)
        self._entriesCache.setdefault(testId, []).append(jrlEntry)

        return jrlEntry
    # end def createEntry

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def addComment(self, text):
        '''
        Creates a new JrlComment entry with the specified comment.

        The comment is split along newlines, and converted to multiple
        JrlComment instances as needed.

        @param  text [in] (str) The text to add.
        '''
        jrlComments = [self.JrlComment(comment) for comment in text.split('\n')]
        for jrlComment in jrlComments:
            jrlComment.dirty = True
        # end for

        self._entries.extend(jrlComments)
    # end def addComment

    def addRunStartComment(self):
        '''
        Adds a new set of comments indicating that a run started.
        '''
        self.addComment("\n".join(("run started on %s" % strftime(self.JrlEntry.TIME_FORMAT, localtime()),
                                   "-----------------------------------------------------------------------------")))
    # end def addRunStartComment

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def getLastEntry(self, testId):
        '''
        Obtains the last valid entry for a testId, or create it if needed.

        @param  testId [in] (str) The test Id identifying the entry

        @return (JrlFile.JrlEntry) The active entry
        '''
        jrlEntry = None

        allEntries = self.getAllEntries(testId)
        if (len(allEntries)):
            jrlEntry = allEntries[-1]
        # end if

        return jrlEntry
    # end def getLastEntry

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def getAllEntries(self, testId):
        '''
        Obtains all the entries for the specified test id

        @param  testId [in] (str) The id of the test to filter out

        @return The entries associated with the test id.
        '''
        jrlEntries = []

        # Is there at least one entry ?
        if (testId in self._entriesCache):
            jrlEntries = self._entriesCache[testId]
        # end if

        return jrlEntries
    # end def getAllEntries

    def load(self, jrlPath=None):
        '''
        Loads the entries from disk

        @option jrlPath [in] (str) The path to save to (use the default if None)
        '''
        if (jrlPath is None):
            jrlPath = self._jrlPath
        # end if

        self._loadJrlEntries(jrlPath)
    # end def load

    def save(self, jrlPath=None):
        '''
        Saves the currently modified entries to disk

        @option jrlPath [in] (str) The path to save to (use the default if None)
        '''
        if (jrlPath is None):
            jrlPath = self._jrlPath
        # end if

        self._saveJrlEntries(jrlPath)
    # end def save

    JRL_FILE_CACHE = {}

    @classmethod
    @synchronized
    def create(cls, jrlPath, erase=False):
        '''
        Creates or obtain a cached instance of a JrlFile, on the specified path.

        @param  jrlPath [in] (str) The path to the journal file.
        @option erase   [in] (bool) Whether to erase the file or not

        @return (JrlFile) An instance of the JrlFile
        '''
        key = abspath(jrlPath)
        if (    (not erase)
            and (key in cls.JRL_FILE_CACHE)):
            result = cls.JRL_FILE_CACHE[key]
        else:
            if (erase):
                cls._createBlankFile(key)
            # end if

            result = cls(key)
            result.load()
            cls.JRL_FILE_CACHE[key] = result
        # end if

        return result
    # end def create
# end class JrlFile

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
