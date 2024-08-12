#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.system.context

@brief  Context Device interface

@author christophe.roquebert

@date   2018/11/26
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.system.device            import BaseSmartDevice
from pylibrary.system.device            import SmartDeviceException
from pylibrary.tools.hexlist            import HexList
from pylibrary.tools.threadutils        import synchronized
from threading                          import RLock
from threading                          import local
from weakref                            import ref

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

_LEVEL_COMMAND = 3

def logreader(func):
    '''
    Decorator that wraps the method, and checks the last accessed reader

    @param  func [in] (callable) the function to check

    @return The decorated function
    '''

    def innerFunction(self, *options):
        '''
        Wraps all calls to decorated logged functions.
        If the reader has changed since the last call, a trace will
        be output to all logs.

        @option options [in] (tuple) all parameters passed to the called function.

        @return result of the decorated function
        '''
        self._checkLastAccessedReader()                                                                                 # pylint:disable=W0212
        return func(self, *options)
    # end def innerFunction

    return innerFunction
# end def logreader

class ContextSmartDevice(BaseSmartDevice):
    '''
    A proxy class, that wraps context-local informations of the given SmartDevice object.

    This allows the SmartDevice consumers to be independent from one another:
    Even if a consumer changes the behavior of the Device through a modification of
    the ContextSmartDevice, the instance used for another consumer will stay the same.

    This class also has an additional state that provides the last response and status.

    This state is better kept in the current context-specific implementation:
    A consumer will not interfere with another.
    '''

    THREAD_LOCAL_DATA = local()

    __B2S = ['%02X' % x for x in range(256)]

    MARKER_MUTEX = RLock()

    @synchronized(MARKER_MUTEX)
    def __init__(self, device, logger):
        '''
        Constructor

        @param  device   [in] (SmartDevice) The decorated smart device
        @param  logger [in] (TestCase)  The test the device is accessed in
        '''
        super(ContextSmartDevice, self).__init__(device.number)

        self.next           = device
        self.lastResponse   = None
        self.lastStatus     = None
        self._logger        = ref(logger)

        # Set a marker, so that we do not unallocate the reader if
        # another ContextSmartDevice instance keeps a reference on the reader
        _next = device
        while hasattr(_next, 'next'):
            _next = _next.next
        # end while
        setattr(_next, '__mark', id(self))
    # end def __init__

    @synchronized(MARKER_MUTEX)
    def __del__(self):
        '''
        Destructor.
        '''
        try:
            # Automatically de-allocate the current device.
            # This is necessary, as PCSC devices need to be released before
            # being used by another thread, or a sharing violation may occur.

            # However, as in some cases the device may already have been
            # unallocated by the caller, we must guard against extraneous
            # unallocation
            if self.is_allocated():
                # Only unallocate if no other context has accessed the device
                _next = self.next
                while hasattr(_next, 'next'):
                    _next = _next.next
                # end while

                if hasattr(_next, '__mark') and (getattr(_next, '__mark') == id(self)):
                    self.unallocate()
                # end if
            # end if
        except Exception:                                                                                               # pylint:disable=W0703
            pass
        # end try
    # end def __del__

    def __getattr__(self, name):
        '''
        Return attributes of ContextSmartDevice

        @param  name [in] (str) Key of the attribute to return

        @return Attribute[name] of ContextDebugger
        '''
        return getattr(self.next, name)
    # end def __getattr__

    def __setattr__(self, name, value):
        '''
        Fixes attributes of ContextSmartDevice

        @param  name  [in] (str)    Name Key of ContextDebugger
        @param  value [in] (object) Name value
        '''
        if (name in ("next", "test", "number", "lastResponse", "lastStatus", "_logger")):
            self.__dict__[name] = value
        else:
            raise AttributeError('Read only attribute: %s' % name)
        # end if
    # end def __setattr__

    # --------------------------------------------------------------------------
    #                           Public interface
    # --------------------------------------------------------------------------
    @classmethod
    def configure(cls, **kwargs):
        '''
        @copydoc pylibrary.system.device.BaseSmartDevice.configure
        '''
        pass
    # end def configure

    def is_allocated(self):
        '''
        @copydoc pylibrary.system.device.BaseSmartDevice.is_allocated
        '''
        return self.next.is_allocated()
    # end def is_allocated

    def allocate(self):
        '''
        @copydoc pylibrary.system.device.BaseSmartDevice.allocate
        '''
        return self.next.allocate()
    # end def allocate

    def unallocate(self):
        '''
        @copydoc pylibrary.system.device.BaseSmartDevice.unallocate
        '''
        return self.next.unallocate()
    # end def unallocate

    @logreader
    def powerUp(self):
        '''
        @copydoc pylibrary.system.device.BaseSmartDevice.powerUp
        '''
        response          = self.next.powerUp()
        self.lastResponse = response
        self.lastStatus   = None

        logger = self._logger()
        logger.log(_LEVEL_COMMAND,
                   'Power up      %s' % (self.next.getReaderName(),))

        self._logBlock('Atr', response)
        self._logTime()

        return response
    # end def powerUp

    def isPoweredUp(self):
        '''
        @copydoc pylibrary.system.device.BaseSmartDevice.isPoweredUp
        '''
        return self.next.isPoweredUp()
    # end def isPoweredUp

    @logreader
    def reset(self):
        '''
        @copydoc pylibrary.system.device.BaseSmartDevice.reset
        '''
        response = self.next.reset()

        self.lastResponse = response
        self.lastStatus   = None

        logger = self._logger()
        logger.log(_LEVEL_COMMAND, 'Reset')

        self._logBlock('DeviceID / VendorID: 0x', response)
        self._logTime()

        return response
    # end def reset

    @logreader
    def powerDown(self):
        '''
        @copydoc pylibrary.system.device.BaseSmartDevice.powerDown
        '''
        logger = self._logger()
        logger.log(_LEVEL_COMMAND, 'Power down')

        return self.next.powerDown()
    # end def powerDown

    @logreader
    def sendPps(self, *pps):
        '''
        @copydoc pylibrary.system.device.BaseSmartDevice.sendPps
        '''
        pps      = HexList(*pps)
        response = self.next.sendPps(pps)

        def logPps(title, pps):
            '''
            Log PPS frame

            @param  title [in] (str)    input/output
            @param  pps   [in] (HexList) frame
            '''
            pck = 0
            ppsTmp = HexList(pps)
            ppsTmp.insert(0, 0xFF)
            for ppsx in ppsTmp:
                pck ^= ppsx
            # end for
            ppsTmp.append(pck)
            self._logBlock(title, ppsTmp)
        # end def logPps

        logPps('Pps', pps)
        self._logBlock('Response', response)
        self._logTime()

        return response
    # end def sendPps

    def getReaderName(self):
        '''
        @copydoc pylibrary.system.device.BaseSmartDevice.getReaderName
        '''
        return self.next.getReaderName()
    # end def getReaderName

    def getReaderInfo(self):
        '''
        @copydoc pylibrary.system.device.BaseSmartDevice.getReaderInfo
        '''
        return self.next.getReaderInfo()
    # end def getReaderInfo

    def getDriverInfo(self):
        '''
        @copydoc pylibrary.system.device.BaseSmartDevice.getDriverInfo
        '''
        return self.next.getDriverInfo()
    # end def getDriverInfo

    def setTearing(self, tearing_time):
        '''
        @copydoc pylibrary.system.device.BaseSmartDevice.setTearing
        '''
        return self.next.setTearing(tearing_time)
    # end def setTearing

    @logreader
    def sendRaw(self, *data):
        '''
        @copydoc pylibrary.system.device.BaseSmartDevice.sendRaw
        '''
        rawInput = HexList(data)
        self._logBlock('Raw input', rawInput)

        response = self.next.sendRaw(*data)
        self._logBlock('Raw output', response)

        return response
    # end def sendRaw

    def getElapsedTime(self):
        '''
        @copydoc pylibrary.system.device.BaseSmartDevice.getElapsedTime
        '''
        return self.next.getElapsedTime()
    # end def getElapsedTime

    def _checkLastAccessedReader(self):
        '''
        Checks that the last accessed reader is the same as the current one.

        If the readers differ, a trace is sent in the log.
        '''
        threadLocalData = self.THREAD_LOCAL_DATA
        if (not hasattr(threadLocalData, 'lastAccessedReader')):
            threadLocalData.lastAccessedReader = None
        # end if

        if (    (threadLocalData.lastAccessedReader is None)
            or  (threadLocalData.lastAccessedReader() is not self)):

            message = 'Now using reader: %s' % (str(self),)

            logger = self._logger()
            logger.logTrace(message)

            threadLocalData.lastAccessedReader = ref(self)
        # end if
    # end def _checkLastAccessedReader

    def _logBlock(self, title, array):
        '''
        Logs a hexadecimal block of data, aligned, with a given title

        @param  title [in] (str)    The label stating the first line
        @param  array [in] (HexList) The HexList containing to the data to log
        '''
        lenArray = len(array)
        if (lenArray > 0):
            blockSize  = 16
            indentSize = 14

            # data
            dataLog     = [title, ' ' * (indentSize - len(title))]
            indentBlock = '\n' + (' ' * indentSize)

            for i in range(0, lenArray, blockSize):
                data = array[i:i+blockSize]

                dataLog.append(' '.join([self.__B2S[x] for x in data]))
                if ((i + blockSize) < lenArray):
                    dataLog.append(indentBlock)
                # end if
            # end for

            logger = self._logger()
            logger.log(_LEVEL_COMMAND, ''.join(dataLog))
        # end if
    # end def _logBlock

    def _logTime(self):
        '''
        Requests the elapsed time of the last command, and logs it if available
        '''
        logger = self._logger()

        elapsedTime = self.next.getElapsedTime()
        if (elapsedTime):
            logger.log(_LEVEL_COMMAND, 'Time          %d ms' % (elapsedTime,))
        # end if

        logger.log(_LEVEL_COMMAND, '\n')
    # end def _logTime

    def getResponse(self):
        '''
        Response of last send command

        @return Last command response
        '''
        return self.lastResponse
    # end def getResponse

    def __repr__(self):
        '''
        Representation of the class

        @return String representation
        '''
        return self.next.getDriverInfo()
    # end def __repr__

    def __str__(self):
        '''
        Representation of the class

        @return String representation
        '''
        if (self.is_allocated()):
            return self.next.getDriverInfo()
        else:
            return 'Reader not allocated'
        # end if
    # end def __str__
# end class ContextSmartDevice

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
