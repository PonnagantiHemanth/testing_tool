#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
@package pyharness.ui.console.main

@brief  Handles the console text interface.

@author christophe.roquebert

@date   2018/02/04
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.arguments import KeywordArguments
from pyharness.core import TestListener
from pyharness.filtering import DEFAULT_FILTERING_PROFILES
from pyharness.filtering import FilteringProfile
from pyharness.sorting import DEFAULT_SORTING_PROFILE
from pyharness.sorting import SortingProfile
from pyharness.testmanager import LocalTestManager
from pyharness.ui.base import BaseProgram
from os import F_OK
from os import access
from os import listdir
from os.path import join
from xml.dom.minidom import parse
import sys


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ErrorLevelListener(TestListener):
    """
    A collector for test results, that updates the ErrorLevel of the
    console program
    """
    def __init__(self):
        """
        Constructor.
        """
        super(ErrorLevelListener, self).__init__(None, None, None, None)
        self.errorLevel = 0
    # end def __init__

    def addFailure(self, test, err):
        """
        @copydoc pyharness.core.TestListener.addFailure
        """
        if self.errorLevel == 0:
            self.errorLevel = 1
        # end if
    # end def addFailure

    def addError(self, test, err):
        """
        @copydoc pyharness.core.TestListener.addError
        """
        if self.errorLevel <= 1:
            self.errorLevel = 2
        # end if
    # end def addError
# end class ErrorLevelListener


class Main(BaseProgram):
    """
    A command-line program that runs a set of tests.

    This is primarily for making test modules conveniently executable.
    """

    # This overrides the default arguments, for the CLI only
    DEFAULT_ARGUMENTS_OVERRIDE = {KeywordArguments.KEY_OUTPUTS: KeywordArguments.OUTPUTS_DEFAULT + ",console",
                                  }

    def __init__(self, argv=None, stdout=None, stderr=None, *args, **kwargs):
        """
        Constructor (and runner)

        @option argv   [in] (tuple) program arguments (including program name)
        @option stdout [in] (stream) The standard output
        @option stderr [in] (stream) The standard error output
        @option args   [in] (tuple) Arguments
        @option kwargs [in] (dict)  Keyword arguments
        """
        BaseProgram.__init__(self, argv, *args, **kwargs)

        self.set_command_line_kw_args(self.parse_args(argv[1:]))

        kw_args = self.get_current_kw_args()
        test_manager = LocalTestManager(kw_args)

        self._updateFilteringProfile(kw_args)
        self._updateSortingProfile(kw_args)

        listeners = self.initializeListeners(test_manager, kw_args)
        error_level_test_listener = ErrorLevelListener()
        listeners.append(error_level_test_listener)
        suites = kw_args[KeywordArguments.KEY_SUITE].split(' ')
        test_manager.run(suites, listeners, kw_args)

        self.result = error_level_test_listener.errorLevel
    # end def __init__

    @staticmethod
    def _updateFilteringProfile(kw_args):
        """
        Updates the KEY_FILTERING_PROFILE in the keyword arguments

        @param  kw_args [in] (dict) The keyword arguments to update
        """
        profile_directory = join(kw_args[KeywordArguments.KEY_ROOT], 'LOCAL', )

        result = DEFAULT_FILTERING_PROFILES[0]
        if access(profile_directory, F_OK):
            # List all *.filter files in the profile directory
            for filename in [filename for filename in listdir(profile_directory)
                             if filename.endswith('.filter')]:

                filepath = join(profile_directory, filename)
                doc = parse(filepath)
                profile_elements = doc.documentElement.getElementsByTagName(FilteringProfile.XML_TAG)
                for profile_element in profile_elements:
                    profile = FilteringProfile.fromElement(profile_element)
                    if profile.getId() == kw_args[KeywordArguments.KEY_FILTERING_PROFILE]:
                        result = profile
                        break
                    # end if
                # end for
            # end for
        # end if

        if result.getId() != kw_args[KeywordArguments.KEY_FILTERING_PROFILE]:
            raise ValueError(f"Cannot find input profile: {kw_args[KeywordArguments.KEY_FILTERING_PROFILE]}")
        # end if

        kw_args[KeywordArguments.KEY_CUSTOM_FILTER] = result.resolveFilters()
    # end def _updateFilteringProfile

    @staticmethod
    def _updateSortingProfile(kw_args):
        """
        Updates the KEY_SORTING_PROFILE in the keyword arguments

        @param kw_args [in] (dict) The keyword arguments to update
        """
        profile_directory = join(kw_args[KeywordArguments.KEY_ROOT], 'LOCAL', )

        result = DEFAULT_SORTING_PROFILE
        if access(profile_directory, F_OK):
            # List all *.filter files in the profile directory
            for filename in [filename for filename in listdir(profile_directory)
                             if filename.endswith('.sorter')]:

                filepath = join(profile_directory, filename)
                doc = parse(filepath)
                profile_elements = doc.documentElement.getElementsByTagName(SortingProfile.XML_TAG)
                for profile_element in profile_elements:
                    profile = SortingProfile.fromElement(profile_element)
                    if profile.getId() == kw_args[KeywordArguments.KEY_SORTING_PROFILE]:
                        result = profile
                    # end if
                # end for
            # end for
        # end if

        if result.getId() != kw_args[KeywordArguments.KEY_SORTING_PROFILE]:
            raise ValueError(f"Cannot find sorting profile: {kw_args[KeywordArguments.KEY_SORTING_PROFILE]}")
        # end if

        kw_args[KeywordArguments.KEY_CUSTOM_SORTER] = result.resolveSorters()
    # end def _updateSortingProfile
# end class Main


if __name__ == '__main__':
    Main(sys.argv, sys.stdout, sys.stderr)
# end if

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
