#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
# pylint:disable=W8008
"""
@package pyharness.tools.archivebuilder

@brief  Creates an archive of the results of the specified configuration

@author christophe.roquebert

@date   2018/12/17
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import sys
from os import access
from os import F_OK
from os import listdir
from os import makedirs
from os.path import dirname
from os.path import expanduser
from os.path import isdir
from os.path import isfile
from os.path import join
from os.path import normpath
from os.path import sep
from pyharness.tools.base import Main
from pylibrary.tools.listener import Listenable
from time import localtime
from time import strftime
from zipfile import ZIP_DEFLATED
from zipfile import ZipFile


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ArchiveBuilder(Main, Listenable):  # pylint:disable=W0223
    """
    A program that:
    - Program_description
    """

    ACTION_UPDATE_PROGRESS = "progress"
    TOTAL_STEPS = 5

    VERSION = '0.5.0.0'

    def __init__(self, argv, stdout, stderr, listeners=None):  # pylint:disable=W0621
        """
        Constructor and main program entry point

        @param  argv      [in] (tuple)  The program arguments
        @param  stdout    [in] (stream) The standard output stream
        @param  stderr    [in] (stream) The standard error stream
        @option listeners [in] (dict)   The listeners for notification
        """
        Main.__init__(self, argv, stdout, stderr)
        Listenable.__init__(self)

        if listeners is None:
            listeners = {}
        # end if

        for action, listener in listeners.items():
            self.addListener(listener, action)
        # end for

        self._zipFile = None
        self._outputFile = None

        self.parse_args(argv)

        base_dir = self._context.getOutputDir()

        def dir_predicate(path_name):
            """
            A predicate for path acceptability.

            @param  path_name [in] (str) The path to test.

            @return Boolean, whether the path is accepted or not.
            """
            if path_name.endswith('.svn'):
                return False
            # end if

            if path_name.endswith('CVS'):
                return False
            # end if

            return True
        # end def dir_predicate

        progress = 0.0
        self.notifyListeners(self, self.ACTION_UPDATE_PROGRESS, progress / self.TOTAL_STEPS)

        if self._outputFile is None:
            author = normpath(expanduser('~')).rsplit(sep, 1)[-1]
            output_file = self._context.getOutputDir()

            now = localtime()
            output_file = normpath(join(output_file,
                                        f"Archive_{strftime('%Y%m%d', now)}_{strftime('%H%M%S', now)}_{author}.zip"))
            self._outputFile = output_file
        # end if

        dir_path = dirname(self._outputFile)
        if not access(dir_path, F_OK):
            makedirs(dir_path)
        # end if

        # Create an empty archive
        zip_file = ZipFile(self._outputFile, "w", ZIP_DEFLATED)
        zip_file.writestr('README.txt',
                          f"This archive contains the results of a validation for the original path:\n{base_dir}")
        zip_file.close()

        # Collect the journal
        self._provider.getLogger().logTrace("Archiving the Journal.jrl file.")
        collector = self._collectTargetFiles(base_dir,
                                             lambda p: False,
                                             lambda f: f.endswith('Journal.jrl') or f.endswith('Settings.ini'),
                                             )
        self.updateArchive(base_dir, collector, current_step=progress)
        progress += 1.0
        self.notifyListeners(self, self.ACTION_UPDATE_PROGRESS,
                             progress / self.TOTAL_STEPS,
                             'Journal archived successfully')

        # Collect the LOGs
        self._provider.getLogger().logTrace("Archiving the LOG log files")
        collector = self._collectTargetFiles(base_dir,
                                             lambda p: 'log' in p and dir_predicate(p),
                                             lambda f: f.endswith('.log'),
                                             )
        self.updateArchive(base_dir, collector, current_step=progress)
        progress += 1.0
        self.notifyListeners(self, self.ACTION_UPDATE_PROGRESS,
                             progress / self.TOTAL_STEPS,
                             'LOGs archived successfully')

        # Collect the XMLs
        self._provider.getLogger().logTrace("Archiving the XML log files")
        collector = self._collectTargetFiles(base_dir,
                                             lambda p: 'xml' in p and dir_predicate(p),
                                             lambda f: f.endswith('.xml'),
                                             )
        self.updateArchive(base_dir, collector, current_step=progress)
        progress += 1.0
        self.notifyListeners(self, self.ACTION_UPDATE_PROGRESS,
                             progress / self.TOTAL_STEPS,
                             'XMLs archived successfully')

        # Collect the coverage files
        self._provider.getLogger().logTrace("Archiving the Coverage files")
        collector = self._collectTargetFiles(base_dir,
                                             lambda p: 'coverage' in p and dir_predicate(p),
                                             lambda f: f.endswith('.xml') or f.endswith('.ccv') or f.endswith('.pfl'),
                                             )
        self.updateArchive(base_dir, collector, current_step=progress)
        progress += 1.0
        self.notifyListeners(self, self.ACTION_UPDATE_PROGRESS,
                             progress / self.TOTAL_STEPS,
                             'Coverage files archived successfully')

        # Collect the DYNAMIC
        self._provider.getLogger().logTrace("Archiving the DYNAMIC results")
        collector = self._collectTargetFiles(base_dir,
                                             lambda p: 'TESTCASES' in p and dir_predicate(p),
                                             lambda f: f.endswith('dynamic'),
                                             )
        self.updateArchive(base_dir, collector, current_step=progress)
        progress += 1.0
        self.notifyListeners(self, self.ACTION_UPDATE_PROGRESS,
                             progress / self.TOTAL_STEPS,
                             'TESTCASES archived successfully')

        self._provider.getLogger().logTrace('Done.')
    # end def __init__

    def get_parser(self):  # pylint:disable=W8012
        """
        @copydoc pyharness.tools.base.Main.get_parser
        """
        parser = Main.get_parser(self)

        parser.add_argument('-o', '--output', dest='output', default=None, metavar='OUTPUT',
                            help='write to OUTPUT file')

        return parser
    # end def get_parser

    def parseOptions(self, args, kw_args):  # pylint:disable=W0613,W8012
        """
        @copydoc pyharness.tools.base.Main.parseOptions
        """
        kw_args = Main.parseOptions(self, args, kw_args)

        if args.output is not None:
            self._outputFile = args.output
        # end if

        return kw_args
    # end def parseOptions

    def _collectTargetFiles(self, base_dir, dir_predicate, file_predicate, collector=None):
        """
        Collects file to archive from the base directory

        @param  base_dir       [in] (str)      The directory to collect from
        @param  dir_predicate  [in] (callable) A predicate for recursively collecting from directories.
        @param  file_predicate [in] (callable) A predicates defining the acceptability of the files.
        @option collector     [in] (list)     A list that collects the files

        @return The collector.
        """
        if collector is None:
            collector = []
        # end if

        for filename in listdir(base_dir):
            fullpath = join(base_dir, filename)
            if ((isdir(fullpath))
                    and (dir_predicate(fullpath))):
                self._collectTargetFiles(fullpath,
                                         dir_predicate,
                                         file_predicate,
                                         collector)
            elif (isfile(fullpath)
                  and (file_predicate(fullpath))):
                collector.append(fullpath)
            # end if
        # end for

        return collector
    # end def _collectTargetFiles

    def updateArchive(self, base_path, target_files, output_file=None, current_step=None):
        """
        Creates an archive of the default directory

        The default output file is named: Archive_DATE_TIME_author.zip

        @param  base_path    [in] (str)   The path to remove from the files
        @param  target_files [in] (tuple) The target files to archive
        @param output_file  [in] (str)   The file to archive to.
        @param current_step [in] (int)   The current global step, for listeners notification.
        """
        if output_file is None:
            output_file = self._outputFile
        # end if

        zip_file = ZipFile(output_file, "a", ZIP_DEFLATED)

        # Specific process for older version of python than 2.6
        from sys import version

        if version < str('2.6.0 0'):
            python_bug_workaround = str
        else:
            python_bug_workaround = lambda x: x
        # end if

        index = 0
        for target_file in target_files:
            if target_file.startswith(base_path):
                arc_name = target_file[len(base_path):]
            else:
                arc_name = target_file
            # end if

            if self._loglevel > 5:
                self._stdout.write(f'Archiving: {arc_name}\n')
            # end if

            if current_step is not None:
                self.notifyListeners(self, self.ACTION_UPDATE_PROGRESS,
                                     (current_step + (float(index) / len(target_files))) / self.TOTAL_STEPS)
            # end if

            zip_file.write(target_file, python_bug_workaround(arc_name))
            index += 1
        # end for
        zip_file.close()
    # end def updateArchive
# end class ArchiveBuilder


if __name__ == '__main__':
    ArchiveBuilder(sys.argv, sys.stdout, sys.stderr)
# end if

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
