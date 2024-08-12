#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.ui.common.frame.logspypanel

@brief  A Panel able that intercepts log information

@author christophe.roquebert

@date   2018/07/26
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.core                      import TestListener
from pyharness.core                      import _LEVEL_TITLE1
from pyharness.core                      import _LEVEL_TITLE2
from pyharness.core                      import _LEVEL_TITLE3
from pyharness.ui.aui.events.events      import EVT_TESTSELECTIONCHANGED
from pyharness.ui.aui.events.events      import TestSelectionChangedEvent
from pyharness.ui.aui.model.datamodel    import DataModel
from threading                          import RLock
import wx

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

# Some pylint messages will generate false positives, as
# wxPython does follow specific coding rules
# pylint: disable=C0103,W0221,W0201

_LEVEL_BRIEF = 1024

_LOGGED_LEVELS = {_LEVEL_TITLE1: "Title 1",
                  _LEVEL_TITLE2: "Title 2",
                  _LEVEL_TITLE3: "Title 3",
                  _LEVEL_BRIEF:  "Description",
                  }

class LogSpyTestListener(TestListener):                                                                                 # pylint:disable=R0904
    '''
    Intercepts the log output for various levels
    '''

    _singleton = None   ##< The one and only instance of the LogSpyTestListener class

    class _CacheEntry(object):
        '''
        A cache entry, containing the last logged messages for various levels of
        a test.

        This class is thread-safe
        '''
        def __init__(self, testId):
            '''
            Constructor.

            @param  testId [in] (str) The Id of the test this message is associated with.
            '''
            self._testId       = testId  ##< The id of the test this entry is associated with.
            self._messageCache = {}      ##< The last logged messages for each level.
            self._lock         = RLock() ##< Synchronization lock
        # end def __init__

        def setMessage(self, level, message):
            '''
            Sets the message for a given level.

            This method is thread-safe

            Usage:
            @code
            cacheEntry.setMessage(_LEVEL_COMMAND, "A0A40000023F00")
            @endcode

            @param  level   [in] (int) The level for which the message is logged.
            @param  message [in] (str) The logged message
            '''
            with self._lock:
                keys = list(self._messageCache.keys())
                for key in keys:
                    if (key < level):
                        del self._messageCache[key]
                    # end if
                # end for
                self._messageCache[level] = message
            # end with

        # end def setMessage

        def getMessage(self, level):
            '''
            Obtains the message associated with the given level.

            This method is thread-safe

            Usage:
            @code
            cacheEntry.getMessage(_LEVEL_COMMAND)
            @endcode

            @param  level   [in] (int) The level for which the message to be obtained.

            @return (str) The logged message, or None if there is no log for this level.
            '''
            with self._lock:
                result = self._messageCache.get(level, None)
            # end try

            return result
        # end def getMessage
    # end class _CacheEntry

    def __init__(self, descriptions, verbosity, outputdir, args):
        '''
        @copydoc pyharness.core.TestListener.__init__
        '''
        TestListener.__init__(self, descriptions, verbosity, outputdir, args)

        self._logCache = {}    ##< A dict<testId, dict<level, _CacheEntry>>
        self._lock = RLock()   ##< The synchronization lock
    # end def __init__

    @staticmethod
    def create(*args, **kwargs):
        '''
        Factory method that re-uses the only instance of the LogSpyTestListener

        The arguments of this method are the same as those of the constructor:
        pyharness.core.TestListener.__init__

        @param  args   [in] (tuple) The arguments of the constructor
        @param  kwargs [in] (dict)  The keyword arguments of the constructor.

        @return The instance of the created object.
        '''
        if (LogSpyTestListener._singleton is None):
            LogSpyTestListener._singleton = LogSpyTestListener(*args, **kwargs)
        # end if

        return LogSpyTestListener._singleton
    # end def create

    def _clearCacheEntry(self, testId=None):
        '''
        Clears the cache entry for the given test.

        If testId is not specified, the whole cache is cleared.

        @param  testId [in] (str) The id of the entry to clear.
                           Clears the whole cache if None.
        '''
        with self._lock:
            if (testId is None):
                self._logCache.clear()
            else:
                self._logCache.pop(testId, None)
            # end if
        # end with

    # end def _clearCacheEntry

    def _getCacheEntry(self, testId):
        '''
        Obtain the cache entry for the given test.
        If the cache entry does not exist, it is created on-the-fly

        This method is thread-safe.

        @param  testId [in] (str) The test id used as a key

        @return The cache entry for the specified test.
        '''
        with self._lock:
            if (testId not in self._logCache):
                self._logCache[testId] = self._CacheEntry(testId)
            # end if
        # end try

        result = self._logCache[testId]

        return result
    # end def _getCacheEntry


    def resetTest(self, test, context):                                                                                 # pylint:disable=W0613
        '''
        @copydoc pyharness.core.TestListener.resetTest
        '''
        testId = test.id()
        self._clearCacheEntry(testId)
    # end def resetTest

    def startTest(self, test):
        '''
        @copydoc pyharness.core.TestListener.startTest
        '''
        testId = test.id()
        self._clearCacheEntry(testId)

        self.log(test, _LEVEL_BRIEF, test.shortDescription())
    # end def startTest

    def stopTest(self, test):
        '''
        @copydoc pyharness.core.TestListener.stopTest
        '''
        testId = test.id()
        self._clearCacheEntry(testId)
    # end def stopTest

    def log(self, test, level, msg, *args, **kwargs):                                                                   # pylint:disable=W0613
        '''
        @copydoc pyharness.core.TestListener.log
        '''
        # This will only intercept the logs for a subset of the levels.
        if (level in _LOGGED_LEVELS):
            message = (msg is None) and 'no log' or (msg % args)

            testId = test.id()
            cacheEntry = self._getCacheEntry(testId)
            cacheEntry.setMessage(level, message)
        # end if
    # end def log

    def getCachedMessage(self, testId, level):
        '''
        Obtain the cached message for the given testId, at the given level.

        @param  testId [in] (str) The id of the test for which to obtain the level.
        @param  level  [in] (str) The level at which to obtain the message.

        @return The last logged message for this test at this level.
                None, of no message was logged.
        '''

        result = None

        cacheEntry = self._getCacheEntry(testId)
        if cacheEntry is not None:
            result = cacheEntry.getMessage(level)
        # end if

        return result
    # end def getCachedMessage


# end class LogSpyTestListener


class LogSpyPanel(wx.Panel):                                                                                            # pylint:disable=R0904
    '''
    A panel that contains TextCtrls that display the logs in 'real-time'.
    The display is actually slightly asynchronous, as the quantity of logs
    may be huge. Therefore, the spy panel regularly polls (n times/seconds)
    a repository containing the last log.

    The SpyPanel is organized in a simple block, containing N lines of TextCtrls.
    '''

    def __init__(self, parent,
                       title,
                       testListener):
        '''
        Constructor

        @param  parent       [in] (Wnd) The parent window
        @param  title        [in] (str) The panel title.
        @param  testListener [in] (TestListener) The TestListener instance that provides access
                                 to the last entered log for the currently
                                 selected test
        '''
        wx.Panel.__init__(self, parent, size=(320, 200), name=title)

        self._testListener  = testListener
        self._currentTestId = None

        keys = list(_LOGGED_LEVELS.keys())

        # Manage Title 1, 2 and 3
        # -----------------------
        textCtrls = {}

        # The main sizer. This will hold the elements
        flexSizer  = wx.FlexGridSizer(rows=len(_LOGGED_LEVELS),
                                      cols=2,
                                      hgap=4,
                                      vgap=4)
        flexSizer.AddGrowableCol(1)

        for key, label in [(k, _LOGGED_LEVELS[k]) for k in sorted(keys, reverse = True)]:
            # Create Label for element
            labelCtrl = wx.StaticText(self,
                                      label=label,
                                      style=wx.ST_NO_AUTORESIZE)
            flexSizer.Add(labelCtrl,
                          flag = wx.ALL|wx.ALIGN_LEFT)

            # Create Content for element
            textCtrl = wx.TextCtrl(self,
                                   style=wx.TE_READONLY |wx.TEXT_ALIGNMENT_RIGHT | wx.EXPAND)
            flexSizer.Add(textCtrl,
                          flag = wx.TEXT_ALIGNMENT_RIGHT| wx.EXPAND)

            textCtrls[key] = textCtrl
        # end for

        self.title1TextCtrl      = textCtrls[_LEVEL_TITLE1]
        self.title2TextCtrl      = textCtrls[_LEVEL_TITLE2]
        self.title3TextCtrl      = textCtrls[_LEVEL_TITLE3]
        self.descriptionTextCtrl = textCtrls[_LEVEL_BRIEF]

        boxSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxSizer.Add(flexSizer, 1, wx.EXPAND | wx.ALL, 5)

        mainSizer = boxSizer


        self.SetSizer(mainSizer)
        mainSizer.Fit(self)

        # Use a timer to refresh the panel.
        self._timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER,             self.OnRefreshTimer)
        self.Bind(EVT_TESTSELECTIONCHANGED, self.OnTestSelectionChanged)
        self._timer.Start(250)
        self._model = None
    # end def __init__

    MSG = ''

    def _refreshCtrl(self, ctrl, level, testId):
        '''
        Refreshes a specific control, for a given level

        @param  ctrl   [in] (TextCtrl) The control to refresh
        @param  level  [in] (int)      The level for which to refresh
        @param  testId [in] (str)      The test id for which to refresh.
        '''
        if (testId is not None):
            message = self._testListener.getCachedMessage(testId, level)
            if (message is None):
                message = self.MSG
            # end if
        else:
            message = self.MSG
        # end if

        if ctrl.GetValue() != message:
            ctrl.SetValue(message)
        # end if
    # end def _refreshCtrl

    def _Refresh(self):
        '''
        Refreshes the panel contents
        '''
        testId = self._currentTestId

        self._refreshCtrl(self.title1TextCtrl,      _LEVEL_TITLE1, testId)
        self._refreshCtrl(self.title2TextCtrl,      _LEVEL_TITLE2, testId)
        self._refreshCtrl(self.title3TextCtrl,      _LEVEL_TITLE3, testId)
        self._refreshCtrl(self.descriptionTextCtrl, _LEVEL_BRIEF,  testId)
    # end def _Refresh

    def OnRefreshTimer(self, evt):
        '''
        Handles the refresh timer.

        @param  evt [in] (Event) The event that triggered the callback.
        '''
        self._Refresh()
        evt.Skip()
    # end def OnRefreshTimer

    def OnTestSelectionChanged(self, evt):
        '''
        Changes the currently selected testId, and updates the contents

        @param  evt [in] (Event) The event that triggered the callback.
        '''
        testIds = evt.testIds

        if (len(testIds) == 1):
            self._currentTestId = testIds[0]
        else:
            self._currentTestId = None
        # end if

        self._Refresh()
        evt.Skip()
    # end def OnTestSelectionChanged

    def setModel(self, model):
        '''
        Sets the model

        @param  model [in] (DataModel) The data model to set
        '''
        self._model = model

        # Register a listener to the model.
        # This listener will post a message to the current object for
        # later processing
        def dataModelListener(source, *args, **kwArgs):                                                                 # pylint:disable=W0613
            '''
            The dataModelListener is notified when an element of the dataModel changes.

            @param  source [in] (object) The notification source
            @option args   [in] (tuple) The arguments
            @option kwArgs [in] (dict) The keyword arguments
            '''
            event = TestSelectionChangedEvent(testIds=source,
                                              force=False)
            wx.PostEvent(self, event)
        # end def dataModelListener

        self._model.addListener(dataModelListener,
                                DataModel.ACTION_SELECTEDTESTSCHANGED)
    # end def setModel


    def getModel(self):
        '''
        Obtains the model

        @return The DataModel
        '''
        return self._model
    # end def getModel
# end class LogSpyPanel

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------

