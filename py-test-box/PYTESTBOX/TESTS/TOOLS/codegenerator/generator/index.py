#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.generator.index
:brief: Generator for index class
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/05/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from string import Template

from codegenerator.generator.common import CommonFileGenerator
from codegenerator.input.autoinput import AutoInput
from codegenerator.input.engine import EventInfo
from codegenerator.input.engine import FunctionInfo
from codegenerator.input.templates import FeatureTemplate
from codegenerator.manager.engine import ConstantTextManager


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class IndexGenerator(object):
    """
    Generate ``class Index``
    """

    @staticmethod
    def get_class_index_values(info_list):
        """
        Generate the key for ``class INDEX`` information

        :param info_list: The list of Function/Event information
        :type info_list: ``list[FunctionInfo | EventInfo]``

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        for value in info_list:
            # Example: Get Friendly Name Len => GET_FRIENDLY_NAME_LEN
            name = value.get_name_upper_underscore()
            if value.index > 0:
                output.append(f'\n{" " * 8}')
            # end if
            output.append(f'{name} = {value.index}')
        # end for
        return "".join(output)
    # end def get_class_index_values

    @staticmethod
    def get_function_data_model_values(version):
        """
        Get ``Data Model`` section values

        :param version: Version
        :type version: ``int``

        :return: Formatted output
        :rtype: ``tuple[str, str]``
        """
        output = []
        multi_version_text = ""
        for function_info in AutoInput.FUNCTION_LIST:
            version_text = ""
            if function_info.check_multi_version():
                version_text = AutoInput.get_version_text(version)
                multi_version_text = version_text
            # end if
            if function_info.is_this_version_applicable(version):
                output.append(Template(FeatureTemplate.FUNCTION_DATA_MODEL).substitute(dict(
                    IndexName=function_info.get_name_upper_underscore(),
                    ApiName=function_info.get_name_without_space(),
                    Response="Response",
                    VersionText=version_text
                )))
            elif function_info.check_bigger_than_upto_version(version) or \
                    function_info.check_bigger_than_only_version(version):
                output.append(Template(FeatureTemplate.FUNCTION_DATA_MODEL).substitute(dict(
                    IndexName=function_info.get_name_upper_underscore(),
                    ApiName="None",
                    Response="",
                    VersionText=""
                )))
            # end if
        # end for
        output = CommonFileGenerator.uniquify_list(output)
        return ",".join(output), multi_version_text
    # end def get_function_data_model_values

    @staticmethod
    def get_event_data_model_values(version):
        """
        Get ``Data Model`` section values

        :param version: Version
        :type version: ``int``

        :return: Formatted output
        :rtype: ``tuple[str, str]``
        """
        output = []
        multi_version_text = ""
        for event_info in AutoInput.EVENT_LIST:
            version_text = ""
            if event_info.check_multi_version():
                version_text = AutoInput.get_version_text(version)
                multi_version_text = version_text
            # end if
            dictionary = None
            if event_info.event.is_this_version_applicable(version):
                dictionary = dict(
                    IndexName=event_info.get_name_upper_underscore(),
                    ApiName=event_info.get_name_without_space(),
                    Event=f"Event{version_text}"
                )
            elif event_info.check_bigger_than_upto_version(version) or \
                    event_info.check_bigger_than_only_version(version):
                dictionary = dict(
                    IndexName=event_info.get_name_upper_underscore(),
                    ApiName="None",
                    Event=""
                )
            # end if
            if dictionary is not None:
                text = Template(FeatureTemplate.EVENT_DATA_MODEL_SINGLE_LINE).substitute(dictionary)
                if len(text) > ConstantTextManager.LINE_WRAP_AT_CHAR:
                    text = Template(FeatureTemplate.EVENT_DATA_MODEL_MULTI_LINE).substitute(dictionary)
                # end if
                output.append(text)
            # end if
        # end for
        output = CommonFileGenerator.uniquify_list(output)
        return ",".join(output), multi_version_text
    # end def get_event_data_model_values
# end class IndexGenerator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
