#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.generator.registration
:brief: Generator for registration section
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2023/03/03
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from string import Template

from codegenerator.generator.common import CommonFileGenerator
from codegenerator.input.autoinput import AutoInput
from codegenerator.input.templates import RegistrationTemplate


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RegistrationGenerator(CommonFileGenerator):
    """
    Generate ``Registration`` section
    """

    @classmethod
    def _get_dictionary(cls):
        """
        Get the Registration related inputs in dictionary format

        :return: Template substitute values
        :rtype: ``dict``
        """
        # get common dictionary first
        dictionary = AutoInput.get_common_dictionary()

        versions = []
        all_versions = AutoInput.get_all_version()
        if len(all_versions) > 1:
            for version_no in all_versions:
                versions.append(Template(RegistrationTemplate.SINGLE_VERSION_TEXT).substitute(dict(
                    NameTitleCaseWithSpace=dictionary["FeatureNameTitleCaseWithSpace"],
                    NameUpperCaseWithUnderscore=dictionary["FeatureNameUpperCaseWithUnderscore"],
                    CategoryUpper=dictionary["HidppCategoryUpper"],
                    FIDUpper=dictionary["HidppFIDUpper"],
                    V="v",
                    No=version_no
                )))
            # end for
        # end if

        dictionary["VersionInfo"] = "\n".join(versions)

        return dictionary
    # end def _get_dictionary

    def __init__(self):
        super().__init__()
        # get input dictionary specific to sub system
        self.input_dictionary = self._get_dictionary()
    # end def __init__

    def process(self):
        """
        Process the list of operations to generate import/constant/implementation sections
        """
        self.update_implementation_section(
            [Template(RegistrationTemplate.GET_REGISTRATION).substitute(self.input_dictionary)])
    # end def process
# end class RegistrationGenerator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
