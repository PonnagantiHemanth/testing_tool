#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.tools.test.migrate

@brief  Testing of migrate module

@author christophe Roquebert

@date   2018/06/11
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from io import StringIO
from os import makedirs
from os.path import abspath
from os.path import join
from shutil import rmtree
from unittest import TestCase

from pyharness.tools.migrate import Main
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class MigrateTestCase(TestCase):
    '''
    Testing of migrate main class
    '''
    def setUp(self):
        '''
        Initialize test.

        This creates a temporary project for testing.
        '''
        TestCase.setUp(self)

        # Create a convenient hierarchy
        self._tempDirPath = abspath(mkdtemp("", "test_%s" % self.id()))

        # If python version is less than 2.6, strip the '\\?\' prefix
        from sys                        import version_info
        if (    (version_info < (2, 6, 0, 0))
            and (self._tempDirPath.startswith('\\\\?\\'))):
            self._tempDirPath = self._tempDirPath[4:]
        # end if

    # end def setUp

    def tearDown( self ):
        '''
        Clean up test.
        '''
        # cleanup
        rmtree(self._tempDirPath, True)

        TestCase.tearDown(self)
    # end def tearDown

    def testMain(self):
        '''
        Test of constructor
        '''
        cfgDir = join(self._tempDirPath, "SETTINGS")
        makedirs(cfgDir)

        iniFileName1 = join(cfgDir, "iniFile1.ini")
        with open(iniFileName1, "w") as iniFile:
            iniFile.write('\n'.join(('Feature    = 0x12AB89',
                                     )))
        # end with

        iniFileName2 = join(cfgDir, "iniFile2.ini")
        with open(iniFileName2, "w") as iniFile:
            iniFile.write('\n'.join(('Feature    = 1289',
                                     )))
        # end with

        argv = ['unused',
                '--inputdir=%s' % self._tempDirPath,
                '--verbose',
                '--force',
                '--action=ini']
        migrator = Main(argv, StringIO(), StringIO())
        self.assertIsNotNone(migrator,
                             'Wrong migrate creation')

        with open(iniFileName1) as iniFile:
            obtained = iniFile.readlines()
        # end with

        expected1 = ['# migration done\n',
                     'Feature = [12AB89]\n']

        self.assertEqual(expected1,
                         obtained,
                         'Wrong migration result')

        with open(iniFileName2) as iniFile:
            obtained = iniFile.readlines()
        # end with

        expected2 = ['Feature    = 1289']

        self.assertEqual(expected2,
                         obtained,
                         'Wrong migration result')

        migrator = Main(argv, StringIO(), StringIO())

        with open(iniFileName1) as iniFile:
            obtained = iniFile.readlines()
        # end with

        self.assertEqual(expected1,
                         obtained,
                         'Wrong migration result')

    # end def testMain
#
#    def testHelp(self):
#        '''
#        Tests the help option
#        '''
#        stdout = StringIO()
#        argv = ('unused',
#                '--help',
#                )
#        try:
#            Main(argv, stdout, StringIO())
#            raise ValueError('Should raise a SystemExit exception')
#        except SystemExit:
#            pass
#        else:
#            raise
#        # end try
#
#        expected = Main.USAGE
#        obtained = '\n'.join(stdout.readlines())
#
#        self.assertEqual(expected,
#                         obtained,
#                         'Wrong help message')
#
#    # end def testHelp

# end class MigrateTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
