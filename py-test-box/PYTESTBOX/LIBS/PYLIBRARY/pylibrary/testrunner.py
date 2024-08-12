#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.testrunner

@brief  PyLibrary main discovery test runner.

@author christophe.roquebert

@date   2018/11/14
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------


from os                                 import listdir
from os                                 import sep
from os.path                            import basename
from os.path                            import dirname
from os.path                            import exists
from os.path                            import join
from unittest                           import TestLoader
from unittest                           import TestSuite

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

# Re-implement unittest discovery

def lookupTestModules(rootDir, collector):
    '''
    Looks up all modules in **/test/*.py

    @param  rootDir   [in] (str)  Path to the root directory to scan.
    @param  collector [in] (list) List that collects module paths.
    '''
    if (basename(rootDir) == 'test'):                                           # @UndefinedVariable
        for fileName in listdir(rootDir):
            if fileName.endswith('.py') and not fileName.startswith('_'):
                collector.append(join(rootDir, fileName))                       # @UndefinedVariable
            # end if
        # end for
    else:
        for childDir in listdir(rootDir):
            if childDir not in ('.svn', 'CVS'):
                childPath = join(rootDir, childDir)                             # @UndefinedVariable
                if exists(join(childPath, '__init__.py')):                      # @UndefinedVariable
                    lookupTestModules(childPath, collector)
                # end if
            # end if
        # end for
    # end if
# end def lookupTestModules

_testModulePaths = []
_sitePath = dirname(dirname(__file__))                                          # @UndefinedVariable
lookupTestModules(_sitePath,
                  _testModulePaths)

_testModules = ['.'.join(testModulePath[len(_sitePath):-3].strip(sep).split(sep)) for testModulePath in _testModulePaths]
_testModules = sorted(set(_testModules))

_loader = TestLoader()
_tests = [_loader.loadTestsFromName(module) for module in _testModules]

def removeAbstract(tests):
    '''
    Remove AbstractXxxTestCase from test list

    @warning Recursive function

    @param  tests [in] (list) TestsSuite or TestCase

    @return (list) filtered tests
    '''
    res = []
    for test in tests:
        if test.__class__.__name__.startswith('TestSuite'):
            test._tests = removeAbstract(test._tests)                           # pylint:disable=W0212

        elif test.__class__.__name__.startswith('Abstract'):
            continue
        # end if

        res.append(test)
    # end fors
    return res
# end def removeAbstract

_tests = removeAbstract(_tests)

class PyLibraryTestRunner(TestSuite):
    '''
    A root PyLibrary test runner
    '''
    def __init__(self):
        '''
        Constructor
        '''
        super(PyLibraryTestRunner, self).__init__(_tests)
    # end def __init__
# end class PyLibraryTestRunner

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
