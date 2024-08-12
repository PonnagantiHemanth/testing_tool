#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.input.xmlui

@brief Providers for the XmlTestListener class

@author christophe.roquebert

@date   2018/05/05
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path                    import abspath
from pyharness.consts            import DEFAULT_OUTPUT_DIRECTORY
from pyharness.files.xmltestcase import XmlTestResultFile
from pyharness.input.providers   import DynamicTestCasesProvider
from pyharness.input.providers   import PerfDataProvider
from pyharness.input.providers   import TestStateTestProvider
from pyharness.arguments         import KeywordArguments
from os                         import F_OK
from os                         import access
from os.path                    import join
from os.path                    import normpath

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class XmlTestProvider(TestStateTestProvider, DynamicTestCasesProvider, PerfDataProvider):
    '''
    Providers for the XmlTestListener class
    '''

    FILE_EXTENSION = 'xml'
    RELATIVE_PATH  = 'xml'

    def _getOutputFilePath(self, outputDir, testId):
        '''
        Obtain the output file for the specified test.

        @param outputDir [in] (str) The output directory
        @param testId [in] (str) The test id
        @return The full path to the output file.
        '''
        filename = "%sTestScript.%s" % (testId, self.FILE_EXTENSION)
        result = normpath(join(outputDir, self.RELATIVE_PATH, filename))

        return result
    # end def _getOutputFilePath

    def _getXmlTestResult(self, testId, product, variant, target):
        '''
        Obtain the TestResult, extracted from the XML

        @param  testId  [in] (str) The testId for which to retrieve the TestCases
        @param  product [in] (str) The product to obtain the history from
        @param  variant [in] (str) The variant to obtain the history from
        @param  target  [in] (str) The target to obtain the history from

        @return The XmlTestResult file for this TestResult
        '''
        root = abspath(self._kwArgs[KeywordArguments.KEY_ROOT])
        versionRoot = join(root, DEFAULT_OUTPUT_DIRECTORY)
        outputDir = join(versionRoot, product, variant, target)

        pathToXml = self._getOutputFilePath(outputDir, testId)
        if (access(pathToXml, F_OK)):
            xmlFile = XmlTestResultFile()
            xmlFile.load(pathToXml)
        else:
            xmlFile = None
        # end if

        return xmlFile
    # end def _getXmlTestResult

    def getTestState(self, testId, product, variant, target):
        '''
        @copydoc pyharness.input.providers.TestStateTestProvider.getTestState
        '''
        xmlFile = self._getXmlTestResult(testId, product, variant, target)
        return xmlFile is not None and xmlFile.getState() or "unknown"
    # end def getTestState

    def getDynamicTestCases(self, testId, product, variant, target):
        '''
        @copydoc pyharness.input.providers.DynamicTestCasesProvider.getDynamicTestCases
        '''
        xmlFile = self._getXmlTestResult(testId, product, variant, target)
        if (xmlFile is not None):
            testCases = [(name, author, comment) for name, (author, comment) in xmlFile.getTestCases().items()]
        else:
            testCases = []
        # end if

        return testCases
    # end def getDynamicTestCases

    def getPerfData(self, testId, product, variant, target):
        '''
        @copydoc pyharness.input.providers.PerfDataProvider.getPerfData
        '''
        xmlFile = self._getXmlTestResult(testId, product, variant, target)
        return xmlFile is not None and xmlFile.getPerfData() or []
    # end def getPerfData
# end class XmlTestProvider

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
