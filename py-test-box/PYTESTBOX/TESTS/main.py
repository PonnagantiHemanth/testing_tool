#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: main
:brief: The main program entry point.
:author: Christophe Roquebert <croquebert@logitech.com>
:version: 0.2.0.0
:date: 2010/12/16
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from atexit import register
from os.path import abspath
from os.path import dirname
from os.path import exists
from os.path import isdir
from os.path import join
from os.path import normpath
from os import environ
from os import getgid
from os import getuid
import pathlib
import random
from subprocess import Popen
import sys
import threading
import traceback


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
# Possibility to have every print to do it both on sys.stdout and a spy file
ADD_SPY_FILE_TO_PRINT = False
# Possibility to enable the faulthandler module of python to know where a segmentation fault occurred
# It is not always activated because it remembers the file descriptor of stderr, usually fd 2. The problem is that fd 2
# may become something else, like a socket, a pipe, an important file, etc.
# There is no reliable way to detect this situation, and so it's safer to not enable faulthandler by default in Python.
# faulthandler is safe in almost all cases, except when a file descriptor stored by faulthandler is replaced.
# Problem also described in the doc: https://docs.python.org/dev/library/faulthandler.html#issue-with-file-descriptors
ADD_FAULT_HANDLER = True

# Possibility to enable the atexit mechanism to change the
ATEXIT_PERMISSION_CLEANUP = False
py_test_box_path = str(pathlib.Path(__file__).parent.resolve()).split("/")
py_test_box_path = "/".join(py_test_box_path[:py_test_box_path.index("PYTESTBOX")])
command_chown_at_exit_py_test_box = ["chown", "-R", f"{getuid()}:{getgid()}", py_test_box_path]
command_chmod_at_exit_py_test_box = ["chmod", "-R", "-s", py_test_box_path]
power_supply_json_path = "/home/pi/framework"
if exists(power_supply_json_path):
    command_chown_at_exit_power_supply_json = ["chown", "-R", f"{getuid()}:{getgid()}", power_supply_json_path]
    command_chmod_at_exit_power_supply_json = ["chmod", "-R", "-s", power_supply_json_path]
else:
    command_chown_at_exit_power_supply_json = None
    command_chmod_at_exit_power_supply_json = None
# end if

if ADD_FAULT_HANDLER:
    import faulthandler
    import signal

    faulthandler.enable()
    current_handler = signal.getsignal(signal.SIGTERM)

    def print_trace_if_signal_term(_sig_number, _stack_frame):
        """
        Wrapper to print the traceback of each associated python thread. For more information, See ``signal.signal`` in:
        https://docs.python.org/3/library/signal.html

        :param _sig_number: The signal number
        :type _sig_number: ``int``
        :param _stack_frame: The current stack frame
        :type _stack_frame: ``object`` or ``None``
        """
        # noinspection PyBroadException
        try:
            # A try is added to be able to reset the SIGTERM signal even if the faulthandler has an exception
            faulthandler.dump_traceback(file=sys.stdout)
        except Exception:
            traceback.print_exc()
            pass
        # end try

        if ATEXIT_PERMISSION_CLEANUP:
            permission_cleanup()
        # end if

        signal.signal(signal.SIGTERM, current_handler)
        signal.pthread_kill(threading.get_ident(), signal.SIGTERM)
    # end def print_trace_if_signal_term

    signal.signal(signal.SIGTERM, print_trace_if_signal_term)
# end if


class MultiFile(object):
    """
    Object to use to write on multiple files the same logs
    """

    def __init__(self, *files):
        """
        :param files: Files that are part of this ``MultiFile``, it has to be a writable object
        :type files: ``tuple[writable object]``
        """
        self.files = files
    # end def __init__

    def write(self, obj):
        """
        Write method to write on each file in the ``MultiFile``.

        :param obj: The object to write
        :type obj: ``object``

        :return: The average number of bytes written on each file
        :rtype: ``int``
        """
        to_return = []
        for _f in self.files:
            to_return.append(_f.write(obj))
            _f.flush()  # If you want the output to be visible immediately
        # end for

        return int(sum(to_return) / len(to_return))
    # end def write

    def flush(self):
        """
        Flush method to flush on each file in the ``MultiFile``.
        """
        for _f in self.files:
            _f.flush()
        # end for
    # end def flush
# end class MultiFile


class Main(object):
    """
    Main framework class.
    """

    def __init__(self):
        """
        Constructor, that runs the validation.
        """
        self.result = 0

        original = None
        f = None
        if ADD_SPY_FILE_TO_PRINT:
            f = open(dirname(abspath(__file__)) + '/spy_file_to_print.txt', 'w')
            original = sys.stdout
            sys.stdout = MultiFile(sys.stdout, f)
        # end if

        self.update_path()
        self.run()

        if ADD_SPY_FILE_TO_PRINT:
            sys.stdout = original
            f.close()
        # end if

    # end def __init__

    @staticmethod
    def update_path():
        """
        Updates the system path.
        """
        # Set Pointer on PySetup
        _PySetup = dirname(abspath(__file__))
        _PySetup = join(_PySetup[:_PySetup.index(normpath('/TESTS/'))], 'LIBS', 'PYSETUP', 'PYTHON')
        if _PySetup not in sys.path:
            sys.path.insert(0, _PySetup)
        # end if
        import pysetup

        # All paths to add
        def _if_present(entry):
            return '' if entry not in pysetup.__dict__ else pysetup.__dict__[entry]
        # end def _if_present

        paths = [  # --------- Common Paths -------------------------------------------------------------
            _PySetup,  # PySetup entry point
            join(getattr(pysetup, "TESTS_PATH"), 'SOURCE'),  # Tests entry point
            join(getattr(pysetup, "LIBS_PROJECT_PATH"), 'PYTHON'),  # Egg Libraries entry point
            getattr(pysetup, "PYLIBRARY"),  # PyLibrary
            getattr(pysetup, "PYHARNESS"),  # PyHarness
            # --------- Special tools Paths ------------------------------------------------------
            _if_present('PYTRANSPORT'),  # PyTransport library: Transport interface wrapper
            _if_present('LOGIUSB'),  # Logiusb library: Logitech custom USB interface wrapper
            _if_present('PYCHANNEL'),  # PyChannel library: Channel interface wrapper
            _if_present('PYUSB'),  # PyUsb library: USB interface wrapper
            _if_present('PYHID'),  # PyHid library: HID Data generator
            _if_present('PYRASPI')  # PyRaspi library: Raspi service library
        ]

        # Create PYTHONPATH if not existing
        if 'PYTHONPATH' not in environ:
            environ['PYTHONPATH'] = ''
        # end if

        # Append previous paths to sys.path and os.environ
        paths = [path for path in paths if isdir(path)]
        for path in paths:
            # Update for current module
            sys.path.insert(0, path)
            # Update for children (subprocess)
            environ['PATH'] = "%s;%s" % (path, environ['PATH'])
            environ['PYTHONPATH'] = "%s;%s" % (path, environ['PYTHONPATH'])
        # end for

        # TODO: TO BE REMOVED WHEN PYHARNESS TAKE IT INTO ACCOUNT
        #       To have no crash on win32com __init__ package during static analysis
        # import win32com

    # end def updatePath

    @staticmethod
    def force_seed_in_randrange(start, stop=None, step=1):
        """
        Overwrite the randrange method from Random module.

        Force a re-initialization of the seed each time the function is called
        """
        random.seed(0)
        return random.randrange(start, stop, step)

    # end def forceSeedInRandrange

    def run(self):
        """
        Runs the validation.
        """
        _module, _class = 'pyharness.main', 'Main'

        # Fix random seed if asked
        if '--no-random' in sys.argv:
            from random import Random
            Random.randrange = self.force_seed_in_randrange
            sys.argv.remove('--no-random')
        # end if

        # Unset .egg parsing by default (only do it if asked)
        if ('--eggs' not in sys.argv) and ('--no-eggs' not in sys.argv):
            sys.argv.append('--no-eggs')
        # end if

        # Lookup the target program
        # importFqn cannot be imported at top, as pylibrary may not be available
        #         from pylibrary.tools.importutils import importFqn
        #         attr = importFqn(_module + "." + _class)
        from pyharness.main import Main

        # Run the program
        result = Main()
        if result is not None and hasattr(result, 'result'):
            self.result = result.result
        # end if
    # end def run
# end class Main


def permission_cleanup():
    Popen(command_chown_at_exit_py_test_box)
    Popen(command_chmod_at_exit_py_test_box)

    if command_chown_at_exit_power_supply_json is not None and command_chmod_at_exit_power_supply_json is not None:
        Popen(command_chown_at_exit_power_supply_json)
        Popen(command_chmod_at_exit_power_supply_json)
    # end if
# end def permission_cleanup


if __name__ == '__main__':
    if ATEXIT_PERMISSION_CLEANUP:
        register(permission_cleanup)
    # end if
    Main()  # DO NOT EXIT WITH RETCODE=Main.result (CI needs)
# end if

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
