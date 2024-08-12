#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.generator.business
:brief: Generator for business class
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
from codegenerator.input.templates import BusinessTemplate
from codegenerator.manager.engine import ConstantTextManager


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BusinessGenerator(CommonFileGenerator):
    """
    Generate ``Business`` file
    """

    @staticmethod
    def _get_dictionary():
        """
        Get the ``Business`` related inputs in dictionary format

        :return: Template substitute values
        :rtype: ``dict``
        """
        # get common dictionary first
        dictionary = AutoInput.get_common_dictionary()

        body = []
        for test_case_info in AutoInput.TEST_CASES_INFO_BUSINESS:
            body.append(ReqResGenerator.get_test_case_item(test_case_info, "Business"))
        # end for

        # Ex: from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyName
        # Ex: from pytestbox.device.hidpp20.common.feature_0007.devicefriendlyname import DeviceFriendlyNameTestCase
        dictionary["ImportStructure"] = [
            AutoInput.get_import_text(Template(BusinessTemplate.IMPORT_BASE_CLASS).substitute(dictionary))]
        dictionary["ClassStructure"] = Template(BusinessTemplate.CLASS_STRUCTURE).substitute(dict(
            Type="business",
            TestCase=dictionary["FeatureNameTitleCaseWithoutSpace"] + "BusinessTestCase",
            FeatureNameTitleCaseWithoutSpace=dictionary["FeatureNameTitleCaseWithoutSpace"],
            BaseTestCase=dictionary["FeatureNameTitleCaseWithoutSpace"] + "TestCase",
            Body="\n".join(body)
        ))

        return dictionary
    # end def _get_dictionary

    def __init__(self):
        super().__init__()
        self.update_import_section([
            ConstantTextManager.IMPORT_LEVEL,
            ConstantTextManager.IMPORT_FEATURES,
            ConstantTextManager.IMPORT_LOG_HELPER
        ])
        # get input dictionary specific to business file
        self.input_dictionary = self._get_dictionary()
    # end def __init__

    def process(self):
        """
        Process the list of operations to generate import/constant/implementation sections
        """
        self.update_import_section(self.input_dictionary["ImportStructure"])
        self.update_constant_section([f"\n_AUTHOR = \"{self.input_dictionary['AuthorName']}\""])
        self.update_implementation_section(self.input_dictionary["ClassStructure"])
    # end def process
# end class BusinessGenerator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
