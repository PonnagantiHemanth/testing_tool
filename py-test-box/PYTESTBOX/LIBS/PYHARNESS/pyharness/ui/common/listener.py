#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.ui.common.listener

@brief  Common listeners for UIs

@author christophe Roquebert

@date   2018/12/18
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.core                      import TestListener
import wx

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class TestSelectionListener(TestListener):
    '''
    Posts an EVT_TESTSELECTIONCHANGED message whenever a new test starts

    This is only done when the option is enabled in the configuration
    '''

    def __init__(self, model):
        '''
        Constructor.

        @param  model [in] (DataModel) The data model to work on
        '''
        super(TestSelectionListener, self).__init__(None, None, None, None)

        self._model = model
    # end def __init__

    def startTest(self, test):
        '''
        @copydoc pyharness.core.TestListener.startTest
        '''
        def callback():
            '''
            Proxy for synchronizing the main thread model, (wxGTK workaround)
            '''
            if (self._model.getSynchronizeSelection()):
                testId = test.id()
                self._model.setSelectedTestIds((testId,))
            # end if
        # end def callback
        wx.CallAfter(callback)
    # end def startTest

    def stopTest(self, test):
        '''
        @copydoc pyharness.core.TestListener.stopTest
        '''
        def callback():
            '''
            Proxy for synchronizing the main thread model, (wxGTK workaround)
            '''
            if (self._model.getSynchronizeSelection()):
                testId = test.id()
                self._model.setSelectedTestIds((testId,), True)
            # end if
        # end def callback
        wx.CallAfter(callback)
    # end def stopTest
# end class TestSelectionListener

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
