#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.listener

@brief  Base implementation of the listeners

@author christophe.roquebert

@date   2018/10/22
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from threading                          import RLock
from pylibrary.tools.threadutils       import synchronized

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class Listener(object):
    '''
    Definition of the interface to be implemented by a listener.
    '''

    def __call__(self, source   = None,
                       action   = None):
        '''
        Callback being notified whenever the specified action (or None if no
        action is available) is triggered.

        Note that the listener is usually called @e after the action is
        performed, not before.

        @option source [in] (object) The object being the listened to.
        @option action [in] (object) The action being performed.
        '''
        raise NotImplementedError()
    # end def __call__
# end class Listener


SYNCHRONIZATION_LOCK = RLock()

class Listenable(object):
    '''
    Base implementation of an object to which listeners can be attached.
    '''

    ACTION_DEFAULT = "default"

    def __init__(self, *args, **kwargs):
        '''
        Constructor

        @option args   [in] (tuple) arguments
        @option kwargs [in] (dict)  keyword arguments
        '''
        super(Listenable, self).__init__(*args, **kwargs)

        self._listeners = {}
    # end def __init__

    @synchronized(SYNCHRONIZATION_LOCK)
    def addListener(self, listener,
                          action    = ACTION_DEFAULT):
        '''
        Adds a listener for the specified action.

        Note that a listener can be added multiple times, and will be called
        once for each addListener call.

        @param  listener [in] (callable) The listener to attach
        @option action   [in] (hashable) The action to attach to
        '''
        actionType = type(action)
        if (   (actionType is list)
            or (actionType is tuple)):
            actions = action
        else:
            actions = (action,)
        # end if

        for action in actions:
            self._listeners.setdefault(action, []).append(listener)
        # end for
    # end def addListener

    @synchronized(SYNCHRONIZATION_LOCK)
    def removeListener(self, listener,
                             action     = ACTION_DEFAULT):
        '''
        Removes a listener from the specified action.

        Note that this only removes @e one instance of the listener, multiple
        @c addListener calls must result in multiple @c removeListener calls.

        @param  listener [in] (callable) The listener to detach
        @option action   [in] (hashable) The action to detach from
        '''
        actionType = type(action)
        if (   (actionType is list)
            or (actionType is tuple)):
            actions = action
        else:
            actions = (action,)
        # end if

        for action in actions:
            listenerList = self._listeners.get(action)
            if (listenerList is not None):
                listenerList.remove(listener)
            # end if
        # end for
    # end def removeListener

    @synchronized(SYNCHRONIZATION_LOCK)
    def hasListener(self, listener,
                          action    = ACTION_DEFAULT):
        '''
        Tests whether the specified listener is attached at least once to the
        action.

        @param  listener [in] (Listener) The listener to test
        @option action   [in] (object)   The action for on the listener is
                                         attached

        @return Whether the listener present at least once for this action
        '''
        return listener in self._listeners.setdefault(action, [])
    # end def hasListener

    def notifyListeners(self, source    = None,
                              action    = ACTION_DEFAULT,
                              *args,
                              **kwargs):
        '''
        Notifiers listeners on the specified action

        @option source [in] (object) The source of the action, usually the
                            object on which the action is performed
        @option action [in] (object) The action performed
        @option args   [in] (tuple)  The listener arguments
        @option kwargs [in] (dict)   The listener keyword arguments
        '''
        if (source is None):
            source = self
        # end if

        for listener in self._listeners.setdefault(action, []):
            listener(source, action, *args, **kwargs)
        # end for
    # end def notifyListeners

    def __getstate__(self):
        '''
        Used to define WHAT elements are to be pickled/unpickled

        This is specifically used to EXCLUDE the listeners from pickling
        and deepcopy.

        @return (dict) A Dict of the data to pickle
        '''
        result = {}
        result.update(self.__dict__)
        del result['_listeners']

        return result
    # end def __getstate__

    def __setstate__(self, state):
        '''
        Used to define WHAT elements are to be pickled/unpickled

        This is specifically used to EXCLUDE the listeners from pickling
        and deepcopy.

        @param  state [in] (dict) A Dict of the data to unpickle
        '''
        self.__dict__.update(state)
        if ('_listeners' not in self.__dict__):
            self.__dict__['_listeners'] = {}
        # end if
    # end def __setstate__
# end class Listenable

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
