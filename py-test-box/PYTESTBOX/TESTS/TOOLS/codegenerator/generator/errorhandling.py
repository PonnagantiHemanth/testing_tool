#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.generator.errorhandling
:brief: Generator for error handling class
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
from codegenerator.input.templates import ErrorHandlingTemplate
from codegenerator.manager.engine import ConstantTextManager


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ErrorHandlingGenerator(CommonFileGenerator):
    """
    Generate ``ErrorHandling`` file
    """

    @classmethod
    def _get_dictionary(cls):
        """
        Get the ``Error Handling`` related inputs in dictionary format

        :return: Template substitute values
        :rtype: ``dict``
        """
        # get common dictionary first
        dictionary = AutoInput.get_common_dictionary()

        body = []
        version = AutoInput.get_version_list()[0]
        for function_info in AutoInput.FUNCTION_LIST:
            if function_info.index != 0:
                continue
            # end if
            name_lower = function_info.get_name_lower_underscore()
            params_key_value = cls._get_params_key_value(function_info, version)

            body.append(Template(ErrorHandlingTemplate.GET_WRONG_FUNCTION_INDEX).substitute(dict(
                FIDLower=dictionary["HidppFIDLower"],
                FIDUpper=dictionary["HidppFIDUpper"],
                FeatureNameTitleCaseWithoutSpace=dictionary["FeatureNameTitleCaseWithoutSpace"],
                FunctionLower=name_lower,
                FunctionName=function_info.get_name_without_space(),
                Index="_index",
                MinValue=ReqResGenerator.get_min_value(function_info, version, include_response=False),
                Number="_0001",
                ParamsKeyValue=params_key_value,
                Request=f"TestUtils.HIDppHelper.{name_lower}_and_check_error("
            )))
            break
        # end for

        for test_case_info in AutoInput.TEST_CASES_INFO_ERROR_HANDLING:
            if "wrong function index" in test_case_info.synopsis.lower() \
                    or "tests wrong index" in test_case_info.synopsis.lower() \
                    or "invalid function index" in test_case_info.synopsis.lower():
                continue
            # end if
            body.append(ReqResGenerator.get_test_case_item(test_case_info, "ErrorHandling"))
        # end for

        # Ex: from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyName
        # Ex: from pytestbox.device.hidpp20.common.feature_0007.devicefriendlyname import DeviceFriendlyNameTestCase
        dictionary["ImportStructure"] = [
            AutoInput.get_import_text(Template(ErrorHandlingTemplate.IMPORT_UTIL_CLASS).substitute(dictionary)),
            AutoInput.get_import_text(Template(ErrorHandlingTemplate.IMPORT_BASE_CLASS).substitute(dictionary))]

        dictionary["ClassStructure"] = Template(ErrorHandlingTemplate.CLASS_STRUCTURE).substitute(dict(
            Type="errorhandling",
            TestCase=dictionary["FeatureNameTitleCaseWithoutSpace"] + "ErrorHandlingTestCase",
            FeatureNameTitleCaseWithoutSpace=dictionary["FeatureNameTitleCaseWithoutSpace"],
            BaseTestCase=dictionary["FeatureNameTitleCaseWithoutSpace"] + "TestCase",
            Body="\n".join(body)
        ))
        return dictionary
    # end def _get_dictionary

    @classmethod
    def _get_params_key_value(cls, function_info, version):
        """
        Get parameters in key=value format

        :param function_info: Function information
        :type function_info: ``FunctionInfo``
        :param version: Version information
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        indent = " " * 4
        params_key_value = f"\n{indent * 4}test_case=self,"
        params_key_value += f"\n{indent * 4}error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID]"
        if len(function_info.request.parameters) > 0:
            params_key_value += f",\n{indent * 4}"
            params_key_value += ReqResGenerator.get_formatted_method_param(
                parameters=function_info.request.parameters,
                version=version,
                format_type="KeyValue",
                separator=f",\n{indent * 4}")
        # end if
        params_key_value += f",\n{indent * 4}function_index=function_index"
        return params_key_value
    # end def _get_params_key_value

    def __init__(self):
        super().__init__()
        self.update_import_section([
            ConstantTextManager.IMPORT_LEVEL,
            ConstantTextManager.IMPORT_FEATURES,
            ConstantTextManager.IMPORT_COMPUTE_WRONG_RANGE,
            ConstantTextManager.IMPORT_HEXLIST,
            ConstantTextManager.IMPORT_HIDPP_2_ERROR_CODES,
            ConstantTextManager.IMPORT_LOG_HELPER
        ])
        self.update_constant_section([
            ConstantTextManager.LOOP_START_FID,
            ConstantTextManager.LOOP_END
        ])
        # get input dictionary specific to error handling file
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
# end class ErrorHandlingGenerator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
