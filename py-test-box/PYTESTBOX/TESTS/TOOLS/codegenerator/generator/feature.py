#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.generator.feature
:brief: Generator for feature class
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/05/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from string import Template

from codegenerator.generator.common import CommonFileGenerator
from codegenerator.generator.common import ReqResGenerator
from codegenerator.generator.index import IndexGenerator
from codegenerator.input.autoinput import AutoInput
from codegenerator.input.templates import FeatureTemplate
from codegenerator.manager.engine import ConstantTextManager


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FeatureGenerator(CommonFileGenerator):
    """
    Generate ``Feature`` file
    """

    @staticmethod
    def _get_subclass_structure():
        """
        Get all subclass information

        :return: Formatted output
        :rtype: ``str``
        """
        parameters = []
        for function_info in AutoInput.FUNCTION_LIST:
            parameters.extend(function_info.request.parameters)
            parameters.extend(function_info.response.parameters)
        # end for
        for event_info in AutoInput.EVENT_LIST:
            parameters.extend(event_info.event.parameters)
        # end for
        return ReqResGenerator.get_subclass_structure(parameters)
    # end def _get_subclass_structure

    def _get_dictionary(self):
        """
        Get the <Feature Name> related inputs in dictionary format

        :return: Template substitute values
        :rtype: ``dict``
        """
        # get common dictionary first
        dictionary = AutoInput.get_common_dictionary()

        ReqResGenerator.clear_import_list()

        value = IndexGenerator.get_class_index_values(AutoInput.FUNCTION_LIST)
        dictionary["FunctionIndexValues"] = "" if value == "" else f"# Function index\n        {value}"
        value = IndexGenerator.get_class_index_values(AutoInput.EVENT_LIST)
        dictionary["EventIndexValues"] = "" if value == "" else f"\n\n        # Event index\n        {value}"

        dictionary["SubClass"] = self._get_subclass_structure()

        function_map_versions = []
        feature_version_info = []
        feature_class_info = []
        previous_version = None
        for version in AutoInput.get_version_list():
            value, fun_multi_version_text = IndexGenerator.get_function_data_model_values(version)
            function_values = Template(FeatureTemplate.FUNCTION_VALUES).substitute(dict(Values=value))
            value, evt_multi_version_text = IndexGenerator.get_event_data_model_values(version)
            if value == "":
                event_values = ""
            else:
                event_values = Template(FeatureTemplate.EVENT_VALUES).substitute(dict(Values=value))
            # end if

            function_map_version_text = ""
            if len(fun_multi_version_text) > 0:
                function_map_version_text = f"_{fun_multi_version_text.lower()}"
            elif len(evt_multi_version_text) > 0:
                function_map_version_text = f"_{evt_multi_version_text.lower()}"
            # end if

            function_map_versions.append(Template(FeatureTemplate.FUNCTION_MAP_VERSION).substitute(
                dict(FunctionMapVersion=function_map_version_text,
                     FunctionValues=function_values,
                     EventValues=event_values)))
            feature_version_info.append(Template(FeatureTemplate.FEATURE_VERSION_ITEM).substitute(
                dict(HidppFeatureVersion=version,
                     FeatureNameTitleCaseWithoutSpace="".join(AutoInput.HIDPP_FEATURE_NAME.split()),
                     FunctionMapVersion=function_map_version_text,
                     V="V")))

            base = f'{dictionary["FeatureNameTitleCaseWithoutSpace"]}Interface'
            if previous_version is not None:
                base = f'{dictionary["FeatureNameTitleCaseWithoutSpace"]}V{previous_version}'
            # end if

            init_values = dict(
                FeatureNameTitleCaseWithoutSpace=dictionary["FeatureNameTitleCaseWithoutSpace"],
                Model="Model",
                Interface="Interface",
                MaxFunctionIndexVersion=f"_V{version}",
            )

            init_values["ReqValue"], init_values["ResValue"], init_values["EventValue"] = \
                ReqResGenerator.get_structure(version, previous_version)
            init_section = ""
            if len(init_values["ReqValue"] + init_values["ResValue"] + init_values["EventValue"]) > 0:
                init_section = Template(FeatureTemplate.FEATURE_CLASS_INIT_SECTION).substitute(init_values)
            # end if
            in_values = dict(
                HidppFeatureVersion=version,
                FeatureNameTitleCaseWithoutSpace=dictionary["FeatureNameTitleCaseWithoutSpace"],
                V="V",
                Base=base,
                ReqResComment=ReqResGenerator.get_api_structure(version, previous_version),
                InitSection=init_section,
                MaxIndexSection=Template(FeatureTemplate.FEATURE_CLASS_MAX_INDEX_SECTION).substitute(init_values)
            )

            feature_class_info.append(Template(FeatureTemplate.FEATURE_CLASS_ITEM).substitute(in_values))
            previous_version = version
        # end for
        function_map_versions = CommonFileGenerator.uniquify_list(function_map_versions)
        dictionary["FunctionMapVersions"] = "".join(function_map_versions)
        dictionary["FeatureVersionInfo"] = ",".join(feature_version_info)
        dictionary["FeatureClassInfo"] = "".join(feature_class_info)
        dictionary["ReqComment"], dictionary["ResComment"], dictionary["EventComment"] \
            = ReqResGenerator.get_feature_interface_structure()

        dictionary["FeatureCommonStructure"] = [ReqResGenerator.get_short_empty_packet_format(),
                                                ReqResGenerator.get_long_empty_packet_format(),
                                                ReqResGenerator.get_all_common_packet_format()]
        dictionary["FeatureRequestStructure"] = [ReqResGenerator.get_request_structure()]
        dictionary["FeatureResponseStructure"] = [ReqResGenerator.get_response_structure()]
        dictionary["FeatureEventStructure"] = [ReqResGenerator.get_event_structure()]

        dictionary["ImportList"] = ReqResGenerator.get_import_list()
        sub_imports = ReqResGenerator.get_subclass_import_structure()
        if len(sub_imports) > 0:
            dictionary["ImportList"].extend(sub_imports)
        # end if
        dictionary["MaxFunctionIndex"] = AutoInput.get_max_function_index()

        return dictionary
    # end def _get_dictionary

    def __init__(self):
        super().__init__()
        self.update_import_section_on_python_library([
            ConstantTextManager.IMPORT_ABC,
        ])
        self.update_import_section([
            ConstantTextManager.IMPORT_BIT_FIELD,
            ConstantTextManager.IMPORT_CHECK_BYTE,
            ConstantTextManager.IMPORT_CHECK_HEXLIST,
            ConstantTextManager.IMPORT_FEATURE_FACTORY,
            ConstantTextManager.IMPORT_FEATURE_INTERFACE,
            ConstantTextManager.IMPORT_FEATURE_MODEL,
            ConstantTextManager.IMPORT_HIDPP_MESSAGE,
            ConstantTextManager.IMPORT_NUMERAL,
            ConstantTextManager.IMPORT_TYPE
        ])
        # get input dictionary specific to feature file
        self.input_dictionary = self._get_dictionary()
    # end def __init__

    def process(self):
        """
        Process the list of operations to generate import/constant/implementation sections
        """
        self.update_import_section(self.input_dictionary["ImportList"])

        self.update_implementation_section([Template(FeatureTemplate.FEATURE_BASE).substitute(self.input_dictionary)])
        self.update_implementation_section([Template(FeatureTemplate.FEATURE_MODEL).substitute(self.input_dictionary)])
        self.update_implementation_section(
            [Template(FeatureTemplate.FEATURE_FACTORY).substitute(self.input_dictionary)])
        self.update_implementation_section(
            [Template(FeatureTemplate.FEATURE_INTERFACE).substitute(self.input_dictionary)])
        self.update_implementation_section([Template(FeatureTemplate.FEATURE_CLASS).substitute(self.input_dictionary)])
        self.update_implementation_section(self.input_dictionary["FeatureCommonStructure"])
        self.update_implementation_section(self.input_dictionary["FeatureRequestStructure"])
        self.update_implementation_section(self.input_dictionary["FeatureResponseStructure"])
        self.update_implementation_section(self.input_dictionary["FeatureEventStructure"])
    # end def process
# end class FeatureGenerator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
