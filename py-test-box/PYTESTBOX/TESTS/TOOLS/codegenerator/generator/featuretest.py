#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.generator.featuretest
:brief: Generator for feature test class
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/05/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from string import Template

from codegenerator.generator.common import CommonFileGenerator
from codegenerator.generator.common import ReqResGenerator
from codegenerator.input.autoinput import AutoInput
from codegenerator.input.templates import FeatureTestTemplate
from codegenerator.manager.engine import ConstantTextManager


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FeatureTestGenerator(CommonFileGenerator):
    """
    Generate ``Feature Unitary Test`` file
    """
    @staticmethod
    def _get_dictionary():
        """
        Get the <Feature Test> related inputs in dictionary format

        :return: Template substitute values
        :rtype: ``dict``
        """
        # get the common dictionary first
        dictionary = AutoInput.get_common_dictionary()

        # Extra fixed values required by the program (do not edit)
        dictionary["MaxVersion"] = AutoInput.get_max_version()
        dictionary["InstantiationTestCase"] = "InstantiationTestCase"
        dictionary["SysImportValues"] = ReqResGenerator.get_sys_import_structure()
        dictionary["ImportValues"] = ReqResGenerator.get_import_structure()
        dictionary["ApiStructure"] = ReqResGenerator.get_api_test_structure()
        dictionary["MaxFunctionIndex"] = AutoInput.get_max_function_index()

        version_info = []
        for version in AutoInput.get_all_version():
            dictionary["InterfaceValues"] = ReqResGenerator.get_interfaces_structure(version=version)
            dictionary["MaxFunctionIndex"] = AutoInput.get_max_function_index_number(version=version)
            dictionary["Version"] = f"V{version}"
            version_info.append(Template(FeatureTestTemplate.FEATURE_VERSION_INFO).substitute(dictionary))
        # end for
        dictionary["VersionInfo"] = "".join(version_info)

        return dictionary
    # end def _get_dictionary

    def __init__(self):
        super().__init__()
        self.update_import_section_on_python_library([
            ConstantTextManager.IMPORT_TEST_CASE
        ])
        self.update_import_section([
            ConstantTextManager.IMPORT_ROOT_TEST_CASE
        ])
        # get input dictionary specific to feature test file
        self.input_dictionary = self._get_dictionary()
    # end def __init__

    def process(self):
        """
        Process the list of operations to generate import/constant/implementation sections
        """
        self.update_import_section_on_python_library(self.input_dictionary["SysImportValues"])
        self.update_import_section(self.input_dictionary["ImportValues"])
        self.update_implementation_section([
            Template(FeatureTestTemplate.INSTANTIATION_TEST_CASE).substitute(self.input_dictionary),
            Template(FeatureTestTemplate.FEATURE_TEST_CASE).substitute(self.input_dictionary)
        ])
    # end def process
# end class FeatureTestGenerator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
