#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.generator.engine
:brief: Generator engine
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/05/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import os
import sys

from codegenerator.generator.business import BusinessGenerator
from codegenerator.generator.common import CommonPackageGenerator
from codegenerator.generator.errorhandling import ErrorHandlingGenerator
from codegenerator.generator.feature import FeatureGenerator
from codegenerator.generator.featurename import FeatureNameGenerator
from codegenerator.generator.featuretest import FeatureTestGenerator
from codegenerator.generator.functionality import FunctionalityGenerator
from codegenerator.generator.hiddispatcher import HidDispatcherGenerator
from codegenerator.generator.interface import InterfaceGenerator
from codegenerator.generator.performance import PerformanceGenerator
from codegenerator.generator.registration import RegistrationGenerator
from codegenerator.generator.robustness import RobustnessGenerator
from codegenerator.generator.security import SecurityGenerator
from codegenerator.generator.settings import SettingsGenerator
from codegenerator.generator.subsystem import SubSystemGenerator
from codegenerator.generator.testrunner import TestRunnerGenerator
from codegenerator.generator.utils import UtilsGenerator
from codegenerator.input.autoinput import AutoInput
from codegenerator.input.templates import BusinessTemplate
from codegenerator.input.templates import ErrorHandlingTemplate
from codegenerator.input.templates import FeatureNameTemplate
from codegenerator.input.templates import FeatureTemplate
from codegenerator.input.templates import FeatureTestTemplate
from codegenerator.input.templates import FunctionalityTemplate
from codegenerator.input.templates import InitTemplate
from codegenerator.input.templates import InterfaceTemplate
from codegenerator.input.templates import PerformanceTemplate
from codegenerator.input.templates import RobustnessTemplate
from codegenerator.input.templates import SecurityTemplate
from codegenerator.input.templates import TestRunnerTemplate
from codegenerator.input.templates import UtilsTemplate
from codegenerator.manager.engine import ConstantTextManager


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PyHidGenerator(CommonPackageGenerator):
    """
    Generate PYHID Library files
    """
    def generate_hid_dispatcher_file(self):
        """
        Generate the hiddispatcher.py file
        """
        self.reset()

        # Process: where sections are populated.
        obj = HidDispatcherGenerator()
        obj.process()
        self.update_values(obj.get_implementation_section())

        self.write_to_file(f"output/LIBS/PYHID/pyhid/hiddispatcher.py")
    # end def generate_hid_dispatcher_file

    def generate_feature_file(self):
        """
        Generate the feature file
        """
        self.reset()

        # Process: where sections are populated.
        obj = FeatureGenerator()
        obj.process()

        self.update_sections(obj, FeatureTemplate, obj.input_dictionary, ConstantTextManager.PY_TEST_BOX)

        path = f"output/LIBS/PYHID/pyhid/hidpp/features/{obj.input_dictionary['HidppCategory']}"
        os.mkdir(path)
        self.write_to_file(f"{path}/{obj.input_dictionary['FeatureNameLowerCaseWithoutSpace']}.py")
    # end def generate_feature_file

    def generate_feature_test_file(self):
        """
        Generate the feature test file
        """
        self.reset()

        # Process: where sections are populated.
        obj = FeatureTestGenerator()
        obj.process()

        self.update_sections(obj, FeatureTestTemplate, obj.input_dictionary, ConstantTextManager.PY_TEST_HARNESS)

        path = f"output/LIBS/PYHID/pyhid/hidpp/features/{obj.input_dictionary['HidppCategory']}/test"
        os.mkdir(path)
        self.write_to_file(f"{path}/{obj.input_dictionary['FeatureNameLowerCaseWithoutSpace']}_test.py")
    # end def generate_feature_test_file
# end class PyHidGenerator


class TestSuiteGenerator(CommonPackageGenerator):
    """
    Generate TestSuite files
    """

    def generate_base_registration_file(self):
        """
        Generate the base/features.py file
        """
        self.reset()

        # Process: where sections are populated.
        obj = RegistrationGenerator()
        obj.process()
        self.update_values(obj.get_implementation_section())

        self.write_to_file(f"output/TESTS/TESTSUITES/pytestbox/base/registration.py")
    # end def generate_base_registration_file

    def generate_base_feature_file(self):
        """
        Generate the base/features.py file
        """
        self.reset()

        # Process: where sections are populated.
        obj = SubSystemGenerator()
        obj.process()
        self.update_values(obj.get_implementation_section())

        self.write_to_file(f"output/TESTS/TESTSUITES/pytestbox/base/features.py")
    # end def generate_base_feature_file

    def generate_settings_file(self):
        """
        Generate the settings.ini file
        """
        self.reset()

        # Process: where sections are populated.
        obj = SettingsGenerator()
        obj.process()
        self.update_values(obj.get_implementation_section())

        self.write_to_file(f"output/TESTS/SETTINGS/SPECIFIC_PRODUCT.settings.ini")
    # end def generate_settings_file

    def generate_utils_file(self):
        """
        Generate the utils file
        """
        self.reset()

        # Process: where sections are populated.
        obj = UtilsGenerator()
        obj.process()

        self.update_sections(obj, UtilsTemplate, obj.input_dictionary, ConstantTextManager.PY_TEST_BOX)

        file_name = obj.input_dictionary['FeatureNameLowerCaseWithoutSpace']
        self.write_to_file(f"output/TESTS/TESTSUITES/pytestbox/device/base/{file_name}utils.py")
    # end def generate_utils_file

    def generate_testsuite_files(self):
        """
        Generate the list of test suite files
        """
        # get input dictionary
        input_dictionary = AutoInput.get_common_dictionary()
        path = f"output/TESTS/TESTSUITES/pytestbox/{input_dictionary['HidppType']}"
        if input_dictionary['HidppType'] != "device":
            os.mkdir(path)
        # end if
        path += "/hidpp20"
        os.mkdir(path)
        path += f"/{input_dictionary['HidppCategory']}"
        os.mkdir(path)
        path += f"/feature_{input_dictionary['HidppFIDLower']}"
        os.mkdir(path)

        self.generate_business_file()
        self.generate_error_handling_file()
        self.generate_functionality_file()
        self.generate_interface_file()
        self.generate_robustness_file()
        self.generate_security_file()
        self.generate_performance_file()
        self.generate_init_file()
        self.generate_feature_name_file()
        self.generate_test_runner_file()
    # end def generate_testsuite_files

    def generate_feature_name_file(self):
        """
        Generate the ``feature name`` test suite file
        """
        self.reset()

        # Process: where sections are populated.
        obj = FeatureNameGenerator()
        obj.process()

        self.update_sections(obj, FeatureNameTemplate, obj.input_dictionary, ConstantTextManager.PY_TEST_BOX)

        self.write_to_file(
            f"{AutoInput.get_feature_location()}/{obj.input_dictionary['FeatureNameLowerCaseWithoutSpace']}.py")
    # end def generate_feature_name_file

    def generate_performance_file(self):
        """
        Generate the ``performance`` test suite file
        """
        if len(AutoInput.TEST_CASES_INFO_PERFORMANCE) == 0:
            sys.stdout.write("\nSkip performance since no test cases found")
            return
        # end if
        self.reset()

        # Process: where sections are populated.
        obj = PerformanceGenerator()
        obj.process()

        self.update_sections(obj, PerformanceTemplate, obj.input_dictionary, ConstantTextManager.PY_TEST_BOX)

        self.write_to_file(f"{AutoInput.get_feature_location()}/performance.py")
    # end def generate_performance_file

    def generate_security_file(self):
        """
        Generate the ``security`` test suite file
        """
        if len(AutoInput.TEST_CASES_INFO_SECURITY) == 0:
            sys.stdout.write("\nSkip security since no test cases found")
            return
        # end if
        self.reset()

        # Process: where sections are populated.
        obj = SecurityGenerator()
        obj.process()

        self.update_sections(obj, SecurityTemplate, obj.input_dictionary, ConstantTextManager.PY_TEST_BOX)

        self.write_to_file(f"{AutoInput.get_feature_location()}/security.py")
    # end def generate_security_file

    def generate_business_file(self):
        """
        Generate the ``business`` test suite file
        """
        if len(AutoInput.TEST_CASES_INFO_BUSINESS) == 0:
            sys.stdout.write("\nSkip business since no test cases found")
            return
        # end if
        self.reset()

        # Process: where sections are populated.
        obj = BusinessGenerator()
        obj.process()

        self.update_sections(obj, BusinessTemplate, obj.input_dictionary, ConstantTextManager.PY_TEST_BOX)

        self.write_to_file(f"{AutoInput.get_feature_location()}/business.py")
    # end def generate_business_file

    def generate_error_handling_file(self):
        """
        Generate the ``error handling`` test suite file
        """
        self.reset()

        # Process: where sections are populated.
        obj = ErrorHandlingGenerator()
        obj.process()

        self.update_sections(obj, ErrorHandlingTemplate, obj.input_dictionary, ConstantTextManager.PY_TEST_BOX)

        self.write_to_file(f"{AutoInput.get_feature_location()}/errorhandling.py")
    # end def generate_error_handling_file

    def generate_functionality_file(self):
        """
        Generate the ``functionality`` test suite file
        """
        if len(AutoInput.TEST_CASES_INFO_FUNCTIONALITY) == 0:
            sys.stdout.write("\nSkip functionality since no test cases found")
            return
        # end if
        self.reset()

        # Process: where sections are populated.
        obj = FunctionalityGenerator()
        obj.process()

        self.update_sections(obj, FunctionalityTemplate, obj.input_dictionary, ConstantTextManager.PY_TEST_BOX)

        self.write_to_file(f"{AutoInput.get_feature_location()}/functionality.py")
    # end def generate_functionality_file

    def generate_interface_file(self):
        """
        Generate the ``interface`` test suite file
        """
        self.reset()

        # Process: where sections are populated.
        obj = InterfaceGenerator()
        obj.process()

        self.update_sections(obj, InterfaceTemplate, obj.input_dictionary, ConstantTextManager.PY_TEST_BOX)

        self.write_to_file(f"{AutoInput.get_feature_location()}/interface.py")
    # end def generate_interface_file

    def generate_robustness_file(self):
        """
        Generate the ``robustness`` test suite file
        """
        self.reset()

        # Process: where sections are populated.
        obj = RobustnessGenerator()
        obj.process()

        self.update_sections(obj, RobustnessTemplate, obj.input_dictionary, ConstantTextManager.PY_TEST_BOX)

        self.write_to_file(f"{AutoInput.get_feature_location()}/robustness.py")
    # end def generate_robustness_file

    def generate_test_runner_file(self):
        """
        Generate the ``test runner`` test suite file
        """
        self.reset()

        # Process: where sections are populated.
        obj = TestRunnerGenerator()
        obj.process()

        self.update_sections(obj, TestRunnerTemplate, obj.input_dictionary, ConstantTextManager.PY_TEST_BOX)

        self.write_to_file(f"{AutoInput.get_feature_location()}/testrunner.py")
    # end def generate_test_runner_file

    def generate_init_file(self):
        """
        Generate the ``__init__.py`` test suite file
        """
        self.reset()

        # get common dictionary first
        dictionary = AutoInput.get_common_dictionary()

        self.update_sections(None, InitTemplate, dictionary, ConstantTextManager.PY_TEST_BOX)

        self.write_to_file(f"{AutoInput.get_feature_location()}/__init__.py")
    # end def generate_init_file
# end class TestSuiteGenerator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
