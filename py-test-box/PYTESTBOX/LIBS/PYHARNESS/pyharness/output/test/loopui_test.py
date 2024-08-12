#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.test.loopui

@brief  Tests of the LoopTestListener

@author christophe Roquebert

@date   2018/06/07
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from shutil import rmtree

from pyharness.arguments import KeywordArguments
from pyharness.output.loopui import LoopTestListener
from pyharness.test.core_test import MockContext
from pyharness.test.core_test import TestListenerTestCase
from pyharness.test.core_test import instantiate_mock_test
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class LoopTestListenerTestCase(TestListenerTestCase):
    '''
    Tests of the Loop TestListener class
    '''

    def setUp(self):
        '''
        Creates a temporary directory for output
        '''
        super(LoopTestListenerTestCase, self).setUp()

        self.__tempDirPath = mkdtemp("", "test_%s" % self.id())
    # end def setUp

    def tearDown(self):
        '''
        Cleans the temporary directory
        '''

        rmtree(self.__tempDirPath, True)

        super(LoopTestListenerTestCase, self).tearDown()
    # end def tearDown

    @staticmethod
    def isAbstract():
        '''
        @copydoc pyharness.test.coretest.TestListenerTestCase.isAbstract
        '''
        return False
    # end def isAbstract

    @staticmethod
    def _getTestListenerClass():
        '''
        @copydoc pyharness.test.coretest.TestListenerTestCase._getTestListenerClass
        '''
        return LoopTestListener
    # end def _getTestListenerClass

    @staticmethod
    def __exc_info():                                                                                                   # pylint:disable=W8015
        '''
        Return a version of sys.exc_info() with the traceback frame minimised;

        Usually the top level of the traceback frame is not needed, as it only
        contains internal, pyharness-specific information.

        @return Tuple
        '''
        import sys
        exctype, excvalue, tb = sys.exc_info()
        if (sys.platform[:4] == 'java'): ## tracebacks look different in Jython
            return (exctype, excvalue, tb)
        # end if
        newtb = tb.tb_next
        if (newtb is None):
            return (exctype, excvalue, tb)
        # end if

        return (exctype, excvalue, newtb)
    # end def __exc_info

    _exc_info = __exc_info

    def test_Success(self):
        '''
        Tests the addSuccess method
        '''
        if (not self.isAbstract()):
            listenerClass    = self._getTestListenerClass()
            args             = self._getKeywordArguments()
            args[KeywordArguments.KEY_LOOP_STOP] = 'success'
            listenerInstance = listenerClass(True, True, self.__tempDirPath, args)

            testResult = self.MockTestResult(self)
            context    = MockContext()
            mockTest   = instantiate_mock_test("test_Success", "Mock test")

            # Now that the listener has been created, simulate a call
            listenerInstance.startRun(context, False)
            self._prepareRun(listenerInstance, [mockTest])
            for unused in range(3):
                listenerInstance.startTest(mockTest)

                listenerInstance.addSuccess(mockTest, None)

                listenerInstance.stopTest(mockTest)
            # end for
            listenerInstance.stopRun(testResult, False)
        # end if
    # end def test_Success

    def test_Failure(self):
        '''
        Tests the addFailure method
        '''
        if (not self.isAbstract()):
            listenerClass    = self._getTestListenerClass()
            args             = self._getKeywordArguments()
            args[KeywordArguments.KEY_LOOP_STOP] = 'failure'
            listenerInstance = listenerClass(True, True, self.__tempDirPath, args)

            testResult = self.MockTestResult(self)
            context    = MockContext()
            mockTest   = instantiate_mock_test("test_Failure", "Mock test, with special chars: éàò")

            # Now that the listener has been created, simulate a call
            listenerInstance.startRun(context, False)
            self._prepareRun(listenerInstance, [mockTest])
            for unused in range(3):
                listenerInstance.startTest(mockTest)

                # create a fake assertionError
                try:
                    raise AssertionError("This is a sample assertion, with special chars: éàò")
                except AssertionError:
                    listenerInstance.addFailure(mockTest, self.__exc_info())                                            # pylint:disable=E1101
                # end try

                listenerInstance.stopTest(mockTest)
            # end for
            listenerInstance.stopRun(testResult, False)
        # end if
    # end def test_Failure

    def test_Error(self):
        '''
        Tests the addError method
        '''
        if (not self.isAbstract()):
            listenerClass    = self._getTestListenerClass()
            args             = self._getKeywordArguments()
            args[KeywordArguments.KEY_LOOP_STOP] = 'error'
            listenerInstance = listenerClass(True, True, self.__tempDirPath, args)

            testResult = self.MockTestResult(self)
            context    = MockContext()
            mockTest   = instantiate_mock_test("test_Error", "Mock test, with special chars: éàò")

            # Now that the listener has been created, simulate a call
            listenerInstance.startRun(context, False)
            self._prepareRun(listenerInstance, [mockTest])
            for unused in range(3):
                listenerInstance.startTest(mockTest)

                # create a fake assertionError
                try:
                    raise AssertionError("This is a sample assertion, with special chars: éàò")
                except AssertionError:
                    listenerInstance.addError(mockTest, self.__exc_info())                                              # pylint:disable=E1101
                # end try

                listenerInstance.stopTest(mockTest)
            # end for
            listenerInstance.stopRun(testResult, False)
        # end if
    # end def test_Error

# end class LoopTestListenerTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
