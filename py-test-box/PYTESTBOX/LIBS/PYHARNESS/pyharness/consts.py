#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.consts

@brief PyHarness constants

This module provides program constants, such as its name and version.

@author christophe.roquebert

@date   2018/09/11
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------

# Import the version from PyHarness's PKG-INFO
from pylibrary.tools.importutils       import getResourceStream
from os.path                            import abspath
from os.path                            import join

def getEggVersion():
    '''
    Extracts the egg version from the PKG-INFO

    @return (str) The egg version.
    '''
    eggVersion = 'Unknown'

    pkgInfoFilePath = abspath(join(__file__, '..', '..', 'EGG-INFO', 'PKG-INFO'))
    pkgInfoFile     = getResourceStream(pkgInfoFilePath)
    lines = [x.strip() for x in pkgInfoFile.readlines()]
    for line in lines:
        if (line.startswith('Version:')):
            eggVersion = line[len('Version:'):].strip()
        # end if
    # end for

    return eggVersion
# end def getEggVersion

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

PROGRAM_NAME    = 'pyHarness'
PROGRAM_VERSION = getEggVersion()
PROGRAM_EDITION = ''
COPYRIGHT       = 'Python Test Harness 2018'

## The name of the SETTINGS directory for the test suite.
DEFAULT_INPUT_DIRECTORY  = 'SETTINGS'

## The name of the OUTPUT directory for the validation.
## This directory was formerly VERSION, and is now LOCAL
DEFAULT_OUTPUT_DIRECTORY = 'LOCAL'

## The maximum number of threads allowed
MAXIMUM_THREADS_PER_RUN = 4

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
