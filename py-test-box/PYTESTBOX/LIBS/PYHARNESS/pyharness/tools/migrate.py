#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
# pylint:disable=W8008
"""
@package pyharness.tools.migrate

@brief  Various migration tools

@author christophe.roquebert

@date   2018/10/09
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from argparse import ArgumentParser
from os import access
from os import chmod
from os import F_OK
from os import stat
from os import W_OK
from os import walk
from os.path import join
from stat import S_IWRITE
from stat import ST_MODE
import re
import sys


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class Main(object):
    """
    A program that migrates various elements from a validation project.
    """
    VERSION = '0.1.0.0'

    ACTION_TASKS = {"ini": "_action_migrate_ini_files"}

    def __init__(self, argv, stdout, stderr):
        """
        Constructor and main program entry point

        @param  argv   [in] (tuple)  The program arguments
        @param  stdout [in] (stream) The standard output stream
        @param  stderr [in] (stream) The standard error stream
        """
        self._stdout = stdout
        self._stderr = stderr
        self.verbose = False
        self.actions = []
        self.force = False
        self.prog_name = argv[0]
        self.input_dir = ''
        self._parser = None
        argv = argv[1:]

        self.parse_args(argv)

        for action in self.actions:
            action()
        # end for

        if len(self.actions) == 0:
            self.usage_exit("Nothing to do")
        # end if
    # end def __init__

    def get_parser(self):
        """
        Get the ArgumentParser instance

        @return (ArgumentParser) ArgumentParser instance
        """
        if self._parser is None:
            parser = ArgumentParser()
            parser.add_argument('--version', action='version', version=self.VERSION)
            action_help = f'Perform the specified action, where action is one of: ' \
                          f'{",".join(tuple(self.ACTION_TASKS.keys()))}'

            parser.add_argument('-v', '--verbose', dest='verbose', help='verbose output', default=False,
                                action='store_true')
            parser.add_argument('-f', '--force', dest='force', help='overwrite files', default=False,
                                action='store_true')
            parser.add_argument('-i', '--inputdir', dest='inputdir', help='input folder', default=None,
                                metavar='INPUT_DIR')
            parser.add_argument('-a', '--action', dest='action', help=action_help, default=None, metavar='ACTION')

            parser.epilog = """
Examples:
  %(prog)s                            - run the program with default arguments
  %(prog)s --action=ini               - run the program, migrating .ini files to the new format
"""
            self._parser = parser
        # end if

        return self._parser
    # end def get_parser

    parser = property(get_parser)

    def parse_args(self, argv):
        """
        Parses the program arguments

        @param  argv [in] (tuple) The arguments passed in the command line.
        """
        parser = self.get_parser()
        args = parser.parse_args(argv)

        # Iterate over the args.
        self.verbose = args.verbose
        self.force = args.force

        if args.inputdir:
            self.input_dir = args.inputdir
        # end if

        if args.action:
            action = args.action
            if action in self.ACTION_TASKS:
                self.actions.append(getattr(self, self.ACTION_TASKS[action]))
            else:
                msg = f"No action with name {action}"
                self.usage_exit(msg)
            # end if
        # end if
    # end def parse_args

    def _action_migrate_ini_files(self):  # pylint:disable=R0912
        """
        Migrates the .ini files located in the SETTINGS directory
        """
        self._stdout.write("Migrating ini files...")
        # Check accessibility of the SETTINGS directory
        path = join(self.input_dir, 'SETTINGS')
        if not access(path, F_OK):
            self.usage_exit("Cannot find SETTINGS directory")
        # end if

        marker = "# migration done"
        hexlist_regex = re.compile("^\\s*([a-zA-Z0-9_]+)\\s*=\\s*0x([0-9A-Fa-f]+)\\s*$")

        # Locate all relevant ini files from the SETTINGS directory
        dir_contents = walk(path)
        for dir_path, unused, filenames in dir_contents:
            # Exclude the .svn directory
            if '.svn' in dir_path:
                continue
            # end if
            for filename in filenames:
                if not filename.endswith('.ini'):
                    continue
                # end if
                filepath = join(dir_path, filename)
                if self.verbose:
                    self._stdout.write(f"Processing {filepath}")
                # end if

                # Read the lines from the filename
                with open(filepath) as iniFile:
                    lines = iniFile.readlines()
                # end with

                marker_present = False
                dirty = False
                new_lines = [marker + '\n']
                for line in lines:
                    # If the marker is present, do not process the line
                    if marker in line:
                        marker_present = True
                        new_lines = lines
                        break
                    # end if

                    re_match = hexlist_regex.match(line)
                    if re_match:
                        new_lines.append(f"{re_match.group(1)} = [{re_match.group(2)}]\n")
                        dirty = True
                    else:
                        new_lines.append(line)
                    # end if
                # end for

                if marker_present:
                    if self.verbose:
                        self._stdout.write("File already processed")
                    # end if
                    continue
                # end if

                if not dirty:
                    if self.verbose:
                        self._stdout.write("File already clean")
                    # end if
                    continue
                # end if

                if not access(filepath, W_OK) and not self.force:
                    self.usage_exit(f"Unable to write file: {filepath}\nUse --force to overwrite")
                # end if

                permissions = stat(filepath)[ST_MODE]
                if not (permissions & S_IWRITE) and self.force:
                    chmod(filepath, permissions | S_IWRITE)
                # end if

                with open(filepath, "w+") as iniFile:
                    iniFile.writelines(new_lines)
                # end with

                if self.verbose:
                    self._stdout.write("File processed")
                # end if
            # end for
        # end for

        self._stdout.write("Migrating ini files done.")
    # end def _action_migrate_ini_files

    def usage_exit(self, msg=None):
        """
        Prints usage and exit.

        @option msg [in] (str) An additional message to display before the usage string.
        """
        msg = '' if (msg is None) else msg + '\n'
        msg += self.parser.format_help()
        self.parser.exit(2, msg)
    # end def usage_exit
# end class Main


if __name__ == '__main__':
    Main(sys.argv, sys.stdout, sys.stderr)
# end if

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
