#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.common

@brief Common definitions for various TestListeners

@author christophe.roquebert

@date   2018/03/29
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path            import join
from os.path            import abspath

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class FileTestListenerMixin(object):
    '''
    Provides various utilities for file-based TestListeners
    '''
    RELATIVE_PATH  = None
    FILE_FORMAT    = None

    def __init__(self, *args, **kwargs):
        '''
        Constructor stub

        @param args   [in] (tuple) arguments
        @param kwargs [in] (dict) keyword arguments
        '''
        pass
    # end def __init__

    def _getOutputFilePath(self, testId):
        '''
        Builds the path to the test log file

        @param  testId [in] (str) The id of the test to log.

        @return The file path to the test log.
        '''
        filename = self.FILE_FORMAT % testId
        result = join(self._resultDirPath(), filename)

        return result
    # end def _getOutputFilePath


    def _resultDirPath(self):
        '''
        Builds the path to the directory containing the log files

        @return The file path to the test log.
        '''
        result = abspath(join(self.outputdir, self.RELATIVE_PATH))

        return result
    # end def _resultDirPath
# end class FileTestListenerMixin

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
