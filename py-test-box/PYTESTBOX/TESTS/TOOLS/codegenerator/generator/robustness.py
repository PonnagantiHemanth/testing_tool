#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.generator.robustness
:brief: Generator for robustness class
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
from codegenerator.input.templates import RobustnessTemplate
from codegenerator.manager.engine import ConstantTextManager


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RobustnessGenerator(CommonFileGenerator):
    """
    Generate ``Robustness`` file
    """

    @classmethod
    def _get_sw_text(cls):
        sw_id = "SwID boundary values [0..F]"
        sw_range = ""
        if len(AutoInput.EVENT_LIST) > 0:
            sw_id = "SwID boundary values [1..F] (0 is not allowed since event is present)"
            sw_range = "[1:]"
        # end if
        return sw_id, sw_range
    # end def _get_sw_text

    @classmethod
    def _get_extension_and_version_no(cls, function_info, version, extension):
        """
        Get extension and version number text

        :param function_info: Function information
        :type function_info: ``FunctionInfo``
        :param version: Version information
        :type version: ``int``
        :param extension: Extension text
        :type extension: ``str``

        :return: Extension text and version text
        :rtype: ``tuple[str, str]``
        """
        version_no = ""
        if function_info.check_multi_version():
            version_no = AutoInput.get_version_text(version)
            extension = f"{extension}_{version_no.lower()}"
        # end if
        return extension, version_no
    # end def _get_extension_and_version_no

    @classmethod
    def _get_padding_type(cls, function_info, version):
        """
        Get padding type

        :param function_info: Function information
        :type function_info: ``FunctionInfo``
        :param version: Version information
        :type version: ``int``

        :return: Padding type
        :rtype: ``str``
        """
        padding_type = "0x11"
        if ReqResGenerator.get_request_report_id_type(function_info, version) == ReqResGenerator.REPORT_ID_SHORT_NAME:
            padding_type = "0x10"
        # end if
        return padding_type
    # end def _get_padding_type

    @classmethod
    def _generate_reserved(cls, body, dictionary, number, count):
        """
        Generate reserved test cases (if any)

        :param body: Body structure for robustness
        :type body: ``list[str]``
        :param dictionary: Dictionary for input
        :type dictionary: ``dict``
        :param number: Prefix number for the test case
        :type number: ``str``
        :param count: Start number of the test case
        :type count: ``int``
        """
        for function_info in AutoInput.FUNCTION_LIST:
            count += 1
            output = []
            for version in AutoInput.get_version_list():
                if not function_info.request.check_data_type(version, ["Reserved"]):
                    continue
                # end if
                extension, version_no = cls._get_extension_and_version_no(function_info, version, "_reserved")
                dictionary["ImportStructure"].append(ConstantTextManager.IMPORT_COMPUTE_WRONG_RANGE)
                dictionary["ConstantStructure"].append(ConstantTextManager.LOOP_START_RESERVED)

                params_key_value = cls._get_params_key_value(function_info, version, ["reserved=reserved"])

                name_lower = function_info.get_name_lower_underscore()

                output.append(Template(RobustnessTemplate.GET_RESERVED).substitute(dict(
                    MinValue=ReqResGenerator.get_min_value(function_info, version),
                    ParamsKeyValue=params_key_value,
                    CheckMapAndFields=ReqResGenerator.get_check_map_and_fields(
                        dictionary=dictionary,
                        function_info=function_info,
                        template=RobustnessTemplate.CHECK_MAP,
                        space_length=12,
                        version=version),
                    SingleItem=ReqResGenerator.get_one_api_format_with_input_and_output(
                        function_info=function_info, version=version, indent=2),
                    Request=f"TestUtils.HIDppHelper.{name_lower}(",
                    FunctionName=function_info.get_name_without_space(),
                    FunctionLower=function_info.get_name_lower_underscore(),
                    Ext=extension,
                    Version=version_no,
                    VersionNo=version_no.lower(),
                    Response="Response",
                    FIDLower=dictionary["HidppFIDLower"],
                    FIDUpper=dictionary["HidppFIDUpper"],
                    ReqCls="_cls",
                    FeatureNameTitleCaseWithoutSpace=dictionary["FeatureNameTitleCaseWithoutSpace"],
                    Number=f"_{number}#{count}",
                    BackupNvs=RobustnessGenerator._get_backup_nvs_text(function_info)
                )))
            # end for
            if len(output) > 0:
                output = CommonFileGenerator.uniquify_list(output)
                body.append("\n".join(output))
            else:
                count -= 1
            # end if
        # end for
    # end def _generate_reserved

    @classmethod
    def _generate_software_id(cls, body, dictionary):
        """
        Generate software id test cases

        :param body: Body structure for robustness
        :type body: ``list[str]``
        :param dictionary: Dictionary for input
        :type dictionary: ``dict``
        """
        sw_id, sw_range = cls._get_sw_text()

        count = 0
        for function_info in AutoInput.FUNCTION_LIST:
            count += 1
            output = []
            for version in AutoInput.get_version_list():
                if not function_info.is_this_version_applicable(version):
                    continue
                # end if
                extension, version_no = cls._get_extension_and_version_no(function_info, version, "_software_id")
                size = ReqResGenerator.get_request_padding_size(function_info.request.parameters, version)
                padding_format = ReqResGenerator.get_padding_format(function_info.request.parameters)
                padding = ".0xPP" * (size // 8)
                padding_type = cls._get_padding_type(function_info, version)

                params_key_value = cls._get_params_key_value(function_info, version, ["software_id=software_id"])

                space = " " * 8
                wrap_length = ConstantTextManager.LINE_WRAP_AT_CHAR - len(space) - 2
                request_format = ReqResGenerator.get_wrapped_text(
                    f"Request: {padding_type}.DeviceIndex.FeatureIndex.FunctionIndex|SwID{padding_format}{padding}",
                    space, wrap_length, ".")
                name_lower = function_info.get_name_lower_underscore()

                output.append(Template(RobustnessTemplate.GET_SOFTWARE_ID).substitute(dict(
                    MinValue=ReqResGenerator.get_min_value(function_info, version),
                    ParamsKeyValue=params_key_value,
                    CheckMapAndFields=ReqResGenerator.get_check_map_and_fields(
                        dictionary=dictionary,
                        function_info=function_info,
                        template=RobustnessTemplate.CHECK_MAP,
                        space_length=12,
                        version=version),
                    SingleItem=ReqResGenerator.get_one_api_format_with_input_and_output(
                        function_info=function_info, version=version, indent=2),
                    RequestFormat=request_format,
                    Request=f"TestUtils.HIDppHelper.{name_lower}(",
                    SoftwareId=sw_id,
                    SoftwareIdRange=sw_range,
                    FunctionName=function_info.get_name_without_space(),
                    FunctionLower=function_info.get_name_lower_underscore(),
                    Ext=extension,
                    Version=version_no,
                    VersionNo=version_no.lower(),
                    Response="Response",
                    FIDUpper=dictionary["HidppFIDUpper"],
                    FeatureNameTitleCaseWithoutSpace=dictionary["FeatureNameTitleCaseWithoutSpace"],
                    Number=f"_0001#{count}",
                    BackupNvs=cls._get_backup_nvs_text(function_info)
                )))
            # end for
            if len(output) > 0:
                output = CommonFileGenerator.uniquify_list(output)
                body.append("\n".join(output))
            else:
                count -= 1
            # end if
        # end for
    # end def _generate_software_id

    @classmethod
    def _generate_padding(cls, body, dictionary):
        """
        Generate padding test cases (if any)

        :param body: Body structure for robustness
        :type body: ``list[str]``
        :param dictionary: Dictionary for input
        :type dictionary: ``dict``

        :return: Count of the last test case number
        :rtype: ``int``
        """
        count = 0
        for function_info in AutoInput.FUNCTION_LIST:
            count += 1
            output = []
            for version in AutoInput.get_version_list():
                if not function_info.is_this_version_applicable(version):
                    continue
                # end if
                size = ReqResGenerator.get_request_padding_size(function_info.request.parameters, version)
                if size <= 0:
                    continue
                # end if
                dictionary["ImportStructure"].append(ConstantTextManager.IMPORT_COMPUTE_SUP_VALUES)
                dictionary["ConstantStructure"].append(ConstantTextManager.LOOP_START_PADDING)

                extension, version_no = cls._get_extension_and_version_no(function_info, version, "_padding")
                padding = ".0xPP" * (size // 8)
                padding_type = cls._get_padding_type(function_info, version)
                padding_format = ReqResGenerator.get_padding_format(function_info.request.parameters)

                params_key_value = cls._get_params_key_value(function_info, version, ["padding=padding"])

                space = " " * 8
                wrap_length = ConstantTextManager.LINE_WRAP_AT_CHAR - len(space) - 2
                request_format = ReqResGenerator.get_wrapped_text(
                    f"Request: {padding_type}.DeviceIndex.FeatureIndex.FunctionIndex|SwID{padding_format}{padding}",
                    space, wrap_length, ".")
                name_lower = function_info.get_name_lower_underscore()

                output.append(Template(RobustnessTemplate.GET_PADDING).substitute(dict(
                    MinValue=ReqResGenerator.get_min_value(function_info, version),
                    ParamsKeyValue=params_key_value,
                    CheckMapAndFields=ReqResGenerator.get_check_map_and_fields(
                        dictionary=dictionary,
                        function_info=function_info,
                        template=RobustnessTemplate.CHECK_MAP,
                        space_length=12,
                        version=version),
                    SingleItem=ReqResGenerator.get_one_api_format_with_input_and_output(
                        function_info=function_info, version=version, indent=2),
                    RequestFormat=request_format,
                    Request=f"TestUtils.HIDppHelper.{name_lower}(",
                    FunctionName=function_info.get_name_without_space(),
                    FunctionLower=function_info.get_name_lower_underscore(),
                    Ext=extension,
                    Version=version_no,
                    VersionNo=version_no.lower(),
                    Response="Response",
                    FIDUpper=dictionary["HidppFIDUpper"],
                    FIDLower=dictionary["HidppFIDLower"],
                    ReqCls="_cls",
                    FeatureNameTitleCaseWithoutSpace=dictionary["FeatureNameTitleCaseWithoutSpace"],
                    Number=f"_0002#{count}",
                    BackupNvs=cls._get_backup_nvs_text(function_info)
                )))
            # end for
            if len(output) > 0:
                output = CommonFileGenerator.uniquify_list(output)
                body.append("\n".join(output))
            else:
                count -= 1
            # end if
        # end for
        return count
    # end def _generate_padding

    @classmethod
    def _get_params_key_value(cls, function_info, version, append_items):
        """
        Get parameters in key=value format

        :param function_info: Function information
        :type function_info: ``FunctionInfo``
        :param version: Version information
        :type version: ``int``
        :param append_items: Items to append in the end
        :type append_items: ``list[str]``

        :return: Formatted output
        :rtype: ``str``
        """
        indent = " " * 4
        params_key_value = f"\n{indent * 4}test_case=self"
        if len(function_info.request.parameters) > 0:
            params_key_value += f",\n{indent * 4}"
            params_key_value += ReqResGenerator.get_formatted_method_param(
                parameters=function_info.request.parameters,
                version=version,
                format_type="KeyValue",
                separator=f",\n{indent * 4}")
        # end if
        for item in append_items:
            params_key_value += f",\n{indent * 4}{item}"
        # end for
        return params_key_value
    # end def _get_params_key_value

    @staticmethod
    def _get_backup_nvs_text(function_info):
        """
        Get text to reload_nvs

        :param function_info: Function information
        :type function_info: ``FunctionInfo``
        """
        return f"\n        self.post_requisite_reload_nvs = True" if function_info.nvs_backup_required else ""
    # end def _get_backup_nvs_text

    def _get_dictionary(self):
        """
        Get the ``Robustness`` related inputs in dictionary format

        :return: Template substitute values
        :rtype: ``dict``
        """
        # get common dictionary first
        dictionary = AutoInput.get_common_dictionary()

        # Ex: from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyName
        # Ex: from pytestbox.device.hidpp20.common.feature_0007.devicefriendlyname import DeviceFriendlyNameTestCase
        dictionary["ImportStructure"] = [
            AutoInput.get_import_text(Template(RobustnessTemplate.IMPORT_FEATURE_CLASS).substitute(dictionary)),
            AutoInput.get_import_text(Template(RobustnessTemplate.IMPORT_UTIL_CLASS).substitute(dictionary)),
            AutoInput.get_import_text(Template(RobustnessTemplate.IMPORT_BASE_CLASS).substitute(dictionary))]
        dictionary["ConstantStructure"] = []

        body = []

        self._generate_software_id(body, dictionary)
        count = self._generate_padding(body, dictionary)
        self._generate_reserved(body, dictionary, "0002", count)

        for test_case_info in AutoInput.TEST_CASES_INFO_ROBUSTNESS:
            if "software id" in test_case_info.synopsis.lower() \
                    or "softwareid" in test_case_info.synopsis.lower() \
                    or "padding" in test_case_info.synopsis.lower():
                continue
            # end if
            body.append(ReqResGenerator.get_test_case_item(test_case_info, "Robustness"))
        # end for

        dictionary["ClassStructure"] = Template(RobustnessTemplate.CLASS_STRUCTURE).substitute(dict(
            Type="robustness",
            TestCase=dictionary["FeatureNameTitleCaseWithoutSpace"] + "RobustnessTestCase",
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
            ConstantTextManager.IMPORT_HEXLIST,
            ConstantTextManager.IMPORT_NUMERAL,
            ConstantTextManager.IMPORT_COMPUTE_INF_VALUES,
            ConstantTextManager.IMPORT_LOG_HELPER
        ])
        self.update_constant_section([
            ConstantTextManager.LOOP_START_SW_ID,
            ConstantTextManager.LOOP_END
        ])
        # get input dictionary specific to robustness file
        self.input_dictionary = self._get_dictionary()
    # end def __init__

    def process(self):
        """
        Process the list of operations to generate import/constant/implementation sections
        """
        self.update_import_section(self.input_dictionary["ImportStructure"])
        self.update_constant_section([f"\n_AUTHOR = \"{self.input_dictionary['AuthorName']}\""])
        data = self.input_dictionary.get("ConstantStructure")
        if data:
            self.update_constant_section(data)
        # end if
        self.update_implementation_section(self.input_dictionary["ClassStructure"])
    # end def process
# end class RobustnessGenerator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
