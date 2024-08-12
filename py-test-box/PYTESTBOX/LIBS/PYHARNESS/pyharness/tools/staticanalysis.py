#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
# pylint:disable=W8008
"""
@package pyharness.tools.staticanalysis

@brief  pyHarness TestCases analysis

@author christophe.roquebert

@date   2018/10/03
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from argparse import ArgumentParser
from os import access
from os import F_OK
from os import makedirs
from os.path import abspath
from os.path import isfile
from os.path import join
from pyharness.core import TestCase
from pyharness.core import TestLoader
from pyharness.core import TestSuite
import builtins
import sys
import warnings


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class NullObject(object):
    """
    A NullObject implementation: a class that always return itself has an
    attribute, and has all attributes.
    """
    def __init__(self, *unused_args, **unused_kw_args):
        """
        Default constructor.

        This is sometimes used when NullObject stands for a TYPE: in such cases
        a call to __new__ is attempted, bypassing the __getattr__ mechanism.

        @option unused_args   [in] (tuple) The unused arguments.
        @option unused_kw_args [in] (dict)  The unused keyword arguments.
        """
        pass
    # end def __init__

    def __getattr__(self, unused):
        """
        Null handler for attribute access

        @param  unused [in] (str) The requested attribute name

        @return self, a null object
        """
        return self
    # end def __getattr__

    @staticmethod
    def __hasattr__(unused):
        """
        Tests whether the object has the associated attribute.
        This is always true.

        @param  unused [in] (str) The requested attribute name

        @return (bool) True
        """
        return True
    # end def __hasattr__
# end class NullObject


class StaticFile(object):
    """
    Represents the contents of a static file.
    """

    def __init__(self, path):
        """
        Constructor.

        @param  path [in] (str) Path to the static file.
        """
        self._path = path
        self._test_cases = {}
    # end def __init__

    def __repr__(self):
        """
        Obtains a string representation of the current object

        @return (str) The current object, as a string.
        """
        return self._path
    # end def __repr__

    def load(self):
        """
        Loads the file from the path
        """
        with open(self._path) as inputFile:
            lines = inputFile.readlines()
        # end with

        test_id = None
        for line in lines:
            if line.startswith('|'):
                test_id = line[1:].strip()
            elif line.startswith(' '):
                line = line.strip()
                test_cases = self._test_cases.setdefault(test_id, [])
                test_cases.append(line)
            # end if
        # end for
    # end def load

    def save(self):
        """
        Saves the file to disk
        """
        lines = []
        for key in sorted(self._test_cases.keys()):
            values = self._test_cases[key]

            lines.append(f'|{key}\n')
            lines.extend([f' {value}\n' for value in values])
            lines.append('\n')
        # end for

        with open(self._path, 'w+') as outputFile:
            outputFile.writelines(lines)
        # end with
    # end def save

    def update(self, values):
        """
        Updates the dictionary with new values

        @param  values [in] (dict) A mapping testId -> tuple of TestCases
        """
        self._test_cases.update(values)
    # end def update

    def getTestCases(self):
        """
        Obtains the dict of TestCases

        @return The dict<testId, testCasesNames>
        """
        return self._test_cases
    # end def getTestCases
# end class StaticFile


class Main(object):
    """
    Perform a static-dynamic analysis of a python tree.

    - The tree is searched for *.py files, and each .py file is parsed.
    - For each *.py file, a list of classes is obtained
    """
    # @name Properties
    # @{
    _BRIEF = 'Generate mapping test scripts / test cases'
    _VERSION = '0.5.2.0'
    # @}

    def get_parser(self):
        """
        Obtains the argument parser, with some options already initialized

        @return ArgumentParser The argument parser, in charge of parsing the command line arguments.
        """
        if self._parser is None:
            parser = ArgumentParser(description=self._BRIEF)
            parser.add_argument('--version', action='version', version=self._VERSION)
            parser.add_argument('-v', '--verbose', dest='verbose', help='maximal output', default=False,
                                action='store_true')
            parser.add_argument('-q', '--quiet', dest='quiet', help='minimal output', default=False,
                                action='store_true')
            parser.add_argument('-o', '--output', dest='output', metavar='OUTPUTS',
                                help='Output to file, defaults to %s' % self.__dict__, default=False)
            parser.add_argument('-F', '--no-files', dest='nofiles', help='Do not writes static files',
                                default=False, action='store_true')
            # positional arguments
            parser.add_argument('files', nargs='+', metavar='FILES', help='pass one or more files')

            parser.epilog = '\n'.join((
                    '',
                    'Examples:',
                    '  %(prog)s                            - analyze the current directory',
                    '  %(prog)s TESTSUITES                 - analyze the TESTSUITES directory',
                    '  %(prog)s --help                     - display this help message',
                    ''))

            self._parser = parser
        # end if

        return self._parser
    # end def get_parser

    parser = property(get_parser)

    def parse_args(self, argv):  # pylint:disable=R0912,R0914,R0915
        """
        Parses the program arguments

        This converts the program arguments to a dictionary, that will be used
        as a parameter to the TestManager instance.

        @param  argv [in] (tuple) The arguments passed in the command line.

        @return (list) List of arguments
        """
        parser = self.get_parser()
        args = parser.parse_args(argv)

        if args.quiet:
            self.verbosity = 0
        # end if

        if args.verbose:
            self.verbosity = 2
            self.descriptions = 1
        # end if

        if args.output:
            self.output = args.output
        # end if

        if args.nofiles:
            self.no_files = True
        # end if

        return args.files
    # end def parse_args

    PACKAGE_MARKERS = {'.test.', '.unittest.', '.integtest.', '.sys.', '.int.', 'unit.', 'integ.'}

    @classmethod
    def analyzeTest(cls, collector, test):
        """
        Analyzes a test for calls to testCaseChecked

        @param  collector [inout] (dict<packageId, dict<testId, testCase>>) The container for collected information
        @param  test      [in]    (TestCase) The test to analyze
        """
        # --- Test suites composite objects are visited recursively
        if isinstance(test, TestSuite):
            for inner_test in test._tests:  # pylint:disable=W0212
                cls.analyzeTest(collector, inner_test)
            # end for

        # --- Test case objects are analyzed directly
        elif isinstance(test, TestCase):
            if not test._testMethodName.startswith("test"):  # pylint:disable=W0212
                return
            # end if

            test_id = test.id()

            test_method = getattr(test, test._testMethodName)  # pylint:disable=W0212
            func = test_method.__func__

            # Extract the package name
            for package_marker in cls.PACKAGE_MARKERS:
                package_end_index = test_id.find(package_marker)
                if package_end_index <= -1:
                    continue
                # end if

                # package_name is used to create the root package for the creation of the static file
                package_name = test_id[:package_end_index + len(package_marker)]

                package_dict = collector.setdefault(package_name, {})

                # A test id must only be checked ONCE
                if test_id not in package_dict:
                    test_cases_for_test = package_dict.setdefault(test_id, [])

                    test_cases_for_test.extend(cls.analyzeCode(func.__code__, func.__globals__))
                # end if
            # end for
        # end if
    # end def analyzeTest

    @staticmethod
    def analyzeCode(co, globs=None):  # pylint:disable=R0912
        """
        Disassemble a code object, looking for calls to:
        - self.testCaseChecked(<globalvar>)
        cf dis — Disassembler for Python bytecode (https://docs.python.org/3/library/dis.html)

        This code uses a FSM to check for the following pattern:
        - LOAD_FAST self
        - LOAD_ATTR testCaseChecked
        - LOAD_GLOBAL <a name>

        @param  co    [in] (func_code) A func_code object
        @param globs [in] (dict)      The globals object for the function

        @return (list) A list of names used as parameters to testCaseChecked
        """
        result = []
        code = co.co_code
        code_len = len(code)
        i = 0
        # from dis import EXTENDED_ARG
        from dis import HAVE_ARGUMENT
        from dis import hasfree
        from dis import haslocal
        from dis import hasname
        from dis import opmap

        op_pop_top = opmap["POP_TOP"]
        op_load_deref = opmap["LOAD_DEREF"]
        op_load_fast = opmap["LOAD_FAST"]
        op_load_attr = opmap["LOAD_ATTR"]
        op_load_method = opmap["LOAD_METHOD"]
        op_load_global = opmap["LOAD_GLOBAL"]
        op_load_consts = opmap["LOAD_CONST"]
        op_dict_update = opmap["DICT_UPDATE"]

        state = 0
        free = None
        while i < code_len:
            op = code[i]

            if (state, op) in ((0, op_load_fast),
                               (0, op_load_deref),
                               (2, op_load_attr),
                               (2, op_load_method),
                               (4, op_load_global),
                               (4, op_load_consts)):
                state += 1
            elif op_pop_top <= op <= op_dict_update:
                # Changed in version 3.11: Some instructions are accompanied by one or more inline cache entries,
                # which take the form of CACHE instructions.
                # That's why we have to exclude def_op('CACHE', 0)
                state = 0
            # end if

            i = i + 1
            if HAVE_ARGUMENT <= op:
                op_arg = code[i]
                # Changed in Python version 3.6: Use 2 bytes for each instruction.
                # Previously the number of bytes varied by instruction.
                i = i + 1  # Skip next byte

                if op in haslocal:
                    if ((state == 1)
                            and (co.co_varnames[op_arg] in ('cls', 'self'))):
                        state += 1
                    else:
                        state = 0
                    # end if

                elif op in hasname:
                    if ((state == 3) and (co.co_names[op_arg] in ('checkTestCase', 'checkTestCaseManual',
                                                                  # Deprecated
                                                                  'testCaseChecked', 'testCaseManualChecked'))):
                        state += 1

                    elif state == 5:
                        if sys.version_info < (3, 10):
                            index = op_arg
                        else:
                            # Changed in version 3.10: The argument of jump, exception handling and loop instructions
                            # is now the instruction offset rather than the byte offset.
                            index = int(op_arg / 2)
                        # end if
                        if index <= len(co.co_names):
                            result.append(co.co_names[index])
                            state = 0
                        # end if
                    else:
                        state = 0
                    # end if

                # Case were the TestCase name is given as a string
                elif (state == 5) and (op in [op_load_consts]):
                    result.append(co.co_consts[op_arg])
                    state = 0

                elif op in hasfree:
                    if free is None:
                        free = co.co_cellvars + co.co_freevars
                    # end if

                    if ((state == 1)
                            and (free[op_arg] in ('cls', 'self'))):
                        state += 1
                    else:
                        state = 0
                    # end if
                elif op <= op_dict_update:
                    state = 0
                # end if
            # end if
        # end while

        if globs is not None:
            result = [r for r in result if (((r in globs) and (r == globs[r])) or (r in co.co_consts))]
        # end if

        return result
    # end def analyzeCode

    def getVersion(self):
        """
        Get version of the static analysis

        @return (str) Version of static analysis
        """
        return self._VERSION
    # end def getVersion

    version = property(getVersion)

    def __init__(self, argv, stdout, stderr):  # pylint:disable=R0912,R0914
        """
        Constructor.

        @param  argv   [in] (tuple)  The program arguments
        @param  stdout [in] (stream) The standard output stream
        @param  stderr [in] (stream) The standard error stream
        """
        self._stdout = stdout
        self._stderr = stderr
        self._parser = None

        self._stdout.write(f"static analysis v {self.getVersion()}\n")
        self.prog_name = argv[0]
        self.default_file = "static"
        self.verbosity = 1
        self.descriptions = 0
        self._static_files = {}
        self.no_files = False
        self.output = None

        args = self.parse_args(argv[1:])

        # Do not replace __import__ by importFqn !
        _import = builtins.__import__
        try:
            def fallback_import(*args, **kwargs):
                """
                An import hook that always works

                @option args   [in] (tuple) arguments
                @option kwargs [in] (dict)  keyword arguments

                @return (Object) The imported target
                """
                try:
                    return _import(*args, **kwargs)
                except ImportError as exception:
                    warnings.warn(exception.msg, category=UserWarning)
                    return NullObject()
                # end try
            # end def fallback_import

            # Do not replace __import__ by importFqn !
            builtins.__import__ = fallback_import

            test_loader = TestLoader()
            for arg in args:
                if isfile(arg):
                    continue
                # end if

                existing_sources = set()
                non_existing_sources = set()

                def method_predicate(method):
                    """
                    Filters test methods, keeping only methods that have an existing source file

                    @param  method [in] (method) The method to inspect

                    @return (bool) Whether the method is acceptable.
                    """
                    f = method.__func__ if hasattr(method, '__func__') else method
                    code = f.__code__ if hasattr(f, '__code__') else f.__code__
                    filename = code.co_filename

                    while True:
                        if filename in existing_sources:
                            return True
                        elif filename in non_existing_sources:
                            return False
                        # end if

                        if access(filename, F_OK):
                            existing_sources.add(filename)
                        else:
                            non_existing_sources.add(filename)
                        # end if
                    # end while
                    return True
                # end def methodPredicate

                tests = test_loader.findTestsInSrcPath(arg, useTestRunner=False, methodPredicate=method_predicate)

                # --- Collect TestCases
                collector = {}
                for test in tests:
                    self.analyzeTest(collector, test)
                # end for

                # --- Write TestCases
                # --- a. Extract the test package list
                for package_name, package_dict in collector.items():

                    test_rel_list = [x for x in package_name.split(".") if (len(x) > 0)]
                    test_cases_rel_list = test_rel_list[:-1]
                    # Static file named from package name and extension .static
                    static_file_name = test_rel_list[-1] if (len(test_cases_rel_list) == 0) else test_cases_rel_list[-1]
                    root = abspath(self.output if (self.output is not None) else arg)
                    test_cases_rel_list.append("testcases")

                    test_cases_dir = join(root, *test_cases_rel_list)
                    if not access(test_cases_dir, F_OK):
                        makedirs(test_cases_dir)
                    # end if

                    test_cases_rel_list.append(f"{static_file_name}.static")
                    test_cases_rel_path = join(*test_cases_rel_list)

                    abs_path = join(root, test_cases_rel_path)

                    static_file = self._static_files.setdefault(abs_path, StaticFile(abs_path))
                    static_file.update(package_dict)
                # end for
            # end for

            # Write all static files
            if not self.no_files:
                for static_file in iter(list(self._static_files.values())):
                    static_file.save()
                # end for
            # end if
        finally:
            # Do not replace __import__ by importFqn !
            builtins.__import__ = _import
        # end try

        self._stdout.write("Done.\n")
    # end def __init__

    def getStaticFiles(self):
        """
        Obtains the list of generated static file objects.

        @return (list) A list of StaticFile instances
        """
        return list(self._static_files.values())
    # end def getStaticFiles
# end class Main


if __name__ == "__main__":
    Main(sys.argv, sys.stdout, sys.stderr)
# end if

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
