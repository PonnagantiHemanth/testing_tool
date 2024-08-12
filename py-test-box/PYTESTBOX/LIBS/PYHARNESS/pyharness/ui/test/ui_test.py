#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package    pyharness.ui.test.uitest

@brief  ui tests

@author christophe roquebert

@date   2018/08/18
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from sys                                import platform
from time                               import sleep
from unittest                           import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class AbstractWinTestCase(TestCase):
    '''
    Windows User Interface tests
    '''

    @staticmethod
    def closeApp(title):
        '''
        Close App window

        @param  title [in] (str) name
        '''
        from pywinauto                  import Application                                                              #@UnresolvedImport #pylint:disable=F0401
        Application.Connect(title = title)[title].Close()
    # end def closeApp

    @staticmethod
    def wait(seconds = 1):
        '''
        Wait for action

        @option seconds [in] (int) delay
        '''
        sleep(seconds)
    # end def wait

# end class AbstractWinTestCase

def getApplication(title):
    '''
    Get application window

    @param  title [in] (str) window title

    @return (Application)
    '''
    if (platform == 'win32'):
        try:
            from pywinauto              import Application                                                              #@UnresolvedImport #pylint:disable=F0401
            from pywinauto.findwindows  import WindowNotFoundError                                                      #@UnresolvedImport #pylint:disable=F0401

            try:
                return Application.Connect(title = title)

            except WindowNotFoundError:
                pass
            # end try
        except ImportError:
            pass
        # end try
    # end if

    return None
# end def getApplication

def getApplication_re(title_re):
    '''
    Get application window

    @param  title_re [in] (str) window title

    @return (Application)
    '''
    if (platform == 'win32'):
        try:
            from pywinauto              import Application                                                              #@UnresolvedImport #pylint:disable=F0401
            from pywinauto.findwindows  import WindowNotFoundError                                                      #@UnresolvedImport #pylint:disable=F0401

            try:
                return Application.Connect(title_re = title_re)

            except WindowNotFoundError:
                pass
            # end try
        except ImportError:
            pass
        # end try
    # end if

    return None
# end def getApplication_re

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
