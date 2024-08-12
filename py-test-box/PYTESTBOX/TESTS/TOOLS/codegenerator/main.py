#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.main
:brief: Code Generator main application
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/05/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import os
import os.path as op
import shutil
import sys


FILE_PATH = op.abspath(__file__)
WS_DIR = FILE_PATH[:FILE_PATH.rfind("TESTS")]
TOOLS_DIR = op.join(WS_DIR, "TESTS", "TOOLS")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)
# end if

# noinspection PyUnresolvedReferences
from codegenerator.generator.engine import PyHidGenerator
# noinspection PyUnresolvedReferences
from codegenerator.generator.engine import TestSuiteGenerator


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class CodeGenerator(object):
    """
    Define main operations in order.
    """

    @staticmethod
    def generate():
        """
        Generate the list of files
        """
        if op.isdir("output"):
            # Remove the existing output folder before any operation
            shutil.rmtree("output")
        # end if

        # Create the output folder
        os.mkdir("output")
        os.mkdir("output/LIBS")
        os.mkdir("output/LIBS/PYHID")
        os.mkdir("output/LIBS/PYHID/pyhid")
        os.mkdir("output/LIBS/PYHID/pyhid/hidpp")
        os.mkdir("output/LIBS/PYHID/pyhid/hidpp/features")
        os.mkdir("output/TESTS")
        os.mkdir("output/TESTS/SETTINGS")
        os.mkdir("output/TESTS/TESTSUITES")
        os.mkdir("output/TESTS/TESTSUITES/pytestbox")
        os.mkdir("output/TESTS/TESTSUITES/pytestbox/base")
        os.mkdir("output/TESTS/TESTSUITES/pytestbox/device")
        os.mkdir("output/TESTS/TESTSUITES/pytestbox/device/base")

        py_hid = PyHidGenerator()

        # Ex: Generate PYTESTBOX/LIBS/PYHID/pyhid/hidpp/features/common/devicefriendlyname.py
        py_hid.generate_feature_file()

        # Ex: Generate PYTESTBOX/LIBS/PYHID/pyhid/hidpp/features/common/devicefriendlyname_test.py
        py_hid.generate_feature_test_file()

        # Ex: Generate PYTESTBOX/LIBS/PYHID/pyhid/hiddispatcher.py
        py_hid.generate_hid_dispatcher_file()

        test_suite = TestSuiteGenerator()

        # Ex: Generate PYTESTBOX/TESTS/TESTSUITES/pytestbox/base/features.py
        test_suite.generate_base_feature_file()

        # Ex: Generate PYTESTBOX/TESTS/TESTSUITES/pytestbox/base/registration.py
        test_suite.generate_base_registration_file()

        # Ex: Generate PYTESTBOX/TESTS/SETTINGS/PRODUCT/PRODUCT.settings.ini
        test_suite.generate_settings_file()

        # Ex: Generate PYTESTBOX/TESTS/TESTSUITES/pytestbox/device/base/devicefriendlynameutils.py
        test_suite.generate_utils_file()

        # Ex: Generate PYTESTBOX/TESTS/TESTSUITES/pytestbox/device/hidpp20/common/feature_0007/*.py
        test_suite.generate_testsuite_files()
    # end def generate
# end class CodeGenerator


# ----------------------------------------------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    CodeGenerator().generate()
# end if

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
