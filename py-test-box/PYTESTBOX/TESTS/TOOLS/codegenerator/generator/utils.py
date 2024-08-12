#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.generator.utils
:brief: Generator for utils class
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
from codegenerator.input.engine import EventInfo
from codegenerator.input.engine import FunctionInfo
from codegenerator.input.templates import UtilsTemplate
from codegenerator.manager.engine import ConstantTextManager


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class UtilsGenerator(CommonFileGenerator):
    """
    Generate ``Utils`` file
    """

    @classmethod
    def _get_dictionary(cls):
        """
        Get the ``Utils`` related inputs in dictionary format

        :return: Template substitute values
        :rtype: ``dict``
        """
        # get common dictionary first
        dictionary = AutoInput.get_common_dictionary()

        dictionary["Utils"] = "utils"
        dictionary["TestUtils"] = "TestUtils"
        dictionary["Helpers"] = ReqResGenerator.get_helper_class()

        output = []
        # add import 1: from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyName
        dictionary["Name"] = dictionary["FeatureNameTitleCaseWithoutSpace"]
        output.append(Template(UtilsTemplate.IMPORT_ITEM).substitute(dictionary))

        # add import 2: from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyNameFactory
        dictionary["Name"] = dictionary["FeatureNameTitleCaseWithoutSpace"] + "Factory"
        output.append(Template(UtilsTemplate.IMPORT_ITEM).substitute(dictionary))

        # add import 3: to_int, rtype for Response/Event objects
        for version in AutoInput.get_version_list():
            for function_info in AutoInput.FUNCTION_LIST:
                output.extend(cls._get_import_text(function_info, version, "Response"))
            # end for

            for event_info in AutoInput.EVENT_LIST:
                output.extend(cls._get_import_text(event_info, version, "Event"))
                output.append(ConstantTextManager.IMPORT_BASE_COMMUNICATION_CHANNEL)
            # end for
        # end for
        dictionary["ImportStructure"] = CommonFileGenerator.uniquify_list(output)
        return dictionary
    # end def _get_dictionary

    @classmethod
    def _get_import_text(cls, info, version, extension):
        """
        Get the text for import statement

        :param info: Function/Event information
        :type info: ``FunctionInfo | EventInfo``
        :param version: Version information
        :type version: ``int``
        :param extension: Extension text
        :type extension: ``str``

        :return: Formatted output
        :rtype: ``list[str]``
        """
        output = []
        if not info.is_this_version_applicable(version):
            return output
        # end if

        if info.check_data_type(version, ["int", "Reserved"]):
            output.append(ConstantTextManager.IMPORT_TO_INT)
        # end if

        if AutoInput.ARGS_OBJECT_REFERENCE == ConstantTextManager.ARGS_OBJ_REF_IMPORT_SECTION:
            name = "".join(info.name.split()) + extension
            version_text = ""
            if info.check_multi_version():
                version_text = AutoInput.get_version_text(version)
            # end if
            text = f'\nfrom pyhid.hidpp.features.{AutoInput.HIDPP_CATEGORY.lower()}.' \
                   f'{"".join(AutoInput.HIDPP_FEATURE_NAME.lower().split())} import {name}{version_text}'
            output.append(text)

            output.append(ConstantTextManager.IMPORT_COMMON_BASE_TEST_UTILS)
        # end if

        return output
    # end def _get_import_text

    def __init__(self):
        super().__init__()
        self.update_import_section([
            ConstantTextManager.IMPORT_HID_DISPATCHER,
            ConstantTextManager.IMPORT_CHANNEL_UTILS,
            ConstantTextManager.IMPORT_HEXLIST,
            ConstantTextManager.IMPORT_DEVICE_BASE_TEST_UTILS,
        ])
        # get input dictionary specific to utils file
        self.input_dictionary = self._get_dictionary()
    # end def __init__

    def process(self, ):
        """
        Process the list of operations to generate import/constant/implementation sections
        """
        self.update_import_section(self.input_dictionary["ImportStructure"])
        self.update_implementation_section([Template(UtilsTemplate.UTILS_BASE).substitute(self.input_dictionary)])
    # end def process
# end class UtilsGenerator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
