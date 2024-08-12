#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package    pylibrary.tools

@brief  Miscellaneous utilities

@author christophe.roquebert

@date   2018/09/12
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

def stringTruncator(value, maxChars = 250):
    '''
    Truncates a string, replacing (if needed) its last 8 bytes by a hash on
    its value.

    If the string can fit in the required number of chars, it is left as-is.

    @param value    [in] (str) The string to process
    @param maxChars [in] (int) The maximum number of characters in the returned string.
    @return The processed string
    '''
    assert maxChars >= 8, "Maximum number of characters must be >= 8"

    if (len(value) > maxChars):
        return value[:maxChars-8] + "%08X" % hash(value)
    # end if

    return value
# end def stringTruncator

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
