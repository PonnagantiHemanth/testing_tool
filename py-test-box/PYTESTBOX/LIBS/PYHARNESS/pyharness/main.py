#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.main

@brief   The main program entry point.

@author christophe Roquebert

@version 0.1.0.0

@date    2018/07/24
'''
# ------------------------------------------------------------------------------
# Update the python path with the current PySetup Python libraries
# ------------------------------------------------------------------------------
from os.path                            import abspath
from os.path                            import join
from os.path                            import normpath
import sys

# ------------------------------------------------------------------------------
# PySetup imports
# ------------------------------------------------------------------------------
# pylint:disable=E0611
if (__name__ == '__main__'):
    PySetupPath = abspath(sys.argv[0])
    PySetupPath = PySetupPath[:PySetupPath.index(normpath('/PYTESTBOX/')) + 4]
    PySetupPath = join(PySetupPath, 'LIBS', 'PYSETUP', 'PYTHON')
    if (PySetupPath not in sys.path):
        sys.path.insert(0, PySetupPath)
    # end if
# end if
import pysetup                                                                                                          # pylint:disable=W0611

from pysetup                            import TESTS_PATH                                                                # @UnresolvedImport
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os                                 import makedirs
from os.path                            import isdir
from os.path                            import isfile

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class Main(object):
    '''
    Main framework class.
    '''
    def __init__(self):
        '''
        Constructor, that runs the validation.
        '''
        self.result = 0

        addEggsToSysPath = True
        if ('--eggs' in sys.argv):
            sys.argv.remove('--eggs')
            addEggsToSysPath = True
        # end if

        if ('--no-eggs' in sys.argv):
            sys.argv.remove('--no-eggs')
            addEggsToSysPath = False
        # end if

        self.updatePath(addEggsToSysPath)
        self.run()
    # end def __init__

    @staticmethod
    def updatePath(addEggsToSysPath):
        '''
        Updates the system path.

        @param addEggsToSysPath [in] (bool) add eggs or not
        '''
        # Perform a magic trick on the path: This adds TESTSUITES to the PYTHONPATH
        sourcePath = join(TESTS_PATH, 'TESTSUITES')
        toolsSourcePath = join(TESTS_PATH, 'TOOLS')
        if (sourcePath not in sys.path):
            sys.path.insert(0, sourcePath)
            sys.path.insert(1, toolsSourcePath)
        # end if

        if addEggsToSysPath:
            pysetup.addEggDependenciesToSysPath(sourcePath)
        # end if

    # end def updatePath

    def run(self):
        '''
        Runs the validation.
        '''
        _module, _class = 'pyharness.ui.console.main', 'Main'

        argToUiModule = {'--cui': 'pyharness.ui.console.main',
                         }

        from pyharness.consts            import DEFAULT_OUTPUT_DIRECTORY                                                 # pylint:disable=F0401
        outputFileDir = join(TESTS_PATH, DEFAULT_OUTPUT_DIRECTORY)
        outputFileDir = str(outputFileDir)

        if sys.platform == 'win32' and not outputFileDir.startswith('\\\\?'):
            outputFileDir = '\\\\?\\' + outputFileDir
        # end if

        if (not isdir(outputFileDir)):
            makedirs(outputFileDir)
        # end if

        outputFilePath = None
        for arg in sys.argv[1:]:
            if arg in argToUiModule:
                _module = argToUiModule[arg]
                sys.argv.remove(arg)

                outputFilePath = join(outputFileDir, arg[2:] + '.pid')
            # end if
        # end for

        if (outputFilePath is not None):
            with open(outputFilePath, 'w+') as outputFile:
                from os                 import getpid
                outputFile.write('%s' % getpid())
            # end with
        # end if

        # Lookup the target program
        # importFqn cannot be imported at top, as pylibrary may not be available
        from pylibrary.tools.importutils import importFqn                                                              # pylint:disable=F0401
        attr = importFqn(_module + "." + _class)

        # Run the program
        result = attr(sys.argv)
        if (    (result is not None)
            and (hasattr(result, 'result'))):
            self.result = result.result
        # end if

        if (outputFilePath is not None):
            if (isfile(outputFilePath)):
                from os                 import remove
                remove(outputFilePath)
            # end if
        # end if

    # end def run
# end class Main

if (__name__ == '__main__'):
    sys.exit(Main().result)
# end if

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
