#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pyharness.output.test.pydevui
    :brief: Tests of the PyDevTestListener
    :author: Christophe Roquebert
    :date: 2018/06/07
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from io import StringIO
from shutil import rmtree

from pyharness.output.pydevui import PyDevTestListener
from pyharness.test.core_test import MockContext
from pyharness.test.core_test import TestListenerTestCase
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
def instantiate_mock_test(param_test_method_name, param_test_method_doc):
    """
    Creates a new Mock test case.

    This is defined as a function, so that the auto-discovery does not detect it
    as a test.

    :param param_test_method_name: The name of the test
    :type param_test_method_name: ``str``
    :param param_test_method_doc: The short description of the test
    :type param_test_method_doc: ``str``

    :return: A new instance of a MockTestCase
    """

    class InnerMockTest:
        """
        A mock test case
        """

        def __init__(self, test_method_name, test_method_doc):
            """
            Constructor

            :param test_method_name: The name of the test
            :type test_method_name: ``str``
            :param test_method_doc: The short description of the test
            :type test_method_doc: ``str``
            """

            self._testMethodName = test_method_name
            self._testMethodDoc = test_method_doc
            self.warning_occurred = False
        # end def __init__
    # end class InnerMockTest

    return InnerMockTest(param_test_method_name, param_test_method_doc)
# end def instantiate_mock_test


class PyDevTestListenerTestCase(TestListenerTestCase):
    """
    Tests of the Eclipse TestListener class
    """
    class TestPyDevTestListener(PyDevTestListener):
        """
        Class overriding stderr for the tests
        """
        _stderr = StringIO()
    # end class TestPyDevTestListener

    def setUp(self):
        """
        Creates a temporary directory for output
        """
        super(PyDevTestListenerTestCase, self).setUp()

        self.__tempDirPath = mkdtemp("", "test_%s" % self.id())
    # end def setUp

    def tearDown(self):
        """
        Cleans the temporary directory
        """

        rmtree(self.__tempDirPath, True)

        super(PyDevTestListenerTestCase, self).tearDown()
    # end def tearDown

    @staticmethod
    def isAbstract():
        """
        @copydoc pyharness.test.coretest.TestListenerTestCase.isAbstract
        """
        return False
    # end def isAbstract

    @staticmethod
    def _getTestListenerClass():
        """
        @copydoc pyharness.test.coretest.TestListenerTestCase._getTestListenerClass
        """
        return PyDevTestListenerTestCase.TestPyDevTestListener
    # end def _getTestListenerClass

    def test_StartStopTest(self):
        """
        Tests the startTest/stopTest method
        """
        if not self.isAbstract():
            listener_class = self._getTestListenerClass()
            listener_instance = listener_class(True, True, self.__tempDirPath, self._getKeywordArguments())

            test_result = self.MockTestResult(self)
            context = MockContext()
            mock_test = instantiate_mock_test("test_StartStopTest", "Mock test")

            # Now that the listener has been created, simulate a call
            listener_instance.startRun(context, False)
            self._prepareRun(listener_instance, [mock_test])
            for unused in range(3):
                listener_instance.startTest(mock_test)
                listener_instance.stopTest(mock_test)
            # end for
            listener_instance.stopRun(test_result, False)
        # end if
    # end def test_StartStopTest
# end class PyDevTestListenerTestCase


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
