#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.checks

@brief  Check utils

@author christophe Roquebert

@date   2018/06/03
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
def checkType(param, types, paramName = None):
    '''
    Checks that @c param type is one of @c types and raise a TypeError exception
    in other case

    @param  param     [in] (object) Parameter to check the type
    @param  types     [in] (type,tuple) Type or tuple of types
    @option paramName [in] (str) Name to use for @c param if wrong type

    @exception TypeError if @c param is not of expected type
    '''
    if not isinstance(types, (type, tuple)):
        raise TypeError('Wrong checkType usage: wrong types type: %s. Shall '
                        'be type or tuple instead')
    # end if
    if not isinstance(param, types):
        name = paramName if paramName is not None else 'parameter'
        typesName = ', '.join(t.__name__ for t in list(types))
        raise TypeError('Wrong %s type: %s. Shall be (%s) instead'
                        % (name, type(param).__name__, typesName))
    # end if
# end def checkType

def checkCallable(func, funcName = None):
    '''
    Checks that @c func is callable

    @param  func     [in] (function) Callable function
    @option funcName [in] (str) Name to use for @c func if wrong type

    @exception TypeError if @c func is not callable
    '''
    if not callable(func):
        name = funcName if funcName is not None else 'function'
        raise TypeError('Wrong %s type: %s. Shall be callable instead'
                        % (name, type(func).__name__))
    # end if
# end def checkCallable

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
