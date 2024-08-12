#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyharness.output.junitui
:brief: JUnit file TestListener
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/12/09
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os import F_OK
from os import access
from os import listdir
from os import makedirs
from os import remove
from os.path import abspath
from os.path import dirname
from os.path import exists
from os.path import join
from threading import RLock
from time import perf_counter
from weakref import ref
from xml.dom.minidom import Node
from xml.dom.minidom import getDOMImplementation
from xml.dom.minidom import parseString

from pyharness.arguments import KeywordArguments
from pyharness.core import TestSuite
from pyharness.core import _LEVEL_INFO
from pyharness.core import _LEVEL_TRACE
from pyharness.output.vblogui import BaseVBLogTestListener
from pyharness.output.vblogui import VBLogFormatter
from pylibrary.tools import stringTruncator
from pylibrary.tools.threadutils import synchronized


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class JUnitTestListener(BaseVBLogTestListener):
    """
    A test listener class that can print formatted text results to an XML file.
    The XML file format is compatible with ant's JUnitTask

    The following format is used, with one file per class:
    @code
    <!-- This is the root, one test class is contained within a test suite   -->
    <!-- This also means that, on start, and unless results are cleared for  -->
    <!-- each run, results will need to be re-read                           -->
    <!-- errors is the number of failures of type error in all test cases    -->
    <!-- within the test suite                                               -->
    <!-- failures is the number of failures of type fail in all test cases   -->
    <!-- within the test suite                                               -->
    <testsuite errors='int, number of errors within child test cases'
               failures='int, number of failures within child test cases'
               name='Fully qualified name of the module containing the tests'
               tests='789'
               time='cumulated time of the test cases, in second'>
        <properties>
          <!-- Interesting values to log: PRODUCT, VARIANT, TARGET, MODE     -->
          <property name='name of the property'
                    value='value of the property'>
        </properties>
        <system-out/>
        <system-err/>
        <testcase classname='Name of the class containing the test'
                  name='Name of the method containing the test'
                  time='Time spent on the test'>
            <failure message='The error message'
                     type='failure,error'>
                Failure complete message. complete trace ?
            </failure>
        </testcase>

    </testsuite>
    @endcode
    """
    RELATIVE_PATH = 'junit'
    FILE_EXTENSION = 'xml'
    SYNCHRONIZATION_LOCK = RLock()
    ENCODING = 'iso-8859-1'

    class TestCaseResult(object):
        """
        Container for a test result.

        The internal state is:
        0: Unknown
        1: Running
        2: Success
        3: Failed
        4: Error
        """

        STATE_UNKNOWN = 0
        STATE_RUNNING = 1
        STATE_SUCCESS = 2
        STATE_FAILED = 3
        STATE_ERROR = 4

        # Limit the number of lines saved in the .xml file to 50k lines
        MAX_LINE_IN_XML = 50000
        HEADER_SIZE = 60

        def __init__(self, class_name, name, parent=None):
            """
            :param class_name: The class name (NOT fully qualified)
            :type class_name: ``str``
            :param name: The method name
            :type name: ``str``
            :param parent: The parent suite result
            :type name: ``TestSuiteResult``
            """
            self._className = class_name
            self._name = name
            if parent is not None:
                parent = ref(parent)
            # end if
            self._parent = parent

            self.state = self.STATE_UNKNOWN

            self._message = ''
            self._log = []
            self._startTime = 0
            self._stopTime = 0
            self._totalTime = 0
        # end def __init__

        def __str__(self):
            state_names = {self.STATE_UNKNOWN: 'Unknown',
                           self.STATE_RUNNING: 'Running',
                           self.STATE_SUCCESS: 'Success',
                           self.STATE_FAILED:  'Failed',
                           self.STATE_ERROR:   'Error'}
            return "%s: %s" % (self._name, state_names.get(self.state, 'undefined'))
        # end def __str__

        def get_class_name(self):
            """
            Obtain the class name

            :return: The class name
            :rtype: ``str``
            """
            return self._className
        # end def get_class_name

        className = property(get_class_name)

        def get_name(self):
            """
            Obtain the method name

            :return: The method name
            :rtype: ``str``
            """
            return self._name
        # end def get_name

        name = property(get_name)

        def get_parent(self):
            """
            Obtain the parent test suite.

            :return: The parent test suite, or None if no parent exists
            :rtype: ``TestSuiteResult | None``
            """
            return self._parent is not None and self._parent() or None
        # end def get_parent

        parent = property(get_parent)

        def get_start_time(self):
            """
            Obtain the start time in ms

            :return: The start time, in ms.
            :rtype: ``int``
            """
            return self._startTime
        # end def get_start_time

        def set_start_time(self, time):                                                                                   # pylint:disable=W0621
            """
            Set the start time, in ms

            :param time: The start time in ms.
            :type time: ``int``
            """
            self._startTime = time
            self._totalTime = 0
        # end def set_start_time

        startTime = property(get_start_time, set_start_time)

        def get_stop_time(self):
            """
            Obtain the stop time in ms

            :return: The stop time in ms.
            :rtype: ``int``
            """
            return self._stopTime
        # end def get_stop_time

        def set_stop_time(self, time):
            # pylint:disable=W0621
            """
            Set the stop time, in ms

            :param time: The stop time in ms.
            :type time: ``int``
            """
            self._stopTime = time
            self._totalTime = self._stopTime - self._startTime
        # end def set_stop_time

        stopTime = property(get_stop_time, set_stop_time)

        def get_total_time(self):
            """
            Get the elapse time, between start and stop.

            :return: The time spend in the test in ms.
            :rtype: ``int``
            """
            return self._totalTime
        # end def get_total_time

        def set_total_time(self, total_time):
            """
            Sets the elapse time, between start and stop.

            :param total_time: The time spend in the test in ms.
            :type total_time: ``int``
            """
            self._totalTime = total_time
        # end def set_total_time

        total_time = property(get_total_time, set_total_time)

        def get_message(self):
            """
            Obtain the message

            :return: The test short message
            :rtype: ``str``
            """
            return self._message
        # end def get_message

        def set_message(self, message):
            """
            Set the message

            :param message: The message to set
            :type message: ``str``
            """
            self._message = message
        # end def set_message

        message = property(get_message, set_message)

        def get_log(self):
            """
            Obtain the text log

            :return: The log, as a list of lines.
            :rtype: ``list[str]``
            """
            return self._log
        # end def get_log

        log = property(get_log)

        def get_text_log(self):
            """
            Obtain the text log

            :return: The text log.
            :rtype: ``str``
            """
            if len(self.log) > self.MAX_LINE_IN_XML:
                return '\n'.join(self.log[:self.HEADER_SIZE]) + '\n!! End of the header block !!\n' +\
                    '\n'.join(self.log[-self.MAX_LINE_IN_XML+self.HEADER_SIZE:])
            else:
                return '\n'.join(self.log)
        # end def get_text_log

        def set_text_log(self, text_log):
            """
            Set the log, as text.

            :param text_log: The log to set.
            :type text_log: ``str``
            """
            del self.log[:]
            self.log.extend(text_log.split('\n'))
        # end def set_text_log

        textLog = property(get_text_log, set_text_log)

        def save(self):
            """
            Save the test result to the parent
            """
            self.parent.save()
        # end def save

        def load(self):
            """
            Load the test result from the parent
            """
            self.parent.load(self)
        # end def load
    # end class TestCaseResult

    class TestSuiteResult(object):
        """
        Container for test suite results
        """
        def __init__(self, name, properties, output_dir_path, output_file_ext):
            """
            :param name: fully qualified name of the test suite module
            :type name: ``str``
            :param properties: {"name": value} dict
            :type properties: ``dict``
            :param output_dir_path: Path to the output directory
            :type name: ``str``
            :param output_file_ext: file extension
            :type name: ``str``
            """
            self._name = name
            self._testcases = dict()
            self._properties = properties
            self._output_dir_path = output_dir_path
            self._output_file_ext = output_file_ext

            self.load()
        # end def __init__

        def __str__(self):
            return '%s (%d test cases)' % (self._name, len(self._testcases))
        # end def __str__

        def get_name(self):
            """
            Obtains the test suite name

            @return the test suite name
            """
            return self._name
        # end def getName

        name = property(get_name)

        def get_test_cases(self):
            """
            Obtain the test cases in this test suite.

            :return: A list of test cases for this test suite.
            :rtype: ``dict``
            """
            return self._testcases
        # end def get_test_cases

        testCases = property(get_test_cases)

        def get_properties(self):
            """
            Obtains the properties for this test suite.

            :return: The list of properties for this test suite.
            :rtype: ``dict``
            """
            return self._properties
        # end def get_properties

        properties = property(get_properties)

        def _xml_file_path(self, test_id):
            """
            Build the path to the output file

            :param test_id: The test fully qualified name to log.
            :type test_id: ``TestCase``

            :return: The file path to the test log.
            :rtype: ``str``
            """
            filename = '.'.join((stringTruncator(test_id), self._output_file_ext))
            result = join(self._output_dir_path, filename)
            # Workaround: Windows does not support extremely long file names.
            # This limits the size of the output file, but the problem can
            # still occur if the path is too long.
            if len(result) > 281:
                filename = ".".join(("%08X" % hash(test_id), self._output_file_ext))
                result = join(self._output_dir_path, filename)
            # end if

            return result
        # end def _xml_file_path

        def save(self):
            """
            Save the test suite xml file to the output directory.
            """

            output_file_path = self._xml_file_path(self.name)

            test_case_results = [test_case_result for test_case_result in list(self.testCases.values()) if (
                    test_case_result.state in (JUnitTestListener.TestCaseResult.STATE_SUCCESS,
                                               JUnitTestListener.TestCaseResult.STATE_FAILED,
                                               JUnitTestListener.TestCaseResult.STATE_ERROR))]
            test_case_results.sort(key=lambda test_case_result: (test_case_result.className, test_case_result.name))

            # Create a new DOM for the current result
            dom = getDOMImplementation()
            doc = dom.createDocument(None, 'testsuite', None)
            element = doc.documentElement

            # Count tests in each state:
            # errors attribute
            errors_count = len([testCaseResult for testCaseResult in test_case_results if
                                testCaseResult.state == JUnitTestListener.TestCaseResult.STATE_ERROR])
            element.setAttribute('errors', str(errors_count))

            # failures attribute
            failures_count = len([testCaseResult for testCaseResult in test_case_results if
                                  testCaseResult.state == JUnitTestListener.TestCaseResult.STATE_FAILED])
            element.setAttribute('failures', str(failures_count))

            # name attribute
            element.setAttribute('name', self.name)

            # tests attribute
            element.setAttribute('tests', str(len(test_case_results)))

            # time attribute
            test_time = 0
            for test_case_result in test_case_results:
                test_time += test_case_result.total_time
            # end for
            element.setAttribute('time', '%0.3f' % (test_time / 1000.0))

            # Properties empty child
            properties_element = doc.createElement('properties')

            for name, value in self.properties.items():
                property_element = doc.createElement('property')
                property_element.setAttribute('name', name)
                property_element.setAttribute('value', value)
                properties_element.appendChild(property_element)
            # end for

            element.appendChild(properties_element)

            # System out empty child
            system_out_element = doc.createElement('system-out')
            element.appendChild(system_out_element)

            # System err empty child
            system_err_element = doc.createElement('system-err')
            element.appendChild(system_err_element)

            for test_case_result in test_case_results:
                test_case_element = doc.createElement('testcase')
                test_case_element.setAttribute('classname', test_case_result.className)
                test_case_element.setAttribute('name', test_case_result.name)
                test_case_element.setAttribute('time', '%0.3f' % (test_case_result.total_time / 1000.0))

                if test_case_result.state in (JUnitTestListener.TestCaseResult.STATE_FAILED,
                                              JUnitTestListener.TestCaseResult.STATE_ERROR):

                    failure_element = doc.createElement('failure')
                    failure_element.setAttribute('message', test_case_result.message)

                    if test_case_result.state == JUnitTestListener.TestCaseResult.STATE_FAILED:
                        failure_type = 'failure'
                    else:
                        failure_type = 'error'
                    # end if
                    failure_element.setAttribute('type', failure_type)

                    if len(test_case_result.textLog):
                        failure_text = doc.createTextNode(test_case_result.textLog)
                        failure_element.appendChild(failure_text)
                    # end if

                    test_case_element.appendChild(failure_element)

                else:
                    if len(test_case_result.textLog):
                        # Remove useless log to free some memory space
                        test_case_result.textLog = ''
                    # end if
                # end if

                element.appendChild(test_case_element)
            # end for

            dir_name = dirname(output_file_path)
            if not exists(dir_name):
                makedirs(dir_name)
            # end if

            with open(output_file_path, "w+") as xmlFile:
                doc.writexml(xmlFile, '', '  ', '\n', encoding=JUnitTestListener.ENCODING)
            # end with
        # end def save

        def load(self):
            """
            Load a test suite xml file from the output directory.
            """
            input_file_path = self._xml_file_path(self.name)
            if exists(input_file_path):
                with open(input_file_path) as xmlFile:
                    doc = parseString(xmlFile.read())
                # end with
                element = doc.documentElement

                assert element.tagName == 'testsuite'
                # Lookup testcase elements.
                # Add the message
                test_case_elements = [child for child in element.childNodes if (
                        (child.nodeType == Node.ELEMENT_NODE) and (child.tagName == 'testcase'))]
                for testCaseElement in test_case_elements:
                    class_name = testCaseElement.getAttribute('classname')
                    name = testCaseElement.getAttribute('name')
                    test_case_result = JUnitTestListener.TestCaseResult(class_name, name, self)

                    test_time = testCaseElement.getAttribute('time')
                    test_case_result.total_time = int(float(test_time) * 1000)

                    state = JUnitTestListener.TestCaseResult.STATE_SUCCESS
                    message = None
                    log = ''

                    # Look for a failure element
                    failure_elements = [child for child in testCaseElement.childNodes if (
                            (child.nodeType == Node.ELEMENT_NODE) and (child.tagName == 'failure'))]

                    assert len(failure_elements) <= 1

                    if len(failure_elements) == 1:
                        failure_element = failure_elements[0]
                        failure_type = failure_element.getAttribute('type')

                        if failure_type == 'failure':
                            state = JUnitTestListener.TestCaseResult.STATE_FAILED
                        elif failure_type == 'error':
                            state = JUnitTestListener.TestCaseResult.STATE_ERROR
                        else:
                            raise ValueError('Unable to load failure type %s for test %s'
                                             % (failure_type, (class_name, name)))
                        # end if

                        message = failure_element.getAttribute('message')
                        log_texts = [child.nodeValue for child in testCaseElement.childNodes if (
                                child.nodeType == Node.TEXT_NODE)]
                        log = ''.join(log_texts)
                    # end if
                    test_case_result.state = state
                    test_case_result.message = message
                    test_case_result.textLog = log
                # end for
            # end if
        # end def load

    # end class TestSuiteResult

    def __init__(self, descriptions, verbosity, outputdir, args):
        # See ``pyharness.core.TestListener.__init__``
        # Keep at least the "info" verbosity level for the .xml file to enable the partial test failure analysis
        verbosity = _LEVEL_INFO if verbosity > _LEVEL_INFO else verbosity
        super().__init__(descriptions, verbosity, outputdir, args)

        self._test_suites = dict()
        self._properties = dict()
    # end def __init__

    def __result_dir_path(self):
        """
        Build the path to the directory containing the log files

        :return: The file path to the test log.
        :rtype: ``str``
        """
        result = abspath(join(self.outputdir, self.RELATIVE_PATH))

        return result
    # end def __result_dir_path

    @synchronized(SYNCHRONIZATION_LOCK)
    def __create_test_case_result(self, test_id):
        """
        Create a logger for the test.

        :param test_id: The test fully qualified name to log.
        :type test_id: ``TestCase``

        :return: The newly created TestCase result
        :rtype: ``TestCaseResult``
        """
        test_case_class_name, test_case_name = test_id.rsplit('.', 1)
        test_suite_result = self.__create_test_suite_result(test_id)

        test_case_results = test_suite_result.get_test_cases()

        key = (test_case_class_name, test_case_name)
        test_case_result = test_case_results.get(key, None)
        if test_case_result is None:
            test_case_result = self.TestCaseResult(test_case_class_name, test_case_name, parent=test_suite_result)
            test_case_results[key] = test_case_result
        # end if

        return test_case_result
    # end def __create_test_case_result

    @synchronized(SYNCHRONIZATION_LOCK)
    def __create_test_suite_result(self, test_id):
        """
        Create a container for the test suite.

        :param test_id: The test fully qualified name to log.
        :type test_id: ``TestCase``

        :return: The newly created TestSuiteResult
        :rtype: ``TestSuiteResult``
        """
        # create a logger
        test_case_module, _, _ = test_id.rsplit('.', 2)
        test_suite_result = self._test_suites.get(test_case_module, None)

        if test_suite_result is None:
            test_suite_result = self.TestSuiteResult(
                test_case_module, self._properties, self.__result_dir_path(), self.FILE_EXTENSION)
            self._test_suites[test_case_module] = test_suite_result
        # end if

        return test_suite_result
    # end def __create_test_suite_result

    def startRun(self, context, resumed):
        # See``TestListener.startRun``
        if (not resumed) and (self.args[KeywordArguments.KEY_ERASELOGS]):

            output_dir = self.__result_dir_path()
            if access(output_dir, F_OK):
                # Erase _all_ tests in the directory.
                for filename in listdir(output_dir):
                    if filename.lower().endswith('.%s' % self.FILE_EXTENSION):
                        remove(join(output_dir, filename))
                    # end if
                # end for
            # end if
        # end if

        self._properties = {'product': context.getCurrentProduct(),
                            'variant': context.getCurrentVariant(),
                            'target': context.getCurrentTarget(),
                            'mode': context.getCurrentMode(),
                            }
    # end def startRun

    def stopRun(self, result, suspended):                                                                               # pylint:disable=W0613
        # See ``TestListener.stopRun``
        if not suspended:

            for test_suite_result in list(self._test_suites.values()):
                test_suite_result.save()
            # end for
        # end if
    # end def stopRun

    def resetTest(self, test, context):                                                                                 # pylint:disable=W0613
        # See ``TestListener.resetTest``
        test_case_result = self.__create_test_case_result(test.id())
        test_case_result.state = self.TestCaseResult.STATE_UNKNOWN
        test_case_result.textLog = ''
        test_case_result.message = ''

        test_case_result.save()
    # end def resetTest

    def startTest(self, test):
        # See ``BaseVBLogTestListener.startTest``
        if isinstance(test, TestSuite):
            self.__create_test_suite_result(test.id())
        else:
            test_case_result = self.__create_test_case_result(test.id())
            test_case_result.set_start_time(int(perf_counter() * 1000))
        # end if
    # end def startTest

    def stopTest(self, test):
        # See ``BaseVBLogTestListener.stopTest``
        super().stopTest(test)

        if not isinstance(test, TestSuite):

            test_case_result = self.__create_test_case_result(test.id())
            test_case_result.set_stop_time(int(perf_counter() * 1000))

            # Discard the log, if needed and no warning occurs
            if ((test_case_result.state != self.TestCaseResult.STATE_FAILED) and (
                    not self.args[KeywordArguments.KEY_KEEPLOGS])):
                test_case_result.textLog = ''
            # end if

            test_case_result.save()
        else:
            test_suite_result = self.__create_test_suite_result(test)
            test_suite_result.save()
        # end if
    # end def stopTest

    def log(self, test, level, msg, *args, **kwargs):
        # See ``BaseVBLogTestListener.log``
        if self.acceptLog(level):

            if len(args) > 0:
                message = msg % args
            elif len(kwargs) > 0:
                message = msg % kwargs
            else:
                message = msg
            # end if

            msg = VBLogFormatter.format(level, message)
            msg_lines = msg.split('\n')
            if (len(msg_lines) > 0) and (len(msg_lines[-1]) == 0):
                del msg_lines[-1]
            # end if

            test_case_result = self.__create_test_case_result(test.id())
            test_case_result.log.extend(msg_lines)
        # end if
    # end def log

    def addSuccess(self, test, unused=None):
        # See ``BaseVBLogTestListener.addSuccess``
        super().addSuccess(test, unused)

        if not isinstance(test, TestSuite):
            test_case_result = self.__create_test_case_result(test.id())
            test_case_result.state = self.TestCaseResult.STATE_SUCCESS
        # end if
    # end def addSuccess

    def addError(self, test, err):
        # See ``TestListener.addError``
        super().addError(test, err)

        if not isinstance(test, TestSuite):
            # Keep the message for later reference
            test_id = test.id()
            test_case_result = self.__create_test_case_result(test.id())
            test_case_result.set_message(self.nonsuccesses[test_id])
            test_case_result.state = self.TestCaseResult.STATE_ERROR
        # end if
    # end def addError

    def addFailure(self, test, err):
        # See ``TestListener.addFailure``
        super().addFailure(test, err)

        if not isinstance(test, TestSuite):
            # Keep the message for later reference
            test_id = test.id()
            test_case_result = self.__create_test_case_result(test.id())
            test_case_result.set_message(self.nonsuccesses[test_id])
            test_case_result.state = self.TestCaseResult.STATE_FAILED
        # end if
    # end def addFailure

# end class JUnitTestListener


class JUnitLogTestListener(JUnitTestListener):
    """
    JUnit listener including the full log trace in case of failure
    """

    FILE_EXTENSION = 'log.xml'

    def __init__(self, descriptions, verbosity, outputdir, args):
        # See ``JUnitTestListener.__init__``
        # Keep at least the "trace" verbosity level for the .log.xml file to enable a complete test failure analysis
        verbosity = _LEVEL_TRACE if verbosity > _LEVEL_TRACE else verbosity
        BaseVBLogTestListener.__init__(self, descriptions, verbosity, outputdir, args)

        self._test_suites = dict()
        self._properties = dict()
    # end def __init__

# end class JUnitLogTestListener

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
