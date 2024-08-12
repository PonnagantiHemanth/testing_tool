#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pyharness.debugger

@brief  DebuggerTestCase implementation

@author christophe.roquebert

@date   2018/06/05
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.system.debugger         import Debugger
from pylibrary.system.debugger         import DebuggerProvider
from pylibrary.system.debugger         import alwaysTrigger
from pylibrary.tools.hexlist            import HexList
from datetime                           import datetime
from pyharness.context                   import ContextLoader
from pyharness.core                      import TestListener
from pyharness.core                      import _LEVEL_ERROR
from pyharness.core                      import _LEVEL_SEPARATOR
from pyharness.core                      import _LEVEL_TRACE
from pyharness.core                      import _MASK_ALWAYS
from pyharness.extensions                import PyHarnessCase
from os                                 import F_OK
from os                                 import access
from os                                 import makedirs
from os.path                            import join
from time                               import time

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class ContextDebugger(object):
    """
    Implements the debugger interface, with additional test-dependent logging
    functions.
    """
    def __init__(self, next, logger):                                                                                   #@ReservedAssignment pylint:disable=W0622
        """
        Constructor

        @param  next   [in] (Debugger) The debugger to decorate
        @param  logger [in] (Logger) Handler of instance that logs data
        """
        self.next = next
        self._logger = logger
    # end def __init__

    def __getattr__(self, name):
        """
        Return attributes of ContextDebugger

        @param  name [in] (str) Key of the attribute to return

        @return Attribute[name] of ContextDebugger
        """
        return getattr(self.next, name)
    # end def __getattr__

    def __str__(self):
        """
        Converts the current object to a string.

        @return (str) The current object, as a string
        """
        return str(self.__next__)
    # end def __str__

    def __setattr__(self, name, value):
        """
        Fixes attributes of ContextDebugger

        @param name  [in] (str) Name Key of ContextDebugger
        @param value [in] (object) Name value
        """
        if (name in ("next", "test")):
            self.__dict__[name] = value
        else:
            setattr(self.next, name, value)
        # end if
    # end def __setattr__

    @staticmethod
    def __formatBlock(startOffset, data, align=16):
        """
        Formats a block of hex data to a string

        @param  startOffset [in] (int)    The address of the first data byte
        @param  data        [in] (HexList) The data to format
        @option align       [in] (int)    The multiple the addresses are aligned on

        @return A string, containing the formatted block
        """

        # Prepare the data so that it is displayed in blocks of 16 bytes, with
        # the address in the the first column
        lines = []
        for index in range(int(startOffset / align) * align, startOffset+len(data), align):
            if (index < startOffset):
                padding = '.. ' * (startOffset - index)
                offset = 0
                length = align - (startOffset - index)
            else:
                padding = ''
                offset = index - startOffset
                length = align
            # end if
            value = data[offset:offset+length]
            line = "0x%08.8X: %s%s" % (index, padding, ' '.join(["%02X" % x for x in value]))
            lines.append(line)
        # end for

        return '\n'.join(lines)
    # end def __formatBlock

    # ------------------------------------------------------------------------
    # F_RUNNING
    # ------------------------------------------------------------------------

    def reset(self, **kwargs):
        """
        @copydoc pylibrary.system.debugger.Debugger.reset
        """
        self._logger.logTrace("Resetting debugger")
        pc = self.next.reset(**kwargs)
        self._logger.logTrace("PC: 0x%08.8X" % (pc,))
        return pc
    # end def reset

    def run(self, **kwargs):
        """
        @copydoc pylibrary.system.debugger.Debugger.run
        """
        self.next.run(**kwargs)
    # end def run

    def stop(self):
        """
        @copydoc pylibrary.system.debugger.Debugger.stop
        """
        self._logger.logTrace("Stopping debugger")
        pc = self.next.stop()
        self._logger.logTrace("PC: 0x%08.8X" % (pc,))
        return pc
    # end def stop

    def waitForStop(self, timeout = None):
        """
        @copydoc pylibrary.system.debugger.Debugger.waitForStop
        """
        self._logger.logDebug("Waiting for stop: timeout %s" % (timeout,))
        pc = self.next.waitForStop(timeout)
        self._logger.logDebug("PC: 0x%08.8X" % (pc,))
        return pc
    # end def waitForStop

    # ------------------------------------------------------------------------
    # F_CYCLES
    # ------------------------------------------------------------------------

    def getCycles(self):
        """
        @copydoc pylibrary.system.debugger.Debugger.getPc
        """
        cycles = self.next.getCycles()
        self._logger.logDebug("Getting Cycles count: %d" % (cycles,))
        return cycles
    # end def getCycles

    # ------------------------------------------------------------------------
    # F_READWRITE
    # ------------------------------------------------------------------------

    def getPc(self):
        """
        @copydoc pylibrary.system.debugger.Debugger.getPc
        """
        pc = self.next.getPc()
        self._logger.logDebug("Getting PC: 0x%08.8X" % (pc,))
        return pc
    # end def getPc

    def setPc(self, addressOrLabel):
        """
        @copydoc pylibrary.system.debugger.Debugger.setPc
        """
        addrName  = str(addressOrLabel)
        addrValue = self.next.getAddress(addressOrLabel)
        self._logger.logTrace("Setting PC at %s (0x%08.8X)" %
                             (addrName, addrValue))
        self.next.setPc(addressOrLabel)
    # end def setPc

    def getRegister(self, register):
        """
        @copydoc pylibrary.system.debugger.Debugger.getRegister
        """
        value = self.next.getRegister(register)
        self._logger.logDebug("Getting register %-5s: 0x%08.8X" %
                             (register, value))
        return value
    # end def getRegister

    def setRegister(self, register,
                          value):
        """
        @copydoc pylibrary.system.debugger.Debugger.setRegister
        """
        self._logger.logTrace("Setting register %-5s: 0x%08.8X" %
                             (register, value))
        self.next.setRegister(register, value)
    # end def setRegister

    def getRegisters(self, registersList):
        """
        @copydoc pylibrary.system.debugger.Debugger.getRegisters
        """
        self._logger.logDebug("Getting registers:")
        registers = self.next.getRegisters(registersList)
        for register, value in registers.items():
            self._logger.logDebug("%-5s: 0x%08.8X" %
                                 (register, value))
        # end for
        return registers
    # end def getRegisters

    def setRegisters(self, registersDict):
        """
        @copydoc pylibrary.system.debugger.Debugger.setRegisters
        """
        self._logger.logTrace("Setting registers:")
        for register, value in registersDict.items():
            self._logger.logTrace("%-5s: 0x%08.8X" %
                                 (register, value))
        # end for
        self.next.setRegisters(registersDict)
    # end def setRegisters

    def readMemory(self, addressOrLabel,
                         length,
                         memoryType = None):
        """
        @copydoc pylibrary.system.debugger.Debugger.readMemory
        """
        addrName  = str(addressOrLabel)
        addrValue = self.next.getAddress(addressOrLabel, memoryType)

        self._logger.logDebug("Reading memory at %s (0x%08.8X):" %
                             (addrName, addrValue))
        data = self.next.readMemory(addressOrLabel, length, memoryType)
        self._logger.logDebug(self.__formatBlock(addrValue, data))

        return data
    # end def readMemory

    def writeMemory(self, addressOrLabel,
                          data,
                          memoryType = None):
        """
        @copydoc pylibrary.system.debugger.Debugger.writeMemory
        """
        addrName  = str(addressOrLabel)
        addrValue = self.next.getAddress(addressOrLabel, memoryType)

        # Type conversions, to prevent later sanity checks

        # data must be of type HexList
        if (not isinstance(data, HexList)):
            data = HexList(data)
        # end if

        dataString = self.__formatBlock(addrValue, data)

        self._logger.logTrace("Writing memory at %s (0x%08.8X): \n%s" % \
                           (  addrName,
                              addrValue,
                              dataString,
                           ))
        response = self.next.writeMemory(addressOrLabel, data, memoryType)

        return response
    # end def writeMemory

    def fillMemory(self, addressOrLabel,
                         length,
                         value,
                         memoryType = None):
        """
        @copydoc pylibrary.system.debugger.Debugger.fillMemory
        """
        # If the address is already an int, don't look it up
        if isinstance(addressOrLabel, int):
            addrName = 'absolute address'
            addrValue = addressOrLabel
        else:
            addrName  = str(addressOrLabel)
            addrValue = self.next.getAddress(addressOrLabel, memoryType)
        # end if

        self._logger.logTrace("Filling memory at %s (0x%08.8X) length 0x%08.8X with 0x%02X" %
                             (addrName, addrValue, length, value))

        self.next.fillMemory(addressOrLabel, length, value, memoryType)
    # end def fillMemory

    # ------------------------------------------------------------------------
    # F_STEPPING
    # ------------------------------------------------------------------------
    def stepInto(self, conditionFunction = alwaysTrigger,
                       mode              = Debugger.STEP_INSTRUCTION):
        """
        @copydoc pylibrary.system.debugger.Debugger.stepInto
        """
        self._logger.logTrace("Stepping into")
        pc = self.next.stepInto(conditionFunction, mode)
        self._logger.logTrace("PC: 0x%08.8X" % (pc,))
        return pc
    # end def stepInto

    def stepOut(self, conditionFunction = alwaysTrigger):
        """
        @copydoc pylibrary.system.debugger.Debugger.stepOut
        """
        self._logger.logTrace("Stepping out")
        pc = self.next.stepOut(conditionFunction)
        self._logger.logTrace("PC: 0x%08.8X" % (pc,))
        return pc
    # end def stepOut

    def stepOver(self, conditionFunction = alwaysTrigger,
                       mode              = Debugger.STEP_INSTRUCTION):
        """
        @copydoc pylibrary.system.debugger.Debugger.stepOver
        """
        self._logger.logTrace("Stepping over")
        pc = self.next.stepOver(conditionFunction, mode)
        self._logger.logTrace("PC: 0x%08.8X" % (pc,))
        return pc
    # end def stepOver

    # ------------------------------------------------------------------------
    # F_RUNFUNCTION
    # ------------------------------------------------------------------------

    def runFunction(self, addressOrLabel,
                          variables = None,
                          output    = None):
        """
        @copydoc pylibrary.system.debugger.Debugger.runFunction
        """
        addrName  = str(addressOrLabel)
        addrValue = self.next.getAddress(addressOrLabel)

        self._logger.logTrace("Running function at %s (0x%08.8X):"
                             % (addrName, addrValue))
        tock = time()
        success = "Call failed (timeout or error)"
        canPerf = False
        cyclesDelta = None
        try:
            canPerf = self.next.getDebuggerInfo(self.next.F_CYCLES)

            # Log performance data
            if (canPerf):
                startCycles = self.next.getCycles()
            # end if

            result  = self.next.runFunction(addressOrLabel, variables, output)
            success = "Call returned"

            # Log performance data
            if (canPerf):
                endCycles = self.next.getCycles()
                cyclesDelta = endCycles - startCycles

                self._logger.addPerformanceData(addrName,
                                                cyclesDelta,
                                                'CPU cycles')
            # end if

        finally:
            tick = time()
            if (canPerf and (cyclesDelta is not None)):
                message = "%s in %.3f s (%d cycles)" % (success, tick - tock, cyclesDelta)
            else:
                message = "%s in %.3f s" % (success, tick - tock)
            # end if
            self._logger.logTrace(message)
        # end try
        return result
    # end def runFunction
# end class ContextDebugger


class DebuggerTestCaseMixin(DebuggerProvider):
    """
    A Mixin that adds getDevice support to an PyHarnessCase instance.

    This is only marginally useful not pure-Device test case classes,
    but it allows implementations to create Device-And-Debugger test case classes
    that do not call the TestCase.setUp and TestCase.tearDown methods twice.
    """
    DEBUGGERS = {}
    COVERAGES = {}

    def tearDown(self):
        """
        Destructor
        """
        for key, debugger in DebuggerTestCaseMixin.DEBUGGERS.items():
            # Activate/deactivate the automatic coverage
            # noinspection PyUnresolvedReferences
            config = self.getContext().getConfig()
            if config.get(ContextLoader.SECTION_CONFIG, ContextLoader.OPTION_COVERAGE) and \
                    debugger.getDebuggerInfo(debugger.F_COVERAGE):

                if debugger.getCoverage():
                    # noinspection PyUnresolvedReferences
                    coverage_dir = join(self.getContext().getOutputDir(), "cov")
                    if not access(coverage_dir, F_OK):
                        makedirs(coverage_dir)
                    # end if

                    # noinspection PyUnresolvedReferences
                    coverage_file_path = join(coverage_dir, self.id())
                    debugger.saveCoverage(coverage_file_path, debugger.FORMAT_NATIVE)
                # end if

                debugger.setCoverage(DebuggerTestCaseMixin.COVERAGES[key])
            # end if

            debugger.close()
        # end for
    # end def tearDown

    def get_dbg(self, index_or_predicate=0, keep_for_test_duration=True, **kwargs):
        """
        @copydoc pylibrary.system.debugger.DebuggerProvider.get_dbg

        In a mono-threaded environment, the parameter @c keep_for_test_duration
        has no effect, as the Debugger instance is only accessed by the
        testing thread.

        In a multithreaded environment, however, it may be necessary to reserve
        access to a Debugger for the whole duration of the test, throughout
        setUp(), test() and tearDown() methods.

        It is therefore advised (even in a mono-threaded context), to reserve
        access to the Debugger by performing a call to @c get_dbg with the
        @c keep_for_test_duration parameter set to True in the setUp() method.

        API Workflow:
        @dot
        digraph G
        {
            node    [fontname=Arial, fontsize = 10, align=center, shape=diamond, width=1.0];
            edge    [fontname=Arial, fontsize = 8, len=0.5];
            ranksep = 0.1;
            rankdir = TB;

            {
                rankdir = LR;
                rank    = same;

                INITIALIZATION [label="Initialization", shape=box];
            }

            {
                rankdir = LR;
                rank    = same;

                KEYINCACHE       [label="Key in cache", shape=diamond];
            }

            {
                rankdir = LR;
                rank    = same;

                RETRIEVEFROMCACHE   [label="Retrieve from\ncache", shape=box];
                RETRIEVEFROMCONTEXT [label="Retrieve from\ncontext", shape=box];
            }

            {
                rankdir = LR;
                rank    = same;

                KEEPFORTESTDURATION      [label="keep for test\nduration ?", shape=diamond];
                KEEPFORTESTDURATIONPOINT [shape=point, width=0.0];
            }

            {
                rankdir = LR;
                rank    = same;

                ADDTOCACHE               [label="Add to cache", shape=box];
            }

            {
                rankdir = LR;
                rank    = same;

                EXITPOINT1 [shape=point, width=0.0];
                EXITPOINT2 [shape=point, width=0.0];
            }

            {
                rankdir = LR;
                rank    = same;

                RETURN                  [label="Return object", shape=box, style=filled, color="#66CC99"];
            }

            INITIALIZATION           -> KEYINCACHE;
            KEYINCACHE               -> RETRIEVEFROMCACHE        [label=" Yes"]
            KEYINCACHE               -> RETRIEVEFROMCONTEXT      [label="   No"]
            RETRIEVEFROMCACHE        -> KEEPFORTESTDURATION
            RETRIEVEFROMCONTEXT      -> KEEPFORTESTDURATION
            KEEPFORTESTDURATION      -> KEEPFORTESTDURATIONPOINT [label="      No"dir=none]
            KEEPFORTESTDURATION      -> ADDTOCACHE               [label="  Yes"]
            ADDTOCACHE               -> EXITPOINT1               [dir=none]
            KEEPFORTESTDURATIONPOINT -> EXITPOINT2               [dir=none]
            EXITPOINT1               -> EXITPOINT2               [dir=none]
            EXITPOINT1               -> RETURN
        }
        @enddot

        :param index_or_predicate: It can either be an index identifying a unique debugger in the cache or
                                   a predicate, taking a Debugger instance as a parameter, and able to test whether
                                   the debugger is acceptable
        :type index_or_predicate: ``int`` or ``callable``
        :param keep_for_test_duration: Flag indicating whether to cache the object or not
        :type keep_for_test_duration: ``bool``
        :param kwargs: Additional parameters
        :type kwargs: ``object``

        :return: The context debugger.
        :rtype: ``ContextDebugger``
        """
        key = id(index_or_predicate)
        result = None
        collected_messages = []  # this will collect the exception messages for reporting.

        if key in DebuggerTestCaseMixin.DEBUGGERS:
            result = DebuggerTestCaseMixin.DEBUGGERS[key]
            result.open(**kwargs)
        else:
            # noinspection PyUnresolvedReferences
            context = self.getContext()
            context.appendDebuggerPredicate(index_or_predicate)
            debugger = context.getDebugger(index_or_predicate)

            if debugger is not None:
                # noinspection PyUnresolvedReferences
                debugger = ContextDebugger(debugger, self.getLogger())

                # Log the reader configuration
                # noinspection PyBroadException
                try:
                    debugger.open(**kwargs)

                    # noinspection PyUnresolvedReferences
                    self.log(_LEVEL_TRACE + _MASK_ALWAYS,
                             f"[debugger]\n - Name    {debugger.__next__.__class__.__name__}\n")

                    result = debugger

                    if keep_for_test_duration:
                        DebuggerTestCaseMixin.DEBUGGERS[key] = result

                        # Activate/deactivate the automatic coverage
                        # noinspection PyUnresolvedReferences
                        config = self.getContext().getConfig()
                        if config.get(ContextLoader.SECTION_CONFIG, ContextLoader.OPTION_COVERAGE) \
                                and result.getDebuggerInfo(result.F_COVERAGE):
                            DebuggerTestCaseMixin.COVERAGES[key] = result.getCoverage()
                            result.setCoverage(True)
                        # end if
                    # end if
                except Exception:
                    import traceback as tb
                    import sys
                    exc_info = sys.exc_info()
                    exc_info_1 = str(exc_info[1], sys.getdefaultencoding(), 'ignore') \
                        if isinstance(exc_info[1], str) else repr(exc_info[1])
                    exc_info_2 = "\n".join([x.strip() for x in tb.format_tb(exc_info[2])])
                    except_message = f"{exc_info[0].__name__}: {exc_info_1}\n{exc_info_2}"
                    collected_messages.append(except_message)
                    # noinspection PyBroadException
                    try:
                        debugger.close()
                    except Exception:
                        pass
                    # end try

                    result = None

                    # noinspection PyUnresolvedReferences
                    self.log(_LEVEL_ERROR + _MASK_ALWAYS, f"Unable to access debugger for {str(index_or_predicate)}")
                # end try
            # end if
        # end if

        if result is None:
            lines = []
            lines.extend(collected_messages)
            lines.extend(("No debugger selected, please:",
                          "- Check your Settings.ini",
                          "- Check that the simulator (if any) is not paused",
                          "- Modify your TestSuite, to check the configuration",
                          "  before running the test",
                          "- Check the above traceback (if any) for further hints"))
            # noinspection PyUnresolvedReferences
            self.fail("\n".join(lines))
        # end if
        return result
    # end def get_dbg
# end class DebuggerTestCaseMixin


class DebuggerTestCase(PyHarnessCase, DebuggerTestCaseMixin):
    """
    DebuggerTestCase implementation

    Provides additional testing methods, useful in a debugger context.
    """

    def setUp(self):
        """
        Initialisation of the test
        """
        PyHarnessCase.setUp(self)
    # end def setUp

    def tearDown(self):
        """
        Destructor
        """
        DebuggerTestCaseMixin.tearDown(self)
        PyHarnessCase.tearDown(self)
    # end def tearDown
# end class DebuggerTestCase


class DebuggerCoverageTestListener(TestListener):
    """
    Test listener to generate a coverage file
    """
    __context = None

    def __init__(self, *args, **kwargs):
        """
        @copydoc pyharness.core.TestListener.__init__
        """
        super(DebuggerCoverageTestListener, self).__init__(None, None, None, None)
    # end def __init__

    def getContext(self):
        """
        Get context instance

        @return (Context) Context instance
        """
        return self.__context
    # end def getContext

    def setContext(self, context):
        """
        Set context

        @param  context [in] (Context) Context instance
        """
        self.__context = context
    # end def setContext

    context = property(getContext, setContext)

    def startRun(self, context, resumed):
        """
        @copydoc pyharness.core.TestListener.startRun
        """
        self.setContext(context)
    # end def startRun

    def stopRun(self, result, suspended):
        """
        @copydoc pyharness.core.TestListener.stopRun
        """
        for predicate in self.__context.getDebuggerPredicates():
            debugger = self.__context.getDebugger(predicate)

            try:
                debugger.open()

                # Activate/deactivate the automatic coverage
                if debugger.getDebuggerInfo(debugger.F_COVERAGE):
                    if (debugger.getCoverage()):
                        coverageDir = join(self.__context.getOutputDir(),
                                                'cov')
                        if (not access(coverageDir, F_OK)):
                            makedirs(coverageDir)
                        # end if

                        coverageFilePath = join(coverageDir, datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
                        debugger.saveCoverage(coverageFilePath, debugger.FORMAT_NATIVE)
                    # end if
                # end if
            finally:
                debugger.close()
            # end try
        # end for

        TestListener.stopRun(self, result, suspended)
    # end def stopRun
# end class DebuggerCoverageTestListener

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
