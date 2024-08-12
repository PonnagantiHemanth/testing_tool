#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: settingsexplorer.utils
:brief: Settings Explorer utility module
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/04/12
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from configparser import ConfigParser

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------

class CaseSensitiveConfigParser(ConfigParser):
    """
    Define a case sensitive ConfigParser
    """
    def __init__(self, *args, **kwargs):
        # See ``ConfigParser.__init__``
        super().__init__(*args, **kwargs)
        self.optionxform = str
    # end def __init__
# end class CaseSensitiveConfigParser


def extract_section_dict(config_dict, section):
    """
    Extract a section's config dict from a bigger config dict going through the levels

    :param config_dict: The config dict to extract the section from
    :type config_dict: ``dict``
    :param section: The section to select in the config dict
    :type section: ``str``

    :return: The config dict starting with the current section
    :rtype: ``dict``

    :raise ``IndexError``: If section doesn't represent a section in the current config dict tree
    """
    sections_level = section.split("/")
    for section_level in sections_level:
        value = config_dict.get(section_level)
        if isinstance(value, dict):
            config_dict = value
        else:
            raise IndexError(f"Section @{section_level} is not a dict")
        # end if
    # end for
    return config_dict
# end def extract_section_dict

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
