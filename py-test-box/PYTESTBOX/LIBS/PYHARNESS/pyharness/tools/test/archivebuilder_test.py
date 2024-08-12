#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyharness.tools.test.archivebuilder_test
:brief: Testing of archivebuilder module
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/06/12
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import sys
from io import StringIO
from os import makedirs
from os import mkdir
from os import walk
from os.path import abspath
from os.path import join
from shutil import rmtree
from unittest import TestCase

from pyharness.tools.archivebuilder import ArchiveBuilder
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ArchiveBuilderTestCase(TestCase):
    """
    Testing of ArchiveBuilder class
    """
    RefClass = ArchiveBuilder

    def setUp(self):
        """
        Initialize test.

        This creates a temporary project for testing.
        """
        super(ArchiveBuilderTestCase, self).setUp()

        # Create a convenient hierarchy
        self._tempDirPath = abspath(mkdtemp("", "test_%s" % self.id()))
        self.outputdir = self._tempDirPath

        sys.path.insert(0, self._tempDirPath)

    # end def setUp

    def tearDown(self):
        """
        Clean up test.
        """
        sys.path.remove(self._tempDirPath)

        # Cleanup
        rmtree(self._tempDirPath, True)

        super(ArchiveBuilderTestCase, self).tearDown()
    # end def tearDown

    @classmethod
    def _createInstance(cls, argv=None, stdout=None, stderr=None, listeners=None):
        """
        Create an instance of referenced class

        @option argv      [in] (tuple)  The program arguments
        @option stdout    [in] (stream) The standard output stream
        @option stderr    [in] (stream) The standard error stream
        @option listeners [in] (dict)   The listeners for notification

        @return (object) Instance of referenced class
        """
        if argv is None:
            argv = ['unused',
                    ]
        # end if

        if stdout is None:
            stdout = StringIO()
        # end if

        if stderr is None:
            stderr = StringIO()
        # end if

        return cls.RefClass(argv, stdout, stderr, listeners)
    # end def _createInstance

    def _createConfigFiles(self):
        """
        Create all config files
        """
        src_path = join(self._tempDirPath, "TESTSUITES")
        mkdir(src_path)

        # Create a features.py
        file_name = join(src_path, "features.py")
        with open(file_name, "w") as fileHdlr:
            fileHdlr.write('\n'.join(('from pyharness.systems import AbstractSubSystem',
                                      'class RootSubSystem(AbstractSubSystem):',
                                      '    def __init__(self):',
                                      '        AbstractSubSystem.__init__(self, \"ROOT\")\n',
                                      '        \n'
                                      '        self.RUNTIME = AbstractSubSystem(\"RUNTIME\")\n',
                                      '        self.RUNTIME.F_Enabled = True\n'
                                      '        self.RUNTIME.F_InputDirPattern    = "../%(MODE)s/%(PRODUCT)s/%(VARIANT)s"',
                                      '        self.RUNTIME.F_OutputDirPattern   = "LOCAL/%(PRODUCT)s/%(VARIANT)s"',
                                      '        self.RUNTIME.F_DeviceManager = "pyusb.libusbdriver.DeviceManagerMock"\n',
                                      '        self.RUNTIME.F_UsbContextClass = "pytransport.usb.logiusbcontext.logiusbcontext.LogiusbUsbContext"\n',
                                      '        self.RUNTIME.DEBUGGERS = self.DebuggersSubSystem()\n',
                                      '    # end def __init__\n',
                                      '\n',
                                      '    class DebuggersSubSystem(AbstractSubSystem):',
                                      '        def __init__(self):',
                                      '            AbstractSubSystem.__init__(self, "DEBUGGERS")',
                                      '            self.F_Enabled = True',
                                      '            self.F_Targets = ()',
                                      '            self.F_Types = ()',
                                      '        # end def __init__',
                                      '    # end class DebuggersSubSystem',
                                      '# end class RootSubSystem',
                                      '',
                                      )))
        # end with

        # Create a CONFIG directory
        dirpath = join(self._tempDirPath, "SETTINGS")
        makedirs(dirpath)

        dirpath = join(dirpath, "PRODUCT")
        makedirs(dirpath)
        file_name = join(dirpath, "main.settings.ini")
        with open(file_name, "w") as fileHdlr:
            fileHdlr.write('\n'.join(('',
                                      )))
        # end with

        dirpath = join(dirpath, "BRANCH")
        makedirs(dirpath)
        file_name = join(dirpath, "BRANCH.settings.ini")
        with open(file_name, "w") as fileHdlr:
            fileHdlr.write('\n'.join(('',
                                      )))
        # end with

        # Create a LOCAL directory
        dirpath = join(self._tempDirPath, "LOCAL")
        makedirs(dirpath)

        file_name = join(dirpath, "Settings.ini")
        with open(file_name, "w") as fileHdlr:
            fileHdlr.write('\n'.join(('[CONTEXT]',
                                      'value = "local"',
                                      '[PRODUCT]',
                                      'value = "PRODUCT"',
                                      '[VARIANT]',
                                      'value = "BRANCH"',
                                      )))
        # end with

    # end def _createConfigFiles

    def _createResultFiles(self):
        """
        Create all files generated by a run
        """
        dirpath = join(self._tempDirPath, "LOCAL", "PRODUCT")
        makedirs(dirpath)
        dirpath = join(dirpath, "BRANCH")
        makedirs(dirpath)
        refpath = dirpath
        self.outputdir = refpath

        file_name = join(refpath, "Journal.jrl")
        with open(file_name, "w") as fileHdlr:
            fileHdlr.write('\n'.join(('# run started on 2012-05-24 17:12:31',
                                      '# -----------------------------------------------------------------------------',
                                      'example.testcases.log                                                           2012-05-24 17:12:34 2012-05-24 17:12:34 Ok',
                                      )))
        # end with

        dirpath = join(refpath, "log")
        makedirs(dirpath)

        # Creation of excluded repositories
        excluded_dir = join(dirpath, ".svn")
        makedirs(excluded_dir)
        excluded_dir = join(dirpath, "CVS")
        makedirs(excluded_dir)

        file_name = join(dirpath, "example.testcases.log")
        with open(file_name, "w") as fileHdlr:
            fileHdlr.write('\n'.join(('# -----------------------------------------------------------------------------',
                                      '# Test name:  example.testcases',
                                      '# -----------------------------------------------------------------------------',
                                      '',
                                      r'# TestCase: TESTCASE_EXAMPLE_01',
                                      r'# TestCase: TESTCASE_EXAMPLE_02',
                                      '',
                                      '# -----------------------------------------------------------------------------',
                                      r'# Title1 example.testcases --> Ok',
                                      '# -----------------------------------------------------------------------------',
                                      )))
        # end with

        dirpath = join(refpath, "TESTCASES")
        makedirs(dirpath)

        file_name = join(dirpath, "testcases.dynamic")
        with open(file_name, "w") as fileHdlr:
            fileHdlr.write('\n'.join(('|example.testcases',
                                      ' TESTCASE_EXAMPLE_01',
                                      ' TESTCASE_EXAMPLE_02',
                                      )))
        # end with
    # end def _createResultFiles

    def testConstructor(self):
        """
        Tests the constructor

        Main process of ArchiveBuilder
        """
        self._createConfigFiles()

        self._createResultFiles()

        argv = ['unused',
                '--root=%s' % self._tempDirPath,
                ]

        self._createInstance(argv)

        dir_contents = walk(self.outputdir)
        found = False
        for _, _, filenames in dir_contents:
            if found:
                break
            # end if
            for filename in filenames:
                if filename.endswith('.zip'):
                    found = True
                    break
                # end if
            else:
                raise IOError('Missing zip file')
            # end for
        else:
            raise IOError('Missing zip file')
        # end for
    # end def testConstructor

# end class ArchiveBuilderTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
