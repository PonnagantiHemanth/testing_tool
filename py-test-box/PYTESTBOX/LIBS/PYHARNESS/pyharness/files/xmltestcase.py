#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.files.xmltestcase

@brief  Classes handling the XML test result file format

@author christophe.roquebert

@date   2018/12/11
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os                                 import F_OK
from os                                 import R_OK
from os                                 import access
from os                                 import makedirs
from os.path                            import dirname
from xml.dom.minidom                    import getDOMImplementation
from xml.dom.minidom                    import parse
from xml.dom.minidom                    import Node
from xml.dom.minidom                    import parseString
from time                               import strftime
from time                               import strptime
from time                               import localtime
from time                               import mktime

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class XmlTestResultFile(object):
    '''
    An image of a XML test case file.

    This class is able to read and write the contents of an XML file containing
    a test result.

    Here is a sample serialized test result
    @code
    <testscript fqn="package.module.ClassName.test_nom_02"
              startdate="2007-01-01 20:00:00"
              stopdate="2007-01-01 20:01:07">
        <description>
            <![CDATA[Sample test description]]>
        </description>

        <error type="&lt;type 'exceptions.ValueError'&gt;"
               message="Message one-liner">
            <![CDATA[Full traceback]]>
        </error>

        <testcases>
        </testcases>

        <perfdata>
        </perfdata>
    </testscript>
    @endcode
    '''

    VERSION_100 = "1.0"
    VERSION_200 = "2.0"
    VERSION_210 = "2.1"

    VERSION = VERSION_210

    TIME_FORMAT_200   = "%Y-%m-%d %H:%M:%S"
    TIME_FORMAT   = "%Y-%m-%dT%H:%M:%S"

    ENCODING = "iso-8859-1"

    def __init__(self, filePath=None):
        '''
        Constructor

        @option filePath [in] (str) Path to the xml file
        '''
        self._xmlPath = filePath

        if (filePath is not None):
            if (not access(self._xmlPath, R_OK)):
                xmlDirPath = dirname(self._xmlPath)
                if (not access(xmlDirPath, F_OK)):
                    makedirs(xmlDirPath)
                # end if
            # end if
        # end if

        self._testId        = None
        self._startDate     = None
        self._stopDate      = None
        self._state         = None
        self._description   = None

        self._exceptionType = None
        self._message       = None
        self._traceback     = None

        self._testCases     = {}
        self._perfData      = {}
    # end def __init__

    def setTestId(self, testId):
        '''
        Sets the test Id

        @param  testId [in] (str) The test id
        '''
        self._testId = testId
    # end def setTestId

    def getTestId(self):
        '''
        Obtains the test Id

        @return the test id
        '''
        return self._testId
    # end def getTestId

    def setStartDate(self, startDate):
        '''
        Sets the start date

        @param  startDate [in] (float) The start date, as given by localtime
        '''
        self._startDate = startDate
    # end def setStartDate

    def getStartDate(self):
        '''
        Obtains the start date

        @return The start date, as given by localtime
        '''
        return self._startDate
    # end def getStartDate

    def setStopDate(self, stopDate):
        '''
        Sets the stop date

        @param  stopDate [in] (float) The stop date, as given by localtime
        '''
        self._stopDate = stopDate
    # end def setStopDate

    def getStopDate(self):
        '''
        Obtains the stop date

        @return The stop date, as given by localtime
        '''
        return self._stopDate
    # end def getStopDate

    def setState(self, state):
        '''
        Sets the test state

        @param  state [in] (str) The test state
        '''
        self._state = state
    # end def setState

    def getState(self):
        '''
        Obtains the test state

        @return The test state
        '''
        return self._state
    # end def getState

    def setDescription(self, description):
        '''
        Sets the description

        @param  description [in] (str) The description
        '''
        self._description = description
    # end def setDescription

    def getDescription(self):
        '''
        Obtains the description

        @return The description
        '''
        return self._description
    # end def getDescription

    def setMessage(self, message):
        '''
        Sets the message

        @param  message [in] (str) The message
        '''
        self._message = message
    # end def setMessage

    def getMessage(self):
        '''
        Obtains the message

        @return The message
        '''
        return self._message
    # end def getMessage

    def setTraceback(self, traceback):
        '''
        Sets the traceback

        @param  traceback [in] (str) The traceback
        '''
        self._traceback = traceback
    # end def setTraceback

    def getTraceback(self):
        '''
        Obtains the traceback

        @return The traceback
        '''
        return self._traceback
    # end def getTraceback

    def setTestCases(self, testCases):
        '''
        Sets the TestCases

        @param  testCases [in] (tuple) The TestCases
        '''
        self._testCases = testCases
    # end def setTestCases

    def getTestCases(self):
        '''
        Obtains the TestCases

        @return The TestCases
        '''
        return self._testCases
    # end def getTestCases

    def setPerfData(self, perfData):
        '''
        Sets the perfData

        @param  perfData [in] (dict) The perfData
        '''
        self._perfData = perfData
    # end def setPerfData

    def getPerfData(self):
        '''
        Obtains the perfData

        @return The perfData
        '''
        return self._perfData
    # end def getPerfData

    @classmethod
    def _toXml_Description(cls, doc, element, description):
        '''
        Serializes a description to an XML element

        @param  doc         [in] (Document) The Document the element belongs to
        @param  element     [in] (Element) The element to serialize to.
        @param  description [in] (str) The description to serialize
        '''
        if (description is not None):
            descriptionElement = doc.createElement('description')
            textNode = doc.createTextNode(description)
            descriptionElement.appendChild(textNode)
            element.appendChild(descriptionElement)
        # end if
    # end def _toXml_Description

    @classmethod
    def _toXml_Traceback(cls, doc, element, classType, traceback):
        '''
        Serializes a traceback to an XML element

        @param  doc         [in] (Document) The Document the element belongs to
        @param  element     [in] (Element) The element to serialize to.
        @param  classType   [in] (str) The type of the exception to serialize
        @param  traceback   [in] (str) The full traceback of the exception, as a string.
        '''

        if (traceback is not None):
            tracebackElement = doc.createElement('traceback')
            if (classType is not None):
                tracebackElement.setAttribute('type', classType)
            # end if

            textNode = doc.createTextNode(traceback)
            tracebackElement.appendChild(textNode)

            element.appendChild(tracebackElement)
        # end if
    # end def _toXml_Traceback

    @classmethod
    def _toXml_Message(cls, doc, element, message):
        '''
        Serializes a message to an XML element

        @param  doc         [in] (Document) The Document the element belongs to
        @param  element     [in] (Element) The element to serialize to.
        @param  message     [in] (str) The message to serialize as a string.
        '''

        if (message is not None):
            messageElement = doc.createElement('message')

            textNode = doc.createTextNode(message)
            messageElement.appendChild(textNode)

            element.appendChild(messageElement)
        # end if
    # end def _toXml_Message

    @classmethod
    def _toXml_TestCases(cls, doc, element, testCases):
        '''
        Serializes a description to an XML element

        @param  doc       [in] (Document) The Document the element belongs to
        @param  element   [in] (Element) The element to serialize to.
        @param  testCases [in] (str) The TestCases to serialize
        '''

        testCasesElement = doc.createElement('testcases')

        for testCase, (author, comment) in testCases.items():
            testCaseElement = doc.createElement('testcase')
            testCaseElement.setAttribute('name', testCase)
            if (author is not None):
                testCaseElement.setAttribute('author', author)
            # end if
            if (comment is not None):
                testCaseElement.setAttribute('comment', comment)
            # end if

            testCasesElement.appendChild(testCaseElement)
        # end for

        element.appendChild(testCasesElement)
    # end def _toXml_TestCases

    @classmethod
    def _toXml_PerfData(cls, doc, element, perfData):
        '''
        Serializes a description to an XML element

        @param  doc      [in] (Document) The Document the element belongs to
        @param  element  [in] (Element) The element to serialize to.
        @param  perfData [in] (dict) The performance data to serialize
        '''

        perfDataElement = doc.createElement('perfdata')

        for key, data in perfData.items():
            for value, unit in data:
                entryElement = doc.createElement('entry')

                entryElement.setAttribute('key',   key)
                entryElement.setAttribute('value', str(value))
                if (unit is not None):
                    entryElement.setAttribute('unit',  unit)
                # end if

                perfDataElement.appendChild(entryElement)
            # end for
        # end for

        element.appendChild(perfDataElement)
    # end def _toXml_PerfData

    @classmethod
    def _toXml_TestResult(cls, doc, element, testResult):
        '''
        Serializes a test result to an XML element

        @param  doc        [in] (Document) The Document the element belongs to
        @param  element    [in] (Element) The element to serialize to.
        @param  testResult [in] (TestResult) The TestResult to serialize
        '''
        # Add the root attributes
        element.setAttribute('fqn',       testResult.getTestId())
        element.setAttribute('startdate', strftime(cls.TIME_FORMAT, testResult.getStartDate()))
        element.setAttribute('stopdate',  strftime(cls.TIME_FORMAT, testResult.getStopDate()))
        element.setAttribute('state',     testResult.getState())

        # Add the description
        cls._toXml_Description(doc, element, testResult.getDescription())
        cls._toXml_Message(doc, element, testResult.getMessage())
        cls._toXml_Traceback(doc, element, None,
                                            testResult.getTraceback())
        cls._toXml_TestCases(doc, element, testResult.getTestCases())
        cls._toXml_PerfData(doc, element, testResult.getPerfData())
    # end def _toXml_TestResult

    def _fromXml_Description(self, element, encoding):
        '''
        Deserializes the current object from an element.

        @param  element [in] (Element) The element to deserialize from.
        @param  encoding [in] (str) The encoding used to decode the strings
        '''
        textNodes = [child for child in element.childNodes
                                  if (  (child.nodeType == Node.TEXT_NODE)
                                    or  (child.nodeType == Node.CDATA_SECTION_NODE))]
        self._description = ""
        for t in textNodes:
            data = t.data#.encode(encoding)
            self._description += data
    # end def _fromXml_Description

    def _fromXml_Message(self, element, encoding):
        '''
        Deserializes the current object from an element.

        @param  element [in] (Element) The element to deserialize from.
        @param  encoding [in] (str) The encoding used to decode the strings
        '''
        textNodes = [child for child in element.childNodes
                           if (  (child.nodeType == Node.TEXT_NODE)
                             or  (child.nodeType == Node.CDATA_SECTION_NODE))]

        self._message = "".join([t.data for t in textNodes])
    # end def _fromXml_Message

    def _fromXml_Traceback(self, element, encoding):
        '''
        Deserializes the current object from an element.

        @param  element [in] (Element) The element to deserialize from.
        @param  encoding [in] (str) The encoding used to decode the strings
        '''
        textNodes = [child for child in element.childNodes
                                  if (  (child.nodeType == Node.TEXT_NODE)
                                    or  (child.nodeType == Node.CDATA_SECTION_NODE))]

        self._traceback = "".join([t.data for t in textNodes])
    # end def _fromXml_Traceback

    def _fromXml_TestCases(self, element, encoding):
        '''
        Deserializes the current object from an element.

        @param  element [in] (Element) The element to deserialize from.
        @param  encoding [in] (str) The encoding used to decode the strings
        '''

        testCaseElements = [child for child in element.childNodes
                                  if (  (child.nodeType == Node.ELEMENT_NODE)
                                    and (child.tagName == 'testcase'))]

        testCases = {}
        for testCaseElement in testCaseElements:
            name    = testCaseElement.getAttribute('name')#.encode(encoding)
            author  = testCaseElement.hasAttribute('author') and testCaseElement.getAttribute('author') or None
            comment = testCaseElement.hasAttribute('comment') and testCaseElement.getAttribute('comment') or None

            testCases[name] = (author, comment)
        # end for
        self._testCases = testCases
    # end def _fromXml_TestCases

    def _fromXml_PerfData(self, element, encoding):
        '''
        Deserializes the current object from an element.

        @param  element [in] (Element) The element to deserialize from.
        @param  encoding [in] (str) The encoding used to decode the strings
        '''

        entryElements = [child for child in element.childNodes
                                  if (  (child.nodeType == Node.ELEMENT_NODE)
                                    and (child.tagName == 'entry'))]

        perfData = {}
        for entryElement in entryElements:
            key   = entryElement.getAttribute('key')#.encode(encoding)
            value = float(entryElement.getAttribute('value'))
            if (entryElement.hasAttribute('unit')):
                unit = entryElement.getAttribute('unit')#.encode(encoding)
            else:
                unit = None
            # end if

            entries = perfData.setdefault(key, [])
            entries.append((value, unit))
        # end for

        self._perfData = perfData
    # end def _fromXml_PerfData

    def _fromXml_TestResult(self, element, encoding):                                                                   # pylint:disable=R0912
        '''
        Deserializes the current object from an element.

        @param  element [in] (Element) The element to deserialize from.
        @param  encoding [in] (str) The encoding used to decode the strings
        '''
        # Add the root attributes
        if element.hasAttribute('fqn'):
            self._testId    = element.getAttribute('fqn')
        else:
            self._testId    = '.'.join((element.getAttribute('classname'),
                                        element.getAttribute('name')))
        # end if

        if (element.hasAttribute('startdate')):
            startDate = element.getAttribute('startdate')
            try:
                self._startDate = strptime(startDate, self.TIME_FORMAT)
            except ValueError:
                try:
                    self._startDate = strptime(startDate, self.TIME_FORMAT_200)
                except ValueError:
                    self._startDate = localtime(float(startDate))
                # end try
            # end try
        else:
            self._startDate = localtime(0)
        # end if

        if (element.hasAttribute('stopdate')):
            stopDate = element.getAttribute('stopdate')
            try:
                self._stopDate  = strptime(stopDate,  self.TIME_FORMAT)
            except ValueError:
                try:
                    self._stopDate  = strptime(stopDate,  self.TIME_FORMAT_200)
                except ValueError:
                    self._stopDate  = localtime(float(stopDate))
                # end try
            # end try
        else:
            self._stopDate = localtime(mktime(self._startDate) + float(element.getAttribute('time')))
        # end if


        self._state     = element.getAttribute('state')

        # Add the message
        messageElements = [child for child in element.childNodes
                                 if (  (child.nodeType == Node.ELEMENT_NODE)
                                   and (child.tagName == 'message'))]

        if (len(messageElements)):
            self._fromXml_Message(messageElements[0], encoding)
        else:
            self._message = None
        # end if

        # Add the description
        descriptionElements = [child for child in element.childNodes
                                  if (  (child.nodeType == Node.ELEMENT_NODE)
                                    and (child.tagName == 'description'))]

        if (len(descriptionElements)):
            self._fromXml_Description(descriptionElements[0], encoding)
        else:
            self._description = None
        # end if

        # Add the traceback
        tracebackElements = [child for child in element.childNodes
                                  if (  (child.nodeType == Node.ELEMENT_NODE)
                                    and (child.tagName == 'traceback'))]

        if (len(tracebackElements)):
            self._fromXml_Traceback(tracebackElements[0], encoding)
        else:
            self._traceback = None
        # end if

        # Add the TestCases
        testCasesElements = [child for child in element.childNodes
                                  if (  (child.nodeType == Node.ELEMENT_NODE)
                                    and (child.tagName == 'testcases'))]

        if (len(testCasesElements)):
            self._fromXml_TestCases(testCasesElements[0], encoding)
        else:
            self._testCases = []
        # end if

        # Add the performance data
        perfdataElements = [child for child in element.childNodes
                                  if (    (child.nodeType == Node.ELEMENT_NODE)
                                      and (child.tagName == 'perfdata'))]

        if (len(perfdataElements)):
            self._fromXml_PerfData(perfdataElements[0], encoding)
        else:
            self._perfData = {}
        # end if
    # end def _fromXml_TestResult

    def save(self, xmlPath=None):
        '''
        Saves the currently modified entry to disk

        @param  xmlPath [in] (str) The path to save to (use the default if None)
        '''
        if (xmlPath is None):
            xmlPath = self._xmlPath
        # end if

        # Create a new DOM for the current result
        dom = getDOMImplementation()
        doc = dom.createDocument(None, 'testscript', None)

        element = doc.documentElement
        element.setAttribute('format', self.VERSION)

        self._toXml_TestResult(doc, element, self)

        with open(xmlPath, "w+") as xmlFile:
            doc.writexml(xmlFile, '', '  ', '\n')#, encoding=self.ENCODING)
        # end with
    # end def save

    def load(self, xmlPath=None):
        '''
        Loads the current entry from disk

        @param  xmlPath [in] (str) The path to load from (Use the default if None).
        '''
        if (xmlPath is None):
            xmlPath = self._xmlPath
        # end if

        doc = parse(xmlPath)

        testResultElement = doc.documentElement
        encoding = doc.encoding or self.ENCODING
        self._fromXml_TestResult(testResultElement, encoding)
    # end def load

    def loadFromString(self, xmlString):
        '''
        Loads the current entry from string

        @param  xmlString [in] (str) The xml string to parse.
        '''
        doc = parseString(xmlString)
        testResultElement = doc.documentElement
        encoding = doc.encoding or self.ENCODING
        self._fromXml_TestResult(testResultElement, encoding)
    # end def loadFromString

# end class XmlTestResultFile

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
