#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.system.threadeddebugger

@brief  A debugger that runs another debugger in a separate thread.

@author christophe.roquebert

@date   2018/01/21
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from queue                              import Empty
from queue                              import Queue
from pylibrary.system.debugger         import Debugger
from pylibrary.system.debugger         import alwaysTrigger
from threading                          import Lock
from threading                          import Thread
from time                               import sleep
from types                              import MethodType

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class ThreadedDebugger(Debugger):
    '''
    A proxy debugger that wraps the instance of another debugger type,
    which is run from another thread.

    For the target debugger to actually run
    '''
    class Command(object):
        '''
        Container for a command, given for processing to the inner thread.
        '''

        ID = 1                                                                                                          # pylint:disable=C0103

        def __init__(self, target, name, *args, **kwargs):
            '''
            Command constructor

            @param  target [in] (callable) The callable object to invoke
            @param  name   [in] (str)      A name for this command
            @option args   [in] (tuple)    The arguments of the callable object
            @option kwargs [in] (dict)     The keyword arguments of the callable object
            '''
            self._target    = target
            self._name      = name
            self._args      = args
            self._kwargs    = kwargs
            self.result     = None
            self.exception  = None
            self.lock       = Lock()
            self.__class__.ID += 1
            self._id        = self.ID
            self.lock.acquire()
        # end def __init__

        def __call__(self):
            '''
            Command processing: Calls the @c self._name method in the target, and
            stores the result and/or exception
            '''

            try:
                self.result = self._target( *(self._args),
                                            **(self._kwargs))
            except StopIteration:
                pass
            except Exception as excp:
                self.exception = excp
            # end try

            self.lock.release()
        # end def __call__

        def __str__(self):
            '''
            Converts the current object to a string

            @return The current command, as a string
            '''
            return 'Command (%d): %s' % (self._id, self._name,)
        # end def __str__
    # end class Command

    def __init__(self, wrappedType,
                       preExecuteThread   = lambda:None,
                       postExecuteThread  = lambda:None,
                       preExecuteCommand  = lambda:None,
                       postExecuteCommand = lambda:None,
                       *args,
                       **kwargs):
        '''
        Constructor

        @param  wrappedType        [in] (Debugger) The type wrapped by this debugger
        @option preExecuteThread   [in] (callable) Thread initialization callback
        @option postExecuteThread  [in] (callable) Thread uninitialization callback
        @option preExecuteCommand  [in] (callable) Command initialization callback
        @option postExecuteCommand [in] (callable) Command uninitialization callback
        @option args               [in] (tuple)    The arguments of the wrapped instance constructor
        @option kwargs             [in] (dict)     The keyword arguments of the wrapped instance constructor.
        '''

        assert issubclass(wrappedType, Debugger), \
               'Invalid debugger type: %s' % (wrappedType.__name__)
        self.next                = wrappedType(*args, **kwargs)

        # The parent constructor must be called _after_ the initialization of
        # the self.next attribute
        super(ThreadedDebugger, self).__init__(*args, **kwargs)

        self._queue              = Queue()
        self._preExecuteThread   = preExecuteThread
        self._postExecuteThread  = postExecuteThread
        self._preExecuteCommand  = preExecuteCommand
        self._postExecuteCommand = postExecuteCommand
        self._thread             = None
    # end def __init__

    @classmethod
    def _threadProc(cls, preExecuteThread,
                         postExecuteThread,
                         preExecuteCommand,
                         postExecuteCommand,
                         queue):
        '''
        Main thread processing

        @param  preExecuteThread   [in] (callable) Thread initialization
        @param  postExecuteThread  [in] (callable) Thread un-initialization
        @param  preExecuteCommand  [in] (callable) Processing done before each command
        @param  postExecuteCommand [in] (callable) Processing done after each command
        @param  queue              [in] (Queue)    The queue used to append commands
        '''
        preExecuteThread()
        try:
            try:
                # Loop until the executor has stopped
                while True:

                    preExecuteCommand()

                    # Consume a task
                    try:
                        task = queue.get_nowait()
                        try:
                            # Execute the task, and append its children to the queue
                            task()
                        finally:
                            # Signal that the processing is done on this task
                            queue.task_done()
                        # end try
                    except Empty:
                        sleep(0.05)
                    # end try

                    postExecuteCommand()
                # end while
            except StopIteration:
                pass
            # end try
        finally:
            postExecuteThread()
        # end try
    # end def _threadProc

    def _getWrapper(self, name):
        '''
        Generic wrapper for method instances

        @param  name [in] (str) The name of the method instance to wrap.

        @return A wrapper method, handling thread synchronization between the
                current thread and the delegate thread.
        '''

        # Only wrap known attributes
        if (hasattr(self.__next__, name)):
            target = getattr(self.__next__, name)
            # Only wrap methods
            if (isinstance(target, MethodType)):
                _self = self
                queue = self._queue
                class Wrapper(object):
                    '''
                    A wrapper class, that contains wraps the payload of a function call
                    to be delegated to another thread in a command.

                    This contains the name of the function to call, and the
                    __call__ method builds, enqueues, and waits for the call
                    completion.
                    '''

                    def __init__(self, name):
                        '''
                        Constructor

                        @param  name [in] (str) A name for this wrapper
                        '''
                        self._name = name
                    # end def __init__

                    @staticmethod
                    def __call__(*args, **kwargs):
                        '''
                        Wrapper around the delegated thread call

                        @option args   [in] (tuple) arguments of the wrapped method call
                        @option kwargs [in] (dict)  keyword arguments of the wrapped method call

                        @return The wrapped call return value
                        '''
                        command = _self.Command(target, name, *args, **kwargs)
                        queue.put_nowait(command)

                        # Wait for the completion of the command
                        command.lock.acquire()

                        if command.exception is not None:
                            raise Exception(command.exception)
                        # end if

                        return command.result
                    # end def __call__

                    def __str__(self):
                        '''
                        Converts the current object to a string.

                        @return (str) The current object, as a string.
                        '''
                        return "Command: %s" % self._name
                    # end def __str__
                # end class Wrapper

                return Wrapper(name)
            # end if
        # end if

        return self.__dict__[name]
    # end def _getWrapper

    def __getattr__(self, name):
        '''
        Attribute accessor

        @param  name [in] (int) The name of the attribute to access

        @return The wrapped attribute
        '''
        return self._getWrapper(name)
    # end def __getattr__

    def __str__(self):                                                                                                  # pylint:disable=W0221,W0222
        '''
        @copydoc pylibrary.system.debugger.Debugger.__str__
        '''
        return self._getWrapper('__str__')()
    # end def __str__

    def close(self):                                                                                                    # pylint:disable=W0221,W0222
        '''
        @copydoc pylibrary.system.debugger.Debugger.close
        '''
        thread = self._thread
        queue  = self._queue
        if (thread is not None):
            result = self._getWrapper('close')()

            if (self._openCount == 0):
                def terminateThread():
                    '''
                    Thread termination callback
                    '''
                    raise StopIteration
                # end def terminateThread

                queue.put_nowait(terminateThread)
                queue.join()
                # We must wait for the thread to terminate.
                # Failing that, the COM objects may incorrectly un-initialize,
                # causing an MTCQ error in XView
                thread.join()

                # Wait for some additional delay before deallocating the thread.
                sleep(self.next.CLOSE_DELAY)

                self._thread = None
            # end if

            return result
        else:
            self._openCount -= 1
        # end if

        return None
    # end def close

    def fillMemory(self, addressOrLabel,
                         length,
                         value,
                         memoryType = None,
                         *args,
                         **kwargs):                                                                                     # pylint:disable=W0221,W0222
        '''
        @copydoc pylibrary.system.debugger.Debugger.fillMemory
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('fillMemory')(addressOrLabel,
                                              length,
                                              value,
                                              memoryType = memoryType,
                                              *args,
                                              **kwargs)
    # end def fillMemory

    def getAddress(self, addressOrLabel,
                         memoryType = None,
                         *args,
                         **kwargs):                                                                                     # pylint:disable=W0221,W0222
        '''
        @copydoc pylibrary.system.debugger.Debugger.getAddress
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('getAddress')(addressOrLabel,
                                              memoryType,
                                              *args,
                                              **kwargs)
    # end def getAddress

    def getCurrentBreakpointId(self, *args, **kwargs):                                                                  # pylint:disable=W0221,W0222
        '''
        @copydoc pylibrary.system.debugger.Debugger.getCurrentBreakpointId
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('getCurrentBreakpointId')(*args,
                                                          **kwargs)
    # end def getCurrentBreakpointId

    def getCycles(self, *args, **kwargs):                                                                               # pylint:disable=W0221,W0222
        '''
        @copydoc pylibrary.system.debugger.Debugger.getCycles
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('getCycles')(*args,
                                             **kwargs)
    # end def getCycles

    def getDebuggerInfo(self, flags = None,
                              *args,
                              **kwargs):                                                                                # pylint:disable=W0221,W0222
        '''
        @copydoc pylibrary.system.debugger.Debugger.getDebuggerInfo
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('getDebuggerInfo')(flags,
                                                   *args,
                                                   **kwargs)
    # end def getDebuggerInfo

    def getLabels(self, address,
                        *args,
                        **kwargs):                                                                                      # pylint:disable=W0221,W0222
        '''
        @copydoc pylibrary.system.debugger.Debugger.getLabels
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('getLabels')(address,
                                             *args,
                                             **kwargs)
    # end def getLabels

    def getPc(self, *args, **kwargs):                                                                                   # pylint:disable=W0221,W0222
        '''
        @copydoc pylibrary.system.debugger.Debugger.getPc
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('getPc')(*args,
                                         **kwargs)
    # end def getPc

    def getRegister(self, register,
                          *args,
                          **kwargs):                                                                                    # pylint:disable=W0221,W0222
        '''
        @copydoc pylibrary.system.debugger.Debugger.getRegister
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('getRegister')(register,
                                               *args,
                                               **kwargs)
    # end def getRegister

    def getRegisters(self, registersList,
                           *args,
                           **kwargs):                                                                                   # pylint:disable=W0221,W0222
        '''
        @copydoc pylibrary.system.debugger.Debugger.getRegisters
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('getRegisters')(registersList,
                                                *args,
                                                **kwargs)
    # end def getRegisters

    def getTimeOut(self, *args, **kwargs):                                                                              # pylint:disable=W0221,W0222
        '''
        @copydoc pylibrary.system.debugger.Debugger.getTimeOut
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('getTimeOut')(*args,
                                              **kwargs)
    # end def getTimeOut

    def getVersion(self, *args, **kwargs):                                                                              # pylint:disable=W0221,W0222
        '''
        @copydoc pylibrary.system.debugger.Debugger.getVersion
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('getVersion')(*args,
                                              **kwargs)
    # end def getVersion

    def isRunning(self, *args, **kwargs):                                                                               # pylint:disable=W0221,W0222
        '''
        @copydoc pylibrary.system.debugger.Debugger.isRunning
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('isRunning')(*args,
                                             **kwargs)
    # end def isRunning

    def loadAdrFile(self, adrFilePath, replace = True, *options, **kwargs):                                             # pylint:disable=W0221,W0222
        '''
        @copydoc pylibrary.system.debugger.Debugger.loadAdrFile
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('loadAdrFile')(adrFilePath,
                                               replace = replace,
                                               *options,
                                               **kwargs)
    # end def loadAdrFile

    def loadMemoryFile(self, memoryFilePath,
                             format     = Debugger.FORMAT_AUTO,                                                         # @ReservedAssignment pylint:disable=W0622
                             memoryType = None,
                             *args,
                             **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.loadMemoryFile
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('loadMemoryFile')(memoryFilePath,
                                                  format     = format,
                                                  memoryType = memoryType,
                                                  *args,
                                                  **kwargs)
    # end def loadMemoryFile

    def readVariables(self, output,
                            memoryType = None,
                            *args,
                            **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.readVariables
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('readVariables')(output,
                                                 memoryType = memoryType,
                                                 *args,
                                                 **kwargs)
    # end def readVariables

    def open(self, *args, **kwargs):                                                                                    # pylint:disable=W0221,W0222
        '''
        @copydoc pylibrary.system.debugger.Debugger.open
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        # assert self._thread is None, "A debugger is already open"
        if (self._thread is None):
            self._thread = Thread(target = self._threadProc,
                                  name   = '%s thread' % (self.next.__class__.__name__,),
                                  args = (self._preExecuteThread,
                                          self._postExecuteThread,
                                          self._preExecuteCommand,
                                          self._postExecuteCommand,
                                          self._queue),
                                  )

            self._thread.start()
        # end if

        result = self._getWrapper('open')(*args,
                                          **kwargs)

        return result

    # end def open

    def readMemory(self, addressOrLabel,
                         length,
                         memoryType = None,
                         *args,
                         **kwargs):                                                                                     # pylint:disable=W0221,W0222
        '''
        @copydoc pylibrary.system.debugger.Debugger.readMemory
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('readMemory')(addressOrLabel,
                                              length,
                                              memoryType = memoryType,
                                              *args,
                                              **kwargs)
    # end def readMemory

    def reset(self, *args, **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.reset
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('reset')(*args,
                                         **kwargs)
    # end def reset

    def run(self, addressOrLabel = None,
                  *args,
                  **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.run
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('run')(addressOrLabel = addressOrLabel,
                                       *args,
                                       **kwargs)
    # end def run

    def runFunction(self, addressOrLabel,
                          variables = None,
                          output    = None,
                           *args,
                           **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.runFunction
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('runFunction')(addressOrLabel,
                                               variables = variables,
                                               output    = output,
                                               *args,
                                               **kwargs)
    # end def runFunction

    def saveMemoryFile(self, addressOrLabel,
                             length,
                             memoryFilePath,
                             format     = Debugger.FORMAT_AUTO,                                                         # @ReservedAssignment pylint:disable=W0622
                             mode       = 'w+',
                             memoryType = None,
                             *args,
                             **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.saveMemoryFile
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('saveMemoryFile')(addressOrLabel,
                                                  length,
                                                  memoryFilePath,
                                                  format     = format,
                                                  mode       = mode,
                                                  memoryType = memoryType,
                                                  *args,
                                                  **kwargs)
    # end def saveMemoryFile

    def setPatchedAddress(self, addressOrLabel,
                                memoryType = None,
                                *args,
                                **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.setPatchedAddress
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('setPatchedAddress')(addressOrLabel,
                                                     memoryType = memoryType,
                                                     *args,
                                                     **kwargs)
    # end def setPatchedAddress

    def setPc(self, addressOrLabel,
                    *args,
                    **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.setPc
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('setPc')(addressOrLabel,
                                         *args,
                                         **kwargs)
    # end def setPc

    def setRegister(self, register,
                          value,
                          *args,
                          **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.setRegister
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('setRegister')(register,
                                               value,
                                               *args,
                                               **kwargs)
    # end def setRegister

    def setRegisters(self, registersDict,
                           *args,
                           **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.setRegisters
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('setRegisters')(registersDict,
                                                *args,
                                                **kwargs)
    # end def setRegisters

    def setTimeOut(self, timeout,
                         *args,
                         **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.setTimeOut
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('setTimeOut')(timeout,
                                              *args,
                                              **kwargs)
    # end def setTimeOut

    def stepInto(self, conditionFunction = alwaysTrigger,
                       mode              = Debugger.STEP_INSTRUCTION,
                       *args,
                       **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.stepInto
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('stepInto')(conditionFunction,
                                            mode = mode,
                                            *args,
                                            **kwargs)
    # end def stepInto

    def stepOut(self, conditionFunction = alwaysTrigger,
                      *args,
                      **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.stepOut
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('stepOut')(conditionFunction = conditionFunction,
                                           *args,
                                           **kwargs)
    # end def stepOut

    def stepOver(self, conditionFunction = alwaysTrigger,
                       mode              = Debugger.STEP_INSTRUCTION,
                       *args,
                       **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.stepOver
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('stepOver')(conditionFunction = conditionFunction,
                                            mode = mode,
                                            *args,
                                            **kwargs)
    # end def stepOver

    def stop(self, *args, **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.stop
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('stop')(*args, **kwargs)
    # end def stop

    def waitForStop(self, timeout = None,
                          *args,
                          **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.waitForStop
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('waitForStop')(timeout,
                                               *args,
                                               **kwargs)
    # end def waitForStop

    def writeMemory(self, addressOrLabel,
                          data,
                          memoryType = None,
                          *args,
                          **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.writeMemory
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('writeMemory')(addressOrLabel,
                                               data,
                                               memoryType = memoryType,
                                               *args,
                                               **kwargs)
    # end def writeMemory

    def writeVariables(self, variables,
                             memoryType = None,
                             *args,
                             **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.writeVariables
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('writeVariables')(variables,
                                                  memoryType = memoryType,
                                                  *args,
                                                  **kwargs)
    # end def writeVariables

    @classmethod
    def wrap(cls, wrappedType,
                  preExecuteThread   = lambda:None,
                  postExecuteThread  = lambda:None,
                  preExecuteCommand  = lambda:None,
                  postExecuteCommand = lambda:None):
        '''
        Wrap the call to the ThreadedDebugger constructor.

        @param  wrappedType        [in] (Debugger) The type to wrap.
        @option preExecuteThread   [in] (callable) The thread initialization callback
        @option postExecuteThread  [in] (callable) The thread uninitialization callback
        @option preExecuteCommand  [in] (callable) The command initialization callback
        @option postExecuteCommand [in] (callable) The command uninitialization callback

        @return A wrapper around the ThreadeDebugger constructor method
        '''
        def wrapper(*args, **kwargs):
            '''
            Wrapper around the wrapped type constructor.

            @option args   [in] (tuple) The wrapped type's constructor arguments
            @option kwargs [in] (dict)  The wrapped type's constructor keyword arguments
            @return A new instance of a ThreadedDebugger
            '''
            return cls(wrappedType,
                       preExecuteThread,
                       postExecuteThread,
                       preExecuteCommand,
                       postExecuteCommand,
                       *args, **kwargs)
        # end def wrapper
        return wrapper
    # end def wrap

    def addBreakpoint(self, addressOrLabel,
                            conditionFunction = alwaysTrigger,
                            isTransient       = False,
                            *args,
                            **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.addBreakpoint
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('addBreakpoint')(addressOrLabel,
                                                 conditionFunction = conditionFunction,
                                                 isTransient       = isTransient,
                                                 *args,
                                                 **kwargs)
    # end def addBreakpoint

    def removeBreakpoint(self, breakpointId,
                               *args,
                               **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.removeBreakpoint
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('removeBreakpoint')(breakpointId,
                                                    *args,
                                                    **kwargs)
    # end def removeBreakpoint

    def removeAllBreakpoints(self, *args, **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.removeAllBreakpoints
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('removeAllBreakpoints')(*args, **kwargs)
    # end def removeAllBreakpoints

    def enableBreakpoint(self, breakpointId,
                               *args,
                               **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.enableBreakpoint
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('enableBreakpoint')(breakpointId,
                                                    *args,
                                                    **kwargs)
    # end def enableBreakpoint

    def disableBreakpoint(self, breakpointId,
                                *args,
                                **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.disableBreakpoint
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('disableBreakpoint')(breakpointId,
                                                     *args,
                                                     **kwargs)
    # end def disableBreakpoint

    def setCoverage(self, on,
                          *args,
                          **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.setCoverage
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('setCoverage')(on,
                                               *args,
                                               **kwargs)
    # end def setCoverage

    def getCoverage(self, *args, **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.getCoverage
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('getCoverage')(*args, **kwargs)
    # end def getCoverage

    def loadCoverage(self, filePath,
                           format = Debugger.FORMAT_COMMON,                                                             # @ReservedAssignment pylint:disable=W0622
                           *args,
                           **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.loadCoverage
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('loadCoverage')(filePath,
                                                format = format,
                                                *args,
                                                **kwargs)
    # end def loadCoverage

    def saveCoverage(self, filePath,
                           format = Debugger.FORMAT_COMMON,                                                             # @ReservedAssignment pylint:disable=W0622
                           *args,
                           **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.saveCoverage
        @option args   [in] (list) extraneous arguments
        @option kwargs [in] (list) extraneous keyword arguments
        '''
        return self._getWrapper('saveCoverage')(filePath,
                                                format = format,
                                                *args,
                                                **kwargs)
    # end def saveCoverage

    def getReuseInstance(self):
        '''
        Gets the reuseInstance attribute

        @return The reuseInstance attribute
        '''
        return self.next.reuseInstance
    # end def getReuseInstance

    def setReuseInstance(self, value):
        '''
        Sets the reuseInstance attribute

        @param  value [in] (bool) The reuseInstance to set
        '''
        self.next.reuseInstance = value
    # end def setReuseInstance

    reuseInstance = property(getReuseInstance, setReuseInstance)

    def _getOpenCount(self):
        '''
        Gets the open count

        @return The current open count
        '''
        return self.next._openCount                                                                                     # pylint:disable=W0212
    # end def _getOpenCount

    def _setOpenCount(self, value):
        '''
        Sets the open count

        @param  value [in] (int) The value of the open count.
        '''
        self.next._openCount = value                                                                                    # pylint:disable=W0212
    # end def _setOpenCount

    _openCount    = property(_getOpenCount, _setOpenCount)

    def _getBreakpoints(self):
        '''
        Gets the wrapped breakpoints dict

        @return The current breakpoints dict
        '''
        return self.next._breakpoints                                                                                   # pylint:disable=W0212
    # end def _getBreakpoints

    def _setBreakpoints(self, value):
        '''
        Sets the wrapped breakpoints list

        @param  value [in] (list) The wrapped breakpoints dict
        '''
        self.next._setBreakpoints = value                                                                               # pylint:disable=W0212
    # end def _setBreakpoints

    _breakpoints = property(_getBreakpoints, _setBreakpoints)

    def _getPatchedAddress(self):
        '''
        @copydoc pylibrary.system.debugger.Debugger._getPatchedAddress
        '''
        raise NotImplementedError
    # end def _getPatchedAddress

    def _loadConfig(self):
        '''
        @copydoc pylibrary.system.debugger.Debugger._loadConfig
        '''
        raise NotImplementedError
    # end def _loadConfig
# end class ThreadedDebugger

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
