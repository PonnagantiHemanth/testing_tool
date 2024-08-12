#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.test.importutilstestcase

@brief Tests of the importutils tools

@author christophe.roquebert

@date   2018/06/05
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import sys
from os import makedirs
from os.path import join
from shutil import rmtree
from unittest import TestCase

from pylibrary.tools.importutils import fqnFromLocation
from pylibrary.tools.importutils import importFqn
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ImportUtilsTestCase(TestCase):
    '''
    Tests of various ImportUtils utilities
    '''

    def setUp(self):
        '''
        Test setup
        '''
        TestCase.setUp(self)
        self.__tempDir = mkdtemp('importutils')

        subPackages = ('package1', 'package2', 'package3')
        path = self.__tempDir
        for packageName in subPackages:
            path = join(path, packageName)
            makedirs(path)

            with open(join(path, '__init__.py'), 'w+') as initPy:
                initPy.write('\n')
            # end with
        # end for

        # Create the final .py file
        with open(join(path, 'module.py'), 'w+') as pyFile:
            pyFile.write('\n'.join(('class TestClass(object):',
                                    '  def method(self):',
                                    '    pass',
                                    '',
                                    )))
        # end with

        sys.path.insert(0, self.__tempDir)
    # end def setUp

    def tearDown(self):
        '''
        Test cleanup
        '''
        TestCase.tearDown(self)

        sys.path.remove(self.__tempDir)
        rmtree(self.__tempDir, True)
    # end def tearDown

    def testImportFqn(self):
        '''
        Test the importFqn API
        '''

        expected = 'TestClass'
        obtained = importFqn('package1.package2.package3.module.TestClass')
        self.assertEqual(expected,
                         obtained.__name__,
                         "Invalid importFqn")
    # end def testImportFqn

    def testFqnFromLocation(self):
        '''
        Tests the fqnFromLocation class
        '''

        # Compute a location
        locationFile = join(self.__tempDir, 'package1', 'package2', 'package3', 'module.py')
        with open(locationFile) as testFile:
            locationLine = 1
            for line in testFile.readlines():
                if (line.lstrip().startswith('def method')):
                    break
                # end if
                locationLine += 1
            else:
                self.fail('Could not find expected line')
            # end for
        # end with

        expected = 'package1.package2.package3.module.TestClass.method'
        obtained = fqnFromLocation(locationFile, locationLine)
        self.assertEqual(expected,
                         obtained,
                         "Invalid FQN")
    # end def testFqnFromLocation
# end class ImportUtilsTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
