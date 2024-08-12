#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.system.dummydebugger

@brief  Dummy debugger implementation

        Most of commands only print in the console

@author christophe Roquebert

@date   2018/05/31
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.system.debugger         import Component
from pylibrary.system.debugger         import Debugger
from pylibrary.tools.hexlist            import HexList
import sys

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DummyDebugger(Debugger):
    '''
    Implementation of a Dummy debugger.
    '''

    _DEFAULT_HOST = 'localhost'
    _DEFAULT_PORT = 9030

    VERSION = '0.1.0'

    ## Register mapping:
    ## Name: (name, offset, length)
    ##
    ## The registers are _replaced_ if a [REGISTERS] section is found in the
    ## configuration file
    ##
    ## To add registers:
    ## In the section [REGISTERS], add
    ## register.1.name      = "R00" # register name, used in @ref getRegister and @ref setRegister
    ## register.1.offset    = 0x00
    ## register.1.bitoffset = 0x00  # [optional]
    ## register.1.bitlength = 0x08
    ## ... And so on for every register.
    _NAME      = 'name'
    _OFFSET    = 'offset'
    _BITOFFSET = 'bitoffset'
    _BITLENGTH = 'bitlength'

    KEYS_REGISTERS = (_NAME, _OFFSET, _BITOFFSET, _BITLENGTH)
    DEFAULT_REGISTERS = ( \
        {_NAME: 'R00',  _OFFSET: 0x00, _BITOFFSET: 0x00, _BITLENGTH: 0x08},
                        )

    MEMORY_START    = 0
    MEMORY_SIZE     = 1

    class DummyComponent(Component):
        '''
        Definition of the Dummy component
        '''
        def __init__(self):                                                                                             # pylint:disable=R0915
            '''
            Constructor
            '''
            super(DummyDebugger.DummyComponent, self).__init__()

            self.addRegisterDefinition(name = 'R00', offset = 0x00, bitOffset = 0x00, bitLength = 0x08, mode = self.MODE.USER)

        # end def __init__
    # end class DummyComponent

    def __init__(self, inputDir       = '.',
                       localDir       = None,
                       debuggerNumber = 0):
        '''
        @copydoc pylibrary.system.debugger.Debugger.__init__
        '''
        super(DummyDebugger, self).__init__(inputDir, localDir, debuggerNumber)

        self._stdout          = sys.stdout
        self.__str__namecache = None
        self.connectionHost   = self._DEFAULT_HOST
        self.connectionPort   = self._DEFAULT_PORT
        self.__socket         = None
    # end def __init__

    def setStdout(self, stdout):
        '''
        Set stdout attribute

        @param  stdout [in] (stream) Stream for output
        '''
        self._stdout = stdout
    # end def setStdout

    def _loadConfig(self):
        '''
        @copydoc pylibrary.system.debugger.Debugger._loadConfig
        '''
        self._component = self.DummyComponent()
    # end def _loadConfig

    def open(self, **kwargs):                                                                                           #@ReservedAssignment
        '''
        @copydoc pylibrary.system.debugger.Debugger.open
        '''
        super(DummyDebugger, self).open(**kwargs)
        self._openCount += 1
    # end def open

    def reset(self, **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.reset
        '''
        self._stdout.write(f'RESET of the simulator with arguments : {kwargs}')
        return 0
    # end def reset

    def run(self, addressOrLabel = None):
        '''
        @copydoc pylibrary.system.debugger.Debugger.run
        '''
        self._suspendCount = 0
        self._stdout.write('RUN of the simulator')
    # end def run

    def isRunning(self):
        '''
        @copydoc pylibrary.system.debugger.Debugger.isRunning
        '''
        if (self._suspendCount <= 0):
            self._stdout.write('simulator is RUNNING')
            return True
        else:
            self._stdout.write('simulator is NOT RUNNING')
            return False
        # end if
    # end def isRunning

    def stop(self):
        '''
        @copydoc pylibrary.system.debugger.Debugger.stop
        '''
        self._suspendCount = 1
        self._stdout.write('STOP of the simulator')
        return 0
    # end def stop

    def loadCoverage(self, filePath,
                           format = Debugger.FORMAT_COMMON):                                                            #@ReservedAssignment pylint:disable=W0622
        '''
        @copydoc pylibrary.system.debugger.Debugger.loadCoverage
        '''
        raise NotImplementedError
    # end def loadCoverage

    def saveCoverage(self, filePath,
                           format = Debugger.FORMAT_COMMON):                                                            #@ReservedAssignment pylint:disable=W0622
        '''
        @copydoc pylibrary.system.debugger.Debugger.saveCoverage
        '''
        raise NotImplementedError
    # end def saveCoverage

    def __str__(self):
        '''
        @copydoc pylibrary.system.debugger.Debugger.__str__
        '''
        name = 'Dummy Debugger'
        self._stdout.write(name)
        return name
    # end def __str__

    def getVersion(self):
        '''
        @copydoc pylibrary.system.debugger.Debugger.getVersion
        '''
        return self.VERSION
    # end def getVersion

    def getRegisters(self, registersList):                                                                              # pylint:disable=W0613
        '''
        @copydoc pylibrary.system.debugger.Debugger.getRegisters
        '''
        registerDefinitions = self._component.getRegisterDefinitions()
        filteredRegisters = [registerDefinitions[registerName] for registerName in registersList]

        result = {}
        for registerDefinition in sorted(filteredRegisters,
                                         key = lambda r: r.offset):
            bitOffset = registerDefinition.bitOffset
            bitLength = registerDefinition.bitLength

            # Read, in bytes
            sizeToRead = ( ( bitOffset + bitLength - 1 ) / 8 ) + 1

            registerAsArray = self.readMemory(registerDefinition.offset,
                                              sizeToRead)

            # Decode bytes
            value = 0

            # One-byte value, most common occurrence
            if (    (bitOffset == 0)
                and (bitLength == 8)):
                value = registerAsArray[0]
            # Non-byte register
            else:
                # LSB first
                for i in reversed(list(range(sizeToRead))):
                    value = value * 256 +registerAsArray[i]
                # end for

                # Shift by the starting offset
                value = value >> bitOffset

                # Truncate to the expected length
                value = value & ((1 << bitLength) - 1)
            # end if

            result[registerDefinition.name] = value
        # end for

        return result
    # end def getRegisters

    def getRegistersDefinition(self):
        '''
        Get the definition of the registers

        @return (dict) Definition of the registers
        '''
        return self._component.getRegisterDefinitions(Component.FORMAT.LIST_DICT)
    # end def getRegistersDefinition

    _registers = property(getRegistersDefinition)

    def readMemory(self, addressOrLabel,
                         length,
                         memoryType = None):
        '''
        @copydoc pylibrary.system.debugger.Debugger.readMemory
        '''
        assert isinstance(addressOrLabel, int), TypeError('Should be int instead')

        assert ((addressOrLabel + length) <= (self.MEMORY_START + self.MEMORY_SIZE)), IndexError('Out of range')

        return HexList(0x10)

    # end def readMemory

# end class DummyDebugger

def dummyPredicate(debugger):
    '''
    Predicate for DummyDebugger

    @param  debugger [in] (Debugger) Debugger instance

    @return (bool) True if the target is the expected
    '''
    debuggerTmp = debugger
    while (hasattr(debuggerTmp, 'next')):
        debuggerTmp = debuggerTmp.__next__
    # end while
    return isinstance(debuggerTmp, DummyDebugger)
# end def dummyPredicate

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
