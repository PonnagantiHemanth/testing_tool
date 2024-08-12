#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.generator.subsystem
:brief: Generator for sub system class
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/05/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from string import Template

from codegenerator.generator.common import CommonFileGenerator
from codegenerator.input.autoinput import AutoInput
from codegenerator.input.templates import SubSystemTemplate


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SubSystemGenerator(CommonFileGenerator):
    """
    Generate ``SubSystem`` section
    """

    @classmethod
    def _get_dictionary(cls):
        """
        Get the subsystem related inputs in dictionary format

        :return: Template substitute values
        :rtype: ``dict``
        """
        versions = []
        for version_no in range(AutoInput.get_max_version() + 1):
            versions.append(f"\n                    self.F_Version_{version_no} = False")
        # end for

        settings = []
        for obj in AutoInput.FUNCTION_LIST:
            for parameter in obj.request.parameters + obj.response.parameters:
                settings.extend(cls._get_data_type(parameter=parameter, category="sub_system"))
            # end if
        # end for
        if len(settings) > 0:
            settings.sort()
            settings = cls.uniquify_list(settings)
            settings.insert(0, "\n\n                    # Supported settings")
        # end if

        # get common dictionary first
        dictionary = AutoInput.get_common_dictionary()
        dictionary["SubSystem"] = "SubSystem"
        dictionary["VersionInfo"] = "".join(versions)
        dictionary["FieldInfo"] = "".join(settings)

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
            [Template(SubSystemTemplate.GET_SUB_SYSTEM).substitute(self.input_dictionary)])
    # end def process
# end class SubSystemGenerator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
