#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pysetup.ansi

@brief   ANSI Escape sequences

These sequences define functions that change display graphics, control cursor
movement and reassign keys.

ANSI escape sequence is a sequence of ASCII characters, the first two of which
are the ASCII "Escape" character 27 (1Bh) and the left-bracket character "[" (5Bh).

The character or characters following the escape and left-bracket characters
specify an alphanumeric code that controls a keyboard or display function.

ANSI escape sequences distinguish between uppercase and lowercase letters.

@see     http://ascii-table.com/ansi-escape-sequences.php

@author  christophe roquebert

@version 0.2.0.0

@date    2010/02/17
'''
# ------------------------------------------------------------------------------
import re
# ------------------------------------------------------------------------------


##@name ANSI Escape sequence
##@{
ESCAPE = '\x1B'
##@}

##@name Cursor Position
##
## Moves the cursor to the specified position (coordinates).
## If you do not specify a position, the cursor moves to the home position at the
## upper-left corner of the screen (line 0, column 0). This escape sequence works
## the same way as the following Cursor Position escape sequence
## - Esc[Line;ColumnH
## - Esc[Line;Columnf
##@{
CP_RE = re.compile(r'(\\x1B\\x5B[\d;\d]?[Hf])')  ##< Cursor position regexp
##@}


##@name Set Graphics Mode
##
## Calls the graphics functions specified by the following values.
## These specified functions remain active until the next occurrence of this escape sequence.
## Graphics mode changes the colors and attributes of text (such as bold and underline) displayed on the screen.
## - Esc[Value;...;Valuem
##@{
SGM_RE = re.compile(r'(\\x1B\\x5B[\d;]+m)')      ##< Set graphic mode regexp
##@}

##@name Set Graphics Mode / Text attributes
##@{
SGM_TA_OFF        = 0 ##< All attributes off
SGM_TA_BOLD       = 1 ##< Bold on
SGM_TA_UNDERSCORE = 4 ##< Underscore (on monochrome display adapter only)
SGM_TA_BLINK      = 5 ##< Blink on
SGM_TA_REVERSE    = 7 ##< Reverse video on
SGM_TA_CONCEALED  = 8 ##< Concealed on
##@}

##@name Set Graphics Mode / Foreground colors
##@{
SGM_FC_BLACK      = 30 ##< Black
SGM_FC_RED        = 31 ##< Red
SGM_FC_GREEN      = 32 ##< Green
SGM_FC_YELLOW     = 33 ##< Yellow
SGM_FC_BLUE       = 34 ##< Blue
SGM_FC_MAGENTA    = 35 ##< Magenta
SGM_FC_CYAN       = 36 ##< Cyan
SGM_FC_WHITE      = 37 ##< White
##@}

##@name Set Graphics Mode / Background colors
##@{
SGM_BC_BLACK      = 40 ##< Black
SGM_BC_RED        = 41 ##< Red
SGM_BC_GREEN      = 42 ##< Green
SGM_BC_YELLOW     = 43 ##< Yellow
SGM_BC_BLUE       = 44 ##< Blue
SGM_BC_MAGENTA    = 45 ##< Magenta
SGM_BC_CYAN       = 46 ##< Cyan
SGM_BC_WHITE      = 47 ##< White
##@}

def setGraphicMode(*args):
    '''
    Build SGM Ansi sequence

    @param args [in] (int) Text attributes,
                           Foreground colors,
                           Background colors

    @return SGM Ansi sequence
    '''
    return '\x1B\x5B%sm' % ((';'.join([str(arg) for arg in args])),)
# end def setGraphicMode

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
