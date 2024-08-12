#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.test.eclipseui

@brief  Tests of the EclipseTestListener

@author christophe Roquebert

@date   2018/06/07
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from io                           import StringIO
from pyharness.output.eclipseui          import EclipseTestListener
from pyharness.output.eclipseui          import _WritelnDecorator
from pyharness.test.core_test             import TestListenerTestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class EclipseTestListenerTestCase(TestListenerTestCase):
    '''
    Tests of the Eclipse TestListener class
    '''
    class TestEclipseTestListener(EclipseTestListener):
        '''
        Class overriding stderr for the tests
        '''
        def __init__(self, descriptions, verbosity, outputdir, args = False):                                           # pylint:disable=W8001
            '''
            copydoc pyharness.output.eclipseui.EclipseTestListener.__init__
            '''
            super(EclipseTestListenerTestCase.TestEclipseTestListener, self).__init__(descriptions, verbosity, outputdir, args)
            self.stream             = _WritelnDecorator(StringIO())
        # end def __init__
    # end class TestEclipseTestListener

    @staticmethod
    def isAbstract ():
        '''
        @copydoc pyharness.test.coretest.TestListenerTestCase.isAbstract
        '''
        return False
    # end def isAbstract

    @staticmethod
    def _getTestListenerClass():
        '''
        @copydoc pyharness.test.coretest.TestListenerTestCase._getTestListenerClass
        '''
        return EclipseTestListenerTestCase.TestEclipseTestListener
    # end def _getTestListenerClass
# end class EclipseTestListenerTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
