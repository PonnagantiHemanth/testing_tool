#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.generator.interface
:brief: Generator for interface class
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
from codegenerator.input.engine import FunctionInfo
from codegenerator.input.templates import InterfaceTemplate
from codegenerator.manager.engine import ConstantTextManager


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class InterfaceGenerator(CommonFileGenerator):
    """
    Generate ``Interface`` file
    """

    @classmethod
    def _get_extension_and_version_no(cls, function_info, version):
        """
        Get extension and version number text

        :param function_info: Function information
        :type function_info: ``FunctionInfo``
        :param version: Version information
        :type version: ``int``

        :return: Extension text and version text
        :rtype: ``tuple[str, str]``
        """
        version_no = ""
        extension = ""
        if function_info.check_multi_version():
            version_no = AutoInput.get_version_text(version)
            extension = f"_{version_no.lower()}"
        # end if
        return extension, version_no
    # end def _get_extension_and_version_no

    @classmethod
    def _get_import_structure(cls, dictionary):
        """
        Get the import structure

        :param dictionary: Dictionary
        :type dictionary: ``dict``

        :return: Import structure
        :rtype: ``list[str]``
        """
        # Ex: from pytestbox.device.base.devicefriendlynameutils import DeviceFriendlyNameUtils
        # Ex: from pytestbox.device.hidpp20.common.feature_0007.devicefriendlyname import DeviceFriendlyNameTestCase
        values = [
            AutoInput.get_import_text(Template(InterfaceTemplate.IMPORT_UTIL_CLASS).substitute(dictionary)),
            AutoInput.get_import_text(Template(InterfaceTemplate.IMPORT_BASE_CLASS).substitute(dictionary))]

        # Ex: from pylibrary.tools.numeral import Numeral (if applicable)
        value = ReqResGenerator.get_import_numeral()
        if len(value) > 0:
            values.append(value)
        # end if

        return values
    # end def _get_import_structure

    @classmethod
    def _get_dictionary(cls):
        """
        Get the ``Interface`` related inputs in dictionary format

        :return: Template substitute values
        :rtype: ``dict``
        """
        # get common dictionary first
        dictionary = AutoInput.get_common_dictionary()

        dictionary["ImportStructure"] = cls._get_import_structure(dictionary)

        body = []
        count = 0
        indent = " " * 4
        for function_info in AutoInput.FUNCTION_LIST:
            count += 1
            output = []
            backup_nvs = f"\n        self.post_requisite_reload_nvs = True" if function_info.nvs_backup_required else ""
            for version in AutoInput.get_version_list():
                if not function_info.is_this_version_applicable(version):
                    continue
                # end if
                extension, version_no = cls._get_extension_and_version_no(function_info, version)

                params_key_value = "test_case=self"
                if len(function_info.request.parameters) > 0:
                    params_key_value = f"\n{indent * 3}test_case=self,\n{indent * 3}"
                    params_key_value += ReqResGenerator.get_formatted_method_param(
                        parameters=function_info.request.parameters,
                        version=version,
                        format_type="KeyValue",
                        separator=f",\n{indent * 3}")
                # end if

                min_value_req = ReqResGenerator.get_method_param_settings_value(
                    parameters=function_info.request.parameters,
                    space=ReqResGenerator.get_new_line_with_space(space_length=8),
                    equal_to=ConstantTextManager.EQUAL_TO,
                    template=InterfaceTemplate.NAME_VALUE_FORMAT,
                    skip_settings_values=False,
                    result=[],
                    version=version)
                min_value_res = ReqResGenerator.get_method_param_settings_value(
                    parameters=function_info.response.parameters,
                    space=ReqResGenerator.get_new_line_with_space(space_length=8),
                    equal_to=ConstantTextManager.EQUAL_TO,
                    template=InterfaceTemplate.NAME_VALUE_FORMAT,
                    skip_settings_values=True,
                    result=min_value_req,
                    version=version)

                name_lower = function_info.get_name_lower_underscore()

                output.append(Template(InterfaceTemplate.GET_INTERFACE).substitute(dict(
                    MinValue="".join(min_value_res),
                    ParamsKeyValue=params_key_value,
                    Request=f"TestUtils.HIDppHelper.{name_lower}(",
                    CheckMapAndFields=ReqResGenerator.get_check_map_and_fields(
                        dictionary=dictionary,
                        function_info=function_info,
                        template=InterfaceTemplate.CHECK_MAP,
                        space_length=8,
                        version=version,
                        include_device_feature=True),
                    FunctionName=function_info.get_name_without_space(),
                    FunctionLower=name_lower,
                    SingleItem=ReqResGenerator.get_one_api_format_with_input_and_output(
                        function_info=function_info, version=version, indent=2),
                    Ext=extension,
                    Version=version_no,
                    VersionNo=version_no.lower(),
                    Response="Response",
                    FIDUpper=dictionary["HidppFIDUpper"],
                    FeatureNameTitleCaseWithoutSpace=dictionary["FeatureNameTitleCaseWithoutSpace"],
                    Number=f"_{count:04}",
                    BackupNvs=backup_nvs
                )))
            # end for
            if len(output) > 0:
                output = CommonFileGenerator.uniquify_list(output)
                body.append("\n".join(output))
            else:
                count -= 1
            # end if
        # end for

        for test_case_info in AutoInput.TEST_CASES_INFO_INTERFACE:
            body.append(ReqResGenerator.get_test_case_item(test_case_info, "Interface"))
        # end for

        dictionary["ClassStructure"] = Template(InterfaceTemplate.CLASS_STRUCTURE).substitute(dict(
            Type="interface",
            TestCase=dictionary["FeatureNameTitleCaseWithoutSpace"] + "InterfaceTestCase",
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
            ConstantTextManager.IMPORT_LOG_HELPER,
            ConstantTextManager.IMPORT_HEXLIST,
        ])
        # get input dictionary specific to interface file
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
# end class InterfaceGenerator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
