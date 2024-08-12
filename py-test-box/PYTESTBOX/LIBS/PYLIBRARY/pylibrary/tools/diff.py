#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.diff

@brief  Hexadecimal buffer implementation

@author christophe.roquebert

@date   2018/07/05
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from difflib import unified_diff

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class DiffableMixin(object):
    '''
    A mixin that adds the diff method to an object.

    The diff method implements a diff-like comparison on the string representation of an object
    '''

    def diff(self, other):
        '''
        Performs a diff between two objects

        @param other [in] (object) The object to diff with
        @return A diff of the two string representations, in unified-diff format
        '''
        left = str(self).split('\n')
        right = str(other).split('\n')

        result = unified_diff(left, right, lineterm='')
        result = '\n'.join(result)

        return result
    # end def diff
# end class DiffableMixin

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
