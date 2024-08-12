#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.system.debugger

@brief  Base Debugger Interface definition.

@author christophe.roquebert

@date   2018/09/11
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path                            import abspath
from pylibrary.tools.hexlist            import HexList
from pylibrary.tools.numeral            import Numeral
from os                                 import stat
from os.path                            import expanduser
from os.path                            import join
from os.path                            import splitext
from stat                               import ST_MTIME
from warnings                           import warn
from weakref                            import ref
import re

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

##@name Conditional function returned values
#
##@{
TRIGGER_BREAK    = True   ##< Break program execution
TRIGGER_CONTINUE = False  ##< Continue program execution
##@}

def alwaysTrigger(unusedDebugger):
    '''
    Utility function that always triggers

    @param  unusedDebugger [in] (Debugger) The debugger that invoked this function.
                                           Unused in this implementation.

    @return True
    '''
    return TRIGGER_BREAK
# end def alwaysTrigger

def neverTrigger(unusedDebugger):
    '''
    Utility function that never triggers

    @param unusedDebugger [in] (Debugger) The debugger that invoked this function.
                                          Unused in this implementation.
    @return False
    '''
    return TRIGGER_CONTINUE
# end def neverTrigger


class DebuggerProvider(object):
    """
    Interface implemented by objects able of provide an instance of an Debugger
    """

    def get_dbg(self, index_or_predicate=0, keep_for_test_duration=True):
        """
        Obtains an instance of a Debugger.

        :param index_or_predicate: It can either be an index identifying a unique debugger in the cache or
                                   a predicate, taking a Debugger instance as a parameter, and able to test whether
                                   the debugger is acceptable
        :type index_or_predicate: ``int`` or ``callable``
        :param keep_for_test_duration: Flag indicating whether to cache the object or not
        :type keep_for_test_duration: ``bool``

        :return: The wanted debugger.
        :rtype: ``Debugger Specific Class``
        """
        raise NotImplementedError
    # end def get_dbg
# end class DebuggerProvider


class Register(object):
    '''
    A register definition.
    '''
    def __init__(self, name, offset, bitOffset, bitLength, mode):
        '''
        Definition of a register.

        @param  name      [in] (str)      Name of the register.
        @param  offset    [in] (int,None) Offset of the register in data memory, if any.
        @param  bitOffset [in] (int)      Offset of the register's LSB in the data read at offset.
        @param  bitLength [in] (int)      Number of bits in the register.
        @param  mode      [in] (object)   Special mode needed for reading/writing to the register.
        '''
        self.name      = name
        self.offset    = offset
        self.bitOffset = bitOffset
        self.bitLength = bitLength
        self.mode      = mode
    # end def __init__

    def __eq__(self, other):
        '''
        Compares two register definitions.

        @param  other [in] (Register) The object to compare to

        @return (int) The equality result
        '''
        if (other is None):
            return -1
        # end if
        
        if not isinstance(other, Register):
            return -1
        # end if

        if not (self.name == other.name):
            return False
        # end if

        if not (self.offset == other.offset):
            return False
        # end if

        if not (self.bitOffset == other.bitOffset):
            return False
        # end if

        if not (self.bitLength == other.bitLength):
            return False
        # end if

        return (self.mode == other.mode)
    # end def __eq__


    def __ne__(self, other):
        '''
        Compares two register definitions for non-equality

        @param  other [in] (Register) The object to compare to

        @return The non-equality result
        '''
        return not (self == other)
    # end def __ne__
# end class Register

class Component(object):
    '''
    Definition of a component, to be switched
    '''

    class FORMAT(object):
        '''
        Format constants
        '''
        DICT_LIST = 0x00
        DICT_DICT = 0x00 | 0x01
        LIST_DICT = 0x02 | 0x00
        LIST_LIST = 0x02 | 0x01
    # end class FORMAT

    class MODE(object):
        '''
        Mode for registers
        '''
        IRRELEVANT = None

        RING0 = 0
        RING1 = 1
        RING2 = 2
        RING3 = 3

        SUPERVISOR = RING0
        USER       = RING3
    # end class MODE

    def __init__(self, registers=None):
        '''
        Constructor

        @option registers [in] (dict) The registers to initialize.
        '''
        self._registers = {}

        if (registers is not None):
            self.addRegisterDefinitions(registers)
        # end if
    # end def __init__


    def getRegisterDefinitions(self, format = FORMAT.DICT_LIST):                                                        # @ReservedAssignment #pylint:disable=W0622
        '''
        Obtains the register definitions, in the given format

        @option format [in] (int) The format to extract the information.

        @return (dict) The register definitions, in the required format.
        '''
        if (format == self.FORMAT.DICT_LIST):
            return self._registers

        elif (format == self.FORMAT.LIST_LIST):
            return [(r.name, r.offset, r.bitOffset, r.bitLength, r.mode)
                    for r in sorted(list(self._registers.values()),
                                    key = lambda x: x.name)]

        elif (format == self.FORMAT.DICT_DICT):
            return dict([(r.name, {'offset':    r.offset,
                                   'bitoffset': r.bitOffset,
                                   'bitlength': r.bitLength,
                                   'mode':      r.mode})
                    for r in sorted(list(self._registers.values()),
                                    key = lambda x: x.name)])

        elif (format == self.FORMAT.LIST_DICT):
            return [{'name': r.name, 'offset': r.offset, 'bitoffset': r.bitOffset, 'bitlength': r.bitLength, 'mode': r.mode}
                    for r in sorted(list(self._registers.values()),
                                    key = lambda x: x.name)]

        else:
            raise ValueError('Invalid format: %s' % format)

        # end if

    # end def getRegisterDefinitions

    def addRegisterDefinition(self, name,
                                    offset,
                                    bitOffset = 0,
                                    bitLength = 8,
                                    mode      = None):
        '''
        Adds a register definition.

        @param  name      [in] (str) Name of the register
        @param  offset    [in] (int) Offset of the register in memory
        @option bitOffset [in] (int) Offset of the register's lsb bit at the memory address.
        @option bitLength [in] (int) number of bits for this register.
        @option mode      [in] (int) mode for the register: None for irrelevant, 0 for user, 1 for supervisor
        '''
        self._registers[name] = Register(name, offset, bitOffset, bitLength, mode)
    # end def addRegisterDefinition

    def addRegisterDefinitions(self, registerDefinitions):
        '''
        Bulk add register definitions.

        @param registerDefinitions [in] (dict,list) Either a dict (name->(offset,bitOffset,bitLength,mode))
                                                    or a list (name,offset,bitOffset,bitLength,mode)
        '''
        if isinstance(registerDefinitions, dict):
            self._registers.update(registerDefinitions)
        else:
            for registerDefinition in registerDefinitions:
                if isinstance(registerDefinition, dict):
                    name, offset, bitOffset, bitLength, mode = [registerDefinition[key] for key in ['name', 'offset', 'bitoffset', 'bitlength', 'mode']]
                else:
                    name, offset, bitOffset, bitLength, mode = registerDefinition
                # end if
                self.addRegisterDefinition(name, offset, bitOffset, bitLength, mode)
            # end for
        # end if
    # end def addRegisterDefinitions
# end class Component

class Debugger(object):
    '''
    Debugger interface definition

    This class defines the interface that a debugger must implement.

    It is up to the implementors to specialize this class, providing
    specialized and optimized methods.
    '''
    ARCHITECTURE    = 'auto'

    ##@name Memory file formats
    #
    # see also #F_READWRITE (loadMemoryFile() & saveMemoryFile())
    ##@{
    FORMAT_AUTO      = 0 ##< Try to detect the file format
    FORMAT_BIN       = 1 ##< .BIN: Raw binary
    FORMAT_SRECORD   = 2 ##< .S19, .S28, .S34: Motorola S-record
    FORMAT_HEX       = 3 ##< .HEX: Intel Hex
    ##@}

    ##@name Coverage file formats
    #
    # see also #F_COVERAGE
    ##@{
    FORMAT_COMMON    = 0 ##< Common format (used for report generation)
    FORMAT_NATIVE    = 1 ##< Debugger native format
    FORMAT_PICKLE    = 2 ##< serializing and de-serializing format
    ##@}

    ##@name Stepping modes
    #
    # see also #F_STEPPING and #F_STEP_SOURCE
    ##@{
    STEP_INSTRUCTION = 0  ##< Stepping operation at instruction level
    STEP_SOURCE      = 1  ##< Stepping operation at source level
    ##@}

    ##@name The features supported by this debugger
    #
    # By default, a debugger should support:
    # - open(), close(), isOpen()
    # - __str__(), getVersion(), getDebuggerInfo()
    # - getTimeOut(), setTimeOut()
    # - getAddress(), getLabels()
    ##@{
    F_SUPPORTED      = None         ##< To be overloaded by derived classes
    F_RUNNING        = 0x00000001   ##< Target management:
                                    ##< - run(), stop(), isRunning()
                                    ##< - reset(), waitForStop()
    F_CYCLES         = 0x00000002   ##< Cycles count:
                                    ##< - getCycles()
    F_READWRITE      = 0x00000004   ##< Memory/Register access:
                                    ##< - readMemory(), writeMemory(), fillMemory()
                                    ##< - loadMemoryFile(), saveMemoryFile()
                                    ##< - getPc(), setPc()
                                    ##< - setRegister(), getRegister()
                                    ##< - setRegisters(), getRegisters()
                                    ##< - readVariables(), writeVariables()
    F_MAPPING        = 0x00000008   ##< Mapping file:
                                    ##< - loadAdrFile()
    F_BREAKPOINTS    = 0x00000010   ##< Breakpoints:
                                    ##< - addBreakpoint(), removeBreakpoint(), removeAllBreakpoints()
                                    ##< - getCurrentBreakpointId()
                                    ##< - enableBreakpoint(), disableBreakpoint()
    F_WATCHPOINTS    = 0x00000020   ##< Watchpoints:
                                    ##< - addWatchpoint(), removeWatchpoint(), removeAllWatchpoints()
                                    ##< - enableWatchpoint(), disableWatchpoint()
    F_STEPPING       = 0x00000040   ##< Stepping:
                                    ##< - stepInto(), stepOver(), stepOut()
                                    ##< - by default mode = STEP_INSTRUCTION
    F_STEP_SOURCE    = 0x00000080   ##< Stepping can be done at the source level
                                    ##< - call with mode = STEP_SOURCE
    F_RUNFUNCTION    = 0x00000100   ##< usually needs #F_READWRITE and #F_STEPPING:
                                    ##< - runFunction()
                                    ##< - setPatchedAddress()
    F_COVERAGE       = 0x00000200   ##< Coverage:
                                    ##< - setCoverage(), getCoverage()
                                    ##< - loadCoverage(), saveCoverage()
    F_ALL            = ((F_COVERAGE << 1) - 1)  ##< All the above features
    ##@}

    ##@name Default memory type
    #
    # These value should be overloaded by derived classes with MemType()
    ##@{
    MEMTYPE_PROGRAM  = None ##< Program memory space
    MEMTYPE_DATA     = None ##< Data memory space
    ##@}

    ## On some debuggers, closing is not an instant operation, and may need
    ## to introduce a small delay. While this delay is not guaranteed to work
    ## it _does_ have beneficial influence over the debugger stability
    ## This is the time, in seconds, that (for instance) a threaded debugger
    ## will wait before terminating the handler thread.
    CLOSE_DELAY = 0.0

    DECREMENT = '-'
    INCREMENT = '+'
    POINTER_MARKERS = (DECREMENT, INCREMENT)
    UPDATE_BEFORE = 'before'
    UPDATE_AFTER = 'after'

    class MemType(object):
        '''
        Memory type
        '''
        def __init__(self, value):
            '''
            Constructor

            @param value [in] (int) memory type id
            '''
            self._value = value
        # end def __init__

        def __str__(self):
            '''
            Obtain string representation

            @return (str)
            '''
            return str(self._value)
        # end def __str__

        def __repr__(self):
            '''
            Obtain string representation

            @return (str)
            '''
            return str(self)
        # end def __repr__

        def __eq__(self, other):
            '''
            Operator ==

            @param  other [in] (MemType) object to compare to

            @return (bool)
            '''
            return (self._value == other._value)                                                                         # pylint:disable=W0212
        # end def __eq__

        def __ne__(self, other):
            '''
            Operator !=

            @param  other [in] (MemType) object to compare to

            @return (bool)
            '''
            return not (self == other)
        # end def __ne__

        def getValue(self):
            '''
            Retrieve memory type value

            @return value
            '''
            return self._value
        # end def getValue
    # end class MemType

    class Triggerpoint(object):
        '''
        Abstract implementation of a breakpoint/watchpoint.

        It is up to the implementors of a debugger to specialize this class,
        providing the enable and disable method implementations.
        '''

        def __init__(self, debugger,
                           address,
                           conditionFunction,
                           transient = False):
            '''
            Constructor

            @param  debugger          [in]  (Debugger) The debugger this breakpoint
                                                       is associated with
            @param  address           [in]  (int)      The address at which to
                                                       set a breakpoint
            @param  conditionFunction [in]  (callable) The condition function associated
                                                       with this breakpoint
            @option transient         [in]  (bool)     Whether this is a transient
                                                       breakpoint or not

            @note   Transient breakpoints are internal to the debugger, and
                    should never be accessed outside the debugger class
            '''
            self.address            = address           ##< Trigger address
            self.conditionFunction  = conditionFunction ##< Trigger condition

            self._debugger          = ref(debugger)
            self._enabled           = False
            self._transient         = transient
        # end def __init__

        def getId(self):
            '''
            Obtain a unique id to this breakpoint.

            @return A unique id to this breakpoint.
            '''
            return id(self)
        # end def getId

        def enable(self):
            '''
            Enable the current breakpoint
            '''
            raise NotImplementedError
        # end def enable

        def disable(self):
            '''
            Disable the current breakpoint
            '''
            raise NotImplementedError
        # end def disable

        def isTransient(self):
            '''
            Test whether this breakpoint is transient or not.

            @return (bool) Whether this breakpoint is transient or not.
            '''
            return self._transient
        # end def isTransient

        def isEnabled(self):
            '''
            Obtain the enabled state of the breakpoint.

            @note   This is only a logical, internal state, that is may be
                    inconsistent with the remote debugger if a breakpoint has
                    been handled directly on the remote side.

            @return (bool) The enabled state of the breakpoint.
            '''
            return self._enabled
        # end def isEnabled

        def __str__(self):
            '''
            Obtain a string representation of the breakpoint.

            @return (str) representation of breakpoint
            '''
            return 'at 0x%08.8X, transient=%s, condition=%s' \
                   % (self.address, self._transient, self.conditionFunction)
        # end def __str__

        __repr__ = __str__
    # end class Triggerpoint

    class AddrWatchpoint(Triggerpoint):
        '''
        Implementation of a data access breakpoint (watchpoint).
        '''
        def __init__(self, debugger,
                           address,
                           length,
                           conditionFunction,
                           stopBeforeWrite,
                           transient = False):
            '''
            Constructor

            @param  debugger          [in]  (Debugger) Debugger instance
            @param  address           [in]  (int)      Address of the breakpoint
            @param  length            [in]  (int)      Length of data to watch
            @param  conditionFunction [in]  (callable) Condition of use of the breakpoint
            @param  stopBeforeWrite   [in]  (bool)     Stop before writing of data
            @option transient         [in]  (bool)     Transient or not
            '''
            super(Debugger.AddrWatchpoint, self).__init__(debugger,
                                                          address,
                                                          conditionFunction,
                                                          transient)

            self.length          = length           ##< Length of data to watch
            self.stopBeforeWrite = stopBeforeWrite  ##< Stop before writing of data
        # end def __init__

        def enable(self):
            '''
            Enable the current breakpoint
            '''
            raise NotImplementedError
        # end def enable

        def disable(self):
            '''
            Disable the current breakpoint
            '''
            raise NotImplementedError
        # end def disable
    # end class AddrWatchpoint

    class AddrBreakpoint(Triggerpoint):
        '''
        Implementation of a code breakpoint.
        '''
        def __init__(self, debugger,
                           address,
                           conditionFunction,
                           transient = False):
            ''' Constructor

            @param  debugger          [in]  (Debugger) Debugger instance
            @param  address           [in]  (int)      Address of the breakpoint
            @param  conditionFunction [in]  (callable) Condition of use of the breakpoint
            @option transient         [in]  (bool)     Transient or not
            '''
            super(Debugger.AddrBreakpoint, self).__init__(debugger,
                                                          address,
                                                          conditionFunction,
                                                          transient)
        # end def __init__

        def enable(self):
            '''
            Enable the current breakpoint
            '''
            raise NotImplementedError
        # end def enable

        def disable(self):
            '''
            Disable the current breakpoint
            '''
            raise NotImplementedError
        # end def disable
    # end class AddrBreakpoint

    def __init__(self, inputDir       = '.',
                       localDir       = None,
                       debuggerNumber = 0):
        '''
        Constructor

        @option inputDir       [in] (str) input/output directory
        @option localDir       [in] (str) The configuration directory.
        @option debuggerNumber [in] (int) Debugger number
        '''
        self._inputDir      = abspath(inputDir)

        self.number         = debuggerNumber

        if (localDir is None):
            self._localDir  = expanduser('~')
        else:
            self._localDir  = abspath(localDir)
        # end if

        self._component      = None

        self._adrFile        = None
        self._statCache      = {}

        self._breakpoints    = {}
        self._watchpoints    = {}

        self._patchedAddress = None
        self._timeout        = self._TIMEOUT

        self._openCount      = 0
        self._suspendCount   = 0
    # end def __init__

    @classmethod
    def available(cls):
        '''
        Checks that at least one of the current debuggers is available on the current machine.

        This is mainly useful for auto-tests, where this can be used to detect the relevance of some test scripts.

        @return (bool) Whether a debugger for the current class is available
        '''
        return False
    # end def available

    def _suspend(self):
        '''
        Suspend the debugger, if necessary.

        This sends the stop() command to the debugger if it is not already stopped.
        It also increments the suspend count, so that further resumes will only
        cause a run when the suspend count reaches 0.
        '''
        if (    (self._suspendCount <= 0)
            and (self.isRunning())):
            self.stop()
        else:
            self._suspendCount += 1
        # end if
    # end def _suspend

    def _resume(self):
        '''
        Resume the execution of the debugger.

        This must be used in conjunction with _suspend, and will only cause a
        run if the suspend count (which is decremented at the beginning of the
        method) reaches 0.
        '''
        self._suspendCount -= 1
        if (self._suspendCount <= 0):
            self.run()
        # end if
    # end def _resume

    # --------------------------------------------------------------------------
    # MANDATORY
    # --------------------------------------------------------------------------
    def _loadConfig(self):
        '''
        Load the configuration for the current debugger instance.
        '''
        raise NotImplementedError
    # end def _loadConfig

    def open(self, **kwargs):                                                                                           #@ReservedAssignment # pylint:disable=W0613
        '''
        Open a connection to the debugger, using previously supplied parameters.

        This method performs all necessary connection, authentication,
        initialization needed to connect to a debugger, emulator, simulator, etc...

        @option kwargs [in] (dict) debugger specific parameters
        '''
        self._loadConfig()
    # end def open

    def isOpen(self):
        '''
        Test whether a connection is already open.

        @return True if a connection is already open.
        '''
        return (self._openCount > 0)
    # end def isOpen

    def close(self):
        ''' Close a connection to the debugger.

        This method performs all necessary cleanup, powerdown, disconnection
        that are needed while disconnection from a debugger, emulator, simulator, etc...
        '''
        self.removeAllBreakpoints()
        self.removeAllWatchpoints()
    # end def close

    def __str__(self):
        '''
        Retrieve debugger's name

        @return (str) debugger name
        '''
        raise NotImplementedError
    # end def __str__

    def getComponent(self):
        '''
        Obtains the current component for this debugger

        @return (Component) The component
        '''
        return self._component
    # end def getComponent

    def setComponent(self, component):
        '''
        Sets the current component definition

        @param  component [in] (Component) The component to set.
        '''
        self._component = component
    # end def setComponent

    def getVersion(self):
        '''
        Obtain the version of this debugger.

        The version (and its format) is dependent on the remote debugger.
        An Dev board or a device may not follow the same version
        conventions.

        @return (str) The debugger version
        '''
        raise NotImplementedError
    # end def getVersion

    def getDebuggerInfo(self, flags = None):
        '''
        Obtain the information on the supported features of the debugger

        The default implementation does not implement any of these features.

        The result is returned as a long, where the input flags are set if
        they are supported and unset otherwise.

        Testing for the availability of a functionality would therefore look like:
        @code
        # Test for the availability of RUNFUNCTION
        if (d.getDebuggerInfo(d.RUNFUNCTION):
            # Do something
            pass
        # end if
        @endcode

        Performing multiple tests would require a slightly more complicated test:
        @code
        # Test for both the availability of STEPPING and READWRITE
        flags = d.STEPPING | d.READWRITE
        if (d.getDebuggerInfo(flags) == flags):
            # Do something
            pass
        # end if
        @endcode

        @option flags [in] (int) The flags to test [#F_RUNNING... #F_ALL],
                                 or None to test all flags.

        @return (int) The supported flags, filtered by the input flags.
        '''
        if (flags is None):
            flags = self.F_ALL
        # end if

        return flags & self.F_SUPPORTED
    # end def getDebuggerInfo

    ## Default timeout
    _TIMEOUT = (60 * 3)

    def setTimeOut(self, timeout):
        '''
        Set the timeout for most commands.

        @param  timeout [in] (float) The timeout, in seconds.
                                     None resets the timeout to the default value.
        '''
        if (timeout is None):
            timeout = self._TIMEOUT
        # end if

        self._timeout = 1.0 * timeout
    # end def setTimeOut

    def getTimeOut(self):
        '''
        Obtain the timeout set for most commands.

        @return (float) The timeout, in seconds.
        '''
        return self._timeout
    # end def getTimeOut

    def _toAddress(self, label,
                         memoryType = None):                                                                                  # pylint:disable=W0613
        '''
        Obtain the address for the specified label.

        @param  label       [in] (str) The memory label
        @option memoryType  [in] (int) The memory type

        @return (int) The address value
        '''
        return self._adrFile.getAddress(label)
    # end def _toAddress

    def getAddress(self, addressOrLabel,
                         memoryType = None):
        '''
        Get the address value from an address or a label.

        @param  addressOrLabel [in] (int, str) The memory address or label
        @option memoryType     [in] (int)      The memory type

        @return (int) The address value
        '''
        if (isinstance(addressOrLabel, str)):
            address = self._toAddress(addressOrLabel, memoryType)
        else:
            address = addressOrLabel
        # end if

        return int(address)
    # end def getAddress

    def getLabels(self, address):
        '''
        Get the labels closest to the specified address.

        @param  address [in] (int) The address to perform a reverse lookup for.

        @return A tuple containing both smaller and greater labels closest to
                the given address.
        '''
        return self._adrFile.getLabels(address)
    # end def getLabels

    # F_MAPPING
    def loadAdrFile(self, adrFilePath,                                                                                  # pylint:disable=W0613
                          replace       = True,
                          *options):
        '''
        Load a .adr file.

        @param  adrFilePath  [in] (str)     Path to the address file to load.
        @option replace      [in] (bool)    Whether the file replaces the loaded addresses
        @option options      [in] (objects) Loading options (local labels...), ignored.

        Example:
        @code
        # Load Mask.adr
        debugger.loadAdrFile("Mask.adr")
        @endcode
        '''
        adrFile  = AdrFile()
        filePath = join(self._inputDir, adrFilePath)

        mustLoad = True
        newTime  = stat(filePath)[ST_MTIME]
        if (filePath in self._statCache):
            cachedTime = self._statCache[filePath]
            if (cachedTime == newTime):
                mustLoad = False
            # end if
        # end if
        self._statCache[filePath] = newTime

        if (mustLoad):
            adrFile.load(filePath)

            if (replace):
                self._adrFile = adrFile
            else:
                self._adrFile.append(adrFile)
            # end if
        # end if
    # end def loadAdrFile

    # --------------------------------------------------------------------------
    # F_RUNNING
    # --------------------------------------------------------------------------

    def reset(self, **kwargs):
        '''
        Reset the debugger.

        Depending on the target being addressed, the behavior may vary:
        - hard reset
        - program reloading...

        @return (int) The current PC.
        '''
        raise NotImplementedError
    # end def reset

    def run(self, addressOrLabel = None):
        '''
        Run the debugger

        @option addressOrLabel [in] (str) The address or label at which to start
                                          the run

        Example:
        @code
        # add a Breakpoint at address 0x1234, start running at 0x1200, and resume.
        debugger.addBreakpoint(0x1234)
        debugger.run(0x1200)
        ...
        debugger.run()
        @endcode
        '''
        raise NotImplementedError
    # end def run

    def isRunning(self):
        '''
        Test whether the debugger is running, or is in a suspended state

        @return (bool) True if the code is currently running
        '''
        raise NotImplementedError
    # end def isRunning

    def stop(self):
        '''
        Stop the debugger

        @return (int) The current PC.

        Example:
        @code
        debugger.run()
        debugger.stop()
        @endcode
        '''
        raise NotImplementedError
    # end def stop

    def waitForStop(self, timeout = None):
        '''
        Wait for the debugger to stop.

        The debugger will stop if a breakpoint or watchpoint is triggered.

        @option timeout [in]  (float) The timeout in seconds,
                                      or None to use the default timeout.

        @return (int) The current PC.
        '''
        raise NotImplementedError
    # end def waitForStop

    # --------------------------------------------------------------------------
    # F_CYCLES
    # --------------------------------------------------------------------------

    def getCycles(self):
        '''
        Obtain the number of elapsed cycles since an arbitrary time.

        The elapsed cycle count is usually counted since the last reset or APDU.

        @return (int) The number of elapsed cycles
        '''
        raise NotImplementedError
    # end def getCycles

    # --------------------------------------------------------------------------
    # F_READWRITE
    # --------------------------------------------------------------------------

    def readMemory(self, addressOrLabel,
                         length,
                         memoryType = None):
        '''
        Read memory from the debugger

        @param  addressOrLabel [in] (int, str) The memory address or label at
                                               which to start reading
        @param  length         [in] (int)      The length of data to read
        @option memoryType     [in] (int)      The memory type to read

        @return (HexList) The obtained data
        '''
        raise NotImplementedError
    # end def readMemory

    def writeMemory(self, addressOrLabel,
                          data,
                          memoryType = None):
        '''
        Write memory to the debugger

        @param  addressOrLabel [in] (int, str) The memory address or label at
                                               which to start writing
        @param  data           [in] (HexList)   The data to write
        @option memoryType     [in] (int)      The memory type to write
        '''
        raise NotImplementedError
    # end def writeMemory

    def fillMemory(self, addressOrLabel,
                         length,
                         value,
                         memoryType = None):
        '''
        Fill a memory area with a byte value

        @param  addressOrLabel [in] (int, str) The memory address or label at
                                               which to start filling
        @param  length         [in] (int)      The length of data to fill
        @param  value          [in] (int)      The byte value
        @option memoryType     [in] (int)      The memory type to fill
        '''
        raise NotImplementedError
    # end def fillMemory

    def getRegister(self, register):
        '''
        Obtain the value of one register.

        @param  register [in] (str) A string designating the register

        @return (int) The register value
        '''
        return self.getRegisters([register])[register]
    # end def getRegister

    def setRegister(self, register,
                          value):
        '''
        Set the value of one register.

        @param  register [in] (str) A string designating the register
        @param  value    [in] (int) The register value
        '''
        self.setRegisters({register: value})
    # end def setRegister

    def getRegisters(self, registersList):
        '''
        Obtain the value of the specified registers, as a list

        @param  registersList [in] (tuple) A list of strings designating the
                                           registers to obtain

        @return A dict containing the register values.

        Example:
        @code
        # Display the value of RAMPZ, ZH, ZL
        registers = debugger.getRegisters(["RAMPZ", "ZH", "ZL"])
        print("RAMPZ = %04X" % (registers["RAMPZ"],))
        print("ZH    = %02X" % (registers["ZH"],))
        print("ZL    = %02X" % (registers["ZL"],))
        @endcode
        '''
        raise NotImplementedError
    # end def getRegisters

    def setRegisters(self, registersDict):
        '''
        Set the value of the specified registers, as a dict

        @param  registersDict [in] (dict) A dictionary of register values

        Example:
        @code
        # set R17, R18 to 0, set R19 to 1
        debugger.setRegisters({ "R17" : 0, "R18" : 0, "R19" : 1})
        @endcode
        '''
        raise NotImplementedError
    # end def setRegisters

    def getPc(self):
        '''
        Obtain the current PC from the debugger.

        The number of bytes this value is encoded on may vary.
        It is however assumed that it can fit in a Python int.

        @return (int) The current PC.

        Example:
        @code
        # Display the value of PC
        pc = debugger.getPC()
        print("pc = %X" % (pc,))
        @endcode
        '''
        return self.getRegister('PC')
    # end def getPc

    def setPc(self, addressOrLabel):
        '''
        Set the current PC from the debugger.

        The number of bytes this value is encoded on may vary.
        It is however assumed that it can fit in a python int.

        @param addressOrLabel [in] (int, str) New PC, either as an integer or a label string

        Example:
        @code
        # Set the value of PC to 0x1234
        debugger.setPC(0x1234)
        @endcode

        Example:
        @code
        # Set the value of PC to startlabel
        debugger.setPC("startlabel")
        @endcode
        '''
        self.setRegister('PC', self.getAddress(addressOrLabel))
    # end def setPc

    def loadMemoryFile(self, memoryFilePath,
                             format     = FORMAT_AUTO,                                                                  # @ReservedAssignment # pylint:disable=W0622
                             memoryType = None):
        '''
        Load a memory file.

        @param  memoryFilePath [in] (str) The path to the file to load.
        @option format         [in] (str) The format of the file to read
        @option memoryType     [in] (int) Memory Type

        Example:
        @code
        # Load Mask.S19 and its associated map file
        debugger.loadMemoryFile("Mask.s19")
        @endcode
        '''

        if (memoryType is None):
            memoryType = self.MEMTYPE_DATA
        # end if

        if (format == self.FORMAT_AUTO):
            if (memoryFilePath[:-4].lower() in ('.s19', '.s28', '.s37')):
                format = self.FORMAT_SRECORD                                                                            # @ReservedAssignment # pylint:disable=W0622
            elif (memoryFilePath[:-4].lower() in ('.hex',)):
                format = self.FORMAT_HEX                                                                                # @ReservedAssignment # pylint:disable=W0622
            else:
                format = self.FORMAT_SRECORD                                                                            # @ReservedAssignment # pylint:disable=W0622
            # end if
        # end if

        if (format == self.FORMAT_BIN):
            with open(memoryFilePath, 'rb') as inputfile:
                data = inputfile.read()
            # end with
            self.writeMemory(0, data, memoryType)

        else:
            raise ValueError('Unknown format: %s' % format)
        # end if
    # end def loadMemoryFile


    def saveMemoryFile(self, addressOrLabel,
                             length,
                             memoryFilePath,
                             format     = FORMAT_AUTO,                                                                  # @ReservedAssignment # pylint:disable=W0622
                             mode       = 'w+',
                             memoryType = None):
        '''
        Save a memory file.

        @param  addressOrLabel [in] (int, str) Starting address or label
        @param  length         [in] (int)      Data length
        @param  memoryFilePath [in] (str)      Path to the file to save
        @option format         [in] (str)      Format of the file to save
        @option mode           [in] (str)      Mode to save the file ("w", "w+")
        @option memoryType     [in] (MemType)  Memory type to save
                                              (implementation dependent)

        @code
        # Dump the program memory to a file
        debugger.saveMemoryFile(0, 40, "coredump.s19")
        @endcode
        '''

        if (not isinstance(memoryType, self.MemType)):
            warn('The saveMemoryFile API has been modified. Please update parameter order',
                 category = DeprecationWarning,
                 stacklevel = 2)

            # old: memoryFilePath, [format, mode,            memoryType, addressOrLabel, length]
            # new: addressOrLabel,  length, memoryFilePath, [format,     mode,           memoryType]

            old_memoryFilePath = addressOrLabel
            old_format         = length
            old_mode           = memoryFilePath
            old_memoryType     = format
            old_addressOrLabel = mode
            old_length         = memoryType

            addressOrLabel = old_addressOrLabel
            length         = old_length
            memoryFilePath = old_memoryFilePath
            format         = old_format                                                                                 # @ReservedAssignment # pylint:disable=W0622
            mode           = old_mode
            memoryType     = old_memoryType
        # end if

        if (memoryType is None):
            memoryType = self.MEMTYPE_DATA
        # end if

        if (format == self.FORMAT_AUTO):
            ext = splitext(memoryFilePath)[1].lower()

            if (ext in ('.s19', '.s28', '.s37')):
                format = self.FORMAT_SRECORD                                                                            # @ReservedAssignment # pylint:disable=W0622

            elif (ext in ('.hex',)):
                format = self.FORMAT_HEX                                                                                # @ReservedAssignment # pylint:disable=W0622

            else:
                raise ValueError('Cannot guess file format: %s' % (ext,))
            # end if
        # end if

        data = self.readMemory(addressOrLabel, length, memoryType)

        if (format == self.FORMAT_BIN):
            if (mode == 'w+'):
                mode = 'wb+'
            elif (mode == 'w'):
                mode = 'wb'
            # end if

            with open(memoryFilePath, mode) as outputfile:
                outputfile.write("".join([chr(x) for x in data]))
            # end with

#         elif (format == self.FORMAT_SRECORD):
#             address = self.getAddress(addressOrLabel, memoryType)
#             binaryFile = MotorolaBinaryFile()
#             binaryFile[address:address+length] = data
#             binaryFile.save(memoryFilePath, address, length)

#         elif (format == self.FORMAT_HEX):
#             address = self.getAddress(addressOrLabel, memoryType)
#             binaryFile = IntelBinaryFile()
#             binaryFile[address:address+length] = data
#             binaryFile.save(memoryFilePath, address, length)

        else:
            raise ValueError('Unknown format: %s' % (format,))
        # end if
    # end def saveMemoryFile

    def readVariables(self, output,
                            memoryType = None):
        '''
        Read the output variables

        @param  output     [in] (tuple) A list of tuples that contain the variables to get.
        @option memoryType [in] (int)   The memory type to read

        @return (dict) containing the obtained variables.

        Each tuple contains:
        -# The address or label of the variable to set
        -# The length of the variable to get.
        -# Optionally, the type of the variable to read.
           If None, a HexList is returned
        '''
        variables = {}
        if (output is not None):
            for variable in output:
                variableAddressOrLabel = variable[0]
                variableLength         = variable[1]
                variableType           = None
                if (len(variable) > 2):
                    variableType = variable[2]
                # end if

                variableValue = self.readMemory(variableAddressOrLabel,
                                                variableLength,
                                                memoryType)

                # Automatic variable conversion
                if (variableType is not None):
                    variableValue = variableType(Numeral(variableValue, variableLength))
                # end if

                variables[variableAddressOrLabel] = variableValue
            # end for
        # end if
        return variables
    # end def readVariables

    def _updatePointer(self, addressOrLabel,
                             update,
                             memoryType = None):
        '''
        Update a pointer address

        @param  addressOrLabel [in] (str,int) Pointer address or label
        @param  update         [in] (str)     Update type ('+' or '-')
        @option memoryType     [in] (int)     The memory type to write

        @return (int) Pointer value
        '''
        address = self.readMemory(addressOrLabel, 2, memoryType).toLong()
        if update == self.INCREMENT:
            address += 1
        elif update == self.DECREMENT:
            address -= 1
        else:
            raise ValueError('Wrong update type: %s, only "+" or "-" supported'
                             % update)
        # end if
        self.writeMemory(addressOrLabel, HexList.fromLong(address, 2), memoryType)
        return address
    # end def _updatePointer

    def writeVariables(self, variables,
                             memoryType = None):
        '''
        Initialize the input variables

        @param  variables  [in] (tuple) A list of tuples that contain the variables to set.
        @option memoryType [in] (int)   The memory type to read

        Each tuple contains:
        -# The address or a string containing the label of the variable to set.
        -# The value of the variable to set
        -# Optionally, the length of the variable to set.
           If None an attempt is made to deduce it from the type.
        .
        '''
        pointerUpdate  = None

        if variables is not None:
            for variable in variables:
                variableAddressOrLabel = variable[0]
                variableValue          = variable[1]
                variableLen            = None
                if len(variable) > 2:
                    variableLen = variable[2]
                # end if

                # Automatic variable type
                if variableLen is None:
                    variableValue = HexList(variableValue)

                else:
                    if (isinstance(variableValue, int)):
                        format = "%%0%d.%dX" % (variableLen*2, variableLen*2)                                           # @ReservedAssignment # pylint:disable=W0622
                        variableValue = HexList(format % variableValue)

                    elif (hasattr(variable, '__hexlist__')):
                        variableValue = HexList(variableValue)
                    # end if

                    variableValue = variableValue[:variableLen]
                # end if

                if isinstance(variableAddressOrLabel, str):
                    if variableAddressOrLabel.startswith(self.POINTER_MARKERS):
                        marker = variableAddressOrLabel[0]
                        variableAddressOrLabel = variableAddressOrLabel[1:]
                        pointerUpdate = self.UPDATE_BEFORE

                    elif variableAddressOrLabel.endswith(self.POINTER_MARKERS):
                        marker = variableAddressOrLabel[-1]
                        pointerMarker = variableAddressOrLabel[:-1]
                        variableAddressOrLabel = self.readMemory(pointerMarker, 2, memoryType)
                        pointerUpdate = self.UPDATE_AFTER

                    # end if

                    if pointerUpdate == self.UPDATE_BEFORE:
                        variableAddressOrLabel = self._updatePointer(variableAddressOrLabel, marker, memoryType)
                    # end if
                # end if

                self.writeMemory(variableAddressOrLabel,
                                 variableValue,
                                 memoryType)

                if pointerUpdate == self.UPDATE_AFTER:
                    self._updatePointer(pointerMarker, marker, memoryType)
                # end if
                pointerUpdate = None
            # end for
        # end if
    # end def writeVariables

    # --------------------------------------------------------------------------
    # F_BREAKPOINTS
    # --------------------------------------------------------------------------

    def addBreakpoint(self, addressOrLabel,
                            conditionFunction = alwaysTrigger,
                            isTransient       = False):
        '''
        Add a breakpoint to the debugger

        @param  addressOrLabel    [in] (int, str) The address or label at which
                                                  to set the breakpoint
        @option conditionFunction [in] (callable) A function that will be called every
                                                  time the breakpoint is triggered.
        @option isTransient       [in] (bool)     Whether the breakpoint is transient.

        @return A breakpoint ID, used afterwards to enable/disable/remove the
                breakpoint.

        @note   A transient breakpoint will be cleared whenever another
                breakpoint is triggered, and its conditionalFunction returns
                True, or when it is itself reached.

        Setting a breakpoint is a common operation while performing white-box
        tests.
        There is a need however, in very specific cases, to use
        <i>conditional breakpoints</i>
        In such cases, the conditionFunction is address this behavior.

        Example 1:
        @code
        # Add a breakpoint at address 0x1234
        debugger.addBreakpoint(0x1234)
        @endcode

        Example 2:
        @code
        # Add a breakpoint at address 0x1234 that will trigger after
        # the 7th execution

        # trigger function
        countdown = [7]
        def breakpointTrigger(debugger):
            countdown[0] -= 1
            return (countdown < 0)
        # end def breakpointTrigger

        debugger.addBreakpoint(0x1234, breakpointTrigger)
        @endcode
        '''
        address    = self.getAddress(addressOrLabel)

        breakpoint = self.AddrBreakpoint(self, address,
                                               conditionFunction,
                                               isTransient)
        breakpoint.enable()
        breakpointId = breakpoint.getId()
        self._breakpoints[breakpointId] = breakpoint

        return breakpointId
    # end def addBreakpoint

    def removeBreakpoint(self, breakpointId):
        '''
        Remove a breakpoint by id

        @param  breakpointId [in] (int) The identifier of the breakpoint to remove

        Example:
        @code
        # Add a breakpoint at address 0x1234, remove it
        bpId = debugger.addBreakpoint(0x1234)
        ...
        debugger.removeBreakpoint(bpId)
        @endcode
        '''
        if (breakpointId in self._breakpoints):
            breakpoint = self._breakpoints[breakpointId]
            breakpoint.disable()

            del self._breakpoints[breakpointId]
        # end if
    # end def removeBreakpoint

    def removeAllBreakpoints(self):
        '''
        Remove all breakpoints

        Example:
        @code
        # Add two breakpoint at addresses 0x1234, 0x1248, remove them
        bpId1 = debugger.addBreakpoint(0x1234)
        bpId2 = debugger.addBreakpoint(0x1248)
        ...
        debugger.removeAllBreakpoints()
        @endcode
        '''
        for breakpoint in iter(list(self._breakpoints.values())):
            breakpoint.disable()
        # end for

        self._breakpoints.clear()
    # end def removeAllBreakpoints

    def enableBreakpoint(self, breakpointId):
        '''
        Enable a breakpoint by id.

        @param  breakpointId [in] (int) The id of the breakpoint to re-enable

        Example:
        @code
        # Add a breakpoint at address 0x1234, disable and enable it
        bpId = debugger.addBreakpoint(0x1234)
        debugger.disableBreakpoint(bpId)
        ...
        debugger.enableBreakpoint(bpId)
        @endcode
        '''
        breakpoint = self._breakpoints[breakpointId]
        breakpoint.enable()
    # end def enableBreakpoint

    def disableBreakpoint(self, breakpointId):
        '''
        Disables a breakpoint by id.

        @param  breakpointId [in] (int) The id of the breakpoint to re-enable

        Example:
        @code
        # Add a breakpoint at address 0x1234, disable it
        bpId = debugger.addBreakpoint(0x1234)
        debugger.disableBreakpoint(bpId)
        @endcode
        '''
        breakpoint = self._breakpoints[breakpointId]
        breakpoint.disable()
    # end def disableBreakpoint

    def getCurrentBreakpointId(self):
        '''
        Obtain the id of the breakpoint associated with the current PC.

        @return The id of the currently triggered breakpoint.
        '''
        result = None
        if (not self.isRunning()):
            pc = self.getPc()
            for bpId, breakpoint in self._breakpoints.items():
                if (    (isinstance(breakpoint, self.AddrBreakpoint))
                    and (pc == breakpoint.address)):
                    result = bpId
                    break
                # end if
            # end for
        # end if
        return result
    # end def getCurrentBreakpointId

    # --------------------------------------------------------------------------
    # F_WATCHPOINTS
    # --------------------------------------------------------------------------

    def addWatchpoint(self, addressOrLabel,
                            length            = 1,
                            conditionFunction = alwaysTrigger,
                            stopBeforeWrite   = True):
        '''
        Add a watchpoint on an address or label.

        @param  addressOrLabel    [in] (string,int) The address or label at which to set the
                                        watchpoint
        @param  length            [in] (int) The data length to watch.
        @param  conditionFunction [in] (callable) A function that will be called every
                                        time the watchpoint is triggered.
        @param  stopBeforeWrite   [in] (bool) Whether the watchpoint will be called
                                        before or after the actual write.

        @return A watchpoint ID, used afterwards to enable/disable/remove the
                watchpoint.

        Example: Trigger whenever an unnecessary update update is made at address
                 0x1234
        @code
        def trigger(d, newValue, oldValue):
            # Fail if the new value is the same as the old value
            assert not (newValue == oldValue)
            return False
        # end def trigger

        self.addWatchpoint(0x1234, 0x10, trigger)
        @endcode
        '''
        address = self.getAddress(addressOrLabel)

        watchpoint = self.AddrWatchpoint(self,
                                         address,
                                         length,
                                         conditionFunction,
                                         stopBeforeWrite)
        watchpoint.enable()
        watchpointId = watchpoint.getId()
        self._watchpoints[watchpointId] = watchpoint

        return watchpointId
    # end def addWatchpoint

    def removeAllWatchpoints(self):
        '''
        Remove all watchpoints

        Example:
        @code
        # Add two watchpoint at addresses 0x1234, 0x1248, remove them
        bpId1 = debugger.addWatchpoint(0x1234)
        bpId2 = debugger.addWatchpoint(0x1248)

        ...

        debugger.removeAllWatchpoints()
        @endcode
        '''

        for watchpoint in iter(list(self._watchpoints.values())):
            watchpoint.disable()
        # end for

        self._watchpoints.clear()
    # end def removeAllWatchpoints

    def removeWatchpoint(self, watchpointId):
        '''
        Remove a watchpoint by id

        @param  watchpointId [in] (str) The id of the watchpoint to remove

        Example:
        @code
        # Add a watchpoint at address 0x1234, remove it
        bpId = debugger.addWatchpoint(0x1234)

        ...

        debugger.removeWatchpoint(bpId)
        @endcode
        '''
        if (watchpointId in self._watchpoints):
            watchpoint = self._watchpoints[watchpointId]
            watchpoint.disable()

            del self._watchpoints[watchpointId]
        # end if
    # end def removeWatchpoint

    def enableWatchpoint(self, watchpointId):
        '''
        Enable a watchpoint by id.

        @param watchpointId [in] (int) The id of the watchpoint to re-enable

        Example:
        @code
        # Add a watchpoint at address 0x1234, disable and enable it
        bpId = debugger.addWatchpoint(0x1234)
        debugger.disableWatchpoint(bpId)

        ...

        debugger.enableWatchpoint(bpId)
        @endcode
        '''
        watchpoint = self._watchpoints[watchpointId]
        watchpoint.enable()
    # end def enableWatchpoint

    def disableWatchpoint(self, watchpointId):
        '''
        Disable a watchpoint by id.

        @param watchpointId [in] (int) The id of the watchpoint to re-enable

        Example:
        @code
        # Add a watchpoint at address 0x1234, disable it
        bpId = debugger.addWatchpoint(0x1234)
        debugger.disableWatchpoint(bpId)
        @endcode
        '''
        watchpoint = self._watchpoints[watchpointId]
        watchpoint.disable()
    # end def disableWatchpoint

    # --------------------------------------------------------------------------
    # F_STEPPING
    # --------------------------------------------------------------------------

    def stepInto(self, conditionFunction = alwaysTrigger,
                       mode              = STEP_INSTRUCTION):
        '''
        Step into the code.

        When supported by the debugger, stepping can be done either on an
        assembler instruction, or on a source line.

        @note The conditionFunction can be used to perform conditional stepping.

        @option conditionFunction [in] (callable) An optional function called after
                                                  each step, that indicates whether
                                                  further stepping is not necessary
        @option mode              [in] (int)      The stepping mode
                                                  (source or instruction)

        @return (int) The current PC.

        Example 1:
        @code
        # Step into the next statement
        debugger.stepInto()
        @endcode
        '''
        raise NotImplementedError
    # end def stepInto

    def stepOver(self, conditionFunction = alwaysTrigger,
                       mode              = STEP_INSTRUCTION):
        '''
        Step over the code.

        When supported by the debugger, stepping can be done either on an
        assembler instruction, or on a source line.

        @note The conditionFunction can be used to perform conditional stepping.

        @option conditionFunction [in] (callable) An optional function called after
                                                  each step, that indicates whether
                                                  further stepping is not necessary
        @option mode              [in] (int) The stepping mode (source or instruction)

        @return (int) The current PC.

        Example 1:
        @code
        # Step over the next statement
        debugger.stepOver()
        @endcode
        '''
        raise NotImplementedError
    # end def stepOver

    def stepOut(self, conditionFunction = alwaysTrigger):
        '''
        Step out of the current subroutine.

        @option conditionFunction [in] (callable) An optional function called after
                                                  each step, that indicates whether
                                                  further stepping is not necessary

        @return (int) The current PC.
        '''
        raise NotImplementedError
    # end def stepOut

    # --------------------------------------------------------------------------
    # F_RUNFUNCTION
    # --------------------------------------------------------------------------

    def setPatchedAddress(self, addressOrLabel,
                                memoryType      = None):
        '''
        Set the address to be patched.

        This disables the patch address auto-detection for the runFunction method,
        and forces the debugger to use the specified patch address.

        Use None to re-activate the patch address auto-detection.

        @param  addressOrLabel [in] (int, str) The address to inject the code to.
        @option memoryType     [in] (int)      The memory type
        '''
        self._patchedAddress = self.getAddress(addressOrLabel, memoryType)
    # end def setPatchedAddress

    def _getPatchedAddress(self):
        '''
        Get the address to be patched.

        @return (int) address
        '''
        raise NotImplementedError
    # end def _getPatchedAddress

    def runFunction(self, addressOrLabel,
                          variables = None,
                          output    = None):
        '''
        Set the input variables, calls the function at @c addressOrLabel, and
        outputs the result.

        @param  addressOrLabel [in]  (int, str) The address or label to call.
        @option variables      [in]  (tuple)    A list of tuples containing
                                                the variables to set.
        @option output         [in]  (tuple)    A list of tuples containing
                                                the variables to read.

        @return (dict) containing the read variables, or None if the function
                did not exit successfully

        @see pylibrary.system.debugger.Debugger.setPatchedAddress

        Example:
        We need to call the function @c G_Addition, declared as:
        @code
        /**
         * Adds the value @c a to the global int variable @c g_value
         * @param a [in] The value to add to @c g_value, as a 32-bits int
         * @return The value of @c g_value @c + @c as a 32-bits int
         */
        int G_Addition(int a)
        {
            return g_value + a;
        }
        @endcode
        We also know that @c a is passed in register @c R16, and @c G_Addition returns
        its result in register @c R0

        A python API to this function (in a class where @c self._debugger contains
        a reference to the current debugger) would be
        @code
        def G_Addition(self, a):
            input  = ( ('R16', HexList(a),   4), )
            output = ( ('R0',  4,         int), )

            result = self._debugger.runFunction('G_Addition', input, output)

            if (result is not None):
                return result['R0']
            # end if
            return None
        # end def G_Addition
        @endcode
        '''
        raise NotImplementedError
    # end def runFunction


    # --------------------------------------------------------------------------
    # F_COVERAGE
    # --------------------------------------------------------------------------

    def setCoverage(self, on):
        '''
        Activate/deactivate the gathering of coverage data.

        Using the @c on parameter set to True will erase any previously
        gathered coverage info.

        @param  on [in] (bool) Whether the coverage must be activated or not
        '''
        raise NotImplementedError
    # end def setCoverage

    def getCoverage(self):
        '''
        Obtain the state of the coverage engine.

        @return (bool) Whether the coverage engine is activated.
        '''
        raise NotImplementedError
    # end def getCoverage

    def loadCoverage(self, filePath,
                           format = FORMAT_COMMON):                                                                     # @ReservedAssignment # pylint:disable=W0622
        '''
        Load coverage data from a file.

        @param  filePath [in] (str) Path to the file to load
        @option format   [in] (str) Format of the file to load
                                    (#FORMAT_COMMON, #FORMAT_NATIVE)
        '''
        raise NotImplementedError
    # end def loadCoverage

    def saveCoverage(self, filePath,
                           format = FORMAT_COMMON):                                                                     # @ReservedAssignment # pylint:disable=W0622
        '''
        Save the coverage data to a file.

        @param  filePath [in] (str) Path to the file to load
        @option format   [in] (str) Format of the file to load
                                    (#FORMAT_COMMON, #FORMAT_NATIVE)
        '''
        raise NotImplementedError
    # end def saveCoverage

# end class Debugger

## Alias
AbstractDebugger = Debugger

class AdrFile(object):
    '''
    Content of an address file.

    Load and save the contents of an address file, which is the conversion
    of a map file to a generic format.

    The generic format for the address file is:
    @code
    # comment
    NameOfAModule
    [space]+LABEL[space]+[0-9A-F]+[space]*L?
    @endcode
    where:
    - Lines beginning with @# are comments
    - Lines beginning with a non-space character other than @# define the beginning
    of a module.
    - Lines beginning with a space character define the declaration of a label.

    For lines that declare a label, there are three main parts
    - The first word in the line defines the name of the label.
    - The following word must be the hexadecimal representation of the address
    - The last character is optional, and defins whether the label is local.
    (This allows multiply defined labels, in different modules)
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self._labels = {}
    # end def __init__

    def getAddress(self, label):
        '''
        Obtain the address of a label

        @param  label [in] (str) Label value

        @return (int) Address of the label
        '''
        try:
            labelList = self._labels[label]

            if (labelList is None):
                raise ValueError('Unexpected address list for label %s'
                                 % (label,))
            # end if

            if (len(labelList) > 1):
                raise ValueError('label %s is multiply defined at addresses: %s'
                                 % (label, '(%s)' % ','.join(['0x%08.8X' % x for x in labelList])))
            # end if

            return labelList[0]

        except KeyError:
            raise AssertionError('Could not find address for label: %s'
                                % (label,))
        # end try
    # end def getAddress

    def setAddress(self, label,
                         value):
        '''
        Set the address of a given label.

        @param  label [in] (str) The label to set the address for.
        @param  value [in] (int) The address for this label.
        '''
        self._labels[label] = (value,)
    # end def setAddress

    def getLabels(self, value = None):
        '''
        Look up the labels closest to the given address

        @option value [in] (str) address for which to retrieve the labels

        @return A tuple (minLabel, maxLabel) of the labels closest to this address.
                minLabel and maxLabel can be equal if the address is an exact label match.
        '''

        if (value is None):
            # Return all labels
            return tuple(self._labels.keys())
        # end if

        lowerBoundAddress  = -1
        lowerBoundLabel    = 'Unknown'
        higherBoundAddress = 0xFFFFFFFFFFFFFFFF
        higherBoundLabel   = 'Unknown'

        for label, addresses in self._labels.items():
            for address in addresses:
                if (address == value):
                    return (label, label,)
                # end if

                if (    (address < value)
                    and (address > lowerBoundAddress)):
                    lowerBoundAddress = address
                    lowerBoundLabel   = label
                elif (    (address > value)
                    and (address < higherBoundAddress)):
                    higherBoundAddress = address
                    higherBoundLabel   = label
                # end if
            # end for
        # end for

        return (lowerBoundLabel, higherBoundLabel,)
    # end def getLabels


    _CHAR_COMMENT = '#'[0]
    _CHAR_SPACE   = ' '[0]
    _LABEL_DECLARATION_REGEX = re.compile(r'\s+([^\s]+)\s+([\dA-Z]+)\s*(L?)')

    def load(self, path):
        '''
        Load an address file from a path

        @param  path [in] (str) Path of the label file
        '''
        with open(path) as adrFile:
            lineNumber = 0
            for line in adrFile.readlines():
                lineNumber += 1
                if (len(line.strip()) > 0):

                    # Ignore comments
                    if (line[0] == self._CHAR_COMMENT):
                        pass
                    # A space is a new label
                    elif (line[0] == self._CHAR_SPACE):
                        groups = self._LABEL_DECLARATION_REGEX.findall(line)
                        if (groups is None):
                            raise ValueError('Unable to parse line %d: %s'
                                             % (lineNumber, line))
                        else:
                            try:
                                label = groups[0][0]
                                address = int(groups[0][1], 16)
                            except:
                                raise ValueError('Unable to parse line %d: %s'
                                                 % (lineNumber, line))
                            # end try

                            labelList = self._labels.setdefault(label, [])
                            labelList.append(address)
                        # end if
                    # Module definition
                    else:
                        # ignored
                        pass
                    # end if
                # end if
            # end for
        # end with
    # end def load

    def append(self, adrFile):
        '''
        Append the contents of the adrFile to the current file

        @param  adrFile [in] (str) The AdrFile to concatenate
        '''
        self._labels += adrFile.getLabels()
    # end def append
# end class AdrFile

class DebuggerException(Exception):
    '''
    Common class for debugger exceptions
    '''

    ##@name Default causes
    ##@{
    CAUSE_UNKNOWN  = None  ##< Unexpected
    CAUSE_MUTE     = 0     ##< Mutisme
    ##@}

    def __init__(self, *options):
        '''
        Constructor

        The constructor takes its parameters from the list of
        CAUSE_XXX constants, and may optionnally provide a message.

        @option options [in] (tuple) The exception cause
        '''
        super(DebuggerException, self).__init__(*options)
    # end def __init__

    def getCause(self):
        '''
        Obtain the exception cause.

        This is the first int argument.

        @return (str) The exception cause, as an int from SmartDeviceException
        '''
        causes = [x for x in self.args if isinstance(x, int)]
        if (len(causes) > 0):
            return causes[0]
        # end if
        return DebuggerException.CAUSE_UNKNOWN
    # end def getCause

    def getMessage(self):
        '''
        Obtain the messages for this exception

        @return (str) The message embedded within this exception.
        '''
        stringMessages = [x for x in self if isinstance(x, str)]
        return ', '.join(stringMessages)
    # end def getMessage
# end class DebuggerException

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
