#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.parser.engine
:brief: Parser engine
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/05/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from string import Template

from codegenerator.manager.engine import ConstantTextManager


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class HeaderSectionParser(object):
    """
    Parse file header operations
    """

    @staticmethod
    def get_file_header(text):
        """
        Get file top header

        :param text: Documentation text
        :type text: ``str``

        :return: Header info
        :rtype: ``list[str]``
        """
        return [
            ConstantTextManager.ENVIRONMENT,
            ConstantTextManager.NEW_LINE, ConstantTextManager.UTF_FORMAT,
            ConstantTextManager.NEW_LINE, ConstantTextManager.HASH_LINE,
            ConstantTextManager.NEW_LINE, text,
            ConstantTextManager.NEW_LINE, ConstantTextManager.HASH_LINE,
        ]
    # end def get_file_header

    @staticmethod
    def get_module_header(values, input_dictionary):
        """
        Get module header section

        :param values: List of Template text
        :type values: ``dict``
        :param input_dictionary: Dictionary for Template values
        :type input_dictionary: ``dict``

        :return: Header info
        :rtype: ``list[str]``
        """
        return [
            ConstantTextManager.NEW_LINE,
            ConstantTextManager.TRIPLE_QUOTE,

            ConstantTextManager.NEW_LINE,
            ConstantTextManager.TOOL_VERSION_INFO,

            ConstantTextManager.NEW_LINE,
            ConstantTextManager.PACKAGE_KEY,
            Template(values["PackageValue"]).substitute(input_dictionary),

            ConstantTextManager.NEW_LINE,
            ConstantTextManager.BRIEF_KEY,
            Template(values["BriefValue"]).substitute(input_dictionary),

            ConstantTextManager.NEW_LINE,
            ConstantTextManager.AUTHOR_KEY,
            Template(values["AuthorValue"]).substitute(input_dictionary),

            ConstantTextManager.NEW_LINE,
            ConstantTextManager.DATE_KEY,
            Template(values["DateValue"]).substitute(input_dictionary),

            ConstantTextManager.NEW_LINE,
            ConstantTextManager.TRIPLE_QUOTE
        ]
    # end def get_module_header

    @staticmethod
    def get_import_header():
        """
        Get the import section code

        :return: Header info
        :rtype: ``list[str]``
        """
        return [
            ConstantTextManager.NEW_LINE, ConstantTextManager.HASH_LINE,
            ConstantTextManager.NEW_LINE, ConstantTextManager.IMPORTS,
            ConstantTextManager.NEW_LINE, ConstantTextManager.HASH_LINE,
        ]
    # end def get_import_header

    @staticmethod
    def get_constant_header():
        """
        Get the constant section code

        :return: Header info
        :rtype: ``list[str]``
        """
        return [
            ConstantTextManager.NEW_LINE,
            ConstantTextManager.NEW_LINE, ConstantTextManager.HASH_LINE,
            ConstantTextManager.NEW_LINE, ConstantTextManager.CONSTANTS,
            ConstantTextManager.NEW_LINE, ConstantTextManager.HASH_LINE,
        ]
    # end def get_constant_header

    @staticmethod
    def get_implementation_header():
        """
        Get the implementation section header

        :return: Header info
        :rtype: ``list[str]``
        """
        # Have two blank lines, before implementation section
        return [
            ConstantTextManager.NEW_LINE,
            ConstantTextManager.NEW_LINE,
            ConstantTextManager.NEW_LINE, ConstantTextManager.HASH_LINE,
            ConstantTextManager.NEW_LINE, ConstantTextManager.IMPLEMENTATION,
            ConstantTextManager.NEW_LINE, ConstantTextManager.HASH_LINE
        ]
    # end def get_implementation_header

    @staticmethod
    def get_main_header():
        """
        Get the main section code

        :return: Header info
        :rtype: ``list[str]``
        """
        return [
            ConstantTextManager.NEW_LINE, ConstantTextManager.HASH_LINE,
            ConstantTextManager.NEW_LINE, ConstantTextManager.MAIN,
            ConstantTextManager.NEW_LINE, ConstantTextManager.HASH_LINE,
        ]
    # end def get_main_header

    @staticmethod
    def get_end_of_file_header():
        """
        Get the 'END OF FILE' section header

        :return: Header info
        :rtype: ``list[str]``
        """
        # Leave a blank line after 'End of file' section.
        return [
            ConstantTextManager.NEW_LINE, ConstantTextManager.HASH_LINE,
            ConstantTextManager.NEW_LINE, ConstantTextManager.END_OF_FILE,
            ConstantTextManager.NEW_LINE, ConstantTextManager.HASH_LINE,
            ConstantTextManager.NEW_LINE
        ]
    # end def get_end_of_file_header
# end class HeaderSectionParser

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
