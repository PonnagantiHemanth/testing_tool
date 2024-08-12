#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.system.gdbmidebugger

@brief   GDB/MI Debugger

@author christophe Roquebert

@date    2012/08/27
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.system.debugger         import Debugger
from pylibrary.system.debugger         import alwaysTrigger
from pylibrary.tools.config            import ConfigParser
from pylibrary.tools.hexlist            import HexList
from pylibrary.tools.threadutils import synchronized
from os.path                            import abspath
from os.path                            import isfile
from os.path                            import join
from os.path                            import splitext
from subprocess                         import PIPE
from subprocess                         import Popen
from subprocess                         import STDOUT
from threading                          import RLock
from time                               import time
import re

try:
    from pysetup                        import GDB                                                                       # @UnresolvedImport # pylint:disable=E0611,F0401
except ImportError:
    GDB = 'gdb'
# end try

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class GdbMiException(Exception):
    '''
    Special exception class for GDB events
    '''
# end class GdbMiException

SYNCHRONIZATION_LOCK = RLock()

class GdbMiDebugger(Debugger):                                                                                            # pylint:disable=W0223
    '''
    GDB/MI Debugger
    '''
    _NAME       = 'GDB/MI Debugger'

    F_SUPPORTED = ( Debugger.F_RUNNING
                  | Debugger.F_READWRITE
                  | Debugger.F_MAPPING
                  | Debugger.F_BREAKPOINTS
                  | Debugger.F_STEPPING
                  | Debugger.F_STEP_SOURCE
                  | Debugger.F_RUNFUNCTION)

    def __init__(self, inputDir       = '.',
                       localDir       = None,
                       debuggerNumber = 0):
        '''
        @copydoc pylibrary.system.debugger.Debugger.__init__
        '''
        super(GdbMiDebugger, self).__init__(inputDir, localDir, debuggerNumber)

        self._id                = 1      # Identifier of the command

        self._interface         = None
        self._connectionHost    = None
        self._connectionPort    = None

        self._runningTime       = None
        self._suspendCount      = 1

        self._regNames          = None
        self.addressCache       = None

        self._response          = None  # Last response for debug/test purpose
    # end def __init__

    @synchronized(SYNCHRONIZATION_LOCK)
    def sendCommand(self, name, *args):
        '''
        Send a command to gdb

        @param  name [in] (str)   gdb/mi command
        @option args [in] (list)  arguments

        @return (GdbMiResponse)
        '''
        # Send command
        self._response = self._interface.sendAndReceive('%s %s'
                                                        % (name,
                                                           ' '.join([str(arg) for arg in args])))

        if (self._response is not None):

            # Check Async Records
            for record in self._response.filterByRecord(GdbMiAsyncExecRecord):
                # Update target state
                self._suspendCount = 1 if record.output_class == 'stopped' else 0
            # end for

            # Check Stream Console Record
            for record in self._response.filterByRecord(GdbMiStreamConsoleRecord):
                if (record.output_class.startswith('SIG')):
                    raise GdbMiException(record.output_class)
                # end if
            # end for

            # Check Result Record
            if (self._response.result.output_class == GdbMiResultRecord.ERROR):
                raise GdbMiException(self._response.result.results['msg'])
            # end if

        # end if

        return self._response
    # end def sendCommand

    class AddrBreakpoint(Debugger.AddrBreakpoint):
        '''
        Specialization of the AddrBreakpoint class for GdbMiDebugger
        '''

        def __init__(self, debugger,
                           address,
                           conditionFunction,
                           transient = False):
            '''
            @copydoc pylibrary.system.debugger.Debugger.AddrBreakpoint.__init__
            '''
            super(GdbMiDebugger.AddrBreakpoint, self).__init__(debugger,
                                                               None,
                                                               conditionFunction,
                                                               transient)

            response = debugger.sendCommand('-break-insert',
                                            # The added breakpoint is created disabled
                                            '-d',
                                            '*0x%X' % (address,))

            # -> -break-insert -d *0xYYYYYY

            # <- ^done,bkpt={number="X",
            #                type="breakpoint",
            #                disp="keep",enabled="n",
            #                addr="0xYYYYYY",
            #                func="name",
            #                file=".../File.c",
            #                fullname=".../File.c",
            #                line="L",
            #                times="0",
            #                original-location="*0xYYYYYY"}
            bkpt = response.result.results['bkpt']
            self.number  = int(bkpt['number'])
            self.address = int(bkpt['addr'], 16)
            self.label   = debugger.getLabels(address)[0]
        # end def __init__

        def enable(self):
            '''
            Enable the current breakpoint
            '''
            # Do not enable an already-enabled breakpoint
            if (not self._enabled):
                self._debugger().sendCommand('-break-enable', self.number)
                # -> -break-enable X
                # <- ^done
                self._enabled = True
            # end if
        # end def enable

        def disable(self):
            '''
            Disable the current breakpoint
            '''
            # Do not disable an already-disabled breakpoint
            if (self._enabled):
                self._debugger().sendCommand('-break-disable', self.number)
                # -> -break-disable X
                # <- ^done
                self._enabled = False
            # end if
        # end def disable

        def delete(self):
            '''
            Delete the current breakpoint
            '''
            self._debugger().sendCommand('-break-delete', self.number)
            # -> -break-delete X
            # <- ^done
            self._enabled = False
        # end def delete

    # end class AddrBreakpoint

    class AddressCache(dict):
        '''
        Dict used to cache label address
        '''
        def __init__(self, debugger):
            '''
            @param  debugger [in] (Debugger) debugger handler
            '''
            self._debugger = debugger

            super(GdbMiDebugger.AddressCache, self).__init__(dict())
        # end def __init__

        _RE_SYMBOL_VALUE = re.compile(r'Symbol "(?P<name>\w+)" .+ (?P<value>0x\w+)')
        def __missing__(self, key):
            '''
            This method is called by the __getitem__ method of the dict class
            when the requested key is not found.

            @param  key [in] (str) label

            @return (int) Address of label found in [symbol-]file
            '''
            response = self._debugger.sendCommand('info', 'address', key)
            # -> info address name
            # <- &"info address name\n"
            # <- ~"Symbol \"name\" is a function at address 0xYYYYYY.\n"
            # <- ^done
            for record in response.filterByRecord(GdbMiStreamConsoleRecord):
                mo = self._RE_SYMBOL_VALUE.match(record.output_class)
                if (mo is not None):
                    if (mo.group('name') == key):
                        address = int(mo.group('value'), 16)
                        self[key] = address
                        return address
                    # end if
                # end if
            # end for
        # end def __missing__
    # end class AddressCache

    def _toAddress(self, label,
                         memoryType = None):                                                                            # pylint:disable=W0613
        '''
        @copydoc pylibrary.system.debugger.Debugger._toAddress
        '''
        return self.addressCache[label]
    # end def _toAddress

    def getAddress(self, addressOrLabel,
                         memoryType = None):
        '''
        @copydoc pylibrary.system.debugger.Debugger.getAddress
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
        @copydoc pylibrary.system.debugger.Debugger.getLabels
        '''
        labels = list()

        self.sendCommand('info symbol', '0x%X' % (address,))
        # -> info symbol 0xYYYYYY

        # <- ~"name in section .text\n"
        # -> ^done
        for record in self._response.filterByRecord(GdbMiStreamConsoleRecord):
            if (' in section ' in record.output_class):
                labels.append(record.output_class[:record.output_class.find(' in ')])
            # end if
        # end for

        return labels
    # end def getLabels


    # --------------------------------------------------------------------------
    # MANDATORY
    # --------------------------------------------------------------------------
    _SECTION_CONNECTION = 'CONNECTION'
    _KEY_PORT = 'port_'
    _KEY_HOST = 'host_'

    def _loadConfig(self):
        '''
        @copydoc pylibrary.system.debugger.Debugger._loadConfig
        '''
        filePath = join(self._localDir, 'GdbMiDebugger.ini')

        config = ConfigParser()

        if (isfile(filePath)):
            config.read([filePath])

        else:
            config.add_section(self._SECTION_CONNECTION)

            config.set(self._SECTION_CONNECTION,
                       '%s%d' % (self._KEY_HOST, self.number),
                       self._connectionHost)

            config.set(self._SECTION_CONNECTION,
                       '%s%d' % (self._KEY_PORT, self.number),
                       self._connectionPort)

            with open(filePath, 'w+') as fp:
                config.write(fp)
            # end with
        # end if

        self._connectionHost = config.get(self._SECTION_CONNECTION, '%s%d'
                                          % (self._KEY_HOST, self.number))
        self._connectionPort = config.get(self._SECTION_CONNECTION, '%s%d'
                                          % (self._KEY_PORT, self.number))
    # end def _loadConfig

    def open(self, **kwargs):                                                                                           #@ReservedAssignment
        '''
        @copydoc pylibrary.system.debugger.Debugger.open

        @par Parameters
             - @c filePath   : exec file
             - @c symbolPath : symbol file
             .
        '''
        super(GdbMiDebugger, self).open(**kwargs)

        if (self._interface is None):
            self._interface = _GdbMiConsole()

            if ('filePath' in kwargs):
                self.sendCommand('-file-exec-and-symbols', abspath(kwargs['filePath']).replace('\\', '/'))
            # end if

            if ('symbolPath' in kwargs):
                self.sendCommand('-file-symbol-file', abspath(kwargs['symbolPath']).replace('\\', '/'))
            # end if

            # [localhost]:port
            # remotehost:port
            if (self._connectionPort is not None):
                connection = ':%s' % (self._connectionPort,)

                if (self._connectionHost is not None):
                    connection = '%s:%s' % (self._connectionHost, self._connectionPort)
                # end if

                self.sendCommand('target extended-remote', connection)
            # end if

            # Cache for breakpoints
            self.addressCache = self.AddressCache(self)

            # Initialize registers
            self.sendCommand('-data-list-register-names')
            # '$' is mandatory to avoid confusion with variable names
            self._regNames = tuple(['$pc', '$sp', '$fp', '$ps']
                                  +['$' + reg for reg in self._response.result.results['register-names']])
        # end if

        self._openCount += 1
    # end def open

    def close(self):
        '''
        @copydoc pylibrary.system.debugger.Debugger.close
        '''
        super(GdbMiDebugger, self).close()

        if (self._openCount == 1):
            # [localhost]:port
            # remotehost:port
            if (self._connectionPort is not None):
                self.sendCommand('disconnect')
            # end if

            self.sendCommand('-gdb-exit')
            self._interface = None
        # end if

        self._openCount -= 1
    # end def close

    def __str__(self):
        '''
        @copydoc pylibrary.system.debugger.Debugger.__str__
        '''
        return self._NAME
    # end def __str__


    _RE_VERSION = re.compile(r'\(.+?\)')

    def getVersion(self):
        '''
        @copydoc pylibrary.system.debugger.Debugger.getVersion
        '''
        self.sendCommand('-gdb-version')
        # -> -gdb-version
        # <- ~"GNU gdb ...
        # <- ~"...
        # <- ~"<http://www.gnu.org/software/gdb/bugs/>.\n"
        version = self._response.filterByRecord(GdbMiStreamConsoleRecord)[0].output_class

        # GNU gdb (GDB) 7.5.50.20120815-cvs (cygwin-special)
        # GNU gdb (Ubuntu/Linaro 7.3-0ubuntu2) 7.3-2011.08
        # GNU gdb 6.3.50-20050815 (Apple version gdb-1824) (Wed Feb  6 22:51:23 UTC 2013)
        return self._RE_VERSION.sub(lambda mo: '', version[8:]).strip()
    # end def getVersion

    # --------------------------------------------------------------------------
    # RUNNING
    # --------------------------------------------------------------------------

    def reset(self, **kwargs):
        '''
        @copydoc pylibrary.system.debugger.Debugger.reset
        '''
        # Set breakpoint on startup code
        for name in ('_start', 'main'):
            try:
                bkpt = self.addBreakpoint(str(name))
                break

            except GdbMiException:
                pass
            # end try
        else:
            raise GdbMiException('No reset symbol found')
        # end for

        # Reset program
        self._runningTime = time()
        self.sendCommand('-exec-run')
        pc = self.waitForStop()

        # Remove breakpoint
        self.removeBreakpoint(bkpt)

        return pc
    # end def reset

    def isRunning(self):
        '''
        @copydoc pylibrary.system.debugger.Debugger.isRunning
        '''
        return (self._suspendCount <= 0)
    # end def isRunning

    def stop(self):
        '''
        @copydoc pylibrary.system.debugger.Debugger.stop
        '''
        self._suspendCount = 1
        return self.getPc()
    # end def stop

    _RUN_CREDIT = 10000

    def run(self, addressOrLabel = None):
        '''
        @copydoc pylibrary.system.debugger.Debugger.run
        '''
        if (addressOrLabel is not None):
            self.setPc(addressOrLabel)
        # end if

        # Basic solution should be to send '-exec-continue' command
        # but while target is running, gdb/mi interface is blocked

        # Current implementation 'step' with a credit of steps
        self._runningTime = time()
        self.sendCommand('step', self._RUN_CREDIT)
        # - Case #1: no more credit --> stopped
        # - Case #1: breakpoint-hit --> stopped
        # --> waitForStop()
    # end def run

    def waitForStop(self, timeout = None):
        '''
        @copydoc pylibrary.system.debugger.Debugger.waitForStop
        '''
        while ((time() - self._runningTime) < self.getTimeOut()):                                                                                            # pylint:disable=C8101

            pc = self.getPc()

            for breakpoint in iter(list(self._breakpoints.values())):
                if (pc == breakpoint.address):
                    if (breakpoint.conditionFunction(self)):

                        # Clear transient breakpoints
                        # Obtain the list of transient breakpoints
                        transientBreakpoints = (bp for bp in iter(list(self._breakpoints.values())) if bp.isTransient())

                        # Remove them
                        for transientBreakpoint in transientBreakpoints:
                            self.removeBreakpoint(transientBreakpoint.getId())
                        # end for

                        self._suspendCount = 1
                        return pc
                    # end if
                # end if
            # end for

            # Resume
            self.sendCommand('continue')  #[CHX]SER: Speed Up test startup (step 1000 too slow)

        # end while

        raise IOError('The debugger was still running when time out expired')

    # end def waitForStop

    # ------------------------------------------------------------------------
    # F_RUNFUNCTION
    # ------------------------------------------------------------------------
    _RE_SYMBOL_NAME   = re.compile(r'Symbol (\w+)')
    _RE_SYMBOL_LENGTH = re.compile(r', length (\w+)')

    def runFunction(self, addressOrLabel,                                                                               # pylint:disable=R0912,R0914
                          variables = None,
                          output    = None):
        '''
        @copydoc pylibrary.system.debugger.Debugger.runFunction
        '''
        label = self.getLabels(self.getAddress(addressOrLabel))[0]

        # Analyze of the function to check its parameters
        self.sendCommand('info scope', label)

        # -> info scope *0xYYYYYY
        # <- &"info scope *0xYYYYYY"
        # <- ~"Scope for *0xYYYYYY:"
        # <- ~"Symbol x is a variable at frame base reg $esp offset 4+0, length 4."

        # GNU gdb (GDB) 7.6.50.20130728-cvs (cygwin-special)
        # -> info scope hello
        # <- Scope for hello:
        # <- Symbol x is a complex DWARF expression:
        # <- 0: DW_OP_fbreg 0
        # <- , length 4.
        # <- Symbol y is a complex DWARF expression:
        # <- 0: DW_OP_fbreg 4
        # <- , length 4.

        symbols = list()

        name   = None
        length = None

        for record in self._response.filterByRecord(GdbMiStreamConsoleRecord):

            mo = self._RE_SYMBOL_NAME.match(record.output_class)
            if (mo is not None):
                name = mo.group(1)
            # end if

            mo = self._RE_SYMBOL_LENGTH.search(record.output_class)
            if (mo is not None):
                length = int(mo.group(1), 16)
            # end if

            if ((name is not None) and (length is not None)):
                symbols.append((name, length))
                name   = None
                length = None
            # end if

        # end for

        # List of parameters for the function
        params = []
        if (variables is not None):
            for varName, varValue, varLength in variables:
                if (varName in self._regNames):
                    self.setRegister(varName, varValue)
                else:
                    params.append((varName, varValue, varLength))
                # end if
            # end for
        # end if

        # Check and ordering of the parameters
        args = list()
        for paramName, paramValue, paramLength in params:

            # C implementation: check symbols
            for (symbolName, symbolLength) in symbols:

                if (symbolName != paramName):
                    continue
                # end if

                if (symbolLength != paramLength):
                    raise ValueError('Wrong parameter length: %d (expected: %d).'
                                     % (paramLength, symbolLength))
                # end if

                break
            # end for

            args.append(str(paramValue))
        # end for

        # Function evaluation
        cmdargs = [label]
        if args:
            cmdargs.append('(%s)' % (','.join(args),))    #[CHX] extend does not work (replace by append)
        else:
            cmdargs.append('()') #[CHX] if not void parameter, provide "()" to GDB
        # end if

        try:
            pc = self.getPc()
            self.sendCommand('call', *cmdargs)

        except GdbMiException:
            # Break in function
            # - conditionFunction returns
            #   - True  --> break
            #   - False --> continue until end of function
            bkp = self.addBreakpoint(pc)
            self.waitForStop()
            self.removeBreakpoint(bkp)

            # exit with pc as result
            return {'$pc': self.getPc()}
        # end try

        # void set(value)
        # -> call  set (x)
        # <- &"call set (x)\n"
        # <- ^done
        returnValue = None

        # int add(op1, op2)
        # -> call  add (x,y)
        # <- &"call add (x,y)\n"
        # <- ~"$2 = z"
        # <- ~"\n"
        # <- ^done

        # int add(op1, op2)
        # -> call  add (x,y)
        # <- &"call add (x,y)\n"
        # <- ~"$2 = z"
        # <- ~"\n"
        # <- ^done

        # const char * Hello(void)
        # -> call Hello()
        # <- &"call Hello ()\n"
        # <- ~"$2 = 0x4031f4 \"Hello world!\""
        # <- ~"\n"
        # <- ^done

        for record in self._response.filterByRecord(GdbMiStreamConsoleRecord):
            if (record.output_class.startswith('$')):
                returnValue = record.output_class.split()[2]
                if not 'void' in returnValue:
                    returnValue = int(returnValue)
                else:
                    returnValue = None
                # end if
                break
            # end if
        # end for

        # Get output values
        results = dict()

        if (output is not None):
            for outName, outValue, outLength in output:

                if (outName in self._regNames):
                    results[outName] = self.getRegister(outName)

                elif (outName.startswith('$')):
                    results[outName] = returnValue

                else:
                    results.update(self.readVariables(((outName, outValue, outLength),)))
                # end if
            # end for
        # end if

        return results
    # end def runFunction

    # --------------------------------------------------------------------------
    # F_BREAKPOINTS
    # --------------------------------------------------------------------------


    # --------------------------------------------------------------------------
    # F_READWRITE
    # --------------------------------------------------------------------------
    def saveMemoryFile(self, addressOrLabel,
                             length,
                             memoryFilePath,
                             format     = Debugger.FORMAT_AUTO,                                                         #@ReservedAssignment pylint:disable=W0622
                             mode       = 'w+',
                             memoryType = None):
        '''
        @copydoc pylibrary.system.debugger.Debugger.saveMemoryFile
        '''


        if (format == self.FORMAT_AUTO):
            ext = splitext(memoryFilePath)[1].lower()

            if (ext in ('.s19', '.s28', '.s37')):
                format = 'srec'                                                                                         #@ReservedAssignment

            elif (ext in ('.HEX',)):
                format = 'ihex'                                                                                         #@ReservedAssignment

            else:
                raise ValueError('Cannot guess file format: %s' % (ext,))
            # end if

        elif (format == self.FORMAT_SRECORD):
            format = 'srec'                                                                                             #@ReservedAssignment

        elif (format == self.FORMAT_HEX):
            format = 'ihex'                                                                                             #@ReservedAssignment

        elif (format == self.FORMAT_BIN):
            format = 'binary'                                                                                           #@ReservedAssignment

        else:
            raise GdbMiException('Format not supported: %d' % (format,))

        # end if

        self.sendCommand('dump',
                         format,
                         'memory',
                         memoryFilePath.replace('\\', '/'),
                         '0x%X' % (self.getAddress(addressOrLabel)),
                         '0x%X' % (self.getAddress(addressOrLabel) + length))
    # end def saveMemoryFile

    def loadMemoryFile(self, memoryFilePath,
                             format     = Debugger.FORMAT_AUTO,                                                         # @ReservedAssignment # pylint:disable=W0622
                             memoryType = None):
        '''
        @copydoc pylibrary.system.debugger.Debugger.loadMemoryFile
        '''

        if (format == self.FORMAT_AUTO):
            ext = splitext(memoryFilePath)[1].lower()

            if (ext not in ('.s19', '.s28', '.s37', '.hex')):
                raise ValueError('Cannot guess file format: %s' % (ext,))
            # end if

        elif (format not in (self.FORMAT_SRECORD, self.FORMAT_HEX, self.FORMAT_BIN)):
            raise GdbMiException('Format not supported: %d' % (format,))

        # end if

        self.sendCommand('restore',
                         memoryFilePath.replace('\\', '/'),
                         'binary' if format == self.FORMAT_BIN else '')
    # end def loadMemoryFile


    def readMemory(self, addressOrLabel,
                         length,
                         memoryType = None):
        '''
        @copydoc pylibrary.system.debugger.Debugger.readMemory
        '''
        if (isinstance(addressOrLabel, str)):
            address = '&' + addressOrLabel
        else:
            address = '0x%X' % (addressOrLabel,)
        # end if

        self.sendCommand('-data-read-memory-bytes', address, length)
        # -> -data-read-memory-bytes 0xYYYYYYYY 3
        # <- ^done,memory=[{begin="0xYYYYYYYY",offset="0x00000000",end="0xYYYYYYZB",contents="ZZZZZZ"}]
        return HexList(self._response.result.results['memory'][0]['contents'])
    # end def readMemory

    def writeMemory(self, addressOrLabel,
                          data,
                          memoryType = None):
        '''
        @copydoc pylibrary.system.debugger.Debugger.writeMemory
        '''
        if (isinstance(addressOrLabel, str)):
            address = '&' + addressOrLabel
        else:
            address = '0x%X' % (addressOrLabel,)
        # end if

        if isinstance(data, int):
            contents = '%X' % (data,)
            if ((len(contents)% 2) != 0):
                contents = '0' + contents
            # end if
        else:
            contents = data
        # end if

        self.sendCommand('-data-write-memory-bytes', address, contents)
        # -> -data-write-memory-bytes 0xYYYYYYYY ZZZZZZ
        # <- ^done
    # end def writeMemory

    def fillMemory(self, addressOrLabel,
                         length,
                         value,
                         memoryType = None):
        '''
        @copydoc pylibrary.system.debugger.Debugger.fillMemory
        '''
        if isinstance(value, int):
            value = HexList(value)
        elif isinstance(value, str):
            value = HexList.fromString(value)
        # end if

        self.writeMemory(addressOrLabel, value * length)
    # end def fillMemory

    def getPc(self):
        '''
        @copydoc pylibrary.system.debugger.Debugger.getPc
        '''
        return self.getRegister('$pc')
    # end def getPc

    def setPc(self, addressOrLabel):
        '''
        @copydoc pylibrary.system.debugger.Debugger.setPc
        '''
        self.setRegister('$pc', self.getAddress(addressOrLabel))
    # end def setPc

    def getRegister(self, register):
        '''
        @copydoc pylibrary.system.debugger.Debugger.getRegister
        '''
        if (register not in self._regNames):
            raise GdbMiException('Unreferenced register: %s' % (register,))
        # end if

        self.sendCommand('p/x', register)
        # -> p/x $pc
        # <- &"p/x $pc\n"
        # <- ~"$1 = 0x100000e70\n"
        # <- ^done
        return int(self._response.filterByRecord(GdbMiStreamConsoleRecord)[-1].output_class.split('=')[-1].strip(), 16)
    # end def getRegister

    def setRegister(self, register, value):
        '''
        @copydoc pylibrary.system.debugger.Debugger.setRegister
        '''
        if (register not in self._regNames):
            raise GdbMiException('Unreferenced register: %s' % (register,))
        # end if

        if isinstance(value, int):
            value = '0x%X' % (value,)
        # end if

        self.sendCommand('set', '%s = %s' % (register, value))
        # -> set $reg=0xYYYY
        # <- &"set $reg=0xYYYY\n"
        # <- ^done

    # end def setRegister

    def getRegisters(self, registersList):
        '''
        @copydoc pylibrary.system.debugger.Debugger.getRegisters
        '''
        registers  = dict()

        for name in registersList:
            registers[name] = self.getRegister(name)
        # end for

        return registers
    # end def getRegisters

    def setRegisters(self, registersDict):
        '''
        @copydoc pylibrary.system.debugger.Debugger.setRegisters
        '''
        for key, value in registersDict.items():
            self.setRegister(key, value)
        # end for
    # end def setRegisters

    # --------------------------------------------------------------------------
    # F_STEPPING
    # --------------------------------------------------------------------------

    def stepInto(self, conditionFunction = alwaysTrigger,
                       mode              = Debugger.STEP_INSTRUCTION):
        '''
        @copydoc pylibrary.system.debugger.Debugger.stepInto
        '''
        while True:
            self.sendCommand('-exec-step-instruction' if mode == Debugger.STEP_INSTRUCTION
                             else '-exec-step')
            pc = self.getPc()

            if conditionFunction(self):
                break
            # end if
        # end while

        return pc
    # end def stepInto

    def stepOver(self, conditionFunction = alwaysTrigger,
                       mode              = Debugger.STEP_INSTRUCTION):
        '''
        @copydoc pylibrary.system.debugger.Debugger.stepOver
        '''
        while True:
            self.sendCommand('-exec-next-instruction' if mode == Debugger.STEP_INSTRUCTION
                             else '-exec-next')
            pc = self.getPc()

            if conditionFunction(self):
                break
            # end if
        # end while

        return pc
    # end def stepOver

    def stepOut(self, conditionFunction = alwaysTrigger):
        '''
        @copydoc pylibrary.system.debugger.Debugger.stepOut
        '''
        while True:
            self.sendCommand('-exec-finish')
            pc = self.getPc()

            if conditionFunction(self):
                break
            # end if
        # end while

        return pc
    # end def stepOut

    # --------------------------------------------------------------------------
    # F_BREAKPOINTS
    # --------------------------------------------------------------------------

# end class GdbMiDebugger


# ------------------------------------------------------------------------------
# GDB/MI Record
# ------------------------------------------------------------------------------

class GdbMiOutputRecord(object):
    '''
    Class built from gdb/mi response
    '''
    _TYPE = None

    _RE_KEY_VALUE = re.compile(r'([-a-zA-Z0-9_]+)=(["[{])') #[CHX]SER: = signs changed in : only if followed by [,{,"
    _RE_KEY_BKPT  = re.compile(r'bkpt={number="(\d+)"')

    def __init__(self, output_class, results = None):
        '''
        Constructor

        @param  output_class [in] (str) output or result-class
        @option results      [in] (str) ( "," result )* nl
        '''
        self.output_class = output_class
        self.results      = None

        if (results is not None):

            # -break-list   --> BreakpointTable={bkpt={number="x",...},bkpt={number="y",...}}
            #               --> BreakpointTable={bkpt-x={number="x",...},bkpt-y={number="y",...}
            if ('BreakpointTable' in results):
                results = self._RE_KEY_BKPT.sub(lambda mo: 'bkpt-%s={number="%s"' % (mo.group(1), mo.group(1)), results)
            # end if

            # key=value     --> 'key':value
            results = self._RE_KEY_VALUE.sub(lambda mo: '"%s":%s' % (mo.group(1),mo.group(2)), results)  #[CHX]SER: = signs changed in : only if followed by [,{,"
            try:
                self.results = eval('{%s}' % (results,))
            except:                                                                                                     # pylint:disable=W0702
                # gdb syntax error: key={...},{...} --> key=[{...},{...}]
                self.results = eval('{%s:[%s]}' % (results[:results.index(':')],
                                                   results[results.index(':')+1:]))
            # end try
        # end if
    # end def __init__

    def __repr__(self):
        '''
        Representation of self

        @return (str) representation
        '''
        return 'output_class: %s\nresults     : %s' % (self.output_class, self.results)
    # end def __repr__

    @classmethod
    def accept(cls, response):
        '''
        Test reponse type

        @param  response [in] (str) gdb/mi syntax

        @return (bool)
        '''
        return response[0] == cls._TYPE
    # end def accept

    @classmethod
    def parse(cls, response):
        '''
        Parse reponse and create record

        @param  response [in] (str) returned by gdb

        @return (GdbMiOutputRecord) Interpreted response record
        '''
        items   = response[1:].split(',', 1)
        result  = items[0]
        results = items[1] if len(items) > 1 else None

        return cls(result, results)
    # end def parse

# end class GdbMiOutputRecord

class GdbMiResultRecord(GdbMiOutputRecord):
    '''
    gdb/mi Result Records
    '''

    ##@name Result
    #
    # In addition to a number of out-of-band notifications, the response to a gdb/mi command
    # includes one of the following result indications.
    ##@{
    DONE        = 'done'        ##< "^done" [ "," results ]
                                ##  The synchronous operation was successful, results are the return values.
    RUNNING     = 'running'     ##< "^running"
                                ##  This result record is equivalent to "^done".
                                ##  Historically, it was output instead of "^done" if the command has resumed the target.
                                ##  This behaviour is maintained for backward compatibility,
                                ##  but all frontends should treat "^done" and "^running" identically
                                ##  and rely on the "*running" output record to determine
    CONNECTED   = 'connected'   ##< "^connected"
                                ##  gdb has connected to a remote target.
    ERROR       = 'error'       ##< "^error" "," c-string
                                ##  The operation failed. The c-string contains the corresponding error message.
    EXIT        = 'exit'        ##< "^exit" gdb has terminated.
    ##@}

    _TYPE = '^'


# end class GdbMiResultRecord

class GdbMiStreamRecord(GdbMiOutputRecord):
    '''
    gdb/mi Stream Records

    gdb internally maintains a number of output streams: the console, the target, and the log.
    The output intended for each of these streams is funneled through the gdb/mi interface
    using stream records.

    Each stream record begins with a unique prefix character which identifies its stream.
    In addition to the prefix, each stream record contains a string-output.
    '''

    @classmethod
    def parse(cls, response):
        '''
        @copydoc pylibrary.system.gdbmidebugger.GdbMiOutputRecord.parse
        '''
        return cls(response[2:-1].replace('\\"', '"').replace('\\n', '\n').strip())
    # end def parse
# end class GdbMiStreamRecord

class GdbMiStreamConsoleRecord(GdbMiStreamRecord):
    '''
    "~" string-output

    The console output stream contains text that should be displayed in the CLI
    console window. It contains the textual responses to CLI commands.
    '''
    _TYPE = '~'
# end class GdbMiStreamConsoleRecord

class GdbMiStreamTargetRecord(GdbMiStreamRecord):
    '''
    "@" string-output

    The target output stream contains any textual output from the running target.
    This is only present when GDB's event loop is truly asynchronous, which is
    currently only the case for remote targets.
    '''
    _TYPE = '@'
# end class GdbMiStreamTargetRecord

class GdbMiStreamLogRecord(GdbMiStreamRecord):
    '''
    "&" string-output

    The log stream contains debugging messages being produced by gdb's internals.
    '''
    _TYPE = '&'
# end class GdbMiStreamLogRecord


class GdbMiAsyncExecRecord(GdbMiOutputRecord):
    '''
    Target execution
    '''
    _TYPE = '*'
# end class GdbMiAsyncExecRecord

class GdbMiAsyncStatusRecord(GdbMiOutputRecord):
    '''
    Target status
    '''
    _TYPE = '+'
# end class GdbMiAsyncStatusRecord

class GdbMiAsyncNotifyRecord(GdbMiOutputRecord):
    '''
    Target changes
    '''
    _TYPE = '='
# end class GdbMiAsyncNotifyRecord

class GdbMiResponse(object):
    '''
    Contains all records in response of a command
    '''
    def __init__(self, records):
        '''
        Constructor

        @param  records [in] (list) of records
        '''
        self._records = records
        self._result  = self.filterByRecord(GdbMiResultRecord)[-1]
    # end def __init__

    result = property(lambda self: self._result)                                                                        # pylint:disable=W0212

    def filterByRecord(self, name, result = None):
        '''
        Get list of dedicated records

        @param  name   [in] (str)   class name
        @param  result [in] (tuple) (key, value)

        @return (list) of records
        '''
        records = list()

        for record in self._records:
            if (not isinstance(record, name)):
                continue
            # end if

            if (result is not None):
                key, value = result                                                                                     # pylint:disable=W0633
                if (key not in record.results):
                    continue
                # end if

                if (value != record.results[key]):
                    continue
                # end if
            # end if

            records.append(record)
        # end for
        return records
    # end def filterByRecord

# end class GdbMiResponse


class _GdbMiConsole(object):
    '''
    A GDB/MI console
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._debug   = False
        self._process = None

        try:
            self._process = Popen([GDB, '-i', 'mi'],
                                  stdin     = PIPE,
                                  stdout    = PIPE,
                                  stderr    = STDOUT)
        except Exception as err:
            raise GdbMiException(err)
        # end try

        self._receive()
        # <- =thread-group-added,id="i1"
        # <- ~"GNU gdb ...
    # end def __init__


    def __del__(self):
        '''
        Destructor
        '''
        if (self._process is not None):
            self._send('gdb-exit')
            self._process = None
        # end if
    # end def __del__

    def _send(self, command):
        '''
        Send a command

        @param  command [in] (str) gdb/mi command
        '''
        if (command[0] != '-' ):
            command = '-interpreter-exec mi "%s"' % (command,)
        # end if

        if (self._debug):
            print(('-> ' + command))
        # end if

        self._process.stdin.write('%s\n' % (command,))                                                                  # pylint:disable=E1101
    # end def _send

    def _receive(self):
        '''
        Receive responses

        @return (list) of responses
        '''
        responses = list()
        while (True):
            response = self._process.stdout.readline().rstrip()                                                        # pylint:disable=E1101

            if (self._debug):
                print(('<- ' + response))
            # end if

            if (response == '(gdb)'):
                break
            # end if

            responses.append(response)
        # end while

        return responses
    # end def _receive

    _GDB_MI_RECORDS = (GdbMiResultRecord,
                       GdbMiStreamConsoleRecord,
                       GdbMiStreamTargetRecord,
                       GdbMiStreamLogRecord,
                       GdbMiAsyncExecRecord,
                       GdbMiAsyncStatusRecord,
                       GdbMiAsyncNotifyRecord,
                       )
    # GDB/MI exchanges are asynchronous
    # Results are not always received in response of a command
    # Ex: ReadRegister
    #   _send    -> -data-list-register-values r X
    # - one response
    #   _receive <- ^done,register-values=[{number="X",value="0xYYYYYYYY"}]
    #            <- (gdb)
    # - two responses needed
    #   _receive <-  ^done
    #            <- (gdb)
    #   _receive <- ^done,register-values=[{number="X",value="0xYYYYYYYY"}]
    #            <- (gdb)

    # Result
    _REC_RESULT         = 0x0001 # ^result
    _REC_RESULT_DONE    = 0x0002 # ^done
    _REC_RESULT_RESULTS = 0x0006 # ^done,results
    # Async
    _REC_EXEC           = 0x0010 # *status
    # Stream
    _REC_CONSOLE        = 0x0100 # ~output
    _REC_TARGET         = 0x0200 # @output
    _REC_LOG            = 0x0400 # &output

    _EXPECTED_RECS      = {# by command                : _REC_XX | _REC_YY
                           '-break-list'               : _REC_RESULT_RESULTS,
                           '-break-insert'             : _REC_RESULT_RESULTS,
                           '-break-enable'             : _REC_RESULT,
                           '-break-disable'            : _REC_RESULT,
                           '-break-delete'             : _REC_RESULT,
                           #
                           '-data-list-register-names' : _REC_RESULT_RESULTS,
                           '-data-list-register-values': _REC_RESULT_RESULTS,
                           '-data-read-memory-bytes'   : _REC_RESULT_RESULTS,
                           '-data-write-memory-bytes'  : _REC_RESULT,
                           #
                           '-exec-run'                 : _REC_EXEC,
                           '-exec-finish'              : _REC_EXEC,
                           #
                           '-file-exec-and-symbols'    : _REC_RESULT,
                           '-file-symbol-file'         : _REC_RESULT,
                           #
                           '-gdb-version'              : _REC_CONSOLE,
                           #
                           'break'                     : _REC_LOG | _REC_CONSOLE,
                           'call'                      : _REC_LOG | _REC_CONSOLE,
                           'clear'                     : _REC_LOG | _REC_CONSOLE,
                           'disconnect'                : _REC_LOG | _REC_CONSOLE,
                           'dump'                      : _REC_LOG,
                           'info'                      : _REC_LOG | _REC_CONSOLE,
                           'p/x'                       : _REC_LOG | _REC_CONSOLE,
                           'restore'                   : _REC_LOG | _REC_CONSOLE,
                           'set'                       : _REC_RESULT,
                           'step'                      : _REC_LOG | _REC_CONSOLE,
                           'target'                    : _REC_LOG | _REC_CONSOLE,
                           }


    def sendAndReceive(self, command):                                                                                  # pylint:disable=R0912
        '''
        Send a command and receive responses

        @param  command [in] (str) gdb/mi command

        @return (GdbMiResponse)
        '''
        self._send(command)

        if (command.startswith('-gdb-exit')):
            return GdbMiResponse([GdbMiResultRecord.parse('^exit'),])
        # end if

        command  = command.split()[0]
        records  = list()

        received = 0
        expected = 0

        while (True):

            for response in self._receive():
                for gdbMiRecord in self._GDB_MI_RECORDS:

                    if (not gdbMiRecord.accept(response)):
                        continue
                    # end if

                    record = gdbMiRecord.parse(response)

                    if   (isinstance(record, GdbMiStreamConsoleRecord)):
                        received |= self._REC_CONSOLE

                    elif (isinstance(record, GdbMiStreamTargetRecord)):
                        received |= self._REC_TARGET

                    elif (isinstance(record, GdbMiStreamLogRecord)):
                        received |= self._REC_LOG

                    elif (isinstance(record, GdbMiAsyncExecRecord)):
                        received |= self._REC_EXEC

                    elif (isinstance(record, GdbMiResultRecord)):

                        # Filter second result
                        # <- ^error,msg="..."
                        # <- ^done
                        if (received & self._REC_RESULT):
                            continue
                        # end if

                        received |= self._REC_RESULT
                        received |= self._REC_RESULT_DONE    if response.startswith('^done')  else 0
                        received |= self._REC_RESULT_RESULTS if response.startswith('^done,') else 0
                    # end if

                    records.append(record)
                    break
                # end for
            # end for

            if ((received & self._REC_RESULT) != self._REC_RESULT):
                # receive next reponses
                continue
            # end if

            if ((received & self._REC_RESULT_DONE) != self._REC_RESULT_DONE):
                # ^running, ^connected, ^error, ^exit
                break
            # end if

            if (command not in self._EXPECTED_RECS):
                from warnings import warn
                warn('GdbMIDebbugger: command %s not checked' %(command,))
                received = self._REC_RESULT
            else:
                expected = self._EXPECTED_RECS[command]
            # end if

            if ((received & expected) != expected):
                received &= self._REC_RESULT_DONE
                continue
            # end if

            break
        # end while

        return GdbMiResponse(records)
    # end def sendAndReceive

# end class _GdbMiConsole

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
