#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.files.test.xmltestcase

@brief Tests of the XmlTestResultFile class

@author christophe.roquebert

@date   2018/12/18
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os import F_OK
from os import access
from os.path import abspath
from os.path import dirname
from os.path import join
from shutil import rmtree
from unittest import TestCase
from xml.dom.minidom import Node
from xml.dom.minidom import getDOMImplementation
from xml.dom.minidom import parse

from pyharness.files.xmltestcase import XmlTestResultFile
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class XmlTestResultFileTestCase(TestCase):
    '''
    Tests of the XmlTestResultFile class
    '''

    TestingClass = XmlTestResultFile

    @classmethod
    def _createInstance(cls, filePath = None):
        '''
        Create a default instance

        @option filePath [in] (str) File Path

        @return (XmlTestResultFile) XmlTestResultFile instance
        '''
        return cls.TestingClass(filePath)
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

    def testLoad(self):
        '''
        Loads a file from disk
        '''
        inputFilePath = join(self.__tempDirPath, 'test.xml')
        with open(inputFilePath, 'w+') as inputFile:
            inputFile.write('\n'.join(('<?xml version="1.0" encoding="utf-8"?>',
                                       '<testscript classname="MyTestCase" name="testMyApi" time="0.0310" starttime="1197902199.8900">',
                                       '  <description><![CDATA[',
                                       '      @brief  Computes AES1 test',
                                       '      ]]></description>',
                                       '  <testcases>',
                                       '    <testcase name="TESTCASE" author="user.test" comment="This is a comment"/>',
                                       '  </testcases>',
                                       '  <perfdata>',
                                       '    <entry key="myKey" value="0.5" unit="s"/>',
                                       '  </perfdata>',
                                       '</testscript>',
                                       )))
        # end with


        xmlFile = self._createInstance(inputFilePath)
        xmlFile.load()

        self.assertEqual('MyTestCase.testMyApi',
                         xmlFile.getTestId(),
                         'Invalid test id')

        self.assertEqual('\n      @brief  Computes AES1 test\n      ',
                         xmlFile.getDescription(),
                         'Invalid description')

        self.assertEqual({'TESTCASE': ('user.test', 'This is a comment')},
                         xmlFile.getTestCases(),
                         'Invalid TestCases')
    # end def testLoad

    def testLoadFromString(self):
        '''
        Tests loadFromString method
        '''
        xmlContent = '\n'.join(('<?xml version="1.0" encoding="utf-8"?>',
                                '<testscript classname="MyTestCase" name="testMyApi" time="0.0310" starttime="1197902199.8900">',
                                '  <description><![CDATA[',
                                '      @brief  Computes AES1 test',
                                '      ]]></description>',
                                '  <testcases>',
                                '    <testcase name="TESTCASE" author="user.test" comment="This is a comment"/>',
                                '  </testcases>',
                                '  <perfdata>',
                                '    <entry key="myKey" value="0.5" unit="s"/>',
                                '  </perfdata>',
                                '</testscript>',
                                ))
        xmlFile = self._createInstance()
        xmlFile.loadFromString(xmlContent)

        self.assertEqual('MyTestCase.testMyApi',
                         xmlFile.getTestId(),
                         'Invalid test id')

        self.assertEqual('\n      @brief  Computes AES1 test\n      ',
                         xmlFile.getDescription(),
                         'Invalid description')

        self.assertEqual({'TESTCASE': ('user.test', 'This is a comment')},
                         xmlFile.getTestCases(),
                         'Invalid TestCases')

    # end def testLoadFromString

    def testSave(self):
        '''
        Tests save method
        '''
        outputFilePath = join(self.__tempDirPath, 'test.xml')
        xmlContent = '\n'.join(('<?xml version="1.0" encoding="utf-8"?>',
                                '<testscript classname="MyTestCase" name="testMyApi" time="0.0310" starttime="1197902199.8900">',
                                '  <description><![CDATA[',
                                '      @brief  Computes AES1 test',
                                '      ]]></description>',
                                '  <testcases>',
                                '    <testcase name="TESTCASE" author="user.test" comment="This is a comment"/>',
                                '  </testcases>',
                                '  <perfdata>',
                                '    <entry key="myKey" value="0.5" unit="s"/>',
                                '  </perfdata>',
                                '</testscript>',
                                ))
        xmlFile = self._createInstance(outputFilePath)
        xmlFile.loadFromString(xmlContent)
        xmlFile.save()

        xmlFile2 = self._createInstance(outputFilePath)
        xmlFile2.load()

        self.assertEqual(xmlFile.getTestId(),
                         xmlFile2.getTestId(),
                         'Invalid test id')

        self.assertEqual(xmlFile.getDescription().strip(),
                         xmlFile2.getDescription().strip(),
                         'Invalid description')

        self.assertEqual(xmlFile.getTestCases(),
                         xmlFile2.getTestCases(),
                         'Invalid TestCases')

    # end def testSave

    def testSpecialChar(self):
        '''
        Tests the serialization of a special character.
        '''
        dom = getDOMImplementation()
        doc = dom.createDocument(None, 'test', None)

        data = "Special character: �� "
        textNode = doc.createTextNode(data)
        root = doc.documentElement
        root.appendChild(textNode)

        xmlPath = join(self.__tempDirPath, 'specialchar.xml')
        with open(xmlPath, "w+", encoding="utf-8") as xmlFile:
            doc.writexml(xmlFile, '', '  ', '\n', encoding="utf-8")
        # end with

        doc = parse(xmlPath)
        root = doc.documentElement
        for childNode in root.childNodes:
            if childNode.nodeType == Node.TEXT_NODE:
                obtained = childNode.data
                break
            # end if
        # end for

        expected = data.strip()
        obtained = obtained.strip()
        self.assertEqual(expected,
                         obtained,
                         "inconsistent XML encoding/decoding")
    # end def testSpecialChar

    def testConstructor(self):
        '''
        Tests the __init__ method
        '''
        # Create a convenient hierarchy
        tmpDir = abspath(mkdtemp("", "test_%s" % self.id()))
        expectedPath = join(tmpDir, 'testingfile.xml')
        self._createInstance(filePath = expectedPath)
        xmlDirPath = dirname(expectedPath)

        self.assertTrue(access(xmlDirPath, F_OK))

        rmtree(tmpDir, True)
    # end def testConstructor

    def testGettersSetters(self):
        '''
        Tests getter and setter methods
        '''
        expectedTestId      = 'testId'
        expectedState       = 'state'
        expectedDescription = 'description'
        expectedStartDate   = 'StartDate'
        expectedStopDate    = 'StopDate'
        expectedMessage     = 'Message'
        expectedTraceback   = 'Traceback'
        expectedTestCases   = ['Testcases']
        expectedPerfdata    = {'Perfdata': 'Perfdata'}
        xmlTestResultFile = self._createInstance()

        xmlTestResultFile.setTestId(expectedTestId)
        xmlTestResultFile.setState(expectedState)
        xmlTestResultFile.setDescription(expectedDescription)
        xmlTestResultFile.setStartDate(expectedStartDate)
        xmlTestResultFile.setStopDate(expectedStopDate)
        xmlTestResultFile.setMessage(expectedMessage)
        xmlTestResultFile.setTraceback(expectedTraceback)
        xmlTestResultFile.setTestCases(expectedTestCases)
        xmlTestResultFile.setPerfData(expectedPerfdata)

        self.assertEqual(expectedTestId, xmlTestResultFile.getTestId(), 'Wrong setter result')
        self.assertEqual(expectedState, xmlTestResultFile.getState(), 'Wrong setter result')
        self.assertEqual(expectedDescription, xmlTestResultFile.getDescription(), 'Wrong setter result')
        self.assertEqual(expectedStartDate, xmlTestResultFile.getStartDate(), 'Wrong setter result')
        self.assertEqual(expectedStopDate, xmlTestResultFile.getStopDate(), 'Wrong setter result')
        self.assertEqual(expectedMessage, xmlTestResultFile.getMessage(), 'Wrong setter result')
        self.assertEqual(expectedTraceback, xmlTestResultFile.getTraceback(), 'Wrong setter result')
        self.assertEqual(expectedTestCases, xmlTestResultFile.getTestCases(), 'Wrong setter result')
        self.assertEqual(expectedPerfdata, xmlTestResultFile.getPerfData(), 'Wrong setter result')

    # end def testGettersSetters

# end class XmlTestResultFileTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
