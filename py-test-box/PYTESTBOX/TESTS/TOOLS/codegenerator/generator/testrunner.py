#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.generator.testrunner
:brief: Generator for test runner class
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/05/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from string import Template

from codegenerator.generator.common import CommonFileGenerator
from codegenerator.input.autoinput import AutoInput
from codegenerator.input.templates import TestRunnerTemplate


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TestRunnerGenerator(CommonFileGenerator):
    """
    Generate ``TestRunner`` file
    """

    @staticmethod
    def _get_dictionary():
        """
        Get the ``Test Runner`` related inputs in dictionary format

        :return: Template substitute values
        :rtype: ``dict``
        """
        # get common dictionary first
        dictionary = AutoInput.get_common_dictionary()

        prefix = f"\nfrom pytestbox.{dictionary['HidppType']}.hidpp20.{dictionary['HidppCategory']}." \
                 f"feature_{dictionary['HidppFIDLower']}"
        name = dictionary['FeatureNameTitleCaseWithoutSpace']
        import_list = [
            "\nfrom pyharness.extensions import PyHarnessSuite",
            AutoInput.get_import_text(f"{prefix}.interface import {name}InterfaceTestCase"),
            AutoInput.get_import_text(f"{prefix}.robustness import {name}RobustnessTestCase"),
            AutoInput.get_import_text(f"{prefix}.errorhandling import {name}ErrorHandlingTestCase"),
        ]
        run_list = [
            f"\n        self.runTest(result, context, {name}InterfaceTestCase)",
            f"\n        self.runTest(result, context, {name}ErrorHandlingTestCase)",
            f"\n        self.runTest(result, context, {name}RobustnessTestCase)"
        ]

        # insert functionality test case (if present) after Interface & before ErrorHandling
        if len(AutoInput.TEST_CASES_INFO_FUNCTIONALITY) > 0:
            import_list.append(AutoInput.get_import_text(f"{prefix}.functionality import {name}FunctionalityTestCase"))
            run_list.insert(1, f"\n        self.runTest(result, context, {name}FunctionalityTestCase)")
        # end if

        # insert business test case (if present) after Interface & before Functionality
        if len(AutoInput.TEST_CASES_INFO_BUSINESS) > 0:
            import_list.append(AutoInput.get_import_text(f"{prefix}.business import {name}BusinessTestCase"))
            run_list.insert(1, f"\n        self.runTest(result, context, {name}BusinessTestCase)")
        # end if

        # Add security test case (if present) last in the list
        if len(AutoInput.TEST_CASES_INFO_SECURITY) > 0:
            import_list.append(AutoInput.get_import_text(f"{prefix}.security import {name}SecurityTestCase"))
            run_list.append(f"\n        self.runTest(result, context, {name}SecurityTestCase)")
        # end if

        # Add performance test case (if present) last in the list
        if len(AutoInput.TEST_CASES_INFO_PERFORMANCE) > 0:
            import_list.append(AutoInput.get_import_text(f"{prefix}.performance import {name}PerformanceTestCase"))
            run_list.append(f"\n        self.runTest(result, context, {name}PerformanceTestCase)")
        # end if

        import_list.sort()
        dictionary["ImportValues"] = import_list
        dictionary["RunTest"] = "".join(run_list)
        dictionary["FeatureTestSuite"] = f"Feature{dictionary['HidppFIDUpper']}TestSuite"
        if dictionary["HidppVersion"] == "HID++ 2.0":
            dictionary["HidppN"] = "Hidpp20"
        elif dictionary["HidppVersion"] == "HID++ 1.0":
            dictionary["HidppN"] = "Hidpp10"
        else:
            dictionary["HidppN"] = "HidppUnknown"
        # end if

        return dictionary
    # end def _get_dictionary

    def __init__(self):
        super().__init__()
        # get input dictionary specific to test runner file
        self.input_dictionary = self._get_dictionary()
    # end def __init__

    def process(self):
        """
        Process the list of operations to generate import/constant/implementation sections
        """
        self.update_import_section(self.input_dictionary["ImportValues"])
        self.update_implementation_section([Template(TestRunnerTemplate.TEST_RUNNER_CLASS).substitute(
            self.input_dictionary)])
    # end def process
# end class TestRunnerGenerator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
