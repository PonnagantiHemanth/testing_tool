#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.stringutils

@brief  Utilities for string conversion

@author christophe.roquebert

@date   2018/10/27
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
import re


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class StringUtils(object):
    '''
    Utilities for string handling:
    - Conversion to/from python from/to string
    - Conversion to/from python from/to intepreter-parseable string
    .
    '''
    # Conversions:
    # Key: type
    # Value: (regex for auto, to_python, check for auto, to_string, to_python_string)
    CONVERSIONS = {'string' : (re.compile("^[\"'](.*)[\"']$"),
                               lambda v: v,
                               lambda v: isinstance(v, str),
                               lambda v: v,
                               repr),
                   'int'    : (re.compile("^([1-9][0-9]*|0x[0-9A-Fa-f]+|0)$"),
                               lambda v: int(v[2:], 16) if v.startswith('0x') else int(v),
                               lambda v: isinstance(v, int),
                               str,
                               repr),
                   'float'  : (re.compile(r'^([0-9]+\.[0-9]+)$'),
                               float,
                               lambda v: isinstance(v, float),
                               str,
                               repr),
                   'hexlist': (re.compile("^(\\[(?:[0-9A-Fa-f]{2}\\s*)+\\])$"),
                               HexList,
                               lambda v: isinstance(v, HexList),
                               str,
                               repr),
                   'boolean': (re.compile('^(true|false)$'),
                               lambda v: v == 'true',
                               lambda v: isinstance(v, bool),
                               lambda v: str(v).lower(),
                               repr),
                   'tuple'  : (re.compile(r'^(\(.*\))$'),
                               lambda v: tuple([x.strip()[1:-1] for x in v[1:-1].split(',')]),
                               lambda v: isinstance(v, tuple),
                               str,
                               repr),
                   'none'   : (re.compile('^none$'),
                               lambda v: None,
                               lambda v: v is None,
                               lambda v: 'none',
                               lambda v: 'None'),
                   'bytes'  : (re.compile("."),
                               lambda v: v,
                               lambda v: isinstance(v, bytes),
                               bytes,
                               repr),
                   }

    @classmethod
    def stringToPython(cls, value, valueType):
        '''
        Converts a string to a python value

        @param  value     [in] (str) Value to interpret
        @param  valueType [in] (str) Type of the value to interpret.

        @return The interpreted value
        '''
        # TODO This would be cleaner if the caller passed an actual __none__ value
        if (value is None):
            valueType = 'none'
        # end if

        if (valueType == 'auto'):

            for valueType, (regex, _, _, _, _) in cls.CONVERSIONS.items():
                if regex.match(value):
                    break
                # end if
            else:
                # Default to string value
                valueType = 'string'
                # raise ValueError('Unable to determine type for value: %s' % self.value)
            # end for
        # end if

        _, to_python, _, _, _ = cls.CONVERSIONS[valueType]  # pylint:disable=W0631

        return to_python(value)
    # end def stringToPython

    @classmethod
    def pythonToString(cls, value, valueType):
        '''
        Converts a python value to a string

        @param  value      [in] (object) Value to set
        @param  valueType  [in] (str) Type of the value to interpret.

        @return The string for the python value
        '''

        if (valueType == 'auto'):
            for valueType, (_, _, check, to_string, _) in cls.CONVERSIONS.items():
                if check(value):
                    break
                # end if
            else:
                raise ValueError('Unable to determine valueType for value: %s' % value)
            # end for
        else:
            _, _, _, to_string, _ = cls.CONVERSIONS[valueType]
        # end if

        return to_string(value)
    # end def pythonToString

    @classmethod
    def pythonToRepr(cls, value, valueType):
        '''
        Converts a python value to an evaluatable string

        @param  value      [in] (object) Value to set
        @param  valueType  [in] (str)    Type of the value to interpret.

        @return The string for the python value
        '''

        if (valueType == 'auto'):
            for valueType, (_, _, check, _, to_repr) in cls.CONVERSIONS.items():
                if check(value):
                    break
                # end if
            else:
                raise ValueError('Unable to determine valueType for value: %s' % value)
            # end for
        else:
            _, _, _, _, to_repr = cls.CONVERSIONS[valueType]
        # end if

        return to_repr(value)
    # end def pythonToRepr

    @classmethod
    def stringToRepr(cls, value, valueType):
        '''
        Converts a string value to an evaluatable string

        @param  value      [in] (str) Value to set
        @param  valueType  [in] (str) Type of the value to interpret.

        @return (str) The string for the python value
        '''
        if (valueType == 'auto'):
            for valueType, (_, to_python, check, _, to_repr) in cls.CONVERSIONS.items():
                if check(value):
                    break
                # end if
            else:
                raise ValueError('Unable to determine valueType for value: %s' % value)
            # end for
        else:
            _, to_python, _, _, to_repr = cls.CONVERSIONS[valueType]
        # end if

        return to_repr(to_python(value))
    # end def stringToRepr

# end class StringUtils

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
