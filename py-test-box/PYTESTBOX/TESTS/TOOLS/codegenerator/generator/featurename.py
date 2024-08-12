#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.generator.featurename
:brief: Generator for feature name class
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
from codegenerator.input.templates import FeatureNameTemplate
from codegenerator.manager.engine import ConstantTextManager


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FeatureNameGenerator(CommonFileGenerator):
    """
    Generate ``FeatureName`` file
    """

    @staticmethod
    def _get_dictionary():
        """
        Get the <FeatureName> related inputs in dictionary format

        :return: Template substitute values
        :rtype: ``dict``
        """
        # get common dictionary first
        dictionary = AutoInput.get_common_dictionary()

        if dictionary["NvsBackupRestore"]:
            backup = FeatureNameTemplate.GET_BACKUP
            restore = FeatureNameTemplate.GET_RESTORE
        else:
            backup = ""
            restore = ""
        # end if

        activate_dictionary = dict(
            Manufacturing=", manufacturing=True" if AutoInput.ACTIVATE_FEATURE_MANUFACTURING else "",
            Compliance=", compliance=True" if AutoInput.ACTIVATE_FEATURE_COMPLIANCE else "",
            Gotthard=", gotthard=True" if AutoInput.ACTIVATE_FEATURE_GOTTHARD else ""
        )
        activate_features_text = ""
        if AutoInput.ENABLE_HIDDEN_FEATURES or AutoInput.ACTIVATE_FEATURE_MANUFACTURING\
                or AutoInput.ACTIVATE_FEATURE_COMPLIANCE or AutoInput.ACTIVATE_FEATURE_GOTTHARD:
            activate_features_text = Template(FeatureNameTemplate.ACTIVATE_FEATURES).substitute(activate_dictionary)
        # end if

        setup_section = ""
        # CODE_GENERATION_TOOL_SETUP_SECTION will have the basic pre-requisites for every test case.
        for test_case_info in AutoInput.TEST_CASES_INFO_SETUP_SECTION:
            setup_section += "\n"
            setup_section += ReqResGenerator.get_description(test_case_info)
        # end for
        if len(setup_section) > 0 and setup_section[-1] == "\n":
            # remove the last \n
            setup_section = setup_section[:-1]
        # end if

        post_requisites = ""
        # CODE_GENERATION_TOOL_TEARDOWN_SECTION will have the basic post-requisites for every test case.
        for test_case_info in AutoInput.TEST_CASES_INFO_TEARDOWN_SECTION:
            if len(post_requisites) > 0:
                post_requisites += "\n"
            # end if
            post_requisites += ReqResGenerator.get_description(test_case_info)
        # end for

        tear_down_section = ""
        if len(post_requisites) > 0 or len(restore) > 0:
            tear_down_section = Template(FeatureNameTemplate.GET_TEARDOWN).substitute(dict(
                PostRequisites=post_requisites,
                Restore=restore
            ))
        # end if

        dictionary["ClassStructure"] = Template(FeatureNameTemplate.CLASS_STRUCTURE).substitute(dict(
            FeatureNameTestCase=dictionary["FeatureNameTitleCaseWithoutSpace"] + "TestCase",
            Utils=dictionary["FeatureNameTitleCaseWithoutSpace"] + "TestUtils",
            FIDLower=dictionary["HidppFIDLower"],
            FIDUpper=dictionary["HidppFIDUpper"],
            Index="_index",
            FeatureNameTitleCaseWithoutSpace=dictionary["FeatureNameTitleCaseWithoutSpace"],
            FeatureNameUpperCaseWithUnderscore=dictionary["FeatureNameUpperCaseWithUnderscore"],
            HidppCategoryUpper=dictionary["HidppCategoryUpper"],
            Backup=backup,
            TeardownSection=tear_down_section,
            SetupSection=setup_section,
            EnableHiddenFeatures=activate_features_text
        ))
        dictionary["ImportStructure"] = [
            AutoInput.get_import_text(Template(FeatureNameTemplate.IMPORT_UTIL_CLASS).substitute(dictionary))]

        return dictionary
    # end def _get_dictionary

    def __init__(self):
        super().__init__()
        self.update_import_section([
            ConstantTextManager.IMPORT_DEVICE_BASE_TEST_CASE,
            ConstantTextManager.IMPORT_DEVICE_TEST_UTILS,
            ConstantTextManager.IMPORT_LOG_HELPER
        ])
        # get input dictionary specific to feature name file
        self.input_dictionary = self._get_dictionary()
    # end def __init__

    def process(self):
        """
        Process the list of operations to generate import/constant/implementation sections
        """
        self.update_import_section(self.input_dictionary["ImportStructure"])
        self.update_implementation_section([self.input_dictionary["ClassStructure"]])
    # end def process
# end class FeatureNameGenerator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
