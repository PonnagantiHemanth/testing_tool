#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
@brief  Test result that export tests à junit file and write summary into the
console

@author laurent.gillet

@date   2019/01/10
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import sys
import unittest
import os.path as op
import xml.etree.ElementTree as ET
from xml.dom import minidom
from os import makedirs

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class JunitResult(unittest.TestResult):
    """
    test result that export unit test as junit file and write summary into
    the console
    """

    junit_content = ""
    junit_element = ET.Element('testsuite')
    error_count = 0
    failure_count = 0

    def addError(self, test, err):
        """
        called each time a test is in error (extend unittest.TestResult)
        """
        full_error = self._exc_info_to_string(err, test)
        summary_error = full_error.splitlines()[-1]
        self._print_console(test, "ERROR", full_error)

        element = ET.Element("error")
        element.set("message", summary_error)
        element.text = full_error

        self._add_in_junit(test, element)
        return super(JunitResult, self).addError(test, err)
    # end def add_error

    def addFailure(self, test, err):
        """
        called each time a test fails (extend unittest.TestResult)
        """
        full_error = self._exc_info_to_string(err, test)
        summary_error = full_error.splitlines()[-1]
        self._print_console(test, "FAIL", full_error)

        element = ET.Element("failure")
        element.set("message", summary_error)
        element.text = full_error

        self._add_in_junit(test, element)
        return super(JunitResult, self).addFailure(test, err)
    # end def addError

    def addSuccess(self, test):
        """
        called each time a test passes (extend unittest.TestResult)
        """
        self._print_console(test, "OK")
        self._add_in_junit(test)
        return super(JunitResult, self).addSuccess(test)
    # end def addPass

    def addSkip(self, test, reason):
        """
        called each time a test is skipped (extend unittest.TestResult)
        """
        """Called when a test is skipped."""
        self._print_console(test, "SKIPPED")
        element = ET.Element("skipped")
        self._add_in_junit(test, element, reason)
        self.skipped.append((test, reason))
    # end def addSkip

    def _print_console(self, test, result, err=""):
        """
        print result in console (standardized way)
        """
        test_name = test.id()
        print("{}... {}".format(test_name, result))
        if err:
            print(err, file=sys.stderr)
        # end if
    # end def _printConsole

    def _add_in_junit(self, test, element=None, stdout=""):
        """
        add test result in junit
        """
        test_name = test.id()
        class_name = test.__class__.__name__

        test_case_element = ET.Element("testcase")
        test_case_element.set("name", test_name)
        test_case_element.set("classname", class_name)
        test_case_element.set("time", "0")

        system_out_element = ET.Element("system-out")
        system_out_element.text = stdout

        system_err_element = ET.Element("system-err")
        system_err_element.text = ""

        if element is not None:
            test_case_element.append(element)
        # end if
        test_case_element.append(system_out_element)
        test_case_element.append(system_err_element)
        self.junit_element.append(test_case_element)
    # end def _add

    def write_junit(self, path):
        """
        export junit file (overwrite if file already exists)
        """
        # create dir if needed
        if not (op.exists(op.dirname(path))):
            makedirs(op.dirname(path))
        # end if

        # build xml and make it pretty (i.e. well indented)
        rough_string = ET.tostring(self.junit_element, 'utf-8')
        mdom = minidom.parseString(rough_string)
        junit_content = mdom.toprettyxml(indent="  ")

        # create junit file (overwrite if file already exists)
        with open(path, "w") as f:
            f.write(junit_content)

        # end with
    # end def writeJunit
# end class MyResult

# ------------------------------------------------------------------------------
# end of filexs
# ------------------------------------------------------------------------------

