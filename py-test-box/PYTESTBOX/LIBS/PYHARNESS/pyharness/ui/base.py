#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
@package pyharness.ui.base

@brief  Base module for the implementation of User Interfaces

@author christophe.roquebert

@date   2018/02/04
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import re
import sys
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from os import R_OK
from os import access
from os.path import abspath
from os.path import join
from os.path import normpath

from pyharness.arguments import KeywordArguments
from pyharness.consts import DEFAULT_OUTPUT_DIRECTORY
from pyharness.context import ContextLoader
from pyharness.core import TestListener
from pyharness.core import _LEVEL_DEBUG
from pyharness.core import _LEVEL_ERROR
from pyharness.core import _LEVEL_RAW
from pyharness.core import _LEVEL_TRACE
from pyharness.debugger import DebuggerCoverageTestListener
from pyharness.output.configui import ConfigTestListener
from pyharness.output.eclipseui import EclipseTestListener
from pyharness.output.jrlui import JrlTestListener
from pyharness.output.junitui import JUnitLogTestListener
from pyharness.output.junitui import JUnitTestListener
from pyharness.output.logui import LogTestListener
from pyharness.output.loopui import LoopTestListener
from pyharness.output.metricsui import MetricsTestListener
from pyharness.output.pydevui import PyDevTestListener
from pyharness.output.reportui import RunReportTestListener
from pyharness.output.stdoutui import StdoutTestListener
from pyharness.output.testcasesui import DynamicTestListener
from pyharness.output.testdataui import TestDataTestListener
from pyharness.output.textui import TextTestListener
from pyharness.output.xmlui import XmlTestListener
from pylibrary.tools.importutils import fqnFromLocation
from pylibrary.tools.importutils import importFqn

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

# @name Available output types
#  These can be either one TestListener type, or several TestListeners at once.
# @{
OUTPUT_TYPES = {
        'console'  : (TextTestListener,),
        'stdout'   : (StdoutTestListener,),
        'xml'      : (XmlTestListener, RunReportTestListener),
        'log'      : (LogTestListener,),
        'jrl'      : (JrlTestListener, DynamicTestListener, ConfigTestListener, LoopTestListener),
        'junit'    : (JUnitTestListener,),
        'junit-log': (JUnitLogTestListener,),
        'pydev'    : (PyDevTestListener,),
        'eclipse'  : (EclipseTestListener,),
        'coverage' : (DebuggerCoverageTestListener,),
        'metrics'  : (MetricsTestListener,),
        'test_data': (TestDataTestListener,),
        }
# @}

OUTPUT_TYPES_KEYS = sorted(OUTPUT_TYPES.keys())

LOOP_STOP_CHOICES = ('error', 'failure', 'success', 'none')

class BaseProgram(object):
    """
    Base implementation of the main program.

    This implementation is in charge or parsing the arguments in a common,
    centralized way, so that ALL implementation of the PyHarness UI share the
    same set of command-line options.
    """

    @staticmethod
    def _get_version_string(full=False):
        """
        Obtains the version string for PyHarness.

        The full version string also lists the loaded egg versions.

        @option full [in] (bool) Whether the full versions are needed.

        @return (str) A version string.
        """
        py_harness_version = 'Unknown'

        # Obtain version from pysetup
        from pysetup import LOADED_EGG_PATHS

        egg_names_and_versions = []
        for egg in list(LOADED_EGG_PATHS.values()):
            egg_name = egg.getName()
            egg_version = egg.getVersion()

            if egg_name == 'PyHarness':
                py_harness_version = egg_version
            # end if

            egg_names_and_versions.append((egg_name, egg_version))
        # end for

        if not full:
            return py_harness_version
        else:
            return f'PyHarness {py_harness_version}\nLoaded eggs:\n  ' \
                   + '\n  '.join([f'{eggName}: {eggVersion}' for eggName, eggVersion in sorted(egg_names_and_versions)])
        # end if
    # end def _get_version_string

    @staticmethod
    def __cmdline_to_list(cmdline):  # pylint:disable=R0912
        """
        Converts a command line to a list

        @param  cmdline [in] (str) The command line to process

        @return A list of arguments
        """
        # Step 1: Translate all literal quotes into QUOTE.  Justify number
        # of backspaces before quotes.
        tokens = []
        bs_buf = ""
        quote = 1
        # pylint:disable=C0103
        for c in cmdline:
            if c == '\\':
                bs_buf += c
            elif c == '"' and bs_buf:
                # A quote preceded by some number of backslashes.
                num_bs = len(bs_buf)
                tokens.extend(["\\"] * (num_bs // 2))
                bs_buf = ""
                if num_bs % 2:
                    # Odd.  Quote should be placed literally in array
                    tokens.append(quote)
                else:
                    # Even.  This quote serves as a string delimiter
                    tokens.append('"')
                # end if
            else:
                # Normal character (or quote without any preceding
                # backslashes)
                if bs_buf:
                    # We have backspaces in buffer.  Output these.
                    tokens.extend(list(bs_buf))
                    bs_buf = ""
                # end if

                tokens.append(c)
            # end if
        # end for

        # Step 2: split into arguments
        # Array of strings
        result = []
        quoted = False
        # Current argument
        arg = []
        tokens.append(" ")
        for c in tokens:
            if c == '"':
                # Toggle quote status
                quoted = not quoted
            elif c == quote:
                arg.append('"')
            elif c in (' ', '\t'):
                if quoted:
                    arg.append(c)
                else:
                    # End of argument.  Output, if anything.
                    if arg:
                        result.append(''.join(arg))
                        arg = []
                    # end if
                # end if
            else:
                # Normal character
                arg.append(c)
            # end if
        # end for

        return result
    # end def __cmdline_to_list

    @classmethod
    def _expand_argv(cls, argv):  # pylint:disable=R0912
        """
        Expands argv's --file argument, to inject

        @param  argv [in] (list) List of args to expand

        @return Expanded args
        """
        new_argv = []
        skip = False
        for i, value in enumerate(argv):
            new_arg = None
            file_path = None
            if not skip:
                if value.startswith('--file='):
                    file_path = value[len('--file='):]
                    new_arg = (value,)
                elif value in ('--file', '-f'):
                    if (i + 1) < len(argv):
                        file_path = argv[i + 1]
                        new_arg = (value, file_path)
                        skip = True
                    # end if
                else:
                    file_path = None
                    new_argv.append(value)
                # end if
            else:
                skip = False
            # end if

            if file_path is not None:

                re_match = cls.PYTHON_FILE_PATTERN.match(file_path)
                if not re_match:
                    # Load the file from the path
                    with open(file_path, 'r') as inputFile:
                        input_lines = [line.strip() for line in inputFile.read().split('\n')]
                    # end with
                    input_lines = [line for line in input_lines if (len(line) and (not line.startswith('#')))]

                    sub_argv = []
                    for input_line in input_lines:
                        sub_argv.extend(cls.__cmdline_to_list(input_line))
                    # end for
                    new_argv.extend(cls._expand_argv(sub_argv))
                else:
                    new_argv.extend(new_arg)
                # end if
            # end if
        # end for

        return new_argv
    # end def _expand_argv

    def get_parser(self):
        """
        Obtains the argument parser, with some options already initialized

        @return ArgumentParser The argument parser, in charge of parsing the command line arguments.
        """
        if self._parser is None:
            parser = ArgumentParser(
                    formatter_class=lambda prog: RawDescriptionHelpFormatter(prog, max_help_position=43, width=115))

            # ------------------------------------------------------------------
            parser.add_argument('--version', action='version', version=self._get_version_string())
            parser.add_argument('-f', '--file', dest='file', metavar='FILE', action='store', default=None,
                                help='parse command line from FILE')
            parser.add_argument('-r', '--root', dest='root', metavar='ROOT', action='store', default=None,
                                help='use ROOT as the test directory')
            parser.add_argument('pargs', nargs='+', metavar='POSITIONAL_ARGS', help='positional arguments')

            # ------------------------------------------------------------------
            group = parser.add_argument_group('Config')
            group.add_argument('-M', '--mode', dest='mode', metavar='MODE', action='store', default=None,
                               help='use the specified MODE')
            group.add_argument('-P', '--product', dest='product', metavar='PRODUCT', action='store', default=None,
                               help='use the specified PRODUCT')
            group.add_argument('-T', '--target', dest='target', metavar='TARGET', action='store', default=None,
                               help='use the specified TARGET')
            group.add_argument('-V', '--variant', dest='variant', metavar='VARIANT', action='store', default=None,
                               help='use the specified VARIANT')

            # ------------------------------------------------------------------
            group = parser.add_argument_group('Input')
            group.add_argument('--no-level', dest='nolevel', metavar='LEVELS', action='store', default=None,
                               help='only run tests without these LEVELS')
            group.add_argument('-i', '--input', dest='profile', metavar='FILTERPROFILE', action='store', default=None,
                               help='use FILTERPROFILE to filter the tests')
            group.add_argument('-l', '--level', dest='level', metavar='LEVELS', action='store', default=None,
                               help='only run tests with these LEVELS')
            group.add_argument('-s', '--sort', dest='sort', metavar='SORTPROFILE', action='store', default=None,
                               help='use SORTPROFILE to sort the tests')

            # ------------------------------------------------------------------
            group = parser.add_argument_group('Output')
            group.add_argument('--nochm', dest='nochm', action='store_true', default=False,
                               help='disable chm generation')
            group.add_argument('--report', dest='report', action='store_true', default=False,
                               help='generate a report after a run (xml output mandatory)')
            group.add_argument('-c', '--coverage', dest='coverage', action='store_true', default=False,
                               help='collect coverage info')
            group.add_argument('-e', '--erase', dest='erase', action='store_true', default=False,
                               help='erase log files/journal before run')
            group.add_argument('-k', '--keep', dest='keep', action='store_true', default=False,
                               help='keep log files if successful')
            group.add_argument('-o', '--output', dest='output', metavar='OUTPUTS', default=False,
                               help=f'output to OUTPUTS formats (defaults: [{KeywordArguments.OUTPUTS_DEFAULT}])')

            # ------------------------------------------------------------------
            group = parser.add_argument_group('Verbosity')
            group.add_argument('-m', '--medium', dest='medium', action='store_true', default=False,
                               help='medium output')
            group.add_argument('-q', '--quiet', dest='quiet', action='store_true', default=False, help='minimal output')
            group.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                               help='maximal output')
            # ------------------------------------------------------------------
            group = parser.add_argument_group('Execution')
            group.add_argument('--loop-count', dest='loopN', metavar='COUNT', action='store', default=0,
                               help='loop at most COUNT times')
            group.add_argument('--loop-stop', dest='loopStop', metavar='CONDITIONS', action='store', default=None,
                               help='stop run on CONDITIONS (error, failure, success)')
            group.add_argument('-t', '--threads', dest='threads', metavar='COUNT', action='store', default=0,
                               help='use COUNT concurrent threads')

            self._parser = parser
        # end if

        return self._parser
    # end def get_parser

    parser = property(get_parser)

    DEFAULT_ARGUMENTS_OVERRIDE = {}

    PYTHON_FILE_PATTERN = re.compile("(.*\\.py)(?::(\\d+))?$")

    def __init__(self, argv=None, *args, **kwargs):
        """
        Constructor.

        Initializes member variables.

        @option argv   [in] (tuple)  Program arguments (including program name)
        @option stdout [in] (stream) The standard output
        @option stderr [in] (stream) The standard error output
        @option args   [in] (tuple)  Arguments
        @option kwargs [in] (dict)   Keyword arguments
        """
        # This is used for USAGE trace
        self.prog_name = (argv and argv[0]) or sys.argv[0]
        self.output_types = ",".join(list(OUTPUT_TYPES.keys()))
        self.result = 0
        self._parser = None

        kw_args = {}
        kw_args.update(KeywordArguments.DEFAULT_ARGUMENTS)
        kw_args.update(self.DEFAULT_ARGUMENTS_OVERRIDE)

        from pysetup import TESTS_PATH

        kw_args[KeywordArguments.KEY_ROOT] = TESTS_PATH

        self._default_kw_args = kw_args

        self._command_line_kw_args = {}
    # end def __init__

    def get_default_kw_args(self):
        """
        Obtains the original, unmodified kw_args

        @return The original, unmodified kw_args
        """
        return self._default_kw_args
    # end def get_default_kw_args

    def get_command_line_kw_args(self, full=True):
        """
        Obtains the command-line kw_args

        @option full [in] (bool) Whether to return the full kw_args, or only
                                 those set from the command line

        @return The command-line kw_args, without the default values
        """
        result = {}

        if full:
            result.update(self.get_default_kw_args())
        # end if

        result.update(self._command_line_kw_args)

        return result
    # end def get_command_line_kw_args

    def set_command_line_kw_args(self, value):
        """
        Set the command line kw_args

        :param value: kw_args
        :type value: ``list``
        :return: None
        """
        self._command_line_kw_args = value
    # end def set_command_line_kw_args

    def get_current_kw_args(self, full=True):
        """
        Obtains the current kw_args
        This is only possible in UIs where the user may dynamically change
        the keyword arguments.

        By default, the original kwargs are returned

        @option full [in] (bool) Whether to return the full kw_args, or only
                         those set from GUI
        @return The current, possibly modified kw_args
        """
        result = {}

        if full:
            result.update(self.get_command_line_kw_args(full))
        # end if

        return result
    # end def get_current_kw_args

    def parse_args(self, argv, kw_args=None, test_ids=None):  # pylint:disable=R0912,R0914,R0915
        """
        Parses the program arguments

        This converts the program arguments to a dictionary, that will be used
        as a parameter to the TestManager instance.

        @param  argv    [in] (tuple) The arguments passed in the command line.
        @param kw_args  [in] (dict)  A collecting dictionary for the keyword arguments.
                                     This should be a COPY for the default keyword arguments.
        @param  test_ids [in] (tuple) A collecting sequence for the available test Ids

        @return A dict of keyword arguments, passed to the inner structures.
        """
        parser = self.get_parser()
        argv = self._expand_argv(argv)
        args = parser.parse_args(argv)

        # The test IDs specified in the command line.
        # These IDs are cleaned up before actual use.
        inner_test_ids = [x for x in args.pargs]
        inner_test_ids = [y.strip() for y in inner_test_ids]
        inner_test_ids = [y for y in inner_test_ids if len(y) > 0]
        if test_ids is None:
            test_ids = inner_test_ids
        else:
            test_ids.extend(inner_test_ids)
        # end if

        # Obtain a copy of the default Keyword arguments
        # The KeywordArguments are a way to pass arguments through all the
        # program layers, without actually adding parameters each time a new
        # argument is needed.
        if kw_args is None:
            kw_args = {}
        # end if

        # Iterate over the args.
        if args.quiet:
            kw_args[KeywordArguments.KEY_VERBOSITY] = KeywordArguments.VERBOSITY_QUIET
        # end if

        if args.medium:
            kw_args[KeywordArguments.KEY_VERBOSITY] = KeywordArguments.VERBOSITY_MEDIUM
        # end if

        if args.verbose:
            kw_args[KeywordArguments.KEY_VERBOSITY] = KeywordArguments.VERBOSITY_VERBOSE
        # end if

        if args.root:
            # The root directory, normally PYTESTBOX/TESTS, but may differ.
            # It MUST contain at least a TESTSUITES sub-directory.
            roots = [abspath(r) for r in args.root.strip().split(',')]
            kw_args[KeywordArguments.KEY_ROOT] = roots[0]

            if len(roots) > 1:
                kw_args[KeywordArguments.KEY_EXTENDEDROOTS] = roots[1:]
            # end if
        # end if

        if args.threads:
            kw_args[KeywordArguments.KEY_THREADS] = int(args.threads)
        # end if

        if args.loopN:
            # Loop <value> times
            loop_count = int(args.loopN)

            overrides = kw_args.setdefault(KeywordArguments.KEY_OVERRIDES, [])
            override = f"INTERNALCONFIG.loopCount={loop_count:d}"
            overrides.append(override)
        # end if

        if args.loopStop:
            # Stop on the run on the specified condition
            stop_conditions = args.loopStop.strip().split(',')
            for cond in stop_conditions:
                if cond not in LOOP_STOP_CHOICES:
                    self.usage_exit(f'Wrong loop-stop choice: {cond}. Should be in {LOOP_STOP_CHOICES}')
                # end if
            # end for
            kw_args[KeywordArguments.KEY_LOOP_STOP] = stop_conditions
        # end if

        if args.coverage:
            override = f"{ContextLoader.SECTION_CONFIG}.{ContextLoader.OPTION_COVERAGE}=True"
            overrides = kw_args.setdefault(KeywordArguments.KEY_OVERRIDES, [])
            overrides.append(override)
        # end if

        if args.file:
            value = args.file.strip()
            re_match = self.PYTHON_FILE_PATTERN.match(value)
            if re_match is not None:
                groups = re_match.groups()
                file_path = groups[0]
                line_num = groups[1]
                if line_num is not None:
                    line_num = int(line_num)
                # end if

                fqn = fqnFromLocation(file_path, line_num)
                if fqn is None:
                    self.usage_exit(
                            f"Unable to locate a test at:\n<{file_path}{line_num is None and '>' or f':{line_num}>'}")
                # end if

                kw_args[KeywordArguments.KEY_SUITE] = fqn
            elif access(value, R_OK):
                with open(value, 'r') as argFile:
                    inner_args = [x.strip() for x in argFile.readlines()]
                # end with
                inner_args = [x for x in inner_args if len(x) > 0]
                inner_args = [x for x in inner_args if not x.startswith('#')]
                self.parse_args(inner_args, kw_args, test_ids)
            # end if
        # end if

        if args.output:
            # kw_args[KEY_OUTPUTS] contains the default keys.
            # depending on the given keys, those are added to, or removed
            default_keys = kw_args.setdefault(KeywordArguments.KEY_OUTPUTS, "").split(",")
            default_keys = set([k for k in default_keys if len(k)])

            mandatory_keys = (key for key, values in OUTPUT_TYPES.items() if values[0].MANDATORY)
            mandatory_keys = set((k for k in mandatory_keys if len(k)))

            options_keys = args.output.strip().split(",")
            disabled_keys = set((k[3:] for k in options_keys if (k.startswith('no-') and (len(k) > 3))))
            enabled_keys = set((k for k in options_keys if ((not k.startswith('no-')) and len(k))))

            new_listener_keys = (default_keys | mandatory_keys | enabled_keys) - disabled_keys
            for key in new_listener_keys:
                # Check that the listener key is appropriate.
                # It must be either:
                # - A key in the pre-defined output types
                # - a valid, fully-qualified name to a class
                listener_class = None
                if key not in OUTPUT_TYPES:
                    try:
                        listener_class = importFqn(key)
                    except ImportError:
                        msg = '\n'.join((f"Unknown output type: {key}",
                                         f" Available OUTPUTS: [{','.join(list(OUTPUT_TYPES.keys()))}]\n"
                                         ))
                        self.usage_exit(msg)
                    except ValueError:
                        self.usage_exit(f"Unable to import: {key}")
                    # end try

                    # If the listener class is not an instance of a TestListener
                    # there is a _potential_ problem (i.e. a class implementing
                    # the same interface as the TestListener class would make do
                    # but it is a _bad_ design decision). So, we stop.
                    if not issubclass(listener_class, TestListener):
                        self.usage_exit(f"Class {key} must be a subclass of TestListener")
                    # end if

                    # The new key is a valid key, for a valid class
                    # We add it to the possible outputs: the listener
                    # instance will be created later.
                    OUTPUT_TYPES[key] = (listener_class,)
                # end if
            # end for

            kw_args[KeywordArguments.KEY_OUTPUTS] = ",".join(new_listener_keys)
        # end if

        if args.level:
            kw_args[KeywordArguments.KEY_LEVELS] = args.level.strip()
        # end if

        if args.nolevel:
            kw_args[KeywordArguments.KEY_NO_LEVELS] = args.nolevel.strip()
        # end if

        if args.keep:
            kw_args[KeywordArguments.KEY_KEEPLOGS] = True
        # end if

        if args.erase:
            kw_args[KeywordArguments.KEY_ERASELOGS] = True
        # end if

        if args.report:
            kw_args[KeywordArguments.KEY_GENERATERUNREPORT] = True
        # end if

        if args.product:
            overrides = kw_args.setdefault(KeywordArguments.KEY_OVERRIDES, [])
            override = f"{ContextLoader.SECTION_PRODUCT}.{ContextLoader.OPTION_VALUE}={args.product}"
            overrides.append(override)
        # end if

        if args.variant:
            overrides = kw_args.setdefault(KeywordArguments.KEY_OVERRIDES, [])
            override = f"{ContextLoader.SECTION_VARIANT}.{ContextLoader.OPTION_VALUE}={args.variant}"
            overrides.append(override)
        # end if

        if args.target:
            overrides = kw_args.setdefault(KeywordArguments.KEY_OVERRIDES, [])
            override = f"{ContextLoader.SECTION_TARGET}.{ContextLoader.OPTION_VALUE}={args.target}"
            overrides.append(override)
        # end if

        if args.mode:
            overrides = kw_args.setdefault(KeywordArguments.KEY_OVERRIDES, [])
            override = f"{ContextLoader.SECTION_MODE}.{ContextLoader.OPTION_VALUE}={args.mode}"
            overrides.append(override)
        # end if

        if args.nochm:
            kw_args[KeywordArguments.KEY_NO_CHM] = 'True'
        # end if

        if args.profile:
            kw_args[KeywordArguments.KEY_FILTERING_PROFILE] = args.profile
        # end if

        if args.sort:
            kw_args[KeywordArguments.KEY_SORTING_PROFILE] = args.sort
        # end if

        if len(test_ids) > 0:
            included_patterns = "|".join([f"(?:{x})" for x in test_ids])
            kw_args[KeywordArguments.KEY_INCLUDEDPATTERNS] = included_patterns
        # end if

        return kw_args
    # end def parse_args

    # Conversion form verbosity to level
    __V2L = (_LEVEL_ERROR, _LEVEL_TRACE, _LEVEL_RAW, _LEVEL_DEBUG)

    def initializeListeners(self, test_manager, kw_args):
        """
        Create the listeners for this test run.

        This converts the listeners from kwArg to instances of the TestListener class.

        @param  test_manager [in] (TestManager) The test_manager that is used to
                                               obtain the output directory.
        @param  kw_args      [in] (dict)        The keyword arguments, extracted from
                                               the command line.
        @return A sequence of listeners created from the listener keys.
        """
        # Obtain the verbosity of the listeners.
        # The verbosity is not used by all listeners, but is necessary.
        verbosity = self.__V2L[kw_args[KeywordArguments.KEY_VERBOSITY]]
        descriptions = False

        # Extract the current configuration from the config file.
        # This is used to deduce the output directory
        selected_product = test_manager.getSelectedProduct()
        selected_variant = test_manager.getSelectedVariant()
        selected_target = test_manager.getSelectedTarget()
        output_dir = str(normpath(join(kw_args[KeywordArguments.KEY_ROOT],
                                       DEFAULT_OUTPUT_DIRECTORY,
                                       selected_product or "No product",
                                       selected_variant or "No variant",
                                       selected_target or "No target")))

        if sys.platform == 'win32' and not output_dir.startswith('\\\\?'):
            output_dir = '\\\\?\\' + output_dir
        # end if

        # Additional arguments for the listeners: Whether to keep the logs
        args = kw_args

        listeners = []
        output_keys = [x for x in kw_args[KeywordArguments.KEY_OUTPUTS].split(",") if len(x) > 0]
        for output_key in output_keys:
            listener_classes = None
            if output_key in OUTPUT_TYPES:
                listener_classes = OUTPUT_TYPES[output_key]
            else:
                try:
                    listener_classes = (importFqn(output_key),)
                except ImportError:
                    self.usage_exit(f"Unknown output: {output_key}")
                # end try
            # end if

            for listener_class in listener_classes:
                listener = listener_class(descriptions, verbosity, output_dir, args)
                listeners.append(listener)
            # end for
        # end for

        for listener in listeners:
            listener.synchronize(listeners)
        # end for

        return listeners
    # end def initializeListeners

    def usage_exit(self, msg=None):
        """
        Prints usage and exit.

        @option msg [in] (str) An additional message to display before the usage string.
        """
        kw_args = self.get_default_kw_args()
        examples = f"""Examples:
  {self.prog_name}                           - run default set of tests
  {self.prog_name} MyTestSuite               - run suite 'MyTestSuite'
  {self.prog_name} MyTestCase.testSomething  - run MyTestCase.testSomething
  {self.prog_name} MyTestCase                - run all 'test*' test methods in MyTestCase
  {self.prog_name} --root=.                  - run all 'test*' test methods in all modules of all packages in 
                                               ./TESTSUITES, using Settings.ini from ./LOCAL/Settings.ini
  {self.prog_name} --output=xml              - run all 'test*' test methods in all modules of all packages in 
                                               {kw_args[KeywordArguments.KEY_ROOT]}/TESTSUITES,
                                               writing results as XML files
  {self.prog_name} --level=manual            - run all tests that have a 'manual' run level, and all tests 
  that do not  specify a level
"""
        msg = '\n'.join(('' if (msg is None) else msg,
                        self.parser.format_help(),
                        examples))

        self.parser.exit(2, msg)
    # end def usage_exit

    @staticmethod
    def _check_config_ini(kw_args):
        """
        Checks the Settings.ini file: if not present, it is initialized.
        If present, proceed.

        @param  kw_args [in] (dict) The keyword arguments of the run.
        """
        root_paths = [kw_args[KeywordArguments.KEY_ROOT]]
        root_paths.extend(kw_args[KeywordArguments.KEY_EXTENDEDROOTS])
        root_paths = [abspath(r) for r in root_paths]

        unused = ContextLoader.loadConfig(rootPaths=root_paths,
                                          overrides=kw_args[KeywordArguments.KEY_OVERRIDES],
                                          failOnError=not kw_args[KeywordArguments.KEY_SILENT_CONFIG_GEN])
        del unused
    # end def _check_config_ini
# end class BaseProgram

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
