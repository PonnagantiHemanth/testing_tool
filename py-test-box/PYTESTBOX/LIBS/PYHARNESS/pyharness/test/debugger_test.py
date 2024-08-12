#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.test.debuggertest

@brief  ContextDebugger test implementation

This module contains the test cases for the ContextDebugger class module.

@author christophe.roquebert

@date   2018/07/22
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.system.debugger         import Debugger
from pylibrary.system.debugger         import alwaysTrigger
from pylibrary.tools.hexlist            import HexList
from pylibrary.tools.logger           import Logger
from pyharness.debugger                  import ContextDebugger
from unittest                           import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ContextDebuggerTestCase(TestCase):
    '''
    Tests of the ContextDebugger class
    '''

    class CollectorMixin(object):
        '''
        A Mixin collecting method calls and providing dummy answers
        '''

        def __init__(self, callCollector):
            '''
            Constructor

            @param  callCollector [in] (list) List that will be appended with the call parameters
            '''
            self.collectedCalls = callCollector
        # end def __init__

        def stub(self, methodName, returnValue = None):
            '''
            Defines a new stub, to replace an instance method.

            @param  methodName  [in] (str) Method name to stub
            @option returnValue [in] (object) Method return value
            '''
            def sink(*args, **kwargs):
                '''
                Method sink, to collect calls and return a fixed value

                @option args   [in] (tuple) Positional arguments
                @option kwargs [in] (tuple) Keyword arguments

                @return The stubbed return value
                '''
                self.collectedCalls.append((methodName, args, kwargs))
                return returnValue
            # end def sink

            setattr(self, methodName, sink)
        # end def stub
    # end class CollectorMixin

    class MockDebugger(Debugger, CollectorMixin):                                                                       # pylint:disable=W0223
        '''
        A mock debugger, that collects call parameters and returns predefined answers
        '''

        def __init__(self, callCollector):
            '''
            Constructor

            @param  callCollector [in] (list) List that will be appended with the call parameters
            '''
            Debugger.__init__(self)
            ContextDebuggerTestCase.CollectorMixin.__init__(self, callCollector = callCollector)

            self.stub('reset', 0)
            self.stub('fillMemory')
            self.stub('getCycles', 100)
            self.stub('getPc', 0x400000)
            self.stub('getRegister', 0x22)
            self.stub('getRegisters', {'R01': 0x99})
            self.stub('readMemory', HexList('00000000'))
            self.stub('run', 0x100)
            self.stub('stop', 0x200)
            self.stub('runFunction', 0x99)
            self.stub('setPc')
            self.stub('setRegister')
            self.stub('setRegisters')
            self.stub('stepInto', 0x300)
            self.stub('stepOut', 0x400)
            self.stub('stepOver', 0x500)
            self.stub('waitForStop', 0x600)
            self.stub('writeMemory')
            self.stub('getAddress', 0x1234)
            self.stub('getDebuggerInfo', Debugger.F_ALL)
        # end def __init__
    # end class MockDebugger

    class MockLogger(Logger, CollectorMixin):                                                                           # pylint:disable=W0223
        '''
        A logger collecting method calls to the log API
        '''
        def __init__(self, callCollector):
            '''
            Constructor

            @param  callCollector [in] (list) List that will be appended with the call parameters
            '''
            Logger.__init__(self)
            ContextDebuggerTestCase.CollectorMixin.__init__(self, callCollector = callCollector)

            self.stub('logTitle1')
            self.stub('logTitle2')
            self.stub('logTitle3')
            self.stub('logError')
            self.stub('logTrace')
            self.stub('logDebug')
            self.stub('log')
            self.stub('logRaw')
            self.stub('logInfo')
            self.stub('logSeparator')
            self.stub('addPerformanceData')
        # end def __init__
    # end class MockLogger

    def _createInstance(self):
        '''
        Creates an instance of the context debugger.

        @return a new instance of the context debugger, using a dummy back-end
        '''
        callCollector = []
        return ContextDebugger(self.MockDebugger(callCollector), self.MockLogger(callCollector)), callCollector
    # end def _createInstance

    def testFillMemory(self):
        '''
        Tests that fillMemory:
        - Works with an address as an int
        - Works with an address as a str
        '''
        debugger, callCollector = self._createInstance()

        # Use a fillMemory with absolute address
        del callCollector[:]
        debugger.fillMemory(0x1234, 0x123, 0x12)
        self.assertTrue(('fillMemory', (0x1234, 0x123, 0x12, None), {}) in callCollector,
                        'fillMemory not called on back-end')

        # Same, with label
        del callCollector[:]
        debugger.fillMemory('label', 0x123, 0x12)
        self.assertTrue(('getAddress', ('label', None), {}) in callCollector,
                        'fillMemory not called on back-end')
        self.assertTrue(('fillMemory', ('label', 0x123, 0x12, None), {}) in callCollector,
                        'fillMemory not called on back-end')

    # end def testFillMemory
#
#    def testStr(self):
#        '''
#        Tests __str__ method
#        '''
#        debugger, callCollector = self._createInstance()
#
#        del callCollector[:]
#        str(debugger)
#        self.assertTrue(('__str__', tuple(), {}) in callCollector,
#                        '__str__ not called on back-end')
#
#    # end def testStr

    def testReset(self):
        '''
        Tests reset method
        '''
        debugger, callCollector = self._createInstance()

        del callCollector[:]
        debugger.reset()
        self.assertTrue(('reset', (), {}) in callCollector,
                        'reset not called on back-end')
        self.assertTrue(('logTrace', ("PC: 0x%08.8X" % 0,), {}) in callCollector,
                        'reset not called on back-end')

        del callCollector[:]
        debugger.reset(soft_reset=False)
        self.assertTrue(('reset', (), {'soft_reset': False}) in callCollector,
                        'reset not called on back-end')
        self.assertTrue(('logTrace', ("PC: 0x%08.8X" % 0,), {}) in callCollector,
                        'reset not called on back-end')

        del callCollector[:]
        debugger.reset(soft_reset=True)
        self.assertTrue(('reset', (), {'soft_reset': True}) in callCollector,
                        'reset not called on back-end')

        self.assertTrue(('logTrace', ("PC: 0x%08.8X" % 0,), {}) in callCollector,
                        'reset not called on back-end')
    # end def testReset

    def testRun(self):
        '''
        Tests that run method:
        - Works with a None address
        - Works with an address as an int
        - Works with an address as a str
        '''
        debugger, callCollector = self._createInstance()

        del callCollector[:]
        debugger.run()
        self.assertTrue(('run', (), {}) in callCollector,
                        'run not called on back-end')
    # end def testRun

    def testStop(self):
        '''
        Tests stop method
        '''
        debugger, callCollector = self._createInstance()

        del callCollector[:]
        debugger.stop()
        self.assertTrue(('stop', tuple(), {}) in callCollector,
                        'stop not called on back-end')

        self.assertTrue(('logTrace', ("Stopping debugger",), {}) in callCollector,
                        'stop not called on back-end')

        self.assertTrue(('logTrace', ("PC: 0x%08.8X" % 0x200,), {}) in callCollector,
                        'stop not called on back-end')

    # end def testStop

    def testWaitForStop(self):
        '''
        Tests that waitForStop method:
        - Works with a None timeout
        - Works with an timeout as an int
        '''
        debugger, callCollector = self._createInstance()

        # None timeout
        del callCollector[:]
        timeout = None
        debugger.waitForStop(timeout)
        self.assertTrue(('waitForStop', (timeout,), {}) in callCollector,
                        'waitForStop not called on back-end')

        self.assertTrue(('logDebug', ("Waiting for stop: timeout %s" % (timeout,),), {}) in callCollector,
                        'run not called on back-end')

        self.assertTrue(('logDebug', ("PC: 0x%08.8X" % (0x600,),), {}) in callCollector,
                        'run not called on back-end')

        # int timeout
        del callCollector[:]
        timeout = 0x666
        debugger.waitForStop(timeout)
        self.assertTrue(('waitForStop', (timeout,), {}) in callCollector,
                        'waitForStop not called on back-end')

        self.assertTrue(('logDebug', ("Waiting for stop: timeout %s" % (timeout,),), {}) in callCollector,
                        'run not called on back-end')

        self.assertTrue(('logDebug', ("PC: 0x%08.8X" % (0x600,),), {}) in callCollector,
                        'run not called on back-end')

    # end def testWaitForStop

    def testGetCycles(self):
        '''
        Tests getCycles method
        '''
        debugger, callCollector = self._createInstance()

        del callCollector[:]
        debugger.getCycles()
        self.assertTrue(('getCycles', tuple(), {}) in callCollector,
                        'getCycles not called on back-end')

        self.assertTrue(('logDebug', ("Getting Cycles count: %d" % (100,),), {}) in callCollector,
                        'run not called on back-end')
    # end def testGetCycles

    def testGetPc(self):
        '''
        Tests getPc method
        '''
        debugger, callCollector = self._createInstance()

        del callCollector[:]
        debugger.getPc()
        self.assertTrue(('getPc', tuple(), {}) in callCollector,
                        'getPc not called on back-end')

        self.assertTrue(('logDebug', ("Getting PC: 0x%08.8X" % (0x400000,),), {}) in callCollector,
                        'getPc not called on back-end')
    # end def testGetPc

    def testSetPc(self):
        '''
        Tests that setPc method:
        - Works with an address as an int
        - Works with an address as a str
        '''
        debugger, callCollector = self._createInstance()

        # int address
        del callCollector[:]
        debugger.setPc(0x1230)
        self.assertTrue(('setPc', (0x1230,), {}) in callCollector,
                        'setPc not called on back-end')

        self.assertTrue(('logTrace', ("Setting PC at %s (0x%08.8X)" % (0x1230, 0x1234),), {}) in callCollector,
                        'setPc not called on back-end')

        self.assertTrue(('getAddress', (0x1230, ), {}) in callCollector,
                        'setPc not called on back-end')

        # str address
        del callCollector[:]
        debugger.setPc('label')
        self.assertTrue(('setPc', ('label',), {}) in callCollector,
                        'setPc not called on back-end')

        self.assertTrue(('logTrace', ("Setting PC at %s (0x%08.8X)" % ('label', 0x1234),), {}) in callCollector,
                        'setPc not called on back-end')

        self.assertTrue(('getAddress', ('label', ), {}) in callCollector,
                        'setPc not called on back-end')

    # end def testSetPc

    def testGetRegister(self):
        '''
        Tests getRegister method
        '''
        debugger, callCollector = self._createInstance()

        # int address
        del callCollector[:]
        register = 'R0'
        debugger.getRegister(register)
        self.assertTrue(('getRegister', (register,), {}) in callCollector,
                        'getRegister not called on back-end')

        self.assertTrue(('logDebug', ("Getting register %-5s: 0x%08.8X" % (register, 0x22),), {}) in callCollector,
                        'getRegister not called on back-end')

    # end def testGetRegister

    def testSetRegister(self):
        '''
        Tests setRegister method
        '''
        debugger, callCollector = self._createInstance()

        # int address
        del callCollector[:]
        register = 'R0'
        value    = 0x98
        debugger.setRegister(register, value)
        self.assertTrue(('setRegister', (register, value), {}) in callCollector,
                        'setRegister not called on back-end')

        self.assertTrue(('logTrace', ("Setting register %-5s: 0x%08.8X" % (register, value),), {}) in callCollector,
                        'setRegister not called on back-end')

    # end def testSetRegister

    def testGetRegisters(self):
        '''
        Tests getRegisters method
        '''
        debugger, callCollector = self._createInstance()

        del callCollector[:]
        registerList = []
        debugger.getRegisters(registerList)
        self.assertTrue(('getRegisters', (registerList,), {}) in callCollector,
                        'getRegisters not called on back-end')

        self.assertTrue(('logDebug', ("Getting registers:",), {}) in callCollector,
                        'getRegisters not called on back-end')

        self.assertTrue(('logDebug', ("%-5s: 0x%08.8X" % ('R01', 0x99),), {}) in callCollector,
                        'getRegisters not called on back-end')

    # end def testGetRegisters

    def testSetRegisters(self):
        '''
        Tests setRegisters method
        '''
        debugger, callCollector = self._createInstance()

        del callCollector[:]
        register = 'R0'
        value    = 0x11
        registerDict = {'R0': value}
        debugger.setRegisters(registerDict)
        self.assertTrue(('setRegisters', (registerDict,), {}) in callCollector,
                        'setRegisters not called on back-end')

        self.assertTrue(('logTrace', ("Setting registers:",), {}) in callCollector,
                        'setRegisters not called on back-end')

        self.assertTrue(('logTrace', ("%-5s: 0x%08.8X" % (register, value),), {}) in callCollector,
                        'setRegisters not called on back-end')

    # end def testSetRegisters

    def testReadMemory(self):
        '''
        Tests that readMemory method:
        - Works with an address as an int
        - Works with an address as a str
        '''
        debugger, callCollector = self._createInstance()

        # int address
        del callCollector[:]
        debugger.readMemory(0x1230, 0x10)
        self.assertTrue(('readMemory', (0x1230, 0x10, None), {}) in callCollector,
                        'readMemory not called on back-end')

        self.assertTrue(('logDebug', ("Reading memory at %s (0x%08.8X):" % (0x1230, 0x1234),), {}) in callCollector,
                        'readMemory not called on back-end')

        self.assertTrue(('getAddress', (0x1230, None), {}) in callCollector,
                        'readMemory not called on back-end')

        # str address
        del callCollector[:]
        debugger.readMemory('label', 0x20)
        self.assertTrue(('readMemory', ('label', 0x20, None), {}) in callCollector,
                        'readMemory not called on back-end')

        self.assertTrue(('logDebug', ("Reading memory at %s (0x%08.8X):" % ('label', 0x1234),), {}) in callCollector,
                        'readMemory not called on back-end')

        self.assertTrue(('getAddress', ('label', None), {}) in callCollector,
                        'readMemory not called on back-end')

    # end def testReadMemory

    def testWriteMemory(self):
        '''
        Tests that writeMemory method:
        - Works with an address as an int
        - Works with an address as a str
        '''
        debugger, callCollector = self._createInstance()

        # int address
        del callCollector[:]
        debugger.writeMemory(0x1230, 0x10)
        self.assertTrue(('writeMemory', (0x1230, HexList('10'), None), {}) in callCollector,
                        'writeMemory not called on back-end')

        formattedData = "0x%8.8X: .. .. .. .. %X" % (0x1230, 0x10)
        self.assertTrue(('logTrace', ("Writing memory at %s (0x%08.8X): \n%s" % (0x1230, 0x1234, formattedData),), {}) in callCollector,
                        'writeMemory not called on back-end')

        self.assertTrue(('getAddress', (0x1230, None), {}) in callCollector,
                        'writeMemory not called on back-end')

        # str address
        del callCollector[:]
        debugger.writeMemory('label', 0x20)
        self.assertTrue(('writeMemory', ('label', HexList('20'), None), {}) in callCollector,
                        'writeMemory not called on back-end')

        formattedData = "0x%8.8X: .. .. .. .. %X" % (0x1230, 0x20)
        self.assertTrue(('logTrace', ("Writing memory at %s (0x%08.8X): \n%s" % ('label', 0x1234, formattedData),), {}) in callCollector,
                        'writeMemory not called on back-end')

        self.assertTrue(('getAddress', ('label', None), {}) in callCollector,
                        'writeMemory not called on back-end')

    # end def testWriteMemory

    def testStepInto(self):
        '''
        Tests stepInto method
        '''
        debugger, callCollector = self._createInstance()

        del callCollector[:]
        debugger.stepInto()
        self.assertTrue(('stepInto', (alwaysTrigger, Debugger.STEP_INSTRUCTION), {}) in callCollector,
                        'stepInto not called on back-end')

        self.assertTrue(('logTrace', ("Stepping into",), {}) in callCollector,
                        'stepInto not called on back-end')

        self.assertTrue(('logTrace', ("PC: 0x%08.8X" % (0x300,),), {}) in callCollector,
                        'stepInto not called on back-end')

    # end def testStepInto

    def testStepOut(self):
        '''
        Tests stepOut method
        '''
        debugger, callCollector = self._createInstance()

        del callCollector[:]
        debugger.stepOut()
        self.assertTrue(('stepOut', (alwaysTrigger, ), {}) in callCollector,
                        'stepOut not called on back-end')

        self.assertTrue(('logTrace', ("Stepping out",), {}) in callCollector,
                        'stepOut not called on back-end')

        self.assertTrue(('logTrace', ("PC: 0x%08.8X" % (0x400,),), {}) in callCollector,
                        'stepOut not called on back-end')

    # end def testStepOut

    def testStepOver(self):
        '''
        Tests stepOver method
        '''
        debugger, callCollector = self._createInstance()

        del callCollector[:]
        debugger.stepOver()
        self.assertTrue(('stepOver', (alwaysTrigger, Debugger.STEP_INSTRUCTION), {}) in callCollector,
                        'stepOver not called on back-end')

        self.assertTrue(('logTrace', ("Stepping over",), {}) in callCollector,
                        'stepOver not called on back-end')

        self.assertTrue(('logTrace', ("PC: 0x%08.8X" % (0x500,),), {}) in callCollector,
                        'stepOver not called on back-end')

    # end def testStepOver

    def testRunFunction(self):
        '''
        Tests that runFunction method:
        - Works with an address as an int
        - Works with an address as a str
        '''
        debugger, callCollector = self._createInstance()

        # int address
        del callCollector[:]
        address = 0x1230
        debugger.runFunction(address)
        self.assertTrue(('runFunction', (address, None, None), {}) in callCollector,
                        'runFunction not called on back-end')

        self.assertTrue(('logTrace', ("Running function at %s (0x%08.8X):" % (address, 0x1234),), {}) in callCollector,
                        'runFunction not called on back-end')

        self.assertTrue(('getAddress', (address, ), {}) in callCollector,
                        'runFunction not called on back-end')

        # str address
        del callCollector[:]
        label = 'label'
        debugger.runFunction(label)
        self.assertTrue(('runFunction', (label, None, None), {}) in callCollector,
                        'runFunction not called on back-end')

        self.assertTrue(('logTrace', ("Running function at %s (0x%08.8X):" % (label, 0x1234),), {}) in callCollector,
                        'runFunction not called on back-end')

        self.assertTrue(('getAddress', ('label', ), {}) in callCollector,
                        'runFunction not called on back-end')

    # end def testRunFunction

# end class ContextDebuggerTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
