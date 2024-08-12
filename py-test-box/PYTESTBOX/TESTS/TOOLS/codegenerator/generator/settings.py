#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.generator.settings
:brief: Generator for settings value
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/05/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from string import Template

from codegenerator.generator.common import CommonFileGenerator
from codegenerator.input.autoinput import AutoInput
from codegenerator.input.templates import SettingsTemplate


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SettingsGenerator(CommonFileGenerator):
    """
    Generate ``Settings`` section
    """

    @classmethod
    def _get_dictionary(cls):
        """
        Get the settings related inputs in dictionary format

        :return: Template substitute values
        :rtype: ``dict``
        """
        # get common dictionary first
        dictionary = AutoInput.get_common_dictionary()

        dictionary["VersionInfo"] = f'\nVersion_{AutoInput.get_max_version()} = True'

        output = []
        for obj in AutoInput.FUNCTION_LIST:
            for parameter in obj.request.parameters + obj.response.parameters:
                output.extend(cls._get_data_type(parameter=parameter, category="settings"))
            # end for
        # end for
        output.sort()
        dictionary["FieldInfo"] = "".join(cls.uniquify_list(output))

        return dictionary
    # end def _get_dictionary

    def __init__(self):
        super().__init__()
        # get input dictionary specific to settings
        self.input_dictionary = self._get_dictionary()
    # end def __init__

    def process(self):
        """
        Process the list of operations to generate settings section
        """
        self.update_implementation_section([Template(SettingsTemplate.GET_SETTINGS).substitute(self.input_dictionary)])
    # end def process
# end class SettingsGenerator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
