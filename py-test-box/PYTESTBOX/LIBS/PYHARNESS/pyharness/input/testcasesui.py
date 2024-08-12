#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.input.testcasesui

@brief Local implementation of the StaticTestCasesProvider

@author christophe.roquebert

@date   2018/05/05
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path             import abspath
from pylibrary.tools.importutils   import importFqn
from pyharness.consts                import DEFAULT_OUTPUT_DIRECTORY
from pyharness.files.dynamic         import DynamicFile
from pyharness.input.providers       import DynamicTestCasesProvider
from pyharness.input.providers       import StaticTestCasesProvider
from pyharness.arguments             import KeywordArguments
from pyharness.tools.staticanalysis  import Main as StaticAnalysis
from os.path                        import join
from os.path                        import normpath
from types                          import MethodType
import inspect

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class TestCasesTestProvider(StaticTestCasesProvider, DynamicTestCasesProvider):
    '''
    Local implementation of the StaticTestCasesProvider and DynamicTestCasesProvider

    This provider works by auto-auditing the code base, and obtaining info
    from files created by the DynamicTestListener
    '''

    def getStaticTestCases(self, testIds):
        '''
        @copydoc pyharness.input.providers.StaticTestCasesProvider.getStaticTestCases
        '''

        if (isinstance(testIds, str)):
            testIds = [testIds]
        # end if

        results = set()
        for testId in testIds:
            innerResults = set()
            try:
                testMethod = importFqn(testId)
                if (    (testMethod is not None)
                    and (inspect.isfunction(testMethod))):

                    innerResults |= set(StaticAnalysis.analyzeCode(testMethod.__code__, testMethod.__globals__))
                # end if
            except AttributeError:
                innerResults.clear()
            except ImportError:
                innerResults.clear()
            # end try
            results |= innerResults
        # end for

        return list(sorted(results))
    # end def getStaticTestCases

    def getDynamicTestCases(self, testId, product, variant, target):
        '''
        @copydoc pyharness.input.providers.DynamicTestCasesProvider.getDynamicTestCases
        '''
        root = abspath(self._kwArgs[KeywordArguments.KEY_ROOT])
        versionRoot = join(root, DEFAULT_OUTPUT_DIRECTORY)
        pathToDynamicFile = normpath(join(versionRoot, product, variant, target, "TESTCASES", "dynamic"))

        dynamicFile = DynamicFile.create(pathToDynamicFile)
        testCaseAuthorComments = dynamicFile.getTestCases(testId)

        return testCaseAuthorComments
    # end def getDynamicTestCases
# end class TestCasesTestProvider

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
