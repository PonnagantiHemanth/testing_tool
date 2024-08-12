#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.strutils

@brief  automatic __str_ mixin support

@author christophe.roquebert

@date   2018/10/01
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import sys

# ------------------------------------------------------------------------------
# Implementation
# ------------------------------------------------------------------------------

class StrAbleMixin(object):
    '''
    Mixin that adds 'easy' string conversion for Elf classes
    '''

    _FIELDS = tuple()

    def __str__(self):
        '''
        Converts the current element fields to string

        @return The current object, as a string.
        '''
        elements = []
        for name, value in self._strable_getFields():
            elements.append('%s = %s' % (name, '\n  '.join(str(value).split('\n'))))
        # end for

        return '%s\n  %s' % (self._strable_getName(), '\n  '.join(elements))
    # end def __str__

    @classmethod
    def _makeStrAble(cls, name, value):
        '''
        Converts an instance to StrAble-Compatible

        @param name  [in] (str) Name of the attribute
        @param value [in] (object) Object to render compatible
        @return the value, as a compatible object
        '''
        if (type(value) in (list, tuple)):
            value = StrAbleListWrapper(value, name)
        elif type(value) in (dict,):
            value = StrAbleDictWrapper(value, name)
        elif type(value) in (int, int):
            value = '%d (0x%x)' % (value, value)
        # end if

        return value
    # end def _makeStrAble

    def _strable_getName(self):
        '''
        Obtain the class name for the printed object

        @return The class name for the printed object
        '''
        return self.__class__.__name__
    # end def _strable_getName

    def _strable_getFields(self):
        '''
        Obtain the list of field names for the current object

        @return List of field names to print.
        '''
        return [(name, self._makeStrAble(name, getattr(self, name))) for name in self._STRABLE_FIELDS]
    # end def _strable_getFields

    __repr__ = __str__
# end class StrAbleMixin

class StrAbleListWrapper(StrAbleMixin):
    '''
    Wrapper around a list, that provides indexed attributes.
    '''

    def __init__(self, target, prefix):
        '''
        Constructor

        @param target [in] (tuple, list) The wrapped object
        @param prefix [in] (str)         The prefix to apply to the wrapped object.
        '''
        super(StrAbleListWrapper, self).__init__()

        self._target = target
        self._prefix = prefix
    # end def __init__

    def _strable_getFields(self):
        '''
        @copydoc pylibrary.tools.strutils.StrAbleMixin._strable_getFields
        '''
        maximum = len(self._target) - 1

        if (maximum == -1):
            return tuple()
        # end if

        count = 0
        while (maximum != 0):
            count += 1
            maximum /= 10
        # end while
        count = max(1, count)

        keyFormat = '%%s[%%0%dd]' % count
        return [(keyFormat % (self._prefix, index), self._target[index]) for index in range(len(self._target))]
    # end def _strable_getFields

    def __getattr__(self, name):
        '''
        Proxy for intercepting predefined key names.

        @param name [in] (str) The name of the attribute to get.
        @return The intercepted attribute.
        '''
        if (name.startswith(self._prefix)):
            numeral = name[len(self._prefix)+1:-1].lstrip('0')
            if len(numeral) == 0:
                numeral = 0
            # end if
            return self._target[int(numeral)]
        # end if
    # end def __getattr__

    def _strable_getName(self):
        '''
        @copydoc pylibrary.tools.strutils.StrAbleMixin._strable_getName
        '''
        return self._target.__class__.__name__
    # end def _strable_getName
# end class StrAbleListWrapper

class StrAbleDictWrapper(StrAbleMixin):
    '''
    Wrapper around a list, that provides keyed attributes.
    '''

    def __init__(self, target, prefix):
        '''
        Constructor

        @param target [in] (tuple, list) The wrapped object
        @param prefix [in] (str)         The prefix to apply to the wrapped object.
        '''
        super(StrAbleDictWrapper, self).__init__()

        self._target = target
        self._prefix = prefix
        self._keyMap = {}
    # end def __init__

    def _strable_getFields(self):
        '''
        @copydoc pylibrary.tools.strutils.StrAbleMixin._strable_getFields
        '''
        result = []

        # If keys are of type int

        #            if (type(key) in (int, long)):
        #                maximum = key - 1
        #                count = 0
        #                while (maximum != 0):
        #                    count += 1
        #                    maximum /= 10
        #                count = max(1, count)
        #                format = '%s%%0%dd' % count
        #            else:
        keyFormat = '%s[%s]'

        for key in sorted(self._target.keys()):

            newKey = keyFormat % (self._prefix, key)
            self._keyMap[newKey] = key
            result.append((newKey, self._makeStrAble(newKey, self._target[key])))
        # end for

        return result
    # end def _strable_getFields

    def __getattr__(self, name):
        '''
        Proxy for intercepting predefined key names.

        @param name [in] (str) The name of the attribute to get.
        @return The intercepted attribute.
        '''
        if (name.startswith(self._prefix+'[')):
            return self._target[self._keyMap[name]]
        # end if
    # end def __getattr__

    def _strable_getName(self):
        '''
        @copydoc pylibrary.tools.strutils.StrAbleMixin._strable_getName
        '''
        return self._target.__class__.__name__
    # end def _strable_getName
# end class StrAbleDictWrapper

def pythonify(objectToConvert):
    '''
    Decodes a string encoded with the file system encoding.

    @param objectToConvert [in] (object) The object to convert from the system default.
    @return The unicode-encoded string.
    '''
    return str(objectToConvert, sys.getdefaultencoding(), 'replace')
# end def pythonify

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
