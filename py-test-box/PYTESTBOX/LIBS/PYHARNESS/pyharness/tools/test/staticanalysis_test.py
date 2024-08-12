#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.tools.test.staticanalysis

@brief  Tests of the static analysis

@author christophe.roquebert

@date   2018/07/21
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import sys
from importlib import reload
from io import StringIO
from os import makedirs
from os.path import join
from random import randint
from shutil import rmtree
from subprocess import PIPE
from subprocess import Popen
from subprocess import STDOUT
from unittest import TestCase

from pyharness.tools.staticanalysis import Main
from pyharness.tools.staticanalysis import NullObject
from pyharness.tools.staticanalysis import StaticFile
from pylibrary.tools.importutils import importFqn
from pylibrary.tools.tempfile import mkdtemp
from pylibrary.tools.warning import ignorewarning


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class NullObjectTestCase(TestCase):
    '''
    Tests of the NullObject class
    '''
    @classmethod
    def _createInstance(cls):
        '''
        Create a default NullObject instance

        @return (NullObject) NullObject instance
        '''
        return NullObject()
    # end def _createInstance

    def testGetAttr(self):
        '''
        Tests __getattr__ method
        '''
        nullObject = self._createInstance()
        self.assertEqual(nullObject.__getattr__('dummyAttribute'),
                         nullObject,
                         'Method __getattr__ should always return self')
    # end def testGetAttr

    def testHasAttr(self):
        '''
        Tests __hasattr__ method
        '''
        nullObject = self._createInstance()
        self.assertTrue(nullObject.__hasattr__('dummyAttribute'),
                        'Method __hasattr__ should always return True')
    # end def testHasAttr

# end class NullObjectTestCase

class StaticFileTestCase(TestCase):
    '''
    Tests StaticFile class
    '''
    @classmethod
    def _createInstance(cls, path   = 'DefaultPath'):
        '''
        Create a default StaticFile instance

        @option path [in] (string) Path

        @return (StaticFile) StaticFile instance
        '''
        return StaticFile(path)
    # end def _createInstance

    def setUp(self):
        '''
        Test setUp
        '''
        TestCase.setUp(self)

        self.__tempDirPath = mkdtemp("", "test_%s" % self.id())
        self.__savedPathes = None
        sys.path.insert(0, self.__tempDirPath)
    # end def setUp

    def tearDown(self):
        '''
        Test tearDown
        '''
        if (self.__savedPathes is not None):
            for savedPath in self.__savedPathes:
                sys.path.insert(0, savedPath)
            # end for
        # end if
        sys.path.remove(self.__tempDirPath)
        rmtree(self.__tempDirPath, True)

        TestCase.tearDown(self)
    # end def tearDown

    def testRepr(self):
        '''
        Tests __repr__ method
        '''
        expected = 'expectedPath'
        staticFile = self._createInstance(expected)

        self.assertEqual(expected,
                         staticFile.__repr__(),
                         'Wrong StaticFile representation')

    # end def testRepr

    def testLoad(self):
        '''
        Tests the load method
        '''
        staticPath = join(self.__tempDirPath, 'test.static')
        with open(staticPath, 'w+') as staticFile:
            staticContent = '\n'.join(('|test1',
                                       ' TESTCASE_1',
                                       ' TESTCASE_2',
                                       '',
                                       '|test2',
                                       ' TESTCASE_1',
                                       ' TESTCASE_3',))

            staticFile.write(staticContent)
        # end with

        staticFile = self._createInstance(staticPath)
        staticFile.load()

        expected = {'test1' : ['TESTCASE_1', 'TESTCASE_2'],
                    'test2' : ['TESTCASE_1', 'TESTCASE_3'],}
        self.assertEqual(expected,
                         staticFile.getTestCases(),
                         'Wrong loading result')

    # end def testLoad

# end class StaticFileTestCase

class StaticAnalysisTestCase(TestCase):
    '''
    Tests of the StaticAnalysis class, and its derived classes
    '''

    def setUp(self):
        '''
        Test setUp
        '''
        TestCase.setUp(self)

        self.__tempDirPath = mkdtemp("", "test_%s" % self.id())
        self.__savedPathes = None
        sys.path.insert(0, self.__tempDirPath)
    # end def setUp

    def tearDown(self):
        '''
        Test tearDown
        '''
        if (self.__savedPathes is not None):
            for savedPath in self.__savedPathes:
                sys.path.insert(0, savedPath)
            # end for
        # end if
        sys.path.remove(self.__tempDirPath)
        rmtree(self.__tempDirPath, True)

        TestCase.tearDown(self)
    # end def tearDown

    def _testConsistency_Module(self, moduleFqn, scriptContents, expectedMapping):
        '''
        Tests the consistency between a mapping extracted from the given script
        contents and the expected mapping.

        @param  moduleFqn       [in] (str)  Fully qualified name of the module
        @param  scriptContents  [in] (str)  The script to write on disk
        @param  expectedMapping [in] (dict) The mapping to compare to
        '''
        self.__savedPathes = [ppath for ppath in sys.path if (   (    ('PYHARNESS' in ppath)
                                                                  and ppath.endswith('TESTSUITES'))
                                                              or (ppath.endswith('PYTHON')))]
        for savedPath in self.__savedPathes:
            sys.path.remove(savedPath)
        # end for

        # Create the script on disk
        elements = moduleFqn.split('.')

        packagePath = self.__tempDirPath
        for element in elements[:-1]:
            packagePath = join(packagePath, element)
            makedirs(packagePath)

            with open(join(packagePath, '__init__.py'), 'w+') as initFile:
                initFile.write('\n')
            # end with

        # end for

        # Creates an dummy pyharness.core.py with empty class TestCase
        pyharnessPath = join(self.__tempDirPath, 'pyharness')
        makedirs(pyharnessPath)

        with open(join(pyharnessPath, '__init__.py'), 'w+') as initFile:
            initFile.write('\n')
        # end with

        coreContents = '\n'.join(('class TestCase(object):',
                                  '    pass',
                                  ''))
        with open(join(pyharnessPath, 'core.py'), 'w+') as coreFile:
            coreFile.write(coreContents)
        # end with

        with open(join(packagePath, elements[-1] + '.py'), 'w+') as moduleFile:
            moduleFile.write(scriptContents)
        # end with

        stdout = StringIO()
        stderr = StringIO()
        analyzer = Main(['staticanalysis', self.__tempDirPath], stdout, stderr)

        if (expectedMapping is not None):
            self.assertEqual(list(expectedMapping.values())[0],
                             analyzer.getStaticFiles()[0].getTestCases(), #pylint:disable=W0212
                             'Inconsistent static analysis for script:\n%s' % scriptContents)
        # end if

    # end def _testConsistency_Module

    def _testConsistency_Method(self, moduleFqn, testClass, testMethod, scriptContents, expectedMapping):
        '''
        Tests the consistency between a mapping extracted from the given script
        contents and the expected mapping.

        @param  moduleFqn       [in] (str) Fully qualified name of the module
        @param  testClass       [in] (str) Name of the class containing the test
        @param  testMethod      [in] (str) Name of the method containing the test
        @param  scriptContents  [in] (str) The script to write on disk
        @param  expectedMapping [in] (dict) The mapping to compare to
        '''
        # Create the script on disk
        elements = moduleFqn.split('.')

        packagePath = self.__tempDirPath
        for element in elements[:-1]:
            packagePath = join(packagePath, element)
            makedirs(packagePath)

            with open(join(packagePath, '__init__.py'), 'w+') as initFile:
                initFile.write('\n')
            # end with
        # end for

        with open(join(packagePath, elements[-1] + '.py'), 'w+') as moduleFile:
            moduleFile.write(scriptContents)
        # end with

        # Force a module reload
        for subModuleFqn in ['.'.join(elements[:i]) for i in range(1, len(elements) + 1)]:
            module = importFqn(subModuleFqn)
            reload(module)
        # end for


        # Parse the file
        testClass = importFqn('.'.join((moduleFqn, testClass)))
        testCase = testClass(testMethod)

        obtainedMapping = {}
        Main.analyzeTest(obtainedMapping, testCase)

        self.assertEqual(expectedMapping,
                         obtainedMapping,
                         'Inconsistent static analysis for script:\n%s' % scriptContents)
    # end def _testConsistency_Method

    def _testConsistency_Class(self, moduleFqn,
                                     testClass,
                                     scriptContents,
                                     expectedMapping):
        '''
        Tests the consistency between a mapping extracted from the given script
        contents and the expected mapping.

        @param  moduleFqn       [in] (str)  Fully qualified name of the module
        @param  testClass       [in] (str)  Name of the class containing the test
        @param  scriptContents  [in] (str)  The script to write on disk
        @param  expectedMapping [in] (dict) The mapping to compare to
        '''
        # Create the script on disk
        elements = moduleFqn.split('.')

        packagePath = self.__tempDirPath
        for element in elements[:-1]:
            packagePath = join(packagePath, element)
            makedirs(packagePath)

            with open(join(packagePath, '__init__.py'), 'w+') as initFile:
                initFile.write('\n')
            # end with
        # end for

        with open(join(packagePath, elements[-1] + '.py'), 'w+') as moduleFile:
            moduleFile.write(scriptContents)
        # end with

        # Force a module reload
        for subModuleFqn in ['.'.join(elements[:i]) for i in range(1, len(elements) + 1)]:
            module = importFqn(subModuleFqn)
            reload(module)
        # end for


        # Parse the file
        testClass = importFqn('.'.join((moduleFqn, testClass)))
        testCases = [testClass(testMethod) for testMethod in dir(testClass) if testMethod.startswith('test') and testMethod not in ('testCaseChecked', 'testCaseManualChecked')]

        obtainedMapping = {}
        for testCase in testCases:
            Main.analyzeTest(obtainedMapping, testCase)
        # end for

        self.assertEqual(expectedMapping,
                         obtainedMapping,
                         'Inconsistent static analysis for script:\n%s' % scriptContents)
    # end def _testConsistency_Class

    def testStaticAnalysis_Basic(self):
        '''
        Tests a basic case of static analysis
        '''
        moduleFqn = 'staticanalysis.test.' + self.id().rsplit('.')[-1]
        testClass = 'TestCase'
        testMethod = 'testSample'
        scriptContents = '\n'.join(('# -*- coding: utf-8 -*-',
                                    'from pyharness.core import TestCase as ET_TestCase',
                                    'MY_TEST_CASE = "MY_TEST_CASE"',
                                    'class %s(ET_TestCase):' % testClass,
                                    '  def %s(self):' % testMethod,
                                    '    self.testCaseChecked(MY_TEST_CASE)',
                                    ''))
        mapping = {'staticanalysis.test.': {'.'.join((moduleFqn, testClass, testMethod)): ['MY_TEST_CASE'], }}

        self._testConsistency_Method(moduleFqn, testClass, testMethod, scriptContents, mapping)
    # end def testStaticAnalysis_Basic

    def testStaticAnalysis_TwoTests(self):
        '''
        Tests a basic case of static analysis
        '''
        moduleFqn = 'staticanalysis.test.' + self.id().rsplit('.')[-1]
        testClass = 'TestCase'
        testMethod = 'testSample'
        scriptContents = '\n'.join(('from pyharness.core import TestCase as ET_TestCase',
                                    'MY_TEST_CASE1 = "MY_TEST_CASE1"',
                                    'MY_TEST_CASE2 = "MY_TEST_CASE2"',
                                    'class %s(ET_TestCase):' % testClass,
                                    '  def %s1(self):' % testMethod,
                                    '    self.testCaseChecked(MY_TEST_CASE1)',
                                    '',
                                    '  def %s2(self):' % testMethod,
                                    '    self.testCaseChecked(MY_TEST_CASE2)',
                                    ''))
        mapping = {'staticanalysis.test.': {'.'.join((moduleFqn, testClass, testMethod + '1')): ['MY_TEST_CASE1'],
                                            '.'.join((moduleFqn, testClass, testMethod + '2')): ['MY_TEST_CASE2'],
                                            }}
        self._testConsistency_Class(moduleFqn, testClass, scriptContents, mapping)
    # end def testStaticAnalysis_TwoTests

    def testStaticAnalysis_Set(self):
        '''
        Tests a case of static analysis for a method with a set definition
        '''
        moduleFqn = 'staticanalysis.test.' + self.id().rsplit('.')[-1]
        testClass = 'TestCase'
        testMethod = 'testSample'
        scriptContents = '\n'.join(('from pyharness.core import TestCase as ET_TestCase',
                                    'MY_TEST_CASE = "MY_TEST_CASE"',
                                    'class %s(ET_TestCase):' % testClass,
                                    '  def %s(self):' % testMethod,
                                    '    s = {1, 2, 3}',
                                    '    self.testCaseChecked(MY_TEST_CASE)',
                                    ''))
        mapping = {'staticanalysis.test.': {'.'.join((moduleFqn, testClass, testMethod)): ['MY_TEST_CASE'], }}

        self._testConsistency_Method(moduleFqn, testClass, testMethod, scriptContents, mapping)
    # end def testStaticAnalysis_Set

    def testStaticAnalysis_Module(self):
        '''
        Tests a basic case of static analysis on a module
        '''
        moduleFqn = 'staticanalysis%d.test.%s' % (randint(1, 100), self.id().rsplit('.')[-1])
        testClass = 'MyTestCase'
        testMethod = 'testSample'
        scriptContents = '\n'.join(('from pyharness.core import TestCase',
                                    'MY_TEST_CASE = "MY_TEST_CASE"',
                                    'class %s(TestCase):' % testClass,
                                    '  def %s(self):' % testMethod,
                                    '    self.testCaseChecked(MY_TEST_CASE)',
                                    ''))
        mapping = {'staticanalysis.test.': {'.'.join((moduleFqn, testClass, testMethod)): ['MY_TEST_CASE'], }}

        self._testConsistency_Module(moduleFqn, scriptContents, mapping)
    # end def testStaticAnalysis_Module

    @ignorewarning(UserWarning)
    def testStaticAnalysis_WrongImport(self):
        '''
        Tests a wrong case of static analysis with wrong import
        '''
        moduleFqn = 'staticanalysis%d.test.%s' % (randint(1, 100), self.id().rsplit('.')[-1])
        testClass = 'MyTestCase'
        testMethod = 'testSample'
        scriptContents = '\n'.join(('from pyharness.core import TestCase',
                                    'from check.a.wrong import Sorry',
                                    'MY_TEST_CASE = "MY_TEST_CASE"',
                                    'class %s(TestCase):' % testClass,
                                    '  def %s(self):' % testMethod,
                                    '    self.testCaseChecked(MY_TEST_CASE)',
                                    ''))
        self._testConsistency_Module(moduleFqn, scriptContents, None)
    # end def testStaticAnalysis_WrongImport

    def _testCommandLine(self, expected, commands):
        '''
        Tests the call of a script with command line

        @param  expected [in] (str)  Expected script output
        @param  commands [in] (list) List of commands
        '''
        for command in commands:
            args = [sys.executable,
                    self._computeStaticPath(),
                    command]
            process = Popen(args   = args,
                            stdout = PIPE,
                            stderr = STDOUT)
            ouputlines = process.stdout.readlines()                                                                     # pylint:disable=E1101
            process.wait()                                                                                              # pylint:disable=E1101
            ouputline = ''.join(ouputlines)
            if isinstance(expected, str):
                if (ouputline.find(expected) == -1):
                    raise ValueError('Wrong result returned')
                # end if
            elif isinstance(expected, (list, tuple)):
                for elt in expected:
                    assert (elt in ouputline), \
                           "Missing element of log! %s" % elt
                # end for
            # end if
        # end for
    # end def _testCommandLine

    @staticmethod
    def _computeStaticPath():
        '''
        Compute static analysis module path

        @return (string) Static analysis module fully qualify name
        '''
        pythonPath = [ppath for ppath in sys.path if (    ('PYHARNESS' in ppath)
                                                      and ppath.endswith('TESTSUITES'))]
        scriptPath = [pythonPath[0],]
        scriptPath.extend(Main.__module__.split('.'))                                                                   #@UndefinedVariable
        scriptPath[-1] = '%s.py' % scriptPath[-1]
        scriptPath = '\\'.join(scriptPath)
        return scriptPath
    # end def _computeStaticPath
#
#    def testHelp(self):
#        '''
#        Tests help output
#        '''
#        expected = '%s\n' % (Main.USAGE % {'progName':    self._computeStaticPath(),
#                                           'defaultFile': "static"})
#        expected = expected.split('\n')
#        self._testCommandLine(expected, ['--help', '-h'])
#    # end def testHelp

# end class StaticAnalysisTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
