#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
@brief  Run auto-tests

@author laurent.gillet

@date   2019/01/10
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------

import sys
import unittest
from .junitResult import JunitResult
import os.path as op

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------

LIBS_TO_IMPORT = ["PYLIBRARY",
                  "PYHARNESS",
                  "PYHID",
                  "PYRASPI",
                  "PYTRANSPORT",
                  "PYCHANNEL",
                  "PYUSB",
                  "PYSETUP",
                  op.join("PYSETUP/PYTHON"),
                  op.join("PYTRANSPORT/pytransport/usb/logiusbcontext/logiusb")]

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class TestRunner(object):
    """
    run auto-tests and generate junit
    """

    def __init__(self, lib_path):
        """
        create object and resolve import
        :param lib_path: library under test
        :return:
        """
        # resolve path
        self.lib_path = op.abspath(lib_path)
        self.lib_dir = op.dirname(self.lib_path)
        self.ws_dir = self.lib_path[:self.lib_path.rfind("LIBS")]

        # resolve import
        for lib_name in LIBS_TO_IMPORT:
            lib_path = op.join(self.ws_dir, "LIBS", lib_name)
            if (lib_path not in sys.path):
                sys.path.insert(0, lib_path)
            # end if
        # end for
    # end def

    def run(self, xml_path=""):
        """
        run tests and create xml in provided path
        :param xml_path: full path name to junit (default = TEST/LOCAL)
        :return:
        """
        suite = unittest.TestLoader().discover(self.lib_dir, pattern="*test.py")
        runner = unittest.TextTestRunner(resultclass=JunitResult)
        result = runner.run(suite)
        if not xml_path:
            result_name = "{}.xml".format(op.basename(self.lib_dir))
            xml_path = op.join(self.ws_dir, "TESTS", "LOCAL", "LIBS", result_name)
        # end if
        result.write_junit(xml_path)
    # end def
# end class

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------

