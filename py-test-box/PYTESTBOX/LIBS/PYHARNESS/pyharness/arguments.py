#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.arguments

@brief  Global arguments for the current application

@author christophe.roquebert

@date   2018/09/13
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path                            import abspath
from pyharness.consts                   import DEFAULT_OUTPUT_DIRECTORY
from os.path                            import join
from os.path                            import sep
import sys

try:
    from pysetup                        import PROJECT_NAME                                                             # @UnresolvedImport #pylint:disable=E0611
except ImportError:
    PROJECT_NAME = 'PYHARNESS'
# end try

try:
    from pysetup                        import TESTS_PATH as ROOT_DEFAULT_GLOBAL                                         # @UnresolvedImport #pylint:disable=E0611
except ImportError:
    ROOT_DEFAULT_GLOBAL = abspath(sys.argv[0])
    BLOCK = sep + 'TESTS' + sep
    ROOT_DEFAULT_GLOBAL = join(ROOT_DEFAULT_GLOBAL[:ROOT_DEFAULT_GLOBAL.index(BLOCK) + len(BLOCK)])
# end try

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KeywordArguments(object):
    '''
    This holds the definition of the constants for the program arguments
    '''

    KEY_VERBOSITY             = "verbosity"
    VERBOSITY_QUIET           = 0
    VERBOSITY_MEDIUM          = 1
    VERBOSITY_COMPLETE        = 2
    VERBOSITY_VERBOSE         = 3
    VERBOSITY_DEFAULT         = VERBOSITY_COMPLETE

    KEY_ROOT                  = "root"
    ROOT_DEFAULT              = ROOT_DEFAULT_GLOBAL

    KEY_EXTENDEDROOTS         = "extendedroots"
    EXTENDEDROOTS_DEFAULT     = tuple()

    KEY_THREADS               = "threads"
    THREADS_DEFAULT           = "1"

    KEY_DEBUG                 = "debug"
    DEBUG_DEFAULT             = "False"

    KEY_INCLUDEDPATTERNS      = "includedpatterns"
    INCLUDEDPATTERNS_DEFAULT  = "(?:.*)"

    KEY_EXCLUDEDPATTERNS      = "excludedpatterns"
    EXCLUDEDPATTERNS_DEFAULT  = "(?:^$)"

    KEY_LEVELS                = "levels"
    LEVELS_DEFAULT            = ".*"

    KEY_NO_LEVELS             = "nolevels"
    NO_LEVELS_DEFAULT         = ""

    KEY_SUITE                 = "suite"
    SUITE_DEFAULT             = "testrunner.RootTestRunner"

    KEY_KEEPLOGS              = "keeplogs"
    KEEPLOGS_DEFAULT          = False

    KEY_ERASELOGS             = "eraselogs"
    ERASELOGS_DEFAULT         = False

    KEY_GENERATERUNREPORT     = "generaterunreport"
    GENERATERUNREPORT_DEFAULT = False

    KEY_OUTPUTDIR             = "outputdir"
    OUTPUTDIR_DEFAULT         = DEFAULT_OUTPUT_DIRECTORY

    KEY_TESTMANAGER           = "testmanager"
    TESTMANAGER_DEFAULT       = "pyharness.testmanager.LocalTestManager"

    KEY_OUTPUTS               = "outputs"
    OUTPUTS_DEFAULT           = "log,xml,jrl"

    KEY_NO_CHM                = "nochm"
    NO_CHM_DEFAULT            = "False"

    KEY_FILTERING_PROFILE     = "filteringprofile"
    FILTERING_PROFILE_DEFAULT = "DEFAULT"

    KEY_SORTING_PROFILE       = "sortingprofile"
    SORTING_PROFILE_DEFAULT   = "DEFAULT"

    KEY_CUSTOM_FILTER         = "customfilter"
    CUSTOM_FILTER_DEFAULT     = lambda _1, _2: True

    KEY_CUSTOM_SORTER         = "customsorter"
    CUSTOM_SORTER_DEFAULT     = lambda _1, _2: 0

    KEY_OVERRIDES             = "overrides"
    OVERRIDES_DEFAULT         = []

    KEY_MANUALUI              = "manualui"
    MANUALUI_DEFAULT          = None

    KEY_LOOP_STOP             = "loop_stop"
    LOOP_STOP_DEFAULT         = tuple()

    KEY_DEBUGGER_COVERAGE     = "auto_coverage"
    DEBUGGER_COVERAGE_DEFAULT = False

    KEY_SILENT_CONFIG_GEN     = "silent_config_generation"
    SILENT_CONFIG_GEN_DEFAULT = False

    DEFAULT_ARGUMENTS = {
                         KEY_VERBOSITY:         VERBOSITY_DEFAULT,
                         KEY_ROOT:              ROOT_DEFAULT,
                         KEY_EXTENDEDROOTS:     EXTENDEDROOTS_DEFAULT,
                         KEY_DEBUG:             DEBUG_DEFAULT,
                         KEY_INCLUDEDPATTERNS:  INCLUDEDPATTERNS_DEFAULT,
                         KEY_EXCLUDEDPATTERNS:  EXCLUDEDPATTERNS_DEFAULT,
                         KEY_LEVELS:            LEVELS_DEFAULT,
                         KEY_NO_LEVELS:         NO_LEVELS_DEFAULT,
                         KEY_SUITE:             SUITE_DEFAULT,
                         KEY_KEEPLOGS:          KEEPLOGS_DEFAULT,
                         KEY_ERASELOGS:         ERASELOGS_DEFAULT,
                         KEY_GENERATERUNREPORT: GENERATERUNREPORT_DEFAULT,
                         KEY_TESTMANAGER:       TESTMANAGER_DEFAULT,
                         KEY_THREADS:           THREADS_DEFAULT,
                         KEY_OUTPUTS:           OUTPUTS_DEFAULT,
                         KEY_NO_CHM:            NO_CHM_DEFAULT,
                         KEY_CUSTOM_FILTER:     CUSTOM_FILTER_DEFAULT,
                         KEY_CUSTOM_SORTER:     CUSTOM_SORTER_DEFAULT,
                         KEY_OVERRIDES:         OVERRIDES_DEFAULT,
                         KEY_MANUALUI:          MANUALUI_DEFAULT,
                         KEY_LOOP_STOP:         LOOP_STOP_DEFAULT,
                         KEY_DEBUGGER_COVERAGE: DEBUGGER_COVERAGE_DEFAULT,
                         KEY_FILTERING_PROFILE: FILTERING_PROFILE_DEFAULT,
                         KEY_SORTING_PROFILE:   SORTING_PROFILE_DEFAULT,
                         KEY_SILENT_CONFIG_GEN: SILENT_CONFIG_GEN_DEFAULT,
                         }
# end class KeywordArguments

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
