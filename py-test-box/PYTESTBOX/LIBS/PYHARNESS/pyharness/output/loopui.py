#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.loopui

@brief  Loop-control specialized TestListener

@author christophe.roquebert

@date   2018/12/09
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.threadutils       import synchronized
from pyharness.arguments                 import KeywordArguments
from pyharness.core                      import TestListener
from pyharness.core                      import TestSuite
from threading                          import RLock

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class LoopTestListener(TestListener):
    '''
    A test listener class that controls the outer loop of the test runs.

    This updates the context depending on the loop conditions,
    contained in the kwArgs
    '''

    SYNCHRONIZATION_LOCK = RLock()

    ## This TestListener is one of the few mandatory listeners
    MANDATORY = True
    VISIBLE   = False

    def __init__(self, descriptions, verbosity, outputdir, args):
        '''
        Constructor.

        @copydoc pyharness.core.TestListener.__init__
        '''
        super(LoopTestListener, self).__init__(descriptions, verbosity, outputdir, args)

        self._context = None
    # end def __init__

    def startRun(self, context, resumed):                                                                               # pylint:disable=W0613
        '''
        @copydoc pyharness.core.TestListener.startRun
        '''
        if (not resumed):
            assert self._context is None, 'Context should be None'
            self._context = context
        # end if
    # end def startRun

    def stopRun(self, result, suspended):                                                                               # pylint:disable=W0613
        '''
        @copydoc pyharness.core.TestListener.stopRun
        '''
        if (not suspended):
            assert self._context is not None, 'Context should be None'
            self._context = None
        # end if
    # end def stopRun

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def addFailure(self, test, err):                                                                                    # pylint:disable=W0613
        '''
        @copydoc pyharness.core.TestListener.addFailure
        '''

        if (not isinstance(test, TestSuite)):
            if 'failure' in self.args[KeywordArguments.KEY_LOOP_STOP]:
                self._context.kill = True
            # end if
        # end if
    # end def addFailure

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def addError(self, test, err):                                                                                      # pylint:disable=W0613
        '''
        @copydoc pyharness.core.TestListener.addError
        '''

        if (not isinstance(test, TestSuite)):
            if 'error' in self.args[KeywordArguments.KEY_LOOP_STOP]:
                self._context.kill = True
            # end if
        # end if
    # end def addError

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def addSuccess(self, test, unused = None):
        '''
        @copydoc pyharness.core.TestListener.addSuccess
        '''
        if (not isinstance(test, TestSuite)):
            if 'success' in self.args[KeywordArguments.KEY_LOOP_STOP]:
                self._context.kill = True
            # end if
        # end if
    # end def addSuccess
# end class LoopTestListener

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
