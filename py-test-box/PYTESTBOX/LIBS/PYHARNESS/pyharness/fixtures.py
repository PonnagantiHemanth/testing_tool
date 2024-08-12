#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.fixtures

@brief  fixtures decorator

@author christophe Roquebert

@date   2018/06/02
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from threading                          import RLock
from types                              import MethodType
from types                              import FunctionType
from pylibrary.tools.checks             import checkCallable
from pylibrary.tools.threadutils        import synchronized
import ast
import json


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
SYNCHRONIZATION_LOCK = RLock()

class Fixtures():
    '''
    Function decorator, that associates a function and its arguments to a method.

    This should be used in tests, on test methods, to declare the test fixtures.

    Example:
    @code
    from pyharness.device                   import PyHarnessCase
    from pyHarness.fixtures          import fixtures

    class MyTest(PyHarnessCase):
        @fixtures(function, *args, **kwargs)
        def test_Example(self):
            self.fail("Test not implemented")
        # end def test_Example
    # end class MyTest
    @endcode
    '''
    _INSTANCE = None

    __EMPTY_SET = frozenset()

    _fixturesToId      = {}
    _classFixturesToId = {}
    _idToFixtures      = {}
    _fixtureHelp       = {}

    @classmethod
    @synchronized(SYNCHRONIZATION_LOCK)
    def __new__(cls, *args, **kwargs):
        '''
        Creator

        @option args   [in] (list) List of arguments
        @option kwargs [in] (dict) Keyword arguments

        @return (Fixtures) Same Fixtures instance for every creation
        '''
        if cls._INSTANCE is None:
            cls._INSTANCE = super(Fixtures, cls).__new__(*args, **kwargs)
        # end if
        return cls._INSTANCE
    # end def __new__

    def __call__(self, *fixturesValues, **kwargs):
        '''
        fixtures decorator call function

        @option fixturesValues [in] (tuple) The fixtures the following function
                                         will be associated with

        @return An inner decorator that associates the function with the fixtures.

        @note   This function will be called when using a fixtures decorator.
                @fixtures(function, *args, **kwargs)
                or
                @fixtures((function1, *args1, **kwargs1),
                          (function2, *args2, **kwargs2))
        '''
        try:
            # Check if we received a single fixture 
            # tuple(function, args)
            #   @fixtures(function, *args, **kwargs)
            callable_obj, *args = fixturesValues
            checkCallable(callable_obj)
            # recreate a list for fixturesAssigner
            fixturesValues = [tuple([callable_obj, *args, str(kwargs)])]
        except:
            # Check if we received a list of fixtures
            # tuple(tuple(function, args), tuple(function, args), ...)
            #   @fixtures((function1, *args1, **kwargs1),
            #             (function2, *args2, **kwargs2))
            for fixturesValue in fixturesValues:
                callable_obj, *args = fixturesValue
                checkCallable(callable_obj)
        # end try

        def fixturesAssigner(f):
            '''
            Inner decorator, that performs the actual association.

            @param  f [in] (MethodType) The function to decorate with the fixtures

            @return The decorated function (Same as the input)
            '''
            if isinstance(f, FunctionType):
                fixturesToId =  self._fixturesToId
            else:
                # Class type
                fixturesToId =  self._classFixturesToId
                
            fId = id(f)
            SYNCHRONIZATION_LOCK.acquire()
            try:
                for fixturesValue in fixturesValues:
                    ids = fixturesToId.get(fixturesValue, None)
                    if (ids is None):
                        ids = set()
                        fixturesToId[fixturesValue] = ids
                    # end if
                    ids.add(fId)

                    _fixtures = self._idToFixtures.get(fId, None)
                    if (_fixtures is None):
                        _fixtures = set()
                        self._idToFixtures[fId] = _fixtures
                    # end if
                    _fixtures.add(fixturesValue)
                # end for
            finally:
                SYNCHRONIZATION_LOCK.release()
            # end try

            return f
        # end def fixturesAssigner
        return fixturesAssigner
    # end def __call__

    @staticmethod
    def __realFunction(f):
        '''
        Extracts the inner FunctionType object from a MethodType object.

        @param  f [in] (MethodType) A MethodType object, from which the
                                    FunctionType object is extracted

        @return The FunctionType object associated with the parameter
        '''
        func = f
        while (isinstance(func, MethodType)):
            func = func.__func__
        # end while
        return func
    # end def __realFunction

    @staticmethod
    def __getFid(f):
        '''
        Get id of inner function

        @param  f [in] (MethodType) A MethodType object, from which the
                                    FunctionType object is extracted

        @return (int) ID of the function
        '''
        return id(Fixtures.__realFunction(f))
    # end def __getFid

    @synchronized(SYNCHRONIZATION_LOCK)
    def getFixtures(self, f = None):
        '''
        Obtains the list of fixtures for which a function is registered.

        @option f [in] (FunctionType) The function to check, None to obtain _all_ fixtures

        @return (list) The list of registered fixtures
        '''
        if f is not None:
            result = []
            fId = Fixtures.__getFid(f)
            stringFixtures = self._idToFixtures.get(fId, self.__EMPTY_SET)
            for function, *args, in stringFixtures:
                kwargs = {}
                for i in range(len(args)):
                    if isinstance(args[i], str):
                        try:
                            kwargs = ast.literal_eval(args[i])
                            if type(kwargs) is dict:
                                args.remove(args[i])
                                break
                            # end if
                        except:
                            # real string found
                            pass
                        # end try
                    # end if
                # end for
                result.append((function, args, kwargs))
            # end for
        else:
            result = list(self._fixturesToId.keys())
        # end if

        return result
    # end def getFixtures
    
    def getClassFixtures(self, cls=None):
        """
        Obtains the list of fixtures for which a class is registered.

        @param f [in] (ClassType) The class type to check, None to obtain _all_ fixtures
        @return The list of registered fixtures
        """
        
        if (cls is not None):
            clsId = id(cls)
            
            result = []
            for (function, *args), values in iter(self._classFixturesToId.items()):
                if clsId in values:
#                     for function, *args, in name:
                    kwargs = {}
                    for i in range(len(args)):
                        if isinstance(args[i], str):
                            try:
                                kwargs = ast.literal_eval(args[i])
                                if type(kwargs) is dict:
                                    args.remove(args[i])
                                    break
                                # end if
                            except:
                                # real string found
                                pass
                            # end try
                        # end if
                    # end for
                    result.append((function, args, kwargs))
                # end if
            # end for
        else:
            result = list(self._classFixturesToId.keys())
        # end if
        
        return result
    # end def getClassFixtures

    def isDecorated(self, f):
        '''
        Tests whether a function has defined a fixture.

        @param  f [in] (FunctionType) The function to test

        @return True if the function has defined a fixture with the fixtures
                decorator
        '''
        fId = Fixtures.__getFid(f)

        result = False
        for fIds in iter(list(self._fixturesToId.values())):
            if fId in fIds:
                result = True
                break
            # end if
        # end for

        return result
    # end def isDecorated
    
    def isClassDecorated(self, cls):
        '''
        Tests whether a function has defined a fixture.

        @param  f [in] (FunctionType) The function to test

        @return True if the function has defined a fixture with the fixtures
                decorator
        '''
        fId = Fixtures.__getFid(cls)

        result = False
        for fIds in iter(list(self._classFixturesToId.values())):
            if fId in fIds:
                result = True
                break
            # end if
        # end for

        return result
    # end def isClassDecorated

    def setHelp(self, fixture, help):                                                                                      #@ReservedAssignment pylint:disable=W0622
        '''
        Sets the help string associated with a fixture

        @param  fixture [in] (str) The fixture value
        @param  help [in] (str) The help string
        '''
        self._fixtureHelp[fixture] = help
    # end def setHelp

    def getHelp(self, fixture = None):
        '''
        Obtains the help string associated with the fixture, or None if no help is defined.

        @option fixture [in] (str) The fixture value

        @return The associated help string, or None if not defined.
        '''
        if (fixture is None):
            result = self._fixtureHelp
        else:
            result = self._fixtureHelp.get(fixture, None)
        # end if

        return result
    # end def getHelp
# end class Fixtures

## The global fixtures monitor. Its name should be ignored by pylint
fixtures = Fixtures()                                                                 #pylint:disable=C0103


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
