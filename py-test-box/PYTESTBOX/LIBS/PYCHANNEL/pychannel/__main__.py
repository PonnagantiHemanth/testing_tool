#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pychannel
:brief: Run auto-tests. Tests are dynamically discovered. To be taken
        into consideration:
            - all package shall contains "__init__.py" file
            - test file shall ends with "test.py"
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/08/06
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import os.path as op
import sys

# import PYSETUP/PYTHON
FILE_PATH = op.abspath(__file__)
WS_DIR = FILE_PATH[:FILE_PATH.rfind("LIBS")]

PYSETUP_DIR = op.join(WS_DIR, "LIBS", "PYSETUP", "PYTHON")
if PYSETUP_DIR not in sys.path:
    sys.path.insert(0, PYSETUP_DIR)
# end if
from pysetup.testRunner import TestRunner


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    test_runner = TestRunner(FILE_PATH)
    test_runner.run()
# end if

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
