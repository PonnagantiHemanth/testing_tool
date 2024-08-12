#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pysetup.console

@brief   Console utilities

@author  christophe roquebert

@version 0.3.0.0

@date    2018/09/22
'''
# ------------------------------------------------------------------------------
from pysetup      import DISABLE_COLORTERM                                                                              # pylint:disable=E0611
from pysetup.ansi import SGM_RE
from pysetup.ansi import SGM_FC_BLACK
from pysetup.ansi import SGM_FC_RED
from pysetup.ansi import SGM_FC_GREEN
from pysetup.ansi import SGM_FC_YELLOW
from pysetup.ansi import SGM_FC_BLUE
from pysetup.ansi import SGM_FC_MAGENTA
from pysetup.ansi import SGM_FC_CYAN
from pysetup.ansi import SGM_FC_WHITE
from pysetup.ansi import SGM_BC_BLACK
from pysetup.ansi import SGM_BC_RED
from pysetup.ansi import SGM_BC_GREEN
from pysetup.ansi import SGM_BC_YELLOW
from pysetup.ansi import SGM_BC_BLUE
from pysetup.ansi import SGM_BC_MAGENTA
from pysetup.ansi import SGM_BC_CYAN
from pysetup.ansi import SGM_BC_WHITE
from pysetup.ansi import ESCAPE
from pysetup.ansi import SGM_TA_BOLD
from os           import getenv
import re
import sys
# ------------------------------------------------------------------------------

class AbstractConsole(object):
    '''
    Console Interface
    '''
    def __init__(self,
                 stdout = sys.stdout,
                 stderr = sys.stderr):
        '''
        Constructor

        @option stdout [in] (FileObject) output stream
        @option stderr [in] (FileObject) error stream
        '''
        self._stdout = stdout
        self._stderr = stderr
    # end def __init__

    # Why this length ? to fit with CMD.exe width !
    _HR = '-' * 77

    def echoTitle(self, msg):
        '''
        Echo the message on the output stream, Title format

        @param  msg [in] (str)  title text
        '''
        raise NotImplementedError
    # end def echoTitle

    def echoTrace(self, msg, newline = True):
        '''
        Echo the message on the output stream, Trace format

        @param  msg      [in] (str)  trace text
        @option newline  [in] (bool) echo or not a trailing newline
        '''
        raise NotImplementedError
    # end def echoTrace

    def echo(self, msg, newline = True):
        '''
        Echo the message on the output stream

        @param  msg      [in] (str) text
        @option newline  [in] (bool) echo or not a trailing newline
        '''
        raise NotImplementedError
    # end def echo

    def echoError(self, msg, newline = True):
        '''
        Echo the message on the error stream

        @param  msg      [in] (str) text
        @option newline  [in] (bool) echo or not a trailing newline
        '''
        raise NotImplementedError
    # end def echoError

    def exit(self, arg = None):
        '''
        Exit from Python

        @option arg [in] (int, str) status or message (echoed on the error stream,
                                                       status = 1)
        '''
        raise NotImplementedError
    # end def exit

# end class AbstractConsole

class RawConsole(AbstractConsole):
    '''
    Basic text console

    On xterm family console, display also ansi escape sequences.
    '''
    def __init__(self,
                 stdout  = sys.stdout,
                 stderr  = sys.stderr):
        '''
        @copydoc pysetup.console.AbstractConsole.__init__
        '''
        super(RawConsole, self).__init__(stdout, stderr)
    # end def __init__

    def echoTitle(self, msg):
        '''
        @copydoc pysetup.console.AbstractConsole.echoTitle
        '''
        self.echoTrace('\n'.join([self._HR, msg, self._HR]))
    # end def echoTitle

    _RE_NEWLINE = re.compile('([\n\r]+)')

    def echoTrace(self, msg, newline = True):
        '''
        @copydoc pysetup.console.AbstractConsole.echoTrace
        '''
        self.echo('# %s' % (self._RE_NEWLINE.sub('\n# ', msg),), newline)
    # end def echoTrace

    def echo(self, msg, newline = True):
        '''
        @copydoc pysetup.console.AbstractConsole.echo
        '''
        self._stdout.write((newline and (msg + '\n')) or msg)
        self._stdout.flush()
    # end def echo

    def echoError(self, msg, newline = True):
        '''
        @copydoc pysetup.console.AbstractConsole.echoError
        '''
        self._stderr.write('! %s' % ((newline and (msg + '\n')) or msg))
        self._stderr.flush()
    # end def echoError

    def exit(self, arg = None):
        '''
        @copydoc pysetup.console.AbstractConsole.exit
        '''
        if (arg):
            if (isinstance(arg, int)):
                status = arg
            else:
                self.echoError(arg)
                status = 1
            # end if
        else:
            status = 0
        # end if
        exit(status)
    # end def exit

# end class RawConsole

class BaseConsole(RawConsole):
    '''
    Deprecated implementation
    '''
    def __init__(self,
                 stdout  = sys.stdout,
                 stderr  = sys.stderr):
        '''
        @copydoc pysetup.console.AbstractConsole.__init__
        '''
        from warnings import warn
        warn('BaseConsole has been renamed RawConsole', DeprecationWarning, stacklevel=2)

        super(BaseConsole, self).__init__(stdout, stderr)
    # end def __init__
# end class BaseConsole

class PlainConsole(RawConsole):
    '''
    Enhanced text console (without ansi sequences)
    '''
    def __init__(self,
                 stdout  = sys.stdout,
                 stderr  = sys.stderr):
        '''
        @copydoc pysetup.console.AbstractConsole.__init__
        '''
        super(PlainConsole, self).__init__(stdout, stderr)
    # end def __init__


    def echo(self, msg, newline = True):
        '''
        @copydoc pysetup.console.AbstractConsole.echo
        '''
        super(PlainConsole, self).echo(SGM_RE.sub('', msg),
                                       newline)
    # end def echo

    def echoError(self, msg, newline = True):
        '''
        @copydoc pysetup.console.AbstractConsole.echoError
        '''
        super(PlainConsole, self).echoError(SGM_RE.sub('', msg),
                                            newline)
    # end def echoError
# end class PlainConsole


if (sys.platform == 'win32'):

    from ctypes import Structure
    from ctypes import byref
    from ctypes import c_short  as _SHORT
    from ctypes import c_ushort as _WORD
    from ctypes import windll

    class _COORD(Structure):
        '''
        Definition from wincon.h

        @code
        typedef struct _COORD {
          SHORT X;
          SHORT Y;
        } COORD, *PCOORD;
        @endcode
        '''
        _fields_ = [('X', _SHORT),
                    ('Y', _SHORT)]
    # end class _COORD

    class _SMALL_RECT(Structure):
        '''
        Definition from wincon.h

        @code
        typedef struct _SMALL_RECT {
          SHORT Left;
          SHORT Top;
          SHORT Right;
          SHORT Bottom;
        } SMALL_RECT, *PSMALL_RECT;
        @endcode
        '''
        _fields_ = [('Left',   _SHORT),
                    ('Top',    _SHORT),
                    ('Right',  _SHORT),
                    ('Bottom', _SHORT)]
    # end class _SMALL_RECT

    class _CONSOLE_SCREEN_BUFFER_INFO(Structure):
        '''
        Definition from wincon.h

        @code
        typedef struct _CONSOLE_SCREEN_BUFFER_INFO {
          COORD dwSize;
          COORD dwCursorPosition;
          WORD  wAttributes;
          SMALL_RECT srWindow;
          COORD dwMaximumWindowSize;
        } CONSOLE_SCREEN_BUFFER_INFO,*PCONSOLE_SCREEN_BUFFER_INFO;
        @endcode
        '''
        _fields_ = [('dwSize',              _COORD),
                    ('dwCursorPosition',    _COORD),
                    ('wAttributes',         _WORD),
                    ('srWindow',            _SMALL_RECT),
                    ('dwMaximumWindowSize', _COORD)]
    # end class _CONSOLE_SCREEN_BUFFER_INFO

    class CmdConsole(RawConsole):
        '''
        Color text 'CMD.exe' console
        '''
        ##@name Foreground colors from wincon.h
        ##@{
        _FOREGROUND_BLACK     = 0x0000
        _FOREGROUND_BLUE      = 0x0001
        _FOREGROUND_GREEN     = 0x0002
        _FOREGROUND_CYAN      = 0x0003
        _FOREGROUND_RED       = 0x0004
        _FOREGROUND_MAGENTA   = 0x0005
        _FOREGROUND_YELLOW    = 0x0006
        _FOREGROUND_GREY      = 0x0007
        _FOREGROUND_INTENSITY = 0x0008 ##< foreground color is intensified.
        ##@}

        ## Foreground color dict: ansi 2 win
        A2F = {SGM_FC_BLACK   : _FOREGROUND_BLACK,
               SGM_FC_RED     : _FOREGROUND_RED,
               SGM_FC_GREEN   : _FOREGROUND_GREEN,
               SGM_FC_YELLOW  : _FOREGROUND_YELLOW,
               SGM_FC_BLUE    : _FOREGROUND_BLUE,
               SGM_FC_MAGENTA : _FOREGROUND_MAGENTA,
               SGM_FC_CYAN    : _FOREGROUND_CYAN,
               SGM_FC_WHITE   : _FOREGROUND_GREY}

        ##@name Background colors from wincon.h
        ##@{
        __BACKGROUND_BLACK     = 0x0000
        __BACKGROUND_BLUE      = 0x0010
        __BACKGROUND_GREEN     = 0x0020
        __BACKGROUND_CYAN      = 0x0030
        __BACKGROUND_RED       = 0x0040
        __BACKGROUND_MAGENTA   = 0x0050
        __BACKGROUND_YELLOW    = 0x0060
        __BACKGROUND_GREY      = 0x0070
        __BACKGROUND_INTENSITY = 0x0080 ##< background color is intensified.
        ##@}

        ## Background color dict: ansi 2 win
        A2B = {SGM_BC_BLACK   : __BACKGROUND_BLACK,
               SGM_BC_RED     : __BACKGROUND_RED,
               SGM_BC_GREEN   : __BACKGROUND_GREEN,
               SGM_BC_YELLOW  : __BACKGROUND_YELLOW,
               SGM_BC_BLUE    : __BACKGROUND_BLUE,
               SGM_BC_MAGENTA : __BACKGROUND_MAGENTA,
               SGM_BC_CYAN    : __BACKGROUND_CYAN,
               SGM_BC_WHITE   : __BACKGROUND_GREY}

        ##@name winbase.h
        ##@{
        __STD_INPUT_HANDLE  = -10 ##< stdin
        __STD_OUTPUT_HANDLE = -11 ##< stdout
        __STD_ERROR_HANDLE  = -12 ##< stderr
        ##@}

        def __init__(self,
                     stdout  = sys.stdout,
                     stderr  = sys.stderr):
            '''
            @copydoc pysetup.console.AbstractConsole.__init__
            '''
            self._errHandle = windll.kernel32.GetStdHandle(self.__STD_ERROR_HANDLE)                                     # @UndefinedVariable
            self._outHandle = windll.kernel32.GetStdHandle(self.__STD_OUTPUT_HANDLE)                                    # @UndefinedVariable

            # Get default colors
            csbi = _CONSOLE_SCREEN_BUFFER_INFO()
            windll.kernel32.GetConsoleScreenBufferInfo(self._outHandle, byref(csbi))                                    # @UndefinedVariable
            self._default = csbi.wAttributes
            self._colors  = csbi.wAttributes

            self._setConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute                                     # @UndefinedVariable

            super(CmdConsole, self).__init__(stdout, stderr)
        # end def __init__

        def _print(self, msg, std):
            '''
            Translate SGM Ansi sequences into ConsoleTextAttribute and print

            @param  msg [in] (str) text
            @param  std [in] (FileObject) stream
            '''
            for seq in SGM_RE.split(msg):
                if (seq == ''):
                    continue
                # end if

                if seq.startswith(ESCAPE):

                    if (seq == '\x1B\x5B0m'):
                        self._colors = self._default

                    else:
                        for value in [int(value) for value in seq[2:-1].split(';')]:

                            if (value == SGM_TA_BOLD):
                                self._colors = self._colors | self._FOREGROUND_INTENSITY

                            elif (value in self.A2F):
                                self._colors = (  (self._FOREGROUND_GREY & self.A2F[value])
                                               | (~self._FOREGROUND_GREY & self._colors))

                            elif (value in self.A2B):
                                self._colors = (  (self.__BACKGROUND_GREY & self.A2B[value])
                                               | (~self.__BACKGROUND_GREY & self._colors))
                            # end if
                        # end for
                    # end if
                    self._setConsoleTextAttribute(self._outHandle,
                                                  self._colors)
                else:
                    std.write(seq)
                    std.flush()
                # end if
            # end for
        # end def _print

        def echo(self, msg, newline = True):
            '''
            @copydoc pysetup.console.AbstractConsole.echo
            '''
            self._print((newline and (msg + '\n')) or msg,
                        self._stdout)
        # end def echo

        def echoError(self, msg, newline = True):
            '''
            @copydoc pysetup.console.AbstractConsole.echoError
            '''
            self._print('! %s' % ((newline and (msg + '\n')) or msg,),
                        self._stdout)
        # end def echoError

        def __del__(self):
            ''' Destructor '''
            self._setConsoleTextAttribute(self._outHandle,
                                          self._default)
        # end def __del__

    # end class CmdConsole
# end if

def ColorConsole(stdout  = sys.stdout,                                                                                  # pylint:disable=C0103
                 stderr  = sys.stderr):
    '''
    Color text console factory

    Depending on platform/term @& DISABLE_COLORTERM constant, return:
    - CmdConsole
    - PlainConsole
    - RawConsole
    .

    @option stdout [in] (FileObject) output stream
    @option stderr [in] (FileObject) error stream

    @return color console
    '''
    if (DISABLE_COLORTERM != 'True'):
        if (getenv('COLORTERM')):
            return RawConsole(stdout, stderr)

        elif (sys.platform == 'win32'):
            return CmdConsole(stdout, stderr)

        # end if
    # end if

    return PlainConsole(stdout, stderr)
# end def ColorConsole

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
