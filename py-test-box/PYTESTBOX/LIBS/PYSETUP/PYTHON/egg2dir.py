#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
# pylint:disable=C0103
"""
@package egg2dir

@brief   Unzip egg file

@author  christophe roquebert

@date    2010/07/20
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from argparse import ArgumentParser
from os import rename
from os.path import exists
from os.path import isdir
from os.path import normpath
from os.path import splitdrive
from os.path import splitext
from zipfile import ZipFile
import sys


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class EggFile(object):
    """
    Egg (zipped) class
    """

    # @name Verbose Level
    # @{
    _QUIET = 0
    _INFO = 1
    _VERBOSE = 2
    # @}

    # @name Properties
    # @{
    _NAME = 'egg2dir'
    _BRIEF = 'Unzip egg file (.pyc are not extracted)'
    _VERSION = '0.2.0.0'
    # @}

    def __init__(self):
        """
        Constructor
        """
        super(EggFile, self).__init__()
        self.verbose_level = self._INFO
    # end def __init__

    def unzip(self, filename):
        """
        Unzip egg file

        @param filename [in] (str) egg (zipped) file
        """
        e_zip = filename + '.zip'

        self._verbose(f'{filename}: Renamed to .zip')
        rename(filename, e_zip)

        egg = ZipFile(e_zip, 'r')

        for name in egg.namelist():

            # Skip filenames including '..' ...
            dest = normpath(name)

            # ... starting with 'drive' ...
            drive, _ = splitdrive(dest)
            if drive:
                continue
            # end if

            # ... starting with '/'
            root, ext = splitext(dest)
            if root.startswith('/'):
                continue
            # end if

            # Skip pyc --> files will be recompiled --> local path in traceback
            if ext == '.pyc':
                continue
            # end if

            self._verbose(f'{filename}: extracting {name}...')
            egg.extract(name, filename)
        # end for
    # end def unzip

    @staticmethod
    def _print(msg):
        """
        Print message to stdout

        @param  msg       [in] (str) text
        """
        # Hack for cygwin
        sys.stdout.write(msg + '\n')
        sys.stdout.flush()
    # end def _print

    def _info(self, msg):
        """
        Print info message

        @param  msg       [in] (str) text
        """
        if self.verbose_level >= self._INFO:
            self._print(msg)
        # end if
    # end def _info

    def _verbose(self, msg):
        """
        Print verbose message

        @param  msg       [in] (str) text
        """
        if self.verbose_level >= self._VERBOSE:
            self._print(msg)
        # end if
    # end def _verbose
# end class EggFile


class Main(EggFile):
    """
    Main interface
    """

    def __init__(self):
        """
        Constructor
        """
        super(Main, self).__init__()

        parser = ArgumentParser(description=self._BRIEF,
                                epilog=f'{self._NAME} v {self._VERSION}')
        parser.add_argument('--version', action='version', version=self._VERSION)

        parser.set_defaults(verbose=self._INFO)
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-q', '--quiet', action='store_const', const=self._QUIET, dest='verbose',
                           help='turn message off')

        group.add_argument('-v', '--verbose', action='store_const', const=self._VERBOSE, dest='verbose',
                           help='print verbose information message')

        # positional arguments
        parser.add_argument('files', nargs='+', metavar='FILES', help='pass one or more egg file(s)')
        args = parser.parse_args()
        self.verbose_level = args.verbose

        for arg in args.files:
            if not exists(arg):
                parser.error(f'{arg}: file not found')
            # end if
        # end for

        for arg in args.files:
            if isdir(arg):
                self._info(f'{arg}: skipping directory')
                continue
            # end if

            self.unzip(arg)
            self._info(f'{arg}: done.')
        # end for
    # end def __init__
# end class Main


if __name__ == '__main__':
    Main()
# end if

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
