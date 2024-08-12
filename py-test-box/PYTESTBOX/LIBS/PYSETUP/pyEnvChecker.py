#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
# pylint:disable=C0103
"""
@package pyEnvChecker

@brief   Check Environment

@author  christophe roquebert

@date    2018/09/19
"""
# ------------------------------------------------------------------------------
# Check Python version
# ------------------------------------------------------------------------------
import sys


if (sys.version_info < (3, 6)) or (sys.version_info >= (4, 0)):
    sys.exit(f"""
pyEnvChecker failed:
- Expected Python versions: 3.6.6 [or 3.7]
- Current Python version:   {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}
""")
# end if

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from argparse import ArgumentParser
from copy import deepcopy
from getpass import getuser
from glob import glob
from hashlib import md5
from os import environ
from os import getcwd
from os import getenv
from os import mkdir
from os import name as OS_NAME
from os import stat
from os import walk
from os.path import abspath
from os.path import basename
from os.path import dirname
from os.path import exists
from os.path import isabs
from os.path import isdir
from os.path import isfile
from os.path import join
from os.path import normpath
from os.path import pathsep
from os.path import splitdrive
from os.path import splitext
from platform import python_implementation
from platform import python_version
from platform import uname
from shutil import rmtree
from sqlite3 import connect
from subprocess import PIPE
from subprocess import Popen
from tempfile import TemporaryFile
from time import strftime
from urllib.error import URLError
from urllib.request import urlopen
import re


# ------------------------------------------------------------------------------
# platform specific imports
# ------------------------------------------------------------------------------
SYSTEM_NAME = uname()[0]

if SYSTEM_NAME == 'Windows':
    try:
        # pylint:disable=F0401
        from win32api import GetFileVersionInfo
        from win32api import RegCloseKey
        from win32api import RegEnumValue
        from win32api import RegOpenKey
        from win32api import RegQueryInfoKey
        from win32api import error as WinError
        from win32con import HKEY_CLASSES_ROOT
        from win32con import HKEY_CURRENT_CONFIG
        from win32con import HKEY_CURRENT_USER
        from win32con import HKEY_LOCAL_MACHINE
        from win32con import HKEY_USERS


        # pylint:enable=F0401
        PyWin32 = True
    except ImportError:
        PyWin32 = False
    # end try
elif SYSTEM_NAME == 'Darwin':
    from xml.dom.minidom import parse
# end if


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
CONFIG_INI = 'Config.ini'
REM_END_OF_FILE_TEXT = """
REM ----------------------------------------------------------------------------
REM END OF FILE
REM ----------------------------------------------------------------------------
"""
END_OF_FILE_TEXT = """
# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
"""

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class Term(object):
    """
    xterm family console
    """
    # Cursor position regexp
    _CP_RE = re.compile(r'(\x1B\x5B[\d;\d]?[Hf])')
    # Set graphic mode regexp
    _SGM_RE = re.compile(r'(\x1B\x5B[\d;]+m)')

    # @name Set Graphics Mode / Text attributes
    # @{
    # All attributes off
    _SGM_TA_OFF = 0
    # Bold on
    _SGM_TA_BOLD = 1
    # Underscore (on monochrome display adapter only)
    _SGM_TA_UNDERSCORE = 4
    # Blink on
    _SGM_TA_BLINK = 5
    # Reverse video on
    _SGM_TA_REVERSE = 7
    # Concealed on
    _SGM_TA_CONCEALED = 8
    # @}

    # @name Set Graphics Mode / Foreground colors
    # @{
    _SGM_FC_BLACK = 30
    _SGM_FC_RED = 31
    _SGM_FC_GREEN = 32
    _SGM_FC_YELLOW = 33
    _SGM_FC_BLUE = 34
    _SGM_FC_MAGENTA = 35
    _SGM_FC_CYAN = 36
    _SGM_FC_WHITE = 37
    # @}

    setGraphicMode = lambda *args: f'\x1B\x5B{(";".join([str(arg) for arg in args]))}m'

    # @name Colors
    # @{
    OFF = setGraphicMode(_SGM_TA_OFF)
    RED = setGraphicMode(_SGM_TA_BOLD, _SGM_FC_RED)
    CYAN = setGraphicMode(_SGM_TA_BOLD, _SGM_FC_CYAN)
    GREEN = setGraphicMode(_SGM_TA_BOLD, _SGM_FC_GREEN)
    YELLOW = setGraphicMode(_SGM_TA_BOLD, _SGM_FC_YELLOW)
    MAGENTA = setGraphicMode(_SGM_FC_MAGENTA)
    # @}

    # Why this length? to fit with CMD.exe width!
    HR = '-' * 77

    def __init__(self, stdout=sys.stdout, stderr=sys.stderr):
        """
        Constructor
        @param stdout [in] (FileObject) output stream
        @param stderr [in] (FileObject) error stream
        """
        self._stdout = stdout
        self._stderr = stderr
        self._color = ((getenv('COLORTERM') is not None)
                       or (getenv('TERM', '').startswith('xterm')))
    # end def __init__

    def disableColor(self):
        """
        Disable output color
        """
        self._color = False
    # end def disableColor

    def echoOut(self, msg, end='\n'):
        """
        Echo message to stdout
        @param msg [in] (str)  text
        @param end [in] (str)  end of line
        """
        self._echo(self._stdout, msg + end)
    # end def echoOut

    def _echo(self, std, msg):
        """
        Echo message
        @param std [in] (File) object
        @param msg [in] (str)  text
        """
        std.write(msg if self._color else self._SGM_RE.sub('', msg))
        std.flush()
    # end def _echo

    def echoErr(self, msg, end='\n'):
        """
        Echo message to stderr
        @param msg [in] (str)  text
        @param end [in] (str)  end of line
        """
        self._echo(self._stderr, msg + end)
    # end def echoErr
# end class Term


if OS_NAME == 'nt':

    from ctypes import Structure
    from ctypes import c_short as _SHORT
    from ctypes import c_ushort as _WORD
    from ctypes import byref
    from ctypes import windll


    class _COORD(Structure):
        """
        Definition from wincon.h
        """
        _fields_ = [('X', _SHORT), ('Y', _SHORT)]
    # end class _COORD

    class _SMALL_RECT(Structure):
        """
        Definition from wincon.h
        """
        _fields_ = [('Left', _SHORT), ('Top', _SHORT),
                    ('Right', _SHORT), ('Bottom', _SHORT)]
    # end class _SMALL_RECT

    class _CONSOLE_SCREEN_BUFFER_INFO(Structure):
        """
        Definition from wincon.h
        """
        _fields_ = [('dwSize', _COORD),
                    ('dwCursorPosition', _COORD),
                    ('wAttributes', _WORD),
                    ('srWindow', _SMALL_RECT),
                    ('dwMaximumWindowSize', _COORD)]
    # end class _CONSOLE_SCREEN_BUFFER_INFO

    class Cmd(Term):
        """
        Color text 'CMD.exe' console
        """
        # pylint:disable=E0602, W0212

        # @name Foreground colors from wincon.h
        # @{
        _FOREGROUND_BLACK = 0x0000
        _FOREGROUND_BLUE = 0x0001
        _FOREGROUND_GREEN = 0x0002
        _FOREGROUND_CYAN = 0x0003
        _FOREGROUND_RED = 0x0004
        _FOREGROUND_MAGENTA = 0x0005
        _FOREGROUND_YELLOW = 0x0006
        _FOREGROUND_GREY = 0x0007
        # foreground color is intensified.
        _FOREGROUND_INTENSITY = 0x0008
        # @}

        #  Foreground color dict: ansi 2 win
        A2F = {Term._SGM_FC_BLACK  : _FOREGROUND_BLACK,
               Term._SGM_FC_RED    : _FOREGROUND_RED,
               Term._SGM_FC_GREEN  : _FOREGROUND_GREEN,
               Term._SGM_FC_YELLOW : _FOREGROUND_YELLOW,
               Term._SGM_FC_BLUE   : _FOREGROUND_BLUE,
               Term._SGM_FC_MAGENTA: _FOREGROUND_MAGENTA,
               Term._SGM_FC_CYAN   : _FOREGROUND_CYAN,
               Term._SGM_FC_WHITE  : _FOREGROUND_GREY}

        def __init__(self, stdout=sys.stdout, stderr=sys.stderr):
            """
            @copydoc pyEnvChecker.Term.__init__
            """
            super(Cmd, self).__init__(stdout, stderr)
            self._color = True

            self._outHandle = windll.kernel32.GetStdHandle(-11)
            self._errHandle = windll.kernel32.GetStdHandle(-12)

            # Get default colors
            csbi = _CONSOLE_SCREEN_BUFFER_INFO()
            windll.kernel32.GetConsoleScreenBufferInfo(self._outHandle, byref(csbi))
            self._default = csbi.wAttributes
            self._colors = csbi.wAttributes

            self._setConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
        # end def __init__

        def __del__(self):
            """
            Destructor
            """
            self._setConsoleTextAttribute(self._outHandle, self._default)
        # end def __del__

        def _echo(self, std, msg):
            """
            @copydoc pyEnvChecker.Term._echo
            """
            hdl = self._errHandle if std == self._stderr else self._outHandle

            for seq in self._SGM_RE.split(msg if self._color else self._SGM_RE.sub('', msg)):

                if seq.startswith('\x1B'):
                    if seq == '\x1B\x5B0m':
                        self._colors = self._default
                    else:
                        for value in [int(value) for value in seq[2:-1].split(';')]:

                            if value == self._SGM_TA_BOLD:
                                self._colors = self._colors | self._FOREGROUND_INTENSITY

                            elif value in self.A2F:
                                self._colors = ((self._FOREGROUND_GREY & self.A2F[value])
                                                | (~self._FOREGROUND_GREY & self._colors))
                            # end if
                        # end for
                    # end if
                    self._setConsoleTextAttribute(hdl, self._colors)
                else:
                    std.write(seq)
                    std.flush()
                # end if
            # end for
        # end def _echo

        # pylint: enable=E0602, W0212
    # end class Cmd
# end if


class Logger(object):
    """
    Logger
    """

    def __init__(self):
        """
        Constructor
        """
        self._console = (Cmd if ((OS_NAME == 'nt') and (
                (getenv('COLORTERM') is None) and (not getenv('TERM', '').startswith('xterm')))) else Term)(
                sys.stdout, sys.stderr)
        self._level = 1
    # end def __init__

    def _echo(self, level, msg, end='\n'):
        """
        Echo mssage according to level
        @param level [in] (int) verbosity
        @param msg   [in] (str) text
        @param end   [in] (str) of line
        """
        if self._level >= level:
            self._console.echoOut(msg, end=end)
        # end if
    # end def _echo

    def error(self, msg):
        """
        Echo error
        @param msg   [in] (str) text
        """
        self._console.echoErr(f'  {Term.RED}{msg}{Term.OFF}')
    # end def error

    def debug(self, level, msg, end='\n'):
        """
        Echo debug info
        @param level [in] (int)  minimum
        @param msg   [in] (str)  text
        @param end   [in] (str)  of line
        """
        self._echo(level, msg, end)
    # end def debug

    def detail(self, msg, end='\n'):
        """
        Echo trace
        @param msg [in] (str) text
        @param end [in] (str) of line
        """
        self._echo(2, f'{msg}', end)
    # end def detail

    def trace(self, msg):
        """
        Echo trace
        @param msg [in] (str) text
        """
        msg = msg.replace('\n', '\n# ')
        self._echo(1, f"# {msg}")
    # end def trace

    def title(self, msg):
        """
        Echo title
        @param msg [in] (str)     text
        """
        msg = msg.replace('\n', '\n# ')
        self._echo(1, f'# {Term.HR}\n# {msg}\n# {Term.HR}')
    # end def title

    def setLevel(self, value):
        """
        Sets the threshold
        @param value [in] (int) threshold
        """
        self._level = value
    # end def setLevel
# end class Logger


class Html(object):
    """
    Html constants
    """
    RED = '#F08080'
    CYAN = '#D5E1E8'
    GREEN = '#90EE90'
    YELLOW = '#F4A460'

    # Reserved Characters in HTML
    _C2E = {
            '"': '&quot;', "'": '&apos;',
            '<': '&lt;', '>': '&gt;',
            '&': '&amp;',
            # ISO 8859-1 Symbols
            '©': '&copy;', '®': '&reg;'}

    @classmethod
    def txt2html(cls, msg):
        """
        Convert characters into HTML Entity Name
        @param msg [in] (str) txt
        @return (str) html
        """
        return ''.join([cls._C2E.get(c, c) for c in str(msg)]) if msg else '&nbsp;'
    # end def txt2html

    @staticmethod
    def url2txt(address):
        """
        Convert @%code into characters
        @param address [in] (str) url
        @return (str) txt
        """
        return address.replace('%20', ' ')
    # end def url2txt
# end class Html


class Misc(object):
    """
    Utilities
    """

    @staticmethod
    def getHash(path):
        """
        Compute hash from path (and attributes)
        @param path [in] (str) dirname/filename
        @return (str, None) hash
        """
        if not exists(path):
            return
        # end if

        m = md5()
        m.update(path.encode('utf-8'))
        if isfile(path):
            s = stat(path)
            m.update(str(s.st_size).encode('utf-8'))
            m.update(str(s.st_mtime).encode('utf-8'))
        # end if
        return m.hexdigest()  # pylint:disable=E1121
    # end def getHash

    @staticmethod
    def pathify(msg):
        """
        Replace unexpected path characters by '_'
        @param msg [in] (str) text
        @return (str)
        """
        return re.sub('[\\/:*?"<>|]+', '_', msg)
    # end def pathify

    @staticmethod
    def slashify(msg, esc=False):
        """
        Replace backward slashes
        @param msg [in] (str)  text
        @param esc [in] (bool) to escape '\'
        @return (str)
        """
        if not msg:
            msg = ''
        # end if

        # C:\\dir --> C:/dir
        if isabs(msg):
            return msg.replace('\\', '/')
        # end if

        if esc:
            return msg.replace('\\', '\\\\')
        # end if

        return msg
    # end def slashify
# end class Misc


class Cache(object):
    """
    Cache
    """

    def __init__(self, dev_path, user_py_setup_path):
        """
        Constructor
        @param dev_path           [in] (str) path
        @param user_py_setup_path [in] (str) path
        """
        self._dev_path = dev_path

        self._database_py_setup = join(user_py_setup_path, f'.{Misc.getHash(user_py_setup_path)}')

        self._cache_py_setup = dict()
        self._cache_project = dict()
    # end def __init__

    def __getitem__(self, key):
        """
        Implement evaluation of self[key]
        @param key [in] (str) path / entry_name
        @return value
        """
        return self._cache_py_setup.get(key, self._cache_project.get(key))
    # end def __getitem__

    def __setitem__(self, key, value):
        """
        Implement evaluation of self[key] = value
        @param key   [in] (str) path / entry_name
        @param value [in] (all) versions / path
        """
        if key.startswith(self._dev_path):
            self._cache_project[key] = value
        else:
            self._cache_py_setup[key] = value
        # end if
    # end def __setitem__

    def load(self):
        """
        Load cache
        """
        self._cache_py_setup = self._read(self._database_py_setup)
    # end def load

    @staticmethod
    def _read(database):
        """
        Read database
        @param database [in] (str) path
        @return (dict)
        """
        cache = dict()

        with connect(database, timeout=10) as con:
            con.text_factory = str
            cur = con.cursor()

            cur.execute(
                    'CREATE TABLE IF NOT EXISTS Version (Path TEXT PRIMARY KEY, Hash TEXT, Value TEXT, Summary TEXT, '
                    'Comments TEXT);')
            cur.execute('SELECT * FROM Version;')
            #  {Path: (Hash, Value,  Summary, Comments)}
            cache.update([(row[0], (row[1], row[2], row[3], row[4])) for row in cur.fetchall()])

            cur.execute('CREATE TABLE IF NOT EXISTS Entry   (Name TEXT PRIMARY KEY, Value TEXT);')
            cur.execute('SELECT * FROM Entry;')
            # {Name: Value}
            cache.update([(row[0], row[1]) for row in cur.fetchall()])
        # end with

        return cache
    # end def _read

    def save(self):
        """
        Save cache
        """
        self._write(self._database_py_setup, self._cache_py_setup)
    # end def save

    @staticmethod
    def _write(database, cache):
        """
        Write cache into database
        @param database [in] (str)  path
        @param cache    [in] (dict) data
        """
        with connect(database, timeout=10) as con:
            con.text_factory = str
            cur = con.cursor()

            cur.execute(
                    'CREATE TABLE IF NOT EXISTS Version (Path TEXT PRIMARY KEY, Hash  TEXT, Value TEXT, Summary TEXT, '
                    'Comments TEXT);')
            cur.execute('CREATE TABLE IF NOT EXISTS Entry   (Name TEXT PRIMARY KEY, Value TEXT);')

            for k, v in cache.items():

                if isinstance(v, tuple):
                    cur.execute(
                            'INSERT OR IGNORE INTO  Version (Path, Hash, Value, Summary, Comments) VALUES (?, ?, ?, '
                            '?, ?);',
                            (k, v[0], v[1], v[2], v[3]))
                    cur.execute('UPDATE Version SET Hash=?, Value=?, Summary=?, Comments=? WHERE Path=?;',
                                (v[0], v[1], v[2], v[3], k))
                else:
                    cur.execute('INSERT OR IGNORE INTO  Entry (Name,   Value)  VALUES (?, ?);', (k, v))
                    cur.execute('UPDATE Entry SET Value=? WHERE Name=?;', (v, k))
                # end if
            # end for

        # end with
    # end def _write

    def clean(self, level):
        """
        Clean cache
        @param level [in] (int) 1=Project / 2=PySetup
        """
        if level > 0:
            self._clean(self._databaseProject)
        # end if

        if level > 1:
            self._clean(self._database_py_setup)
        # end if
    # end def clean

    @staticmethod
    def _clean(database):
        """
        Clean database
        @param database [in] (str) path
        """
        with connect(database, timeout=10) as con:
            cur = con.cursor()
            cur.execute('DROP TABLE IF EXISTS Version;')
            cur.execute('DROP TABLE IF EXISTS Entry;')
        # end with
    # end def _clean
# end class Cache


class CheckEnv(object):
    """
    Check the project environment setup
    """
    # @name Properties (Application Name, Application Description, Application Version, PySetup Version)
    # @{
    _NAME = 'CheckEnv'
    _BRIEF = 'Check Local Environment'
    _VERSION = '2.1.0.0'
    _PYSETUP = '2018.10'
    # @}

    _PROJECT_PATH = None
    _ENV_PATHS = None
    _STR_PATHS = None

    def __init__(self, dev_path, project=None):
        """
        Constructor

        @param dev_path  [in] (str)  .../PYTESTBOX
        @param project  [in] (str) name
        """
        self._context = self.Context(dev_path, project)
        self._logger = Logger()

        # Data
        self._configs = list()
        self._entries = dict()
        self._knowledges = dict()

        # Results
        self._score = 0
        self._success = 0
        self._failures = list()
        self._errors = list()
        self._status = 0
    # end def __init__

    def run(self, profiles=list(), clean=0,  # pylint:disable=W0102,W8201
            verbose=0, minimum=False, test=False, pause=False):
        """
        Check the environment setup

        @param profiles [in] (list) of configs
        @param clean    [in] (int)  level
        @param verbose  [in] (int)  level
        @param minimum  [in] (bool) profile
        @param test     [in] (bool) instead of check
        @param pause    [in] (bool) at the end of the process
        @return (int) status
        """
        # Clean
        if clean > 0:
            self._context.clean(clean)
            return 0
        # end if

        # Verbose level
        self._logger.setLevel(verbose)

        # Profile
        if minimum or profiles:
            profiles.insert(0, '#Minimum')
        # end if
        profile = ' + '.join((f'{name[1:]}' for name in profiles if name.startswith('#')))

        # Header
        self._echoHeader(profile, test)

        # Read
        self._discover_configs(profiles)

        # Check
        test |= self._check_entries()

        # Write
        if test:
            self._context.clean(0)
            self._write_test_html(profile)
        else:
            self._write_local(profile)
        # end if

        # Footer
        self._echo_footer(profile, test)

        # Pause
        if (self._score != 100.0) and pause:
            self._logger.detail('%78s' % ('Press <ENTER> to exit...',), '')
            input()
        # end if

        # Status
        if self._errors and self._entries[self._errors[-1]].u_exit:
            return 3
        elif self._errors:
            return 2
        elif self._failures:
            return 1
        else:
            return 0
        # end if
    # end def run

    def _echoHeader(self, profile, test):
        """
        Echo header information

        @param profile [in] (str)  title
        @param test    [in] (bool) or check
        """
        t_val = "Testing" if test else "Checking"
        p_val = f'\nProfile: {profile}' if profile else ''
        self._logger.title(f'{t_val} {self._context.project_name} environment setup{p_val}')
    # end def _echoHeader

    class Entry(object):  # pylint:disable=R0902
        """
        Entry
        """
        # @name Type
        # @{
        #  Constant
        TYPE_C = 'C'
        # Application
        TYPE_A = 'A'
        # Directory
        TYPE_D = 'D'
        # file Exists
        TYPE_E = 'E'
        # regular File
        TYPE_F = 'F'
        # Knowledge base
        TYPE_K = 'K'
        # Package
        TYPE_P = 'P'
        # environment Variable
        TYPE_V = 'V'
        # @}

        # @name Status
        # @{
        STATUS_P = 0  # CheckInProgress
        STATUS_S = 1  # Success
        STATUS_F = 2  # Failure
        STATUS_E = 3  # Error
        STATUS_K = 4  # Skipped
        # @}

        # Name<-py*> --> Name-py*
        _RE_ALIAS = re.compile(r'[<>]')

        # Name<-py*> --> Name
        _RE_NAME = re.compile(r'<.+?>')

        # Name.ext   --> Name_ext
        _RE_WNAME = re.compile(r'\W+')

        def __init__(self, section, options):
            """
            Constructor

            @param section [in] (str)  [SECTION]
            @param options [in] (dict) option = value
            """
            # Source
            self.ini_file = options.pop('_ini_file', None)
            self.ini_line = options.pop('_ini_line', None)

            # Type|Name
            # Type|Name|Ext
            # ------------------------------------------------------------------
            sections = section.split('|')

            # Type
            self.type = sections[0]

            # Alias
            alias = sections[1]
            root, ext = splitext(self._RE_NAME.sub('', sections[1]))

            # Name
            if 'name' in options:
                names = [options.pop('name'), ]
            else:
                # A|name.ext --> name --> NAME
                names = [root if (self.type == self.TYPE_A) else root + ext, ]
            # end if

            # name --> prefix_name --> PREFIX_NAME
            if 'prefix' in options:
                names.insert(0, options.pop('prefix'))
            # end if

            # D|name --> name_PATH --> NAME_PATH
            if self.type == self.TYPE_D:
                names.append('PATH')
            # end if

            # 7-Zip --> D7-Zip --> D7_ZIP
            if names[0][0] in '0123456789':
                names[0] = 'D' + names[0]
            # end if

            # My Name-X++.ext --> MY_NAME_XPP_EXT
            self.name = self._RE_WNAME.sub('_', '_'.join(names).replace('+', 'P').upper())

            self.summary = options.pop('summary', None)

            # Ext
            self.ext = '.' + sections[2] if len(sections) > 2 else ext

            # Updates
            # ------------------------------------------------------------------
            self.u_inis = list()
            self.u_aliases = [self._getAlias(alias), ]
            self.u_options = None
            self.u_exit = None

            self.u_values = None
            self.u_value_cmd = None
            self.u_value_cwd = None

            self.u_dirnames = None
            self.u_dirname_cwd = None

            self.u_version_exe = None
            self.u_version_opt = None
            self.u_version_cmd = None
            self.u_version_cwd = None

            self.u_version_txt = None
            self.u_version_pat = None
            self.u_version_rec = None
            self.u_version_fld = None

            self.u_version_min = None
            self.u_version_not = None
            self.u_version_max = None
            self.u_version = None

            self.u_href = None
            self.u_title = None

            # Results
            # ------------------------------------------------------------------
            self.value = None
            # From win32 resources
            self.comments = None
            self.version = None

            self.status = None
            self.failure = None
            self.error = None
        # end def __init__

        def __repr__(self):
            """
            Representation of an Entry

            @return (str) representation
            """
            return '\n'.join((f'{k:<14}: {self.__dict__[k]}'
                              for k in sorted(self.__dict__.keys())))
        # end def __repr__

        @staticmethod
        def _getAlias(name):
            """
            Retrieve alias from name

            @param name [in] (str) root.ext
            @return alias
            """
            alias = CheckEnv.Entry._RE_ALIAS.sub('', name)  # pylint:disable=W0212
            # system nt:    name.exe / name.bat / name.cmd
            # system posix: name
            if OS_NAME != 'nt':
                root, ext = splitext(alias)
                if ext in ('.exe', '.bat', '.cmd'):
                    return root
                # end if
            # end if
            return alias
        # end def _getAlias

        @staticmethod
        def _str2list(value):
            """
            Split value

            @param value [in] (str) '|' separated
            @return (tuple) of str
            """
            items = list()

            for item in value.replace('\n', '').split('|'):
                item = item.strip()
                if item != '':
                    items.append(item)
                # end if
            # end for

            return items
        # end def _str2list

        def update(self, ini, options):  # pylint:disable=R0912
            """
            Update values

            @param ini     [in] (str)  path
            @param options [in] (dict) values
            """
            if 'entry_href' in options:
                self.u_href = options['entry_href']
            # end if

            if 'entry_title' in options:
                self.u_title = options['entry_title']
            # end if

            if ini is None:
                return
            # end if

            self.u_inis.append(ini)
            cwd = dirname(ini)

            if 'alias' in options:
                self.u_aliases[1:] = [self._getAlias(name) for name in self._str2list(options['alias'])]
            # end if

            if 'exit' in options:
                self.u_exit = options['exit']
            # end if

            if 'option' in options:
                self.u_options = self._str2list(options['option'])
            # end if

            if 'value' in options:
                self.u_values = self._str2list(
                        options['value'].replace('${PATH}', CheckEnv._STR_PATHS))  # pylint:disable=W0212
                self.u_value_cwd = cwd
            # end if

            if 'value_cmd' in options:
                self.u_value_cmd = options['value_cmd']
                self.u_value_cwd = cwd
            # end if

            if 'dirname' in options:
                self.u_dirnames = self._str2list(
                        options['dirname'].replace('${PATH}', CheckEnv._STR_PATHS))  # pylint:disable=W0212
                self.u_dirname_cwd = cwd
            # end if

            if 'version_exe' in options:
                self.u_version_exe = options['version_exe']
                self.u_version_cwd = cwd
            # end if

            if 'version_opt' in options:
                self.u_version_opt = options['version_opt']
            # end if

            if 'version_cmd' in options:
                self.u_version_cmd = options['version_cmd']
                self.u_version_cwd = cwd
            # end if

            if 'version_txt' in options:
                self.u_version_txt = options['version_txt']
                self.u_version_cwd = cwd
            # end if

            if 'version_pat' in options:
                self.u_version_pat = options['version_pat']
            # end if

            if 'version_rec' in options:
                self.u_version_rec = options['version_rec']
            # end if

            if 'version_fld' in options:
                self.u_version_fld = options['version_fld']
            # end if

            if 'version_max' in options:
                self.u_version_max = min(options['version_max'], self.u_version_max) if self.u_version_max else options[
                    'version_max']
            # end if

            if 'version_not' in options:
                self.u_version_not = dict()

                for version_not in self._str2list(options['version_not']):
                    version = version_not.split(':', 1)
                    self.u_version_not[version[0].strip()] = version[1].strip() if (
                            len(version) > 1) else 'Not recommended'
                # end for
            # end if

            if 'version_min' in options:
                self.u_version_min = max(options['version_min'], self.u_version_min) if self.u_version_min else options[
                    'version_min']
            # end if

            if 'version' in options:
                self.u_version = options['version']
            # end if

        # end def update

        _S2H = {None    : Html.CYAN,
                STATUS_K: Html.CYAN,
                STATUS_S: Html.GREEN,
                STATUS_F: Html.YELLOW,
                STATUS_E: Html.RED}

        def get_color(self):
            """
            Get color from status

            @return (str) Html color
            """
            return self._S2H[self.status]
        # end def get_color

    # end class Entry

    class Config(object):
        """
        Config
        """

        def __init__(self, ini, summary, icon='Dir'):
            """
            Constructor

            @param ini     [in] (str) .../Config.ini
            @param summary [in] (str) description
            @param icon    [in] (str) for html output
            """
            self.ini = CheckEnv._devify(ini)  # pylint:disable=W0212
            self.summary = summary
            self.icon = icon
            self.entries = list()
        # end def __init__

        def __repr__(self):
            """
            Representation of a Config

            @return (str) representation
            """
            return '\n'.join((f'{k:<14}: {self.__dict__[k]}'
                              for k in sorted(self.__dict__.keys())))
        # end def __repr__

        def add(self, entry):
            """
            Add an entry

            @param entry [in] (str) name
            """
            for i, e in enumerate(self.entries):
                if entry.name < e.name:
                    self.entries.insert(i, entry)
                    break
                # end if
            else:
                self.entries.append(entry)
            # end for
        # end def add

    # end class Config

    class Context(object):
        """
        Context
        """
        def __init__(self, dev_path, project=None):
            """
            Constructor

            @param dev_path [in] (str) to determine PROJECT_PATH
            @param project [in] (str) to create Index.dxt
            """
            # pylint:disable=W0212
            CheckEnv._PROJECT_PATH = dev_path
            CheckEnv._ENV_PATHS = [normpath(join(splitdrive(path)[0].upper(), splitdrive(path)[1]))
                                   for path in getenv('PATH').split(pathsep)]
            CheckEnv._STR_PATHS = '|'.join(CheckEnv._ENV_PATHS)
            # pylint:enable=W0212

            # PYTESTBOX
            self.dev_path = dev_path

            # PYTESTBOX/LIBS
            self.tools_path = join(self.dev_path, 'LIBS')

            # PYTESTBOX/LIBS/PYSETUP
            self.pysetup_path = join(self.dev_path, 'LIBS', 'PYSETUP')

            # PYTESTBOX/LIBS/PROJECT
            self.project_path = join(self.dev_path, 'LIBS', 'PROJECT')
            self.project_name = project
            self.user_name = basename(getuser())

            # LIBS/PROJECT/ABOUT/Index.dxt
            self._create_index()

            # PYTESTBOX/LIBS/LOCAL
            self.local_path = join(self.dev_path, 'LIBS', 'LOCAL')
            self.local_about_path = join(self.local_path, 'ABOUT')
            self.local_img_path = join(self.local_path, 'IMG')
            self.local_tmp_path = join(self.local_path, 'TMP')

            # User
            self.user_py_setup_path = join(getenv('USERPROFILE' if (SYSTEM_NAME == 'Windows') else 'HOME'), '.PYSETUP')

            # Config.ini
            self.user_py_setup_config = join(self.user_py_setup_path, CONFIG_INI)
            self._create_configs()

            # Cache
            self.cache = Cache(self.dev_path, self.user_py_setup_path)

            # Binary paths
            if OS_NAME == 'nt':
                self.binPaths = ['C:\\Program Files', 'C:\\Program Files (x86)', getenv('SYSTEMROOT')]

                for drive in range(ord('D'), ord('Z') + 1):
                    for path in ['Prog', 'App']:
                        self.binPaths.append('%c:\\%s*' % (drive, path))
                    # end for
                # end for

            elif OS_NAME == 'posix':
                self.binPaths = ['/bin', '/usr/bin', '/usr/local/bin', '/sbin', '/usr/sbin', '/usr/local/sbin']

                if SYSTEM_NAME == 'Darwin':
                    self.binPaths.append('/Applications')
                # end if
            # end if

        # end def __init__

        def _create_index(self):
            """
            Create PROJECT/ABOUT/Index.dxt
            """
            index = join(self.dev_path, 'ABOUT', 'index.dxt')

            if isfile(index):

                re_project_name = re.compile(r'projectname\s+(.+)')

                with open(index, 'r') as fo:
                    for line in fo:

                        if not self.project_name:
                            mo = re_project_name.search(line)
                            if mo is not None:
                                self.project_name = mo.group(1).strip()
                                continue
                            # end if
                        # end if

                        if self.project_name:
                            break
                        # end if
                    # end for
                # end with
            else:

                while not self.project_name:
                    sys.stdout.write('Please enter the Project Name: ')
                    sys.stdout.flush()
                    self.project_name = input().strip()
                # end while

                with open(index, 'w') as fo:
                    fo.write(f"""
// -----------------------------------------------------------------------------
// \\projectname {self.project_name}
// -----------------------------------------------------------------------------
// Python Test Harness
// -----------------------------------------------------------------------------
// [Summary]   Index - {self.project_name} Project Main page
//
// [Author]  {self.user_name}
//
// [DateTime]    {strftime('%Y/%m/%d - %H:%M:%S')}
// -----------------------------------------------------------------------------
/*!
\\mainpage   \\projectname

\\section    S_ABOUT_OVERVIEW  Overview

-- Please, update project documentation here --
*/
// -----------------------------------------------------------------------------
// END OF FILE
// -----------------------------------------------------------------------------
""")
                # end with
            # end if
        # end def _create_index

        def _create_configs(self):
            """
            Create ~/.PYSETUP Configs
            """
            # ${USER_PATH}/.PYSETUP/Config.ini
            if not isdir(self.user_py_setup_path):
                mkdir(self.user_py_setup_path)
            # end if

            if not isfile(self.user_py_setup_config):
                with open(self.user_py_setup_config, 'w') as fo:
                    fo.write(f"""
; ------------------------------------------------------------------------------
; [Summary]   PYSETUP main config for {self.user_name}
; [Author]  {CheckEnv._NAME}
; [Version] {CheckEnv._VERSION}
; [DateTime]    {strftime('%Y/%m/%d - %H:%M:%S')}
; ------------------------------------------------------------------------------
[__CONFIG__]
summary = User PYSETUP config

; ------------------------------------------------------------------------------
; END OF FILE
; ------------------------------------------------------------------------------
""")
                # end with
            # end if
        # end def _create_configs

        def create_paths(self):
            """
            Create PYTESTBOX/LIBS/LOCAL paths
            """
            if not isdir(self.local_path):
                mkdir(self.local_path)
            # end if

            if not isdir(self.local_about_path):
                mkdir(self.local_about_path)
            # end if

            if not isdir(self.local_img_path):
                mkdir(self.local_img_path)
            # end if

            if not isdir(self.local_tmp_path):
                mkdir(self.local_tmp_path)
            # end if
        # end def create_paths

        def clean(self, level):
            """
            Clean context

            @param level [in] (int) of operation
            """
            # Remove LIBS/LOCAL files
            rmtree(self.local_path, True)

            self.cache.clean(level)
        # end def clean
    # end class Context

    def _discover_configs(self, profiles):  # pylint:disable=R0912,R0915
        """
        Read all Configs

        @param profiles [in] (list) of configs
        """
        self._logger.trace('Parsing Config.ini files')

        # Implicit Config - Identification
        # ----------------------------------------------------------------------
        check = self.Config(None, 'Project properties', 'Id')
        self._configs.append(check)

        index = join(self._context.project_path, 'ABOUT', 'Index.dxt')

        entry = self.Entry('C|PROJECT_NAME', {'summary': 'This project'})
        entry.u_inis = [index, ]
        entry.value = self._context.project_name
        entry.failure = None
        if not self._context.project_name:
            entry.failure = 'See PYSETUP-Manual to update LIBS/PROJECT/ABOUT/Index.dxt'
        # end if
        entry.status = entry.STATUS_S if self._context.project_name else entry.STATUS_F

        self._entries['PROJECT_NAME'] = entry
        check.entries.append(entry)

        entry = self.Entry('C|USER_NAME', {'summary': 'You'})
        entry.value = self._context.user_name
        entry.status = entry.STATUS_S

        self._entries['USER_NAME'] = entry
        check.entries.append(entry)

        entry = self.Entry('C|USER_PATH', {'summary': 'Your home directory'})
        entry.value = dirname(self._context.user_py_setup_path)
        entry.status = entry.STATUS_S

        self._entries['USER_PATH'] = entry
        check.entries.append(entry)

        # Implicit Config - Host properties
        # ----------------------------------------------------------------------
        check = self.Config(None, 'Host properties', 'Desktop')
        self._configs.append(check)

        entry = self.Entry('C|HOST_NAME', {'summary': "The computer's network name"})
        entry.value = uname()[1]
        entry.summary += f' [machine: {uname()[4]}]'
        entry.status = entry.STATUS_S

        self._entries['HOST_NAME'] = entry
        check.entries.append(entry)

        entry = self.Entry('C|OS_NAME', {'summary': "The operating system's name"})
        entry.value = OS_NAME
        entry.status = entry.STATUS_S
        self._entries['OS_NAME'] = entry
        check.entries.append(entry)

        entry = self.Entry('C|SYSTEM_NAME', {'summary': "The system's name"})

        entry.value = SYSTEM_NAME
        entry.version = uname()[2]
        entry.status = entry.STATUS_S

        if SYSTEM_NAME == 'Darwin':
            from platform import mac_ver

            entry.version = mac_ver()[0]

            v2n = {'10.5' : 'Leopard',
                   '10.6' : 'Snow Leopard',
                   '10.7' : 'Lion',
                   '10.8' : 'Mountain Lion',
                   '10.9' : 'Mavericks',
                   '10.10': 'Yosemite',
                   '10.11': 'El Capitan', }
            for version in v2n:
                if entry.version.startswith(version):
                    entry.summary += f' [codename: {v2n[version]}]'
                    break
                # end if
            # end for
        # end if

        self._entries['SYSTEM_NAME'] = entry
        check.entries.append(entry)

        if entry.value == 'Linux':
            import distro

            entry = self.Entry('C|DISTRO_NAME', {'summary': "The Linux distro's name"})

            entry.value = distro.id()
            entry.version = distro.version()
            if distro.name() != '':
                entry.summary += f' [codename: {distro.name()}]'
            # end if

            entry.status = entry.STATUS_S
            self._entries['DISTRO_NAME'] = entry
            check.entries.append(entry)
        # end if

        # Implicit Config - PySetup
        # ----------------------------------------------------------------------
        check = self.Config(None, 'PySetup', 'Tools')
        self._configs.append(check)

        entry = self.Entry('C|PYSETUP_DOC', {'summary': 'Distribution'})
        entry.value = 'CheckEnv'
        entry.version = self._PYSETUP
        entry.status = entry.STATUS_S
        self._entries['PYSETUP_DOC'] = entry
        check.entries.append(entry)

        entry = self.Entry('C|DISABLE_COLORTERM', {'summary': 'Disable color output of the console'})
        entry.u_values = (getenv('DISABLE_COLORTERM', '0'),)
        entry.status = entry.STATUS_S
        self._entries['DISABLE_COLORTERM'] = entry
        check.entries.append(entry)

        # Implicit Config - PySetup default paths
        # ----------------------------------------------------------------------
        check = self.Config(None, 'PySetup libraries paths')
        self._configs.append(check)

        entry = self.Entry('C|PROJECT_PATH', {'summary': 'Project Root path'})
        entry.value = self._context.dev_path
        entry.status = entry.STATUS_S
        self._entries['PROJECT_PATH'] = entry
        check.entries.append(entry)

        entry = self.Entry('C|LIBS_PATH', {'summary': 'LIBS root path'})
        entry.value = self._context.tools_path
        entry.status = entry.STATUS_S
        self._entries['LIBS_PATH'] = entry
        check.entries.append(entry)

        entry = self.Entry('C|LIBS_PYSETUP_PATH', {'summary': 'Generic PYSETUP tools'})
        entry.value = self._context.pysetup_path
        entry.status = entry.STATUS_S
        self._entries['LIBS_PYSETUP_PATH'] = entry
        check.entries.append(entry)

        entry = self.Entry('C|LIBS_PROJECT_PATH', {'summary': f'Specific {self._context.project_name} tools'})
        entry.value = self._context.project_path
        entry.status = entry.STATUS_S
        self._entries['LIBS_PROJECT_PATH'] = entry
        check.entries.append(entry)

        entry = self.Entry('C|LIBS_LOCAL_PATH', {'summary': 'Local configuration'})
        entry.value = self._context.local_path
        entry.status = entry.STATUS_S
        self._entries['LIBS_LOCAL_PATH'] = entry
        check.entries.append(entry)

        entry = self.Entry('C|LIBS_LOCAL_IMG_PATH',
                           {'summary': 'Local Image path for documentation (About, Doxygen...)'})
        entry.value = join(self._context.local_path, 'IMG')
        entry.status = entry.STATUS_S
        self._entries['LIBS_LOCAL_IMG_PATH'] = entry
        check.entries.append(entry)

        entry = self.Entry('C|LIBS_LOCAL_TMP_PATH', {'summary': 'Local Temporary path'})
        entry.value = join(self._context.local_path, 'TMP')
        entry.status = entry.STATUS_S
        self._entries['LIBS_LOCAL_TMP_PATH'] = entry
        check.entries.append(entry)

        entry = self.Entry('C|WORKING_PATH', {'summary': 'Unofficial release path'})
        entry.value = join(self._context.dev_path, 'WORKING')
        entry.status = entry.STATUS_S
        self._entries['WORKING_PATH'] = entry
        check.entries.append(entry)

        entry = self.Entry('C|TESTS_PATH', {'summary': 'Test suites path'})
        entry.value = join(self._context.dev_path, 'TESTS')
        entry.status = entry.STATUS_S
        self._entries['TESTS_PATH'] = entry
        check.entries.append(entry)

        entry = self.Entry('C|RELEASE_PATH', {'summary': 'Official release path'})
        entry.value = join(self._context.dev_path, 'RELEASE')
        entry.status = entry.STATUS_S
        self._entries['RELEASE_PATH'] = entry
        check.entries.append(entry)

        # Profiles
        # ----------------------------------------------------------------------
        if profiles:
            profiles.extend((join(self._context.pysetup_path, 'ABOUT', CONFIG_INI),
                             join(self._context.pysetup_path, 'PYENVCHECKER', CONFIG_INI),
                             join(self._context.pysetup_path, 'DOXYGEN', CONFIG_INI),
                             join(self._context.pysetup_path, 'ENV', 'DOXYGEN', CONFIG_INI),
                             join(self._context.pysetup_path, 'ENV', 'GRAPHVIZ', CONFIG_INI),
                             join(self._context.pysetup_path, 'ENV', 'MSCGEN', CONFIG_INI),
                             join(self._context.pysetup_path, 'ENV', 'PYTHON', CONFIG_INI),
                             join(self._context.pysetup_path, 'PYTHON', CONFIG_INI)))

            # Remove duplicates
            profiles = list(set(profiles))
        # end if

        # Project Configs
        # ----------------------------------------------------------------------
        top_paths = [join(self._context.dev_path, 'RELEASE'), join(self._context.dev_path, 'WORKING')]

        for top_path in [self._context.pysetup_path, self._context.project_path, self._context.tools_path,
                         self._context.dev_path]:

            for (dir_path, dir_names, file_names) in walk(top_path):

                # Skip path already walked
                if dir_path in top_paths:
                    dir_names[:] = []
                    continue
                # end if

                # Don't visit some directories
                for dir_name in [dirName for dirName in dir_names
                                 if (dirName.upper() in ['.SVN', 'CVS', 'LOCAL', 'WORKING'])]:
                    dir_names.remove(dir_name)
                # end for

                # Force alphabetical order
                dir_names.sort()
                file_names.sort()

                for file_name in file_names:
                    if file_name.startswith('Config') and file_name.endswith('.ini'):

                        ini = join(dir_path, file_name)

                        if profiles:
                            if ini in profiles:
                                skip_it = False
                                profiles.remove(ini)
                            else:
                                skip_it = True
                            # end if
                        else:
                            skip_it = False
                        # end if

                        self._read_config(ini, skip_it)
                    # end if
                # end for
            # end for

            top_paths.append(top_path)
        # end for

        # Remote Config.ini
        for ini in profiles:
            if ini.startswith('#'):
                continue
            # end if
            self._read_config(ini)
        # end for

        self._read_config(self._context.user_py_setup_config)

        # Update Knowledge options
        for name, options in self._knowledges.items():
            if name in self._entries:
                self._entries[name].update(None, options)
            # end if
        # end for

        # Force Python data
        entry = self._entries['PYTHON']
        entry.summary = f'Interpreter {python_implementation()} ' \
                        f'[architecture: {64 if sys.maxsize > 2 ** 32 else 32}-bit]'
        entry.value = sys.executable
        entry.version = python_version()
        entry.status = entry.STATUS_S

        # DISABLE_COLORTERM ?
        entry = self._entries['DISABLE_COLORTERM']
        entry.value = entry.u_values[0]

        if entry.value != '0':
            self._logger._console.disableColor()  # pylint:disable=W0212
        # end if
    # end def _discover_configs

    def _read_config(self, ini, skip_it=False):  # pylint:disable=R0912
        """
        Read a Config

        @param ini    [in] (str)  path
        @param skip_it [in] (bool) not in profile

        @warning recursive function
        """
        try:
            sections = self._parse(ini)

        except (IOError, URLError):
            self._logger.error(f'{ini}: file not found')
            return
        # end try

        if sections is None:
            return
        # end if

        summary = ''
        default = dict()

        for option, value in sections.pop('__CONFIG__', dict()).items():

            if option == 'summary':
                summary = value
                continue
            # end if

            if option == 'include':
                for include in value.split('|'):
                    include = include.strip()
                    self._read_config(include if include.startswith(('http:', '//'))
                                      else join(dirname(ini), include),
                                      skip_it)
                # end for
                continue
            # end if

            default[option] = value
        # end for

        config = CheckEnv.Config(ini, summary)

        self._logger.debug(4, f"""
{Term.CYAN}{config.ini}{Term.OFF}
    summary      {config.summary}
""")

        if skip_it:
            sections = dict()
        # end if

        # [SECTION]
        for section in sections.keys():

            options = deepcopy(default)
            options.update(sections[section])

            entry = CheckEnv.Entry(section, options)

            if entry.type == entry.TYPE_K:
                self._knowledges[entry.name] = options
                continue
            # end if
            value = '\n    '.join((f'{Term.MAGENTA}{option:<12}{Term.OFF} {value}'
                                   for option, value in options.items()))
            self._logger.debug(4, f"""
{Term.CYAN}{entry.name}{Term.OFF}
    {Term.MAGENTA}section{Term.OFF}      [{section}]
    {value}
""")

            if entry.name in self._entries:

                if entry.type != self._entries[entry.name].type:
                    # Skip entry with different type
                    self._logger.error(
                            f'{self._entries[entry.name].ini_file}: {self._entries[entry.name].ini_line}: {entry.name} '
                            f'defined first with type: {self._entries[entry.name].type}')

                    self._logger.error(
                            f'{entry.ini_file}: {entry.ini_line}: {entry.name} defined again with type: {entry.type}')
                    continue
                # end if

            else:

                # Skip entry without valid option
                if entry.type != entry.TYPE_V:
                    for option, value in options.items():
                        if option.startswith(('value', 'dirname', 'version')):
                            if value is not None:
                                break
                            # end if
                        # end if
                    else:
                        continue
                    # end for
                # end if

                # Environment variable?
                if entry.name in environ:

                    if entry.type != entry.TYPE_V:
                        self._logger.error(
                                f'{entry.ini_file}: {entry.ini_line}: {entry.name} already defined in environment')
                    # end if

                    entry.u_inis.append(join(self._context.local_path, 'Local.env'))
                    entry.type = entry.TYPE_V
                    entry.value = environ[entry.name]
                # end if

                # Record entry
                config.add(entry)
                self._entries[entry.name] = entry
            # end if

            # Update entry
            self._entries[entry.name].update(ini, options)
        # end for

        self._configs.append(config)
    # end def _read_config

    _RE_INI_SECTION = re.compile(r'^\[([^\]]+)\]')
    _RE_INI_ENTRY = re.compile(r'[ACDEFKPV]\|[^\|]+\|?(\w+)?')  # Type|Name[|Ext]
    _RE_INI_OPTION = re.compile(r'^([\w]+)\s*=\s*(.+)?')
    _RE_INI_VALUE = re.compile(r'^\s(.+)')

    def _parse(self, ini):  # pylint:disable=R0912
        """
        Config.ini parser

        @param ini [in] (str) path
        @return (dict) sections
        """
        fo = urlopen(ini) if ini.startswith('http:') else open(ini, 'r')
        a_lines = fo.readlines()
        fo.close()

        sections = dict()
        section = None
        option = None
        value = None

        for i_line, v_line in enumerate(a_lines):

            v_line = v_line.rstrip()

            # Blank or comment line
            if len(v_line) == 0 or v_line[0] == ';' or v_line[0] == '#':
                option = None
                value = None
                continue
            # end if

            # Next value line
            if value is not None:
                mo = self._RE_INI_VALUE.search(v_line)
                if mo is not None:
                    value = f'{value}\n{v_line[1:]}'
                    sections[section][option] = value
                    continue
                # end if

                value = None
            # end if

            # [SECTION]
            mo = self._RE_INI_SECTION.search(v_line)
            if mo is not None:
                section = mo.group(1)
                option = None
                value = None

                if section != '__CONFIG__':
                    mo = self._RE_INI_ENTRY.match(section)
                    if mo is None:
                        self._logger.error(f'{ini}: {i_line + 1}: invalid section: {section}')
                        section = None
                        continue
                    # end if
                # end if

                sections[section] = {'_ini_file': ini,
                                     '_ini_line': i_line + 1}
                continue
            # end if

            if section is None:
                continue
            # end if

            mo = self._RE_INI_OPTION.search(v_line)
            if mo is not None:
                option = mo.group(1).lower()

                # Skip '_option' (internal use only)
                if option[0] == '_':
                    continue
                # end if

                # Skip not 'option_<ARCH>'
                postfix = option.rsplit('_', 1)[-1]

                # Python <ARCH>
                if postfix in ('32', '64'):
                    if postfix != ('64' if sys.maxsize > 2 ** 32 else '32'):
                        continue
                    # end if

                    option = option[:-3]
                # end if

                # Skip not '<OS_NAME>/<SYSTEM_NAME>_option'
                prefix = option.split('_', 1)[0]

                # <OS_NAME>
                # py2.6: 'posix', 'nt', 'mac', 'os2', 'ce', 'java', 'riscos'
                # py2.7: 'posix', 'nt',        'os2', 'ce', 'java', 'riscos'
                if prefix in ('posix', 'nt', 'mac', 'os2', 'ce', 'java', 'riscos'):
                    if prefix != OS_NAME:
                        continue
                    # end if

                    option = option[len(prefix) + 1:]
                # end if

                # <SYSTEM_NAME>
                prefix = prefix.capitalize()
                if prefix in ('Darwin', 'Java', 'Linux', 'Windows'):
                    if prefix != SYSTEM_NAME:
                        continue
                    # end if

                    option = option[len(prefix) + 1:]
                # end if

                value = mo.group(2)
                sections[section][option] = value
            # end if
        # end for

        return sections
    # end def _parse

    def _check_entries(self):  # pylint:disable=R0912
        """
        Check Entries

        @return (bool) exit on error
        """
        exit_on_error = False

        self._logger.trace('Start installation verification')
        self._context.cache.load()

        offset = 0
        for config in self._configs:
            for entry in config.entries:
                offset = max(offset, len(entry.name))
            # end for
        # end for

        for config in self._configs:

            # Skip empty config (--minimum or OS_NAME)
            if len(config.entries) == 0:
                continue
            # end if

            self._logger.detail(f'\n  {Term.CYAN}{config.ini or config.summary}{Term.OFF}')

            for entry in config.entries:

                self._logger.detail('  + %%-%ds ' % (offset,) % (entry.name,), '')

                # Knowledge Base
                entry.u_href = self._evaluate(entry.u_href)
                entry.u_title = self._evaluate(entry.u_title)

                self._get_value(entry)

                if (entry.value is None) and (entry.u_options is not None):

                    for option in entry.u_options:
                        value = self._get_value(option)
                        if value is not None:
                            entry.value = option
                            break
                        # end if
                    # end for

                    if entry.value is not None:
                        entry.status = entry.STATUS_K
                        self._logger.detail(
                                f'{Term.GREEN}Replaced{Term.OFF} by {Term.CYAN}{self._devify(entry.value)}{Term.OFF}')
                        self._success += 1
                        continue
                    # end if
                # end if

                if entry.status == entry.STATUS_E:
                    self._errors.append(entry.name)

                    self._logger.detail(f'{Term.RED}Error{Term.OFF}{f" - {entry.error}" if entry.error else ""}')
                    if entry.u_exit:
                        self._logger.detail(f'{Term.RED}Exit{Term.OFF} - {entry.u_exit}')
                        exit_on_error = True
                        break
                    # end if

                    continue
                # end if

                self._check_version(entry)

                if entry.status == entry.STATUS_F:
                    self._failures.append(entry.name)
                    self._logger.detail(
                            f'{Term.YELLOW}Failure{Term.OFF} -'
                            f'{entry.version or self._devify(entry.value)} {Term.YELLOW}{entry.failure}{Term.OFF}')
                    continue
                # end if

                self._success += 1
                self._logger.detail(f'{Term.GREEN}Success{Term.OFF} - {entry.version or self._devify(entry.value)}')
            else:
                continue
            # end for
            break
        # end for

        self._score = (self._success * 100.0) / len(self._entries)

        self._context.cache.save()
        self._logger.detail('')

        return exit_on_error
    # end def _check_entries

    def _get_value(self, entry):  # pylint:disable=R0912
        """
        Determine value of entry

        @param entry [in] (Entry, str) to check
        @return (str) value
        """
        def cyg_path(cyg_value):
            """
            Windows + Cygwin hacks

            @param cyg_value [in] (str) path
            @return (str)
            """
            if cyg_value and (SYSTEM_NAME == 'Windows'):
                # Windows + Cygwin hacks

                if cyg_value.startswith('/cygdrive/'):
                    # /cygdrive/c/dir --> C:/dir
                    cyg_value = f'{cyg_value[10].upper()}:{cyg_value[11:]}'

                elif cyg_value.startswith('/'):
                    # /usr --> C:/cygwin/usr
                    root = self._get_value('CYGWIN_ROOT_PATH')
                    if root:
                        cyg_value = root + cyg_value
                    # end if
                # end if

                if isabs(cyg_value):
                    drive, tail = splitdrive(cyg_value)
                    cyg_value = f'{drive.upper()}{normpath(tail)}'
                # end if
            # end if

            return cyg_value
        # end def cyg_path

        if not isinstance(entry, self.Entry):

            # By default, get value from environment variables
            if entry not in list(self._entries.keys()):
                return getenv(entry)
            # end if

            entry = self._entries[entry]
        # end if

        # Avoid recursivity
        if entry.status is None:
            entry.status = entry.STATUS_E
        else:
            return entry.value
        # end if

        # Value
        if (entry.value is None) and (entry.u_value_cmd is not None):

            cmd = self._evaluate(entry.u_value_cmd)
            if cmd is None:
                return None
            # end if

            status, fo = self._call(cmd, entry.u_value_cwd)
            if status != 0:
                return None
            # end if

            line = fo.readline()
            if isinstance(line, bytes):
                exp = line.decode("utf-8").strip()
            else:
                exp = line.strip()
            # end if

            entry.u_values = [exp, ]
        # end if

        if entry.type in (entry.TYPE_A, entry.TYPE_D, entry.TYPE_E, entry.TYPE_F):

            self._get_path(entry)

        elif entry.type == entry.TYPE_V:

            if entry.value is None:
                entry.error = 'Undefined variable'
            else:
                entry.value = cyg_path(entry.value)

                if entry.u_values:
                    # Compare to expected value
                    for value in entry.u_values:
                        value = self._evaluate(value)
                        if entry.value.replace('\\', '/') == value.replace('\\', '/'):
                            break
                        # end if
                    else:
                        entry.failure = f'[ != {entry.u_values} ]'
                    # end for
                # end if
            # end if

        elif entry.u_values:

            for value in entry.u_values:
                value = self._evaluate(value)
                if value is not None:
                    if entry.type == entry.TYPE_C:
                        # Constant: string
                        entry.value = value

                    elif entry.type == entry.TYPE_P:
                        # Package: non-empty string
                        entry.value = value or None
                    # end if

                    break
                # end if
            # end for
        # end if

        if entry.value is not None:
            entry.value = cyg_path(entry.value)
            entry.status = entry.STATUS_F if entry.failure else entry.STATUS_S
        # end if

        return entry.value
    # end def _get_value

    _RE_MACRO_VAR = re.compile(r'\${([A-Z_0-9]+)}')
    _RE_MACRO_DEF = re.compile(r'\${(\w+)\(([^\$]*?)\)}')

    def _evaluate(self, expression):  # pylint:disable=R0912
        """
        Evaluate expression

        @param expression [in] (str) text with macro
        @return (str) text without macro
        """
        try:
            # Filter bash syntax
            result = expression.replace('$${', '\x06')

            while '${' in result:
                # Variable ?
                mo = self._RE_MACRO_VAR.search(result)
                if mo is not None:
                    result = result.replace(mo.group(0), self._get_value(mo.group(1)))
                    continue
                # end if

                # Function ?
                mo = self._RE_MACRO_DEF.search(result)
                if mo is not None:
                    function = mo.group(1)
                    param = self._evaluate(mo.group(2))

                    if function == 'enter':
                        value = '\n'

                    elif function == 'empty':
                        value = ''

                    elif function == 'call':
                        status, fo = self._call(param)
                        value = None if (status != 0) else fo.readline().strip()
                        fo.close()

                    else:
                        params = [p.strip() for p in param.split(',')]

                        if (function == 'basename') and (len(params) == 1):
                            value = basename(params[0])

                        elif (function == 'dirname') and (len(params) == 1):
                            value = dirname(params[0])

                        elif (function == 'replace') and (len(params) == 3):
                            value = params[0].replace(params[1], params[2])

                        elif ((OS_NAME == 'nt') and
                              (function == 'registry') and (len(params) == 3)):
                            value = self._registry(params[0], params[1], params[2]) if PyWin32 else ''

                        else:
                            self._logger.error(f'Unknown macro: {function}')
                            return None
                        # end if
                    # end if

                    result = result.replace(mo.group(0), f'{value}')
                    continue
                # end if

                self._logger.error(f'Invalid expression: {expression}')
                return None
            # end while

            return result.replace('\x06', '${')
        except Exception:  # pylint:disable=W0703
            return None
        # end try
    # end def _evaluate

    def _call(self, cmd, cwd=None):
        """
        Execute command line.

        @param cmd [in] (str) ex:<tt>"executable" --option argument'</tt>
        @param cwd [in] (str) the child's current directory
        @return (int, FileObject) status + temporary stream with offset at 0
        """
        status = 127
        fo = TemporaryFile()
        try:
            po = Popen(cmd,
                       stdin=PIPE,
                       stdout=fo,
                       stderr=fo,
                       cwd=cwd if cwd else None,
                       shell=(OS_NAME != 'nt'))

            if cmd.endswith('\n'):
                po.stdin.write('\n')
            # end if

            status = po.wait()  # pylint:disable=E1101
            fo.seek(0)

        except Exception:  # pylint:disable=W0703
            pass
        # end try
        lines = fo.readlines()
        exp = ''
        for line in lines:
            if isinstance(line, bytes):
                exp += line.decode("utf-8").strip()
            else:
                exp += line.strip()
            # end if
        # end for

        self._logger.debug(3,
                           '\n%scall\n  command%s %s\n  %sstatus%s  %s\n  %soutput%s  %s%-30s'
                           % (Term.MAGENTA, Term.OFF, cmd,
                              Term.MAGENTA, Term.OFF, str(status),
                              Term.MAGENTA, Term.OFF, exp,
                              '\n'),
                           '')
        fo.seek(0)

        return status, fo
    # end def _call

    if OS_NAME == 'nt':

        if PyWin32:
            _S2K = {'HKCR': HKEY_CLASSES_ROOT,
                    'HKCU': HKEY_CURRENT_USER,
                    'HKLM': HKEY_LOCAL_MACHINE,
                    'HKU' : HKEY_USERS,
                    'HKCC': HKEY_CURRENT_CONFIG}

            def _registry(self, h_key, sub_key, name):
                """
                Extract value from registry

                @param h_key    [in] (str) HKEY_
                @param sub_key  [in] (str) Windows\\path\\form
                @param name    [in] (str) data
                @return (str) value
                """
                value = None

                while True:
                    try:
                        key = RegOpenKey(CheckEnv._S2K[h_key], sub_key)

                        for i in range(RegQueryInfoKey(key)[1]):
                            key_name, key_value, _ = RegEnumValue(key, i)
                            if key_name == name:
                                value = key_value.strip('" ')
                                break
                            # end if
                        # end for

                        RegCloseKey(key)
                    except Exception:  # pylint:disable=W0703
                        # SOFTWARE\Microsoft\Windows\...
                        # SOFTWARE\Wow6432Node\Microsoft\Windows\...
                        if r'SOFTWARE\Microsoft' in sub_key:
                            sub_key = sub_key.replace(r'SOFTWARE\Microsoft', r'SOFTWARE\Wow6432Node\Microsoft')
                            continue
                        # end if
                    # end try

                    self._logger.debug(3,
                                       '\n%sregistry\n  hKey%s   %s\n  %ssubKey%s %s\n  %sname%s   %s\n  %svalue%s  '
                                       '%s%-30s'
                                       % (Term.MAGENTA, Term.OFF, h_key,
                                          Term.MAGENTA, Term.OFF, sub_key,
                                          Term.MAGENTA, Term.OFF, name,
                                          Term.MAGENTA, Term.OFF, value,
                                          '\n'),
                                       '')
                    break
                # end while

                return value
            # end def _registry

            @staticmethod
            def _get_file_version_info(path):
                """
                Retrieve File Version Info from rc

                @param path [in] (str) binary path
                @return (tuple) version, description, comments
                """
                version = None
                description = None
                comments = None

                try:
                    version_info = GetFileVersionInfo(path, '\\')
                    version = f'{version_info["FileVersionMS"] >> 16}.{version_info["FileVersionMS"] & 0xFFFF}.' \
                              f'{version_info["FileVersionLS"] >> 16}.{version_info["FileVersionLS"] & 0xFFFF}'

                    translation = GetFileVersionInfo(path, '\\VarFileInfo\\Translation')

                    if version == '0.0.0.0':

                        # Release x.y
                        # x.y (r....)
                        product = '0.0.0.0'
                        for product in GetFileVersionInfo(path,
                                                          '\\StringFileInfo\\%04x%04x\\ProductVersion'
                                                          % translation[0]).split():
                            if product.startswith('0123456789'):
                                break
                            # end if
                        # end for

                        if CheckEnv._cmp_version(product, version) > 0:
                            version = product
                        else:
                            version = None
                        # end if
                    # end if

                    description = GetFileVersionInfo(path,
                                                     '\\StringFileInfo\\{:04x}{:04x}\\FileDescription'
                                                     .format(translation[0]))

                    comments = GetFileVersionInfo(path,
                                                  '\\StringFileInfo\\{:04x}{:04x}\\Comments'
                                                  .format(translation[0]))
                except WinError:
                    pass
                # end try
                return version, description, comments
            # end def _get_file_version_info

        else:

            raise NotImplementedError

        # end if

        def _get_sym_link(self, path):
            """
            Retrieve target from symlink

            @warning cygwin implementation / cygpath required

            @param path [in] (str) source path
            @return (str) target path
            """
            target = path

            try:
                link = open(path, 'rb')
                data = link.read(10)
                link.close()

                if data == '!<symlink>':
                    target = Popen(f'"{self._get_value("CYGPATH")}" -m "{path}"',
                                   stdout=PIPE).communicate()[0].strip()
                # end if
            except:  # pylint:disable=W0702
                pass
            # end try

            return target
        # end def _get_sym_link

    # end if

    _PRUNE_DIRS = (
            # Build system
            '.SVN', 'CVS',
            # documentation
            'DOC', 'DOCS', 'HELP', 'HTML', 'CSS', 'PDF',
            # audio, image, video
            'BITMAP', 'BITMAPS', 'ICON', 'ICONS', 'IMAGE', 'IMAGES',
            'MEDIA', 'PIC', 'PICS', 'PIXMAP', 'PIXMAPS', 'SKIN', 'SKINS',
            # localization
            'LANG', 'LANGUAGE', 'LANGUAGES', 'LOCALE', 'LOCALES', 'ZI',
            # installation
            'CONF', 'CONFIGURATION', 'DEFAULT', 'DEFAULTS',
            'INSTALL', 'UNINSTALL', 'SETUP', 'SETTINGS',
            # sample
            'DEMO', 'DATA', 'EXAMPLE', 'EXAMPLES',
            'SAMPLE', 'SAMPLES', 'TEMPLATE', 'TEMPLATES',
            # temporary
            'BACKUP', 'CACHE', 'LOCAL', 'DEBUG', 'DOWNLOAD',
            'ERROR', 'ERRORS', 'LOG', 'LOGS', 'TMP', 'TEMP', 'TEST',
            # win32
            'INF')

    if SYSTEM_NAME == 'Darwin':

        @staticmethod
        def _get_info_property_list(path):
            """
            Retrieve Property from Info.plist

            @param path [in] (str) binary path
            @return (str) version
            """
            # /Application/.../<App>.app/Contents/MacOS/<App>
            if not path.startswith('/Application'):
                return
            # end if

            # /Application/.../<App>.app/Contents/Info.plist
            while len(path) > 1:
                path = dirname(path)
                if basename(path) == 'Contents':
                    break
                # end if
            # end while

            info = join(path, 'Info.plist')
            if not isfile(info):
                return
            # end if

            dom = parse(info)

            for node in dom.getElementsByTagName('key'):
                if node.childNodes[0].data not in ('CFBundleShortVersionString', 'CFBundleVersion'):
                    continue
                # end if
                while node:
                    node = node.nextSibling
                    if node.localName == 'string':
                        return node.childNodes[0].data
                    # end if
                # end while
                return
            # end for
        # end def _get_info_property_list

    # end if

    def _get_path(self, entry):  # pylint:disable=R0912
        """
        Retrieve entry's path

        @param entry [in] (Entry) to check
        """

        def is_path(path_value):
            """
            Find the first pathname matching a specified pattern according to
            the rules used by the Unix shell and check its type

            @param path_value [in] (str) path specification
            @return (bool)
            """
            if not path_value:
                return False
            # end if

            paths = glob(normpath(path_value))
            if len(paths) == 0:
                return False
            # end if

            # 0 --> latest version
            paths.sort(key=self.cmp_to_key(self._cmp_version), reverse=True)

            value = paths[0]

            if entry.type == entry.TYPE_D:
                if not isdir(value):
                    return False
                # end if
            elif entry.type == entry.TYPE_F:
                if not isfile(value):
                    return False
                # end if
            # end if

            if SYSTEM_NAME == 'Windows':
                # Get Windows absolute path of Cygwin symbolic link
                value = self._get_sym_link(value)
            # end if

            entry.value = value
            return True
        # end def is_path

        # Absolute path ?
        if entry.u_value_cmd or entry.u_values:
            for alias in entry.u_aliases:
                alias = self._evaluate(alias)

                for dir_name in entry.u_values:
                    dir_name = self._evaluate(dir_name)
                    if dir_name is None:
                        continue
                    # end if

                    if is_path(join(entry.u_value_cwd, dir_name, alias)):
                        return
                    # end if
                # end for
            # end for
            return
        # end if

        # Default path ?
        if entry.u_dirnames:
            for alias in entry.u_aliases:
                alias = self._evaluate(alias)

                for dir_name in entry.u_dirnames:
                    dir_name = self._evaluate(dir_name)
                    if dir_name is None:
                        continue
                    # end if

                    if is_path(join(entry.u_dirname_cwd, dir_name, alias)):
                        return
                    # end if
                # end for
            # end for
        else:
            # Config path ?
            for alias in entry.u_aliases:
                if is_path(join(dirname(entry.u_inis[0]), alias)):
                    return
                # end if
            # end for
        # end if

        # Cache ?
        if is_path(self._context.cache[entry.name]):
            return
        # end if

        # PATH ?
        for alias in entry.u_aliases:
            for path in CheckEnv._ENV_PATHS:
                if is_path(join(path, alias)):
                    self._context.cache[entry.name] = entry.value
                    return
                # end if
            # end for
        # end for

        # Binary paths ?
        self._logger.detail(f'Looking for "{alias}", please wait...\n', end='')

        for alias in entry.u_aliases:
            for bin_path in self._context.binPaths:
                for root_path in glob(bin_path):
                    for dir_path, dir_names, _ in walk(root_path):
                        if is_path(join(dir_path, alias)):
                            self._context.cache[entry.name] = entry.value
                            return
                        # end if

                        for dir_name in [pruneDir for pruneDir in dir_names
                                         if ((pruneDir.split()[0].upper() in self._PRUNE_DIRS)
                                             or (pruneDir[0] in ('$', '(', '.', '{')))]:
                            dir_names.remove(dir_name)
                        # end for
                    # end for
                # end for
            # end for
        # end for
    # end def _get_path

    def _check_version(self, entry):  # pylint:disable=R0912
        """
        Get version and compare to limits

        @param entry [in] (Entry) to check
        """
        if not (entry.u_version_min or entry.u_version_not or entry.u_version_max or entry.u_version):
            return
        # end if

        # Regular file ?
        file_hash = Misc.getHash(entry.value)

        if file_hash is not None:

            # Read version from cache
            if entry.version is None:
                cache = self._context.cache[entry.value]
                if cache is not None:
                    cache_hash, entry.version, entry.summary, entry.comments = cache
                    if file_hash != cache_hash:
                        entry.version = None
                    # end if
                # end if
            # end if

            # Read version from registry
            if entry.version is None:
                if OS_NAME == 'nt':
                    entry.version, description, entry.comments = self._get_file_version_info(entry.value)
                    entry.summary = entry.summary or description

                elif SYSTEM_NAME == 'Darwin':
                    entry.version = self._get_info_property_list(entry.value)
                # end if
            # end if
        # end if

        if entry.version is None:
            # Read version from entry data
            self._get_version(entry)
        # end if

        entry.status = entry.STATUS_F

        if not entry.failure:

            if file_hash:
                self._context.cache[entry.value] = (file_hash, entry.version, entry.summary, entry.comments)
            # end if

            if entry.u_version:
                # Compare to expected version
                if entry.u_version != '*' and self._cmp_version(entry.version, entry.u_version) != 0:
                    entry.failure = f'[ != {entry.u_version} ]'
                    return
                # end if

            else:
                # Compare to version_min / version_max
                if entry.u_version_min and self._cmp_version(entry.version, entry.u_version_min) < 0:
                    entry.failure = f'[ < {entry.u_version_min} ]'
                    return
                # end if

                if entry.u_version_max and self._cmp_version(entry.version, entry.u_version_max) >= 0:
                    entry.failure = f'[ >= {entry.u_version_max} ]'
                    return
                # end if
            # end if

            if entry.u_version_not and entry.version in entry.u_version_not:
                entry.failure = f'[ {entry.u_version_not[entry.version]} ]'
                return
            # end if

            entry.status = entry.STATUS_S
        # end if
    # end def _check_version

    _RE_VERSION_FIELD = re.compile(r'[\s:=,;"\'\(\)/]+')
    _RE_VERSION_VALUE = re.compile(r'^\D+')

    def _get_version(self, entry):  # pylint:disable=R0912
        """
        Retrieve entry's version

        @param entry [in] (Entry) to check
        """
        try:
            if entry.u_version_opt:
                entry.u_version_cmd = f'"{entry.u_version_exe if entry.u_version_exe else entry.value}" ' \
                                      f'{entry.u_version_opt}'
            # end if

            if entry.u_version_cmd:
                _, fo_txt = self._call(self._evaluate(entry.u_version_cmd),
                                       entry.u_version_cwd)

            elif entry.u_version_txt:
                try:
                    fo_txt = open(join(entry.u_version_cwd,
                                       self._evaluate(entry.u_version_txt)), 'r')
                except IOError:
                    raise ValueError(f"'version_txt = {entry.u_version_txt}' not found")
                # end try

            else:
                try:
                    fo_txt = open(entry.value, 'r')
                except IOError:
                    raise ValueError(f"'value = {entry.value}' not found")
                # end try
            # end if

            record = None

            if entry.u_version_pat:
                re_pat = re.compile(entry.u_version_pat)

                for record in fo_txt:
                    mo = re_pat.search(record)
                    if mo is not None:
                        record = record[mo.start(0):]
                        break
                    # end if
                else:
                    raise IndexError(f"'version_pat = {entry.u_version_pat}' not found")
                # end for

            else:
                entry.u_version_rec = int(entry.u_version_rec) if entry.u_version_rec else 1

                for _ in range(0, entry.u_version_rec):
                    record = fo_txt.readline()
                # end for

                if not record:
                    raise IndexError(f"'version_rec = {entry.u_version_rec}' invalid record")
                # end if

                if isinstance(record, bytes):
                    # Convert bytes object into string
                    record = record.decode("utf-8")
                # end if

                if OS_NAME == 'nt':

                    if record[0:2] == '\x4D\x5A':
                        raise ValueError("can't parse MZ DOS EXE format")
                    # end if

                    if record[0:2] == '\x00\x20':
                        raise ValueError("can't parse Windows Old style EXE format")
                    # end if

                    if record[0:2] == '\x4E\x45':
                        raise ValueError("can't parse Windows NE EXE format")
                    # end if
                else:
                    if record[0:2] == '\x75\x45\x4C\x46':
                        raise ValueError("can't parse ELF format")
                    # end if
                # end if

            # end if
            fo_txt.close()

            # versionRec         --> versionFlds
            # '1.0'                  [ '1.0' ]
            # '1.0.'                 [ '1.0' ]
            # 'v1.0'                 [ '1.0' ]
            # 'tool version 1.0'     [ '', '', '1.0' ]
            # 'in2out version 1.0'   [ '2out', '', '1.0' ]
            fields = [self._RE_VERSION_VALUE.sub('', f)
                      for f in self._RE_VERSION_FIELD.split(record.strip())]

            entry.u_version_fld = int(entry.u_version_fld) if entry.u_version_fld else 1

            for field in fields[entry.u_version_fld - 1:]:
                if field:
                    # field      --> version
                    # '1.0.'         '1.0'
                    entry.version = '.'.join([f for f in field.split('.') if f != ''])
                    break
                # end if
            else:
                raise IndexError(f"'version_fld = {entry.u_version_fld}' invalid field")
            # end for

        except (IndexError, ValueError) as msg:
            entry.version = '?.?.?'
            entry.failure = f'[ {msg} ]'
        # end try
    # end def _get_version

    @staticmethod
    def cmp(a, b):
        """If you really need the cmp() functionality,
        you could use the expression (a > b) - (a < b)"""
        return (a > b) - (a < b)
    # end def cmp

    @staticmethod
    def _cmp_version(x, y):
        """
        Compare 2 versions

        @param x [in] (str) version #1
        @param y [in] (str) version #2
        @return (int) The return value is:
                      - negative if x < y
                      - zero if x == y
                      - strictly positive if x > y.
        """
        if x == y:
            return 0
        # end if

        xs = x.split('.')
        xl = len(xs)

        # Remove trailing 0
        while xl and xs[xl - 1].isdigit() and not int(xs[xl - 1]):
            xl -= 1
        # end while

        ys = y.split('.')
        yl = len(ys)

        # Remove trailing 0
        while yl and ys[yl - 1].isdigit() and not int(ys[yl - 1]):
            yl -= 1
        # end while

        for i in range(min(xl, yl)):
            xi = xs[i]
            yi = ys[i]

            if xi.isdigit() and yi.isdigit():
                value = CheckEnv.cmp(int(xi), int(yi))
            else:
                value = CheckEnv.cmp(xi, yi)
            # end if

            if value:
                break
            # end if
        else:
            value = CheckEnv.cmp(xl, yl)
        # end for

        return value
    # end def _cmp_version

    @staticmethod
    def cmp_to_key(mycmp):
        """Convert a cmp= function into a key= function"""
        class K(object):

            def __init__(self, obj, *args):
                self.obj = obj
            # end def __init__

            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0
            # end def __lt__

            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0
            # end def __gt__

            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0
            # end def __eq__

            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0
            # end def __le__

            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0
            # end def __ge__

            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0
            # end def __ne__
        return K
    # end def cmp_to_key

    @staticmethod
    def _devify(msg, esc=False):
        """
        Format msg replacing PROJECT_PATH by PROJECT

        @param msg [in] (str)  text
        @param esc [in] (bool) to escape '@\'
        @return (str)
        """
        if not msg:
            return ''
        # end if

        if msg.startswith(CheckEnv._PROJECT_PATH) and msg != CheckEnv._PROJECT_PATH:
            return msg.replace(CheckEnv._PROJECT_PATH, 'PROJECT').replace('\\', '/')
        # end if

        return Misc.slashify(msg, esc)
    # end def _devify

    def _write_local(self, profile):
        """
        Write Local files

        @param profile [in] (str) of current configuration
        """
        self._logger.trace('Writing Local files...')
        self._context.create_paths()

        self._write_local_txt(profile)
        self._write_local_env(profile)

        self._write_local_bat(profile)
        self._write_local_mak(profile)
        self._write_local_properties(profile)
        self._write_local_py(profile)
        self._write_local_sh(profile)

        self._logger.detail('')
    # end def _write_local

    def _write_test_html(self, profile):
        """
        Write PYTESTBOX/Test.html

        @param profile [in] (str) of current configuration
        """
        with open(join(self._context.dev_path, 'Test.html'), 'w') as fo:
            fail_value = '<br>'.join([f'<tt>{len(self._failures)}</tt>']
                                     + [
                                             f'<a href="#{name}"><b>{name}</b></a> - '
                                             f'{Html.txt2html(self._entries[name].version)} '
                                             f'{Html.txt2html(self._entries[name].failure)}'
                                             for name in self._failures])
            err_value = '<br>'.join([f'<tt>{len(self._errors)}</tt>']
                                    + ['<a href="#%s"><b>%s</b>%s</a>'
                                       % (name, name,
                                          f' -  {self._entries[name].u_exit}' if
                                          self._entries[name].u_exit else '') for name in self._errors])
            fo.write(f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN">
<html>
<head>
  <title>{Html.txt2html(self._context.project_name)} - pyEnvChecker Test</title>
  <link href="LIBS/PYSETUP/ABOUT/ABOUT/AboutFavicon.png" rel="icon" type="image/png">
  <link href="LIBS/PYSETUP/DOXYGEN/PySetup.css" rel="stylesheet" type="text/css"/>
</head>
<body>
<div class="ezd_header">
{Html.txt2html(self._context.project_name)} - <i>Refresh/pyEnvChecker --test</i> results
</div>

<div style="margin: 10px">

<h2>Overview</h2>
<p>The {Html.txt2html(self._context.project_name)} environment is tested at <b>{self._score:0.1f}</b>%%</p>

<table border="1" cellpadding="3" cellspacing="0">
<tr bgcolor="{Html.CYAN}">
  <td width="75">Profile </td>
  <td width="625">{profile}</td>
</tr>
<tr bgcolor="{Html.GREEN}">
  <td>Success</td>
  <td>{self._success}</td>
</tr>
<tr bgcolor="{Html.YELLOW}">
  <td valign="top">Failure</td>
  <td>{fail_value}</td>
</tr>
<tr bgcolor="{Html.RED}">
  <td valign="top">Error</td>
  <td>{err_value}</td>
</tr>
</table>

<p>For more information about installing third-party tools, see chapter 3 of the
<a href="LIBS/PYSETUP/DOC">user manual</a>.</p>

<h2>Details</h2>""")

            for config in self._configs:
                if not config.entries:
                    continue
                # end if

                # Config
                fo.write(f"""
<table border="0" cellpadding="0" cellspacing="3">
<tr>
  <td width="24"><img src="LIBS/PYSETUP/DOXYGEN/ABOUT/Tree{config.icon}_24.png" alt="" border="0"></td>
  <td><b>{config.ini}</b>{' - ' if (config.ini and config.summary) else '&nbsp;'}{Html.txt2html(config.summary)}</td>
</tr>
</table>""")

                # Entries
                fo.write("""
<table border="0" cellpadding="0" cellspacing="1">
""")
                for entry in config.entries:
                    if entry.status == entry.STATUS_K:
                        entry_value = f'Replaced by <a href="#{entry.value}"><b>{entry.value}</b></a>'
                    else:
                        entry_value = Html.txt2html(self._devify(entry.value))
                    # end if
                    if entry.u_inis:
                        ini_value = ', '.join([
                                f'<a href="{ini if ini.startswith("http:") else f"file:///{ini}"}">'
                                f'{basename(ini)}</a>' for ini in entry.u_inis])
                    else:
                        ini_value = ''
                    # end if
                    if entry.u_href:
                        kb_value = f'<a href="{entry.u_href}"><img ' \
                                   f'src="LIBS/PYSETUP/DOXYGEN/ABOUT/TreeIntranet_32.png" alt="" border="0" title="' \
                                   f'{entry.u_title}"></a>'
                    else:
                        kb_value = '&nbsp;'
                    # end if
                    fo.write(f"""
<tr>
  <td>
    <a name="{entry.name}"></a>
    <table border="1" cellpadding="3" cellspacing="0">
    <tr bgcolor="{entry.get_color()}">
      <td valign="top" width="500">
        <tt><b>{entry.name}</b></tt><i>{' - ' if entry.summary else '&nbsp;'}{Html.txt2html(entry.summary)}</i>
        {'<br>' if entry.value else ''}<tt>{entry_value}</tt>{'<br>' if entry.comments else ''}<i>
        {Html.txt2html(entry.comments)}</i></td>
      <td valign="top" width="200">{ini_value}{'<br>' if entry.version else ''}{Html.txt2html(entry.version)}
      {'<br>' if entry.failure else ''}{Html.txt2html(entry.failure)}</td>
    </tr>
    </table></td>
  <td>{kb_value}</td>
</tr>""")
                # end for
                fo.write('</table>')
            # end for

            fo.write(f"""
</div>
<div class="ezd_footer">Generated by {self._NAME} v {self._VERSION} on {strftime('%Y/%m/%d - %H:%M:%S')}</div>
</body></html>""")
        # end with
    # end def _write_test_html

    def _write_local_txt(self, profile):
        """
        Write PYTESTBOX/LIBS/LOCAL/Local.txt

        @param profile [in] (str) of current configuration
        """
        with open(join(self._context.local_path, 'Local.txt'), 'w') as fo:
            fail_value = '\n'.join([f'{len(self._failures)}']
                                   + [f'#          {name} - {self._entries[name].version} {self._entries[name].failure}'
                                      for name in self._failures])
            err_value = '\n'.join([f'{len(self._errors)}']
                                  + [f'#          {name}' for name in self._errors])
            fo.write(f"""
# ------------------------------------------------------------------------------
# [Summary]  Local {self._context.project_name} configuration
#
# profile    {profile}
#
# score      {self._score:0.1f}%
#
# success    {self._success}
# failure    {fail_value}
# error      {err_value}
#
# [Author]   {self._NAME}
# [Version]  {self._VERSION}
# [DateTime] {strftime('%Y/%m/%d - %H:%M:%S')}
# ------------------------------------------------------------------------------
# DO NOT MANAGE THIS FILE UNDER CONFIGURATION
# ------------------------------------------------------------------------------
""")

            for config in self._configs:
                if not config.entries:
                    continue
                # end if

                fo.write(f"""
# ------------------------------------------------------------------------------
# {config.ini or config.summary}
# ------------------------------------------------------------------------------
""")

                for entry in config.entries:
                    if entry.status in [entry.STATUS_S, entry.STATUS_F]:
                        fo.write(f"""
name    : {entry.name}
value   : {entry.value if entry.value is not None else ''}
version : {entry.version if entry.version is not None else 'None'}
""")
                    else:
                        fo.write(f"""
# name  : {entry.name}
""")
                    # end if
                # end for
            # end for

            fo.write(END_OF_FILE_TEXT)
        # end with
    # end def _write_local_txt

    def _write_local_env(self, profile):
        """
        Write PYTESTBOX/LIBS/LOCAL/Local.env

        @param profile [in] (str) of current configuration
        """
        with open(join(self._context.local_path, 'Local.env'), 'w') as fo:
            fo.write(f"""
# ------------------------------------------------------------------------------
# [Summary]  Local {self._context.project_name} checked environment variables
#
# [Profile]  {profile}
#
# [Author]   {self._NAME}
# [Version]  {self._VERSION}
# [DateTime] {strftime('%Y/%m/%d - %H:%M:%S')}
# ------------------------------------------------------------------------------
# DO NOT MANAGE THIS FILE UNDER CONFIGURATION
# ------------------------------------------------------------------------------
""")

            for config in self._configs:
                if not config.entries:
                    continue
                # end if

                environs = list()
                for entry in config.entries:
                    if (entry.type == entry.TYPE_V) and (entry.value is not None):
                        environs.append(f'{entry.name}={entry.value}')
                    # end if
                # end for

                if environs:
                    env_value = '\n'.join(environs)
                    fo.write(f"""
# ------------------------------------------------------------------------------
# {config.ini or config.summary}
# ------------------------------------------------------------------------------
{env_value}
""")
                # end if
            # end for

            fo.write(END_OF_FILE_TEXT)
        # end with
    # end def _write_local_env

    def _write_local_bat(self, profile):
        """
        Write PYTESTBOX/LIBS/LOCAL/Local.bat

        @param profile [in] (str) of current configuration
        """
        if OS_NAME != 'nt':
            return
        # end if

        with open(join(self._context.local_path, 'Local.bat'), 'w') as fo:
            fo.write(f"""
@echo off
REM ----------------------------------------------------------------------------
REM [Summary]  Local {self._context.project_name} batch configuration
REM
REM [Profile]  {profile}
REM
REM [Author]   {self._NAME}
REM [Version]  {self._VERSION}
REM [DateTime] {strftime('%Y/%m/%d - %H:%M:%S')}
REM ----------------------------------------------------------------------------
REM DO NOT MANAGE THIS FILE UNDER CONFIGURATION
REM ----------------------------------------------------------------------------
""")

            for config in self._configs:
                if not config.entries:
                    continue
                # end if
                ent_value = '\n'.join((f'set {entry.name}="{entry.value}"'
                                       if entry.status in (entry.STATUS_S, entry.STATUS_F)
                                       else f'REM {entry.name}'
                                       for entry in config.entries))
                fo.write(f"""
REM ----------------------------------------------------------------------------
REM {config.ini or config.summary}
REM ----------------------------------------------------------------------------
{ent_value}
""")
            # end for
            fo.write(REM_END_OF_FILE_TEXT)
        # end with
    # end def _write_local_bat

    def _write_local_mak(self, profile):
        """
        Write PYTESTBOX/LIBS/LOCAL/Local.mak

        @param profile [in] (str) of current configuration
        """
        with open(join(self._context.local_path, 'Local.mak'), 'w') as fo:
            fo.write(f"""
# ------------------------------------------------------------------------------
# [Summary]  Local {self._context.project_name} make configuration
#
# [Profile]  {profile}
#
# [Author]   {self._NAME}
# [Version]  {self._VERSION}
# [DateTime] {strftime('%Y/%m/%d - %H:%M:%S')}
# ------------------------------------------------------------------------------
# DO NOT MANAGE THIS FILE UNDER CONFIGURATION
# ------------------------------------------------------------------------------
MakePath                         ?= $1
NormPath                         ?= $1
# ------------------------------------------------------------------------------
""")

            for config in self._configs:
                if not config.entries:
                    continue
                # end if
                mak_value = '\n'.join(("%-28s := $(call MakePath,%s)" % (entry.name, entry.value.replace('#', '\\#'))
                                       if entry.status in (entry.STATUS_S, entry.STATUS_F)
                                       else f'# {entry.name}'
                                       for entry in config.entries
                                       if (entry.name != 'MAKE')))
                fo.write(f"""
# ------------------------------------------------------------------------------
# {config.ini or config.summary}
# ------------------------------------------------------------------------------
{mak_value}
""")
            # end for
            fo.write(END_OF_FILE_TEXT)
        # end with
    # end def _write_local_mak

    def _write_local_properties(self, profile):
        """
        Write PYTESTBOX/LIBS/LOCAL/Local.properties

        @param profile [in] (str) of current configuration
        """
        with open(join(self._context.local_path, 'Local.properties'), 'w') as fo:
            fo.write(f"""
# ------------------------------------------------------------------------------
# @brief   Local {self._context.project_name} Ant configuration
#
# @profile {profile}
#
# @author  {self._NAME}
# @version {self._VERSION}
# @date    {strftime('%Y/%m/%d - %H:%M:%S')}
# ------------------------------------------------------------------------------
# DO NOT MANAGE THIS FILE UNDER CONFIGURATION
# ------------------------------------------------------------------------------
""")

            for config in self._configs:
                if not config.entries:
                    continue
                # end if
                ent_value = '\n'.join(('pysetup.%s=%s' % (entry.name, entry.value.replace('\\', '\\\\'))
                                       if entry.status in (entry.STATUS_S, entry.STATUS_F)
                                       else f'# {entry.name}'
                                       for entry in config.entries))
                fo.write(f"""
# ------------------------------------------------------------------------------
# {config.ini or config.summary}
# ------------------------------------------------------------------------------
{ent_value}
""")

            # end for
            fo.write(END_OF_FILE_TEXT)
        # end with
    # end def _write_local_properties

    def _write_local_py(self, profile):
        """
        Write PYTESTBOX/LIBS/LOCAL/local.py

        @param profile [in] (str) of current configuration
        """
        with open(join(self._context.local_path, 'local.py'), 'w') as fo:
            fo.write(f"""
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
'''
@package local

@brief   Local {self._context.project_name} Python Configuration

@profile {profile}

@author  {self._NAME}
@version {self._VERSION}
@date    {strftime('%Y/%m/%d - %H:%M:%S')}
'''
# ------------------------------------------------------------------------------
# DO NOT MANAGE THIS FILE UNDER CONFIGURATION
# ------------------------------------------------------------------------------
""")

            for config in self._configs:
                if not config.entries:
                    continue
                # end if
                ent_value = '\n'.join((f"{entry.name:<28} = r'{entry.value}'"
                                       if entry.status in (entry.STATUS_S, entry.STATUS_F)
                                       else f'# {entry.name}'
                                       for entry in config.entries))
                fo.write(f"""
# ------------------------------------------------------------------------------
# {config.ini or config.summary}
# ------------------------------------------------------------------------------
{ent_value}
""")
            # end for

            paths = list()
            for entry in self._entries.values():

                if entry.status not in (entry.STATUS_S, entry.STATUS_F):
                    continue
                # end if

                if entry.ext not in ['.egg', '.py', '.pyc', '.pyd', '.pyo']:
                    continue
                # end if

                path = entry.value if entry.ext == '.egg' else dirname(entry.value)

                if path not in paths:
                    paths.append(path)
                # end if
            # end for

            p_value = ',\n  '.join((f"r'{path}'" for path in sorted(paths)))
            fo.write(f"""
# ------------------------------------------------------------------------------
# PYTESTBOX/LIBS/PYSETUP/PYTHON/pysetup/__init__.py
# ------------------------------------------------------------------------------
LOCAL_PYTHON_PATH = (
  {p_value}
)

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
""")
        # end with
    # end def _write_local_py

    def _write_local_sh(self, profile):
        """
        Write PYTESTBOX/LIBS/LOCAL/Local.sh

        @param profile [in] (str) of current configuration
        """
        with open(join(self._context.local_path, 'Local.sh'), 'w') as fo:
            fo.write(f"""
# ------------------------------------------------------------------------------
# [Summary]  Local {self._context.project_name} bash configuration
#
# [Profile]  {profile}
#
# [Author]   {self._NAME}
# [Version]  {self._VERSION}
# [DateTime] {strftime('%Y/%m/%d - %H:%M:%S')}
# ------------------------------------------------------------------------------
# DO NOT MANAGE THIS FILE UNDER CONFIGURATION
# ------------------------------------------------------------------------------
""")

            for config in self._configs:
                if not config.entries:
                    continue
                # end if
                ent_value = '\n'.join((f"declare -r {entry.name}='{Misc.slashify(entry.value, True)}'"
                                       if entry.status in [entry.STATUS_S, entry.STATUS_F]
                                       else f'# {entry.name}' for entry in config.entries))
                fo.write(f"""
# ------------------------------------------------------------------------------
# {config.ini or config.summary}
# ------------------------------------------------------------------------------
{ent_value}
""")
            # end for
            fo.write(END_OF_FILE_TEXT)
        # end with
    # end def _write_local_sh

    def _echo_footer(self, profile, test, no_html=True):
        """
        Echo footer information

        @param profile [in] (str) title
        @param test    [in] (bool) or check
        @param no_html [in] (bool) no About.html
        """
        color = Term.GREEN

        if self._failures:
            color = Term.YELLOW
            f_value = '\n  '.join(('%s - %s %s%s'
                                   % (name,
                                      self._entries[name].version or self._devify(self._entries[name].value),
                                      self._entries[name].failure,
                                      f'\n{" " * (4 + len(name))} see {Term.CYAN}'
                                      f'{Html.url2txt(self._entries[name].u_href)}{Term.OFF}' if self._entries[
                                          name].u_href else '')
                                   for name in self._failures))
            failure = f'\n\n- {color}Failure {len(self._failures)}{Term.OFF}\n  {f_value}'
        else:
            failure = ''
        # end if

        if self._errors:
            color = Term.RED
            error = '\n\n- %sError   %s%s\n  %s' \
                    % (color, len(self._errors), Term.OFF,
                       '\n  '.join(('%s%s%s'
                                    % (name,
                                       f' - {self._entries[name].u_exit}' if self._entries[name].u_exit else '',
                                       f' - see {Term.CYAN}{Html.url2txt(self._entries[name].u_href)}{Term.OFF}' if
                                       self._entries[name].u_href else '')
                                    for name in self._errors)))
        else:
            error = ''
        # end if

        footer = "{} environment {} at {}{:0.1f}%{}{}{}{}{}" \
            .format(self._context.project_name,
                    'tested' if test else 'checked',
                    color,
                    self._score,
                    Term.OFF,
                    f'\nProfile: {profile}' if profile else '',
                    failure,
                    error,
                    "\n\nSee < PYTESTBOX/{} > for details".format(
                            'Test.html' if test else f'LIBS/LOCAL/{"Local.txt" if no_html else "About.html"}'))

        self._logger.title(join(footer))
    # end def _echo_footer
# end class CheckEnv


class Main(CheckEnv):
    """
    User Interface
    """

    def __init__(self):  # pylint:disable=R0912
        """
        Constructor
        """
        parser = ArgumentParser(description=self._BRIEF,
                                epilog=f"""
Arguments:
  Config.ini
  Profile.pfl

See Also:
    PYTESTBOX/LIBS/PYSETUP/DOC manuals

{self._NAME} v {self._VERSION}
""")
        parser.add_argument('--version', action='version', version=self._VERSION)

        # Options
        parser.add_argument('-C', '--clean',
                            help='clean up local data and exit\n--clean: PYTESTBOX/LIBS/LOCAL folder + About.html '
                                 'files\n--clean --clean: .project cache + .version cache\n--clean --clean --clean: '
                                 '.pysetup cache',
                            action='count',
                            dest='clean',
                            default=0)

        group = parser.add_mutually_exclusive_group()
        group.add_argument('-d', '--debug',
                           help='print lots of debugging information\n--debug: xxx_cmd + call() [+ registry() on '
                                'Windows] details\n--debug --debug: Config.ini content',
                           action='count',
                           dest='verbose',
                           default=1)

        group.add_argument('-q', '--quiet',
                           help="don't show details",
                           action='store_const',
                           const=1,
                           dest='verbose',
                           default=2)

        parser.set_defaults(verbose=2)

        parser.add_argument('-m', '--minimum',
                            help='check the minimum set of tools',
                            action='store_true',
                            dest='minimum',
                            default=False)

        parser.add_argument('-t', '--test',
                            help='check tools only (no local items generation)',
                            action='store_true',
                            dest='test',
                            default=False)

        parser.add_argument('-P', '--pause',
                            help='prompt the user in case of error and/or failure',
                            action='store_true',
                            dest='pause',
                            default=False)

        # positional arguments
        parser.add_argument('profiles', nargs='*', metavar='PROFILES', help='pass one or more profiles', default=None)
        args = parser.parse_intermixed_args()

        # PROJECT_PATH
        path = abspath(sys.argv[0])
        drive, tail = splitdrive(path)

        project_path = None
        while len(tail) > 1:
            if basename(tail) == 'PYTESTBOX':
                # Hack cygwin path: force drive to uppercase
                project_path = drive.upper() + tail
                break
            # end if
            tail = dirname(tail)
        else:
            parser.error('PYTESTBOX root folder not found in "%s"' % (path,))
        # end while

        super(Main, self).__init__(project_path)

        # Arguments
        profiles = list()

        def check_args(value, cwd):
            """
            Check CLI arguments

            @param value [in] (str) .pfl or .ini
            @param cwd   [in] (str) current working directory
            @return (str) name
            """
            lines = []
            new_path = None
            try:
                if value.startswith('http'):
                    new_path = value
                    fo = urlopen(value)
                else:
                    # By default, arg is relative to current path
                    new_path = normpath(join(cwd, value))

                    if not isfile(new_path):
                        # Legacy implementation: arg can be relative relative to PROJECT_PATH
                        new_path = normpath(join(project_path, value))
                    # end if

                    fo = open(new_path, 'r')
                # end if

                lines = fo.readlines()
                fo.close()

            except (IOError, URLError):
                parser.error('%s: argument not found' % (value,))
            # end try

            root, ext = splitext(value)

            if ext == '.pfl':
                for line in lines:
                    line = line.strip()

                    if not line or line.startswith(';'):
                        continue
                    # end if

                    check_args(line, dirname(new_path))
                # end for
                return basename(root)

            elif ext == '.ini':
                profiles.append(new_path)
                return basename(dirname(new_path))

            else:
                parser.error(f'{value}: invalid argument extension "{ext}"')
            # end if

        # end def checkArg

        for arg in args.profiles:
            profiles.append(f'#{check_args(arg, getcwd())}')
        # end for

        # args.profiles is positional argument. It is not part of options dictionary.
        # option parser is upgraded to argument parser.
        # (opts, args) = OptionParser.parse_args() ==> args = ArgumentParser.parse_args()
        # opts ==> args
        # args ==> args.profiles
        # **opts.__dict__ ==> **args.__dict__
        del args.profiles
        sys.exit(self.run(profiles, **args.__dict__))
    # end def __init__
# end class Main


if __name__ == '__main__':
    Main()
# end if

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
