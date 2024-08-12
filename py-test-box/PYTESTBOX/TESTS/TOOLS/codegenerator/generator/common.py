#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.generator.common
:brief: Common functions for all generators
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/05/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import re
import sys
from string import Template

from codegenerator.input.autoinput import AutoInput
from codegenerator.input.engine import EventInfo
from codegenerator.input.engine import FunctionInfo
from codegenerator.input.engine import Parameter
from codegenerator.input.engine import SubParameter
from codegenerator.input.engine import TestCaseInfo
from codegenerator.input.templates import CommonTemplate
from codegenerator.input.templates import ErrorHandlingTemplate
from codegenerator.input.templates import FeatureTemplate
from codegenerator.input.templates import FeatureTestTemplate
from codegenerator.input.templates import RobustnessTemplate
from codegenerator.input.templates import UtilsTemplate
from codegenerator.manager.engine import ConstantTextManager
from codegenerator.manager.engine import FileManager
from codegenerator.parser.engine import HeaderSectionParser
from codegenerator.validator.engine import SizeValidator


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DataType(object):
    """
    Provide constants/enumerations for data types
    """
    RESERVED = "Reserved"
    PADDING = "padding"
    NONE = "None"
# end class DataType


class CommonFileGenerator(object):
    """
    Provide common and reusable functions for all file generator classes
    """

    @classmethod
    def _get_data_type(cls, parameter, category):
        """
        Get data type from parameter

        :param parameter: Parameter information
        :type parameter: ``Parameter | SubParameter``
        :param category: Category
        :type category: ``str``

        :return: Formatted output
        :rtype: ``list[str]``
        """
        output = []
        if parameter.has_sub_parameters():
            for sub_parameter in parameter.sub_parameters:
                output.extend(cls._get_data_type(parameter=sub_parameter, category=category))
            # end for
        else:
            if parameter.settings_data_type is not None:
                if category == "sub_system":
                    name = parameter.get_name_without_space()
                    data = "()" if parameter.settings_data_type.startswith("tuple") else "None"
                    output.append(f'\n                    self.F_{name} = {data}')
                elif category == "settings":
                    data, name = cls._get_name_and_data(parameter)
                    output.append(f'\n{name} = {data}')
                # end if
            # end if
        # end if
        return output
    # end def _get_data_type

    @staticmethod
    def _get_name_and_data(parameter):
        """
        Get name and data from parameter

        :param parameter: Parameter information
        :type parameter: ``Parameter | SubParameter``

        :return: Formatted output
        :rtype: ``tuple[str, str]``
        """
        name = parameter.get_name_without_space()

        if parameter.settings_default_value is not None:
            return parameter.settings_default_value, name
        # end if
        data = "?"
        if parameter.settings_data_type == "str":
            data = '"?"'
        elif parameter.settings_data_type == "tuple(int)":
            data = '(?, ?)'
        elif parameter.settings_data_type == "tuple(str)":
            data = '("?", "?")'
        elif parameter.settings_data_type == "tuple":
            data = '()'
        elif parameter.settings_data_type == "list":
            data = "[]"
        elif parameter.settings_data_type == "bool":
            data = False
        # end if
        return data, name
    # end def _get_name_and_data

    def __init__(self):
        self.__import_list = []
        self.__import_list_python = []
        self.__constant_list = []
        self.__implementation_list = []
        self.__main_list = []
    # end def __init__

    def update_import_section_on_python_library(self, values):
        """
        Update the import section list for system libraries

        :param values: Values to update
        :type values: ``list[str]``
        """
        self.__import_list_python.extend(values)
    # end def update_import_section_on_python_library

    def update_import_section(self, values):
        """
        Update the import section list for project libraries

        :param values: Values to update
        :type values: ``list[str]``
        """
        self.__import_list.extend(values)
    # end def update_import_section

    @staticmethod
    def uniquify_list(input_list):
        """
        Compute a list with unique elements in the input order is preserved

        :param input_list: List with possible duplicated elements
        :type input_list: ``list[str]``

        :return: List of unique elements
        :rtype: ``list[str]``
        """
        output_list = []
        for element in input_list:
            if element not in output_list:
                output_list.append(element)
            # end if
        # end for
        return output_list
    # end def uniquify_list

    def get_import_section(self):
        """
        Get the import section code

        :return: Text of import section
        :rtype: ``list[str]``
        """
        # use dictionary keys to remove duplicate entries.
        list1 = list(dict.fromkeys(self.__import_list_python))
        list1 = self.uniquify_list(list1)
        list1.sort()
        list2 = list(dict.fromkeys(self.__import_list))
        list2 = self.uniquify_list(list2)
        list2.sort()
        if len(list1) > 0:
            return list1 + [ConstantTextManager.NEW_LINE] + list2
        # end if
        return list2
    # end def get_import_section

    def update_constant_section(self, values):
        """
        Update the constant section list

        :param values: Values to update
        :type values: ``list[str]``
        """
        self.__constant_list.extend(values)
    # end def update_constant_section

    def get_constant_section(self):
        """
        Get the constant section code

        :return: Text of constant section
        :rtype: ``list[str]``
        """
        self.__constant_list.sort()
        return self.uniquify_list(self.__constant_list)
    # end def get_constant_section

    def update_implementation_section(self, values):
        """
        Update the implementation section list

        :param values: Values to update
        :type values: ``list[str]``
        """
        self.__implementation_list.extend(values)
    # end def update_implementation_section

    def get_implementation_section(self):
        """
        Get the implementation section code

        :return: Text of implementation section
        :rtype: ``list[str]``
        """
        return self.__implementation_list
    # end def get_implementation_section

    def update_main_section(self, values):
        """
        Update the main section list

        :param values: Values to update
        :type values: ``list[str]``
        """
        self.__main_list.extend(values)
    # end def update_main_section

    def get_main_section(self):
        """
        Get the main section code

        :return: Text of main section
        :rtype: ``list[str]``
        """
        return self.__main_list
    # end def get_main_section
# end class CommonFileGenerator


class CommonPackageGenerator(object):
    """
    Provide common and reusable functions for package generator classes (i.e., PYHID & TESTSUITES)
    """

    def __init__(self):
        self.__output = []
    # end def __init__

    def reset(self):
        """
        Reset the content
        """
        self.__output.clear()
    # end def reset

    def update_values(self, values):
        """
        Update the values in the output list.

        :param values: Values to update
        :type values: ``list[str]``
        """
        self.__output.extend(values)
    # end def update_values

    def write_to_file(self, file_name):
        """
        Write the contents to file

        :param file_name: Name of the file
        :type file_name: ``str``
        """
        FileManager.write_file(file_name, self.__output)
    # end def write_to_file

    # noinspection PyUnresolvedReferences
    def update_sections(self, obj, template, dictionary, header_text):
        """
        Update the 'import, constant, implementation, main, EOF' sections in output.

        :param obj: The object which has the output section
        :type obj: ``CommonFileGenerator | None``
        :param template: Template to use
        :type template: ``type[CommonTemplate]``
        :param dictionary: The dictionary which has the substitute values
        :type dictionary: ``dict``
        :param header_text: The header text
        :type header_text: ``str``
        """
        # Section: header
        self.update_values(HeaderSectionParser.get_file_header(header_text))
        values = dict(
            PackageValue=template.PACKAGE_VALUE,
            BriefValue=template.BRIEF_VALUE,
            AuthorValue=template.AUTHOR_VALUE,
            DateValue=template.DATE_VALUE
        )
        self.update_values(HeaderSectionParser.get_module_header(values, dictionary))

        if obj is None:
            self.update_values([ConstantTextManager.NEW_LINE, ConstantTextManager.NEW_LINE])
        else:
            # Section: import
            self.update_values(HeaderSectionParser.get_import_header())
            self.update_values(obj.get_import_section())

            # Section: constant
            section = obj.get_constant_section()
            if len(section) > 0:
                self.update_values(HeaderSectionParser.get_constant_header())
                self.update_values(section)
            # end if

            # Section: implementation
            self.update_values(HeaderSectionParser.get_implementation_header())
            self.update_values(obj.get_implementation_section())

            # Section: main
            section = obj.get_main_section()
            if len(section) > 0:
                self.update_values(HeaderSectionParser.get_main_header())
                self.update_values(section)
            # end if
        # end if

        # Section: end of file
        self.update_values(HeaderSectionParser.get_end_of_file_header())
    # end def update_sections
# end class CommonPackageGenerator


class ReqResGenerator(object):
    """
    Generate both Request & Response common operations
    """

    REPORT_ID_LONG_SIZE = 128
    REPORT_ID_LONG_NAME = "LONG"
    REPORT_ID_SHORT_SIZE = 24
    REPORT_ID_SHORT_NAME = "SHORT"

    _import_list = []
    _version_map = {
        0: "ZERO",
        1: "ONE",
        2: "TWO",
        3: "THREE",
        4: "FOUR",
        5: "FIVE",
        6: "SIX",
        7: "SEVEN",
        8: "EIGHT",
        9: "NINE",
        10: "TEN",
        11: "ELEVEN",
        12: "TWELVE",
        13: "THIRTEEN",
        14: "FOURTEEN",
        15: "FIFTEEN"
    }

    @classmethod
    def clear_import_list(cls):
        """
        Clear the import list
        """
        cls._import_list.clear()
    # end def clear_import_list

    @classmethod
    def get_import_list(cls):
        """
        Get the import list

        :return: Category list for import section
        :rtype: ``list[str]``
        """
        return cls._import_list
    # end def get_import_list

    @classmethod
    def get_common_base_test_case_name(cls):
        """
        Get common base test case name

        :return: Testcase name
        :rtype: ``str``
        """
        prefix = ""
        if AutoInput.ARGS_OBJECT_REFERENCE == ConstantTextManager.ARGS_OBJ_REF_NAME_WITH_PATH:
            prefix = "pytestbox.base.basetest."
        # end if
        return f"{prefix}CommonBaseTestCase"
    # end def get_common_base_test_case_name

    @classmethod
    def get_formatted_method_param(cls, parameters, version, format_type="Value", separator=", ", is_optional=False):
        """
        | Get the method's parameters in special format (comma separated string)
        | Example: 0x0007 Device Friendly Name::
        |     [1] getFriendlyName(byteIndex) -> byteIndex, nameChunk
        | GetFriendlyName parameters::
        |     (format_type: Value) => 'byte_index'
        |     (format_type: KeyValue) => 'byte_index=byte_index'
        | GetFriendlyNameResponse parameters::
        |     (format_type: Value) => 'byte_index, name_chunk'
        |     (format_type: KeyValue) => 'byte_index=byte_index, name_chunk=name_chunk'

        :param parameters: Parameter information
        :type parameters: ``list[Parameter | SubParameter]``
        :param version: Version information
        :type version: ``int``
        :param format_type: Format type - OPTIONAL
        :type format_type: ``str``
        :param separator: Separator to join the string - OPTIONAL
        :type separator: ``str``
        :param is_optional: Flag indicating if optional text is appended - OPTIONAL
        :type is_optional: ``bool``

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        for parameter in parameters:
            if not parameter.is_given_version_present(version):
                continue
            # end if
            if parameter.exclusion:
                # Rationale: Some functions are deprecated even if this information is not written in the specification.
                # Example: x1815 - HostInfo - GetFeatureInfoResponseV1ToV2.__init__()
                # 'moveHost' and 'deleteHost' are forbidden.
                # That's why the capability bits 'Move Host' and 'Delete Host' were not exposed in the request API.
                # In the same way, 'eQuad HD' and 'USB HD' were never used by our firmwares.
                # Refer column P in tab 'API Info' in sheet:
                # https://docs.google.com/spreadsheets/d/1dQIU9SQnbkZG91g7vb5xZtRfm_G2EPyemC0dn6Lt2Mg
                continue
            # end if
            if parameter.data_type == DataType.RESERVED:
                # ignore reserved field
                continue
            # end if
            if parameter.has_sub_parameters():
                # Sub parameters are available.
                # Get the same comma separated format values by calling recursive method
                formatted_value = cls.get_formatted_method_param(
                    parameter.sub_parameters, version, format_type, separator, is_optional)
            else:
                formatted_value = cls.get_formatted_value(format_type, parameter, version, is_optional)
            # end if
            output.append(formatted_value)
        # end for
        return separator.join(output)
    # end def get_formatted_method_param

    @classmethod
    def get_formatted_value(cls, format_type, parameter, version, is_optional=False):
        """
        Get formatted value

        :param format_type: Format type
        :type format_type: ``str``
        :param parameter: Parameter information
        :type parameter: ``Parameter | SubParameter``
        :param version: Version information
        :type version: ``int``
        :param is_optional: Flag indicating if optional text is appended - OPTIONAL
        :type is_optional: ``bool``

        :return: Formatted output
        :rtype: ``str``
        """
        name_lower_underscore = parameter.get_name_lower_underscore()
        if format_type == "KeyAndValueWithHexList":
            if parameter.data_type == "int" and parameter.get_size(version) % 8 == 0:
                formatted_value = f"{name_lower_underscore}=HexList({name_lower_underscore})"
            else:
                formatted_value = f"{name_lower_underscore}={name_lower_underscore}"
            # end if
        elif format_type == "KeyValue":
            formatted_value = f"{name_lower_underscore}={name_lower_underscore}"
        else:
            if parameter.default_value is not None:
                # Rationale: Simplify the instantiation of the class to maintain the feature.
                # Example: x1815 - HostInfo - GetFeatureInfoResponseV1ToV2.__init__(set_os_version=False)
                # Refer column Q in tab 'API Info' in sheet:
                # https://docs.google.com/spreadsheets/d/1dQIU9SQnbkZG91g7vb5xZtRfm_G2EPyemC0dn6Lt2Mg
                formatted_value = f"{name_lower_underscore}={parameter.default_value}"
            elif is_optional:
                formatted_value = f"{name_lower_underscore}=None"
            else:
                formatted_value = name_lower_underscore
            # end if
        # end if
        return formatted_value
    # end def get_formatted_value

    @staticmethod
    def get_padding_format(parameters, prefix_dot=True):
        """
        | Get the padding format (dot separated string)
        | Example: 0x0007 Device Friendly Name::
        |     [3] setFriendlyName(byteIndex, nameChunk) -> nameLen
        | SetFriendlyName padding format::
        |     'ByteIndex.NameChunk'

        :param parameters: Parameter information
        :type parameters: ``list[Parameter | SubParameter]``
        :param prefix_dot: Prefix the dot char - OPTIONAL
        :type prefix_dot: ``bool``

        :return: Formatted output
        :rtype: ``str``
        """
        if len(parameters) == 0:
            return ""
        # end if
        output = []
        for parameter in parameters:
            if parameter.data_type == DataType.RESERVED:
                continue
            # end if
            output.append(parameter.get_name_without_space())
        # end for
        text = ".".join(output)
        if prefix_dot:
            text = "." + text
        # end if
        return text
    # end def get_padding_format

    @classmethod
    def get_method_param_settings_value(cls, parameters, space, equal_to, template, skip_settings_values, result,
                                        version):
        """
        | Get the test field format with config values
        | Example: sample values from settings.ini
        | int: F_FieldValue = 0
        |    "field_value = HexList(to_int(self.config.F_FieldValue))"
        | str: F_FieldValue = "ABC"
        |    "field_value = HexList(self.config.F_FieldValue)"
        | tuple(int): F_FieldValue = (0, 1, 2)
        |    "field_value = [HexList(to_int(item)) for item in self.config.F_FieldValue]"
        | tuple(str): F_FieldValue = ("A", "B", "C")
        |    "field_value = [HexList(item) for item in self.config.F_FieldValue]"

        :param parameters: Parameter information
        :type parameters: ``list[Parameter | SubParameter]``
        :param space: Space format
        :type space: ``str``
        :param equal_to: EqualTo format
        :type equal_to: ``str``
        :param template: Template to use
        :type template: ``str``
        :param skip_settings_values: Flag to skip settings value
        :type skip_settings_values: ``bool``
        :param result: Result of this function
        :type result: ``list[str]``
        :param version: Version information
        :type version: ``int``

        :return: Formatted output
        :rtype: ``list[str]``
        """
        if len(parameters) == 0:
            return result
        # end if
        for parameter in parameters:
            if parameter.has_sub_parameters():
                cls.get_method_param_settings_value(
                    parameter.sub_parameters, space, equal_to, template, skip_settings_values, result, version)
                continue
            # end if
            if not parameter.is_given_version_present(version):
                continue
            # end if
            if parameter.data_type == DataType.RESERVED:
                # ignore reserved field
                continue
            # end if
            if parameter.settings_data_type is not None:
                if skip_settings_values and parameter.settings_data_type in ["int", "str"]:
                    # Skip this field since it is handled in utils default check map.
                    continue
                # end if
                value = cls.get_settings_data_type(parameter)
            else:
                value = cls.get_data_type(parameter)
            # end if
            result.append(Template(template).substitute(dict(
                Space=space,
                EqualTo=equal_to,
                Name=parameter.get_name_lower_underscore(replace_bit_map=True),
                Value=value
            )))
        # end for
        result = CommonFileGenerator.uniquify_list(result)
        return result
    # end def get_method_param_settings_value

    @staticmethod
    def get_data_type(parameter):
        """
        Get Settings data type

        :param parameter: Parameter information
        :type parameter: ``Parameter``

        :return: Formatted output
        :rtype: ``str``
        """
        data_type = f"\"TODO: provide data for this field (data_type = {parameter.data_type})\""
        if parameter.data_type == "int":
            data_type = "0x0"
        elif parameter.data_type in ["HexList", "str", "list"]:
            data_type = "HexList(0x0)"
        elif parameter.data_type == "bool":
            data_type = "HexList(False)"
        # end if
        return data_type
    # end def get_data_type

    @staticmethod
    def get_settings_data_type(parameter):
        """
        Get Settings data type

        :param parameter: Parameter information
        :type parameter: ``Parameter``

        :return: Formatted output
        :rtype: ``str``
        """
        name = parameter.get_name_without_space()
        value = f"\"TODO: provide data for this field (data_type = {parameter.data_type})\""
        if parameter.settings_data_type in ["str", "HexList"]:
            value = f"HexList(self.config.F_{name})"
        elif parameter.settings_data_type in ["tuple", "tuple(str)"]:
            value = f"[HexList(item) for item in self.config.F_{name}]"
        elif parameter.settings_data_type == "tuple(int)":
            value = f"[HexList(Numeral(item)) for item in self.config.F_{name}]"
        elif parameter.settings_data_type == "int":
            value = f"HexList(Numeral(self.config.F_{name}))"
        elif parameter.settings_data_type == "bool":
            value = "HexList(False)"
        elif parameter.settings_data_type == "list":
            value = "HexList(0x0)"
        # end if
        return value
    # end def get_settings_data_type

    @classmethod
    def get_method_param_min_value(cls, parameters, space, equal_to, template, name, version):
        """
        | Get the unit test method parameters format (comma separated string)
        | Example: 0x0007 Device Friendly Name::
        |    [1] getFriendlyName(byteIndex) -> byteIndex, nameChunk
        | GetFriendlyName parameters::
        |    ", byte_index=0"
        | GetFriendlyNameResponse parameters::
        |    ", byte_index=0, name_chunk=''.join(choices(ascii_uppercase + digits, k=1))"

        :param parameters: Parameter information
        :type parameters: ``list[Parameter | SubParameter]``
        :param space: Space format
        :type space: ``str``
        :param equal_to: EqualTo format
        :type equal_to: ``str``
        :param template: Template to use
        :type template: ``str``
        :param name: Name of the function or event
        :type name: ``str``
        :param version: Version information
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        if len(parameters) == 0:
            return ""
        # end if
        output = []
        for parameter in parameters:
            if not parameter.is_given_version_present(version):
                continue
            # end if
            if parameter.data_type == DataType.RESERVED:
                # ignore reserved field
                continue
            # end if
            if parameter.has_sub_parameters():
                data = cls.get_method_param_min_value(parameter.sub_parameters, space, equal_to, template,
                                                      name, version)
            else:
                data = cls.get_min_value_data(equal_to, space, template, parameter, name)
            # end if
            output.append(data)
        # end for
        output = CommonFileGenerator.uniquify_list(output)
        return "".join(output)
    # end def get_method_param_min_value

    @staticmethod
    def get_min_value_data(equal_to, space, template, parameter, name):
        """
        | Get the unit test method parameters format (comma separated string)
        | Example: 0x0007 Device Friendly Name::
        |    [1] getFriendlyName(byteIndex) -> byteIndex, nameChunk
        | GetFriendlyName parameters::
        |    ", byte_index=0"
        | GetFriendlyNameResponse parameters::
        |    ", byte_index=0, name_chunk=''.join(choices(ascii_uppercase + digits, k=1))"

        :param equal_to: EqualTo format
        :type equal_to: ``str``
        :param space: Space format
        :type space: ``str``
        :param template: Template to use
        :type template: ``str``
        :param parameter: Parameter information
        :type parameter: ``Parameter | SubParameter``
        :param name: Name of the function or event
        :type name: ``str``

        :return: Formatted output
        :rtype: ``str``
        """
        value = f"\"TODO: (Suresh Thiyagarajan) for data type {parameter.data_type}\""
        if parameter.data_type == "str":
            value = "''.join(choices(ascii_uppercase + digits, k=1))"
        elif parameter.data_type == "HexList":
            value = "HexList(0)"
        elif parameter.data_type == "list":
            value = f'HexList("00" * ({name}.LEN.{parameter.get_name_upper_underscore()} // 8))'
        elif parameter.data_type == "int":
            value = 0
        elif parameter.data_type == "bool":
            value = False
        # end if
        return Template(template).substitute(dict(
            Space=space,
            EqualTo=equal_to,
            Name=parameter.get_name_lower_underscore(),
            Value=value
        ))
    # end def get_min_value_data

    @classmethod
    def get_method_param_max_value(cls, parameters, space, equal_to, name, version):
        """
        | Get the unit test method parameters format (comma separated string)
        | Example: 0x0007 Device Friendly Name::
        |    [1] getFriendlyName(byteIndex) -> byteIndex, nameChunk
        | GetFriendlyName parameters::
        |    ", byte_index=0xff"
        | GetFriendlyNameResponse parameters::
        |    ", byte_index=0xff, name_chunk=''.join(choices(ascii_uppercase + digits, k=15))"

        :param parameters: Parameter information
        :type parameters: ``list[Parameter | SubParameter]``
        :param space: Space format
        :type space: ``str``
        :param equal_to: EqualTo format
        :type equal_to: ``str``
        :param name: Name of the function or event
        :type name: ``str``
        :param version: Version information
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        if len(parameters) == 0:
            return ""
        # end if
        output = []
        for parameter in parameters:
            if not parameter.is_given_version_present(version):
                continue
            # end if
            if parameter.data_type == DataType.RESERVED:
                # ignore reserved field
                continue
            # end if
            if parameter.has_sub_parameters():
                data = cls.get_method_param_max_value(parameter.sub_parameters, space, equal_to, name, version)
            else:
                data = cls.get_max_value_data(equal_to, name, space, parameter, version)
            # end if
            output.append(data)
        # end for
        return "".join(output)
    # end def get_method_param_max_value

    @staticmethod
    def get_max_value_data(equal_to, name, space, parameter, version):
        """
        Get max value data

        :param equal_to: EqualTo format
        :type equal_to: ``str``
        :param name: Name
        :type name: ``str``
        :param space: Space format
        :type space: ``str``
        :param parameter: Parameter information
        :type parameter: ``Parameter | SubParameter``
        :param version: Version information
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        if parameter.data_type == "str":
            value = f"''.join(choices(ascii_uppercase + digits, k={parameter.get_size(version) // 8}))"
        elif parameter.data_type == "HexList":
            value = f'HexList("FF" * ({name}.LEN.{parameter.get_name_upper_underscore()} // 8))'
        elif parameter.data_type == "list":
            value = f'HexList("FF" * ({name}.LEN.{parameter.get_name_upper_underscore()} // 8))'
        elif parameter.data_type == "int":
            value = hex(pow(2, parameter.get_size(version)) - 1).upper().replace('0X', '0x')
        elif parameter.data_type == "bool":
            value = True
        else:
            value = f'"TODO: (Suresh Thiyagarajan) for data type {parameter.data_type}"'
        # end if
        return Template(FeatureTestTemplate.NAME_VALUE_FORMAT).substitute(dict(
            Space=space,
            EqualTo=equal_to,
            Name=parameter.get_name_lower_underscore(),
            Value=value
        ))
    # end def get_max_value_data

    @classmethod
    def get_from_hexlist_body(cls, parameters, bitfield_class_name, version):
        """
        | Get the ``fromHexList`` method body format
        | Example: 0x4220 Lock Key State::
        |    [0] GetLockKeyState() -> lockStates
        |    where lockStates has inner states Kana, Compose, ScrLock, CapsLock, NumLock
        |  GetLockKeyStateResponse.fromHexList body::
        |    mixin.lock_key_state_format = cls.LockKeyStateFormat.fromHexList(mixin.lock_key_state_format)

        :param parameters: Parameter information
        :type parameters: ``list[Parameter | SubParameter]``
        :param bitfield_class_name: Name of the Class
        :type bitfield_class_name: ``str``
        :param version: Version information
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        if len(parameters) == 0:
            return ""
        # end if
        output = []
        for parameter in parameters:
            if not parameter.is_given_version_present(version):
                continue
            # end if
            if parameter.has_sub_parameters():
                field_name = parameter.get_name_lower_underscore(replace_bit_map=True)
                version_text = ""
                if parameter.check_multi_version():
                    version_text = AutoInput.get_version_text(version)
                # end if
                cls_name = parameter.get_name_without_space() + version_text
                output.append(Template(FeatureTemplate.DEF_HEXLIST_ONE_LINE).substitute(
                    dict(FieldName=field_name, ClassName=cls_name)))
            # end if
        # end for
        if len(output) == 0:
            return ""
        # end if
        return Template(FeatureTemplate.DEF_HEXLIST_BODY).substitute(
            dict(Response=bitfield_class_name, Fields="".join(output)))
    # end def get_from_hexlist_body

    @classmethod
    def get_init_method_body(cls, parameters, version):
        """
        | Get the ``__init__`` method body format
        | Example1: 0x0007 Device Friendly Name::
        |    [1] getFriendlyName(byteIndex) -> byteIndex, nameChunk
        | GetFriendlyName.__init__ body::
        |    self.byte_index = byte_index
        | GetFriendlyNameResponse.__init__ body::
        |    self.byte_index = byte_index
        |    self.name_chunk = name_chunk
        |
        | Example2: 0x4220 Lock Key State::
        |    [0] GetLockKeyState() -> lockStates
        |    where lockStates has inner states Kana, Compose, ScrLock, CapsLock, NumLock
        |  GetLockKeyStateResponse.__init__ body::
        |    self.lock_states = self.LockStates(kana=kana, compose=compose, scr_lock=scr_lock, num_lock=num_lock)

        :param parameters: Parameter information
        :type parameters: ``list[Parameter | SubParameter]``
        :param version: Version information
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        for parameter in parameters:
            if not parameter.is_given_version_present(version):
                continue
            # end if
            if parameter.exclusion:
                # Rationale: Some functions are deprecated even if this information is not written in the specification.
                # Example: x1815 - HostInfo - GetFeatureInfoResponseV1ToV2.__init__()
                # 'moveHost' and 'deleteHost' are forbidden.
                # That's why the capability bits 'Move Host' and 'Delete Host' were not exposed in the request API.
                # In the same way, 'eQuad HD' and 'USB HD' were never used by our firmwares.
                # Refer column P in tab 'API Info' in sheet:
                # https://docs.google.com/spreadsheets/d/1dQIU9SQnbkZG91g7vb5xZtRfm_G2EPyemC0dn6Lt2Mg
                continue
            # end if

            if parameter.data_type == DataType.RESERVED:
                # ignore reserved field
                continue
            # end if
            if parameter.has_sub_parameters():
                txt = parameter.get_name_lower_underscore_with_prefix(replace_bit_map=True)
                version_text = ""
                if parameter.check_multi_version():
                    version_text = AutoInput.get_version_text(version)
                # end if
                cls_name = parameter.get_name_without_space() + version_text
                space = " " * len(f"        self.{txt} = self.{cls_name}(")
                formatted_value = cls.get_formatted_method_param(
                    parameters=parameter.sub_parameters, version=version,
                    format_type="KeyValue", separator=f",\n{space}")
                output.append(Template(FeatureTemplate.DEF_INIT_BODY).substitute(
                    dict(Key=f"{txt}", Value=f"self.{cls_name}({formatted_value})")))
                continue
            # end if

            output1, key, value = cls.get_field_key_value(parameter)
            output.extend(output1)
            dictionary = dict(Key=key, Value=value)
            output.append(Template(FeatureTemplate.DEF_INIT_BODY).substitute(dictionary))
        # end for
        return "".join(output)
    # end def get_init_method_body

    @classmethod
    def get_field_key_value(cls, parameter):
        """
        Get field text format

        :param parameter: Parameter information
        :type parameter: ``Parameter | SubParameter``

        :return: Formatted output
        :rtype: ``tuple(list[str], str, str)``
        """
        output = []
        txt = parameter.get_name_lower_underscore_with_prefix()
        key = txt
        value = txt

        if parameter.data_type == "str":
            output.append(f"\n\n        {txt} = HexList.fromString({txt}) if isinstance({txt}, str) else {txt}")
            output.append(f"\n        {txt}_copy = HexList({txt}.copy())")
            output.append(f"\n        {txt}_copy.addPadding(self.LEN.{txt.upper()} // 8, fromLeft=False)")
            value = f"{txt}_copy"
        elif parameter.size % 8 == 0:
            if parameter.data_type == "HexList":
                output.append(f"\n\n        {txt}_copy = HexList({txt}.copy())")
                output.append(f"\n        {txt}_copy.addPadding(self.LEN.{txt.upper()} // 8)")
                value = f"{txt}_copy"
            elif parameter.data_type == "list":
                output.append(f"\n\n        {txt} = HexList({txt})")
                output.append(f"\n        {txt}.addPadding(self.LEN.{txt.upper()} // 8)")
                value = f"{txt}"
            else:
                value = f"HexList(Numeral({txt}, self.LEN.{txt.upper()} // 8))"
            # end if
        # end if
        return output, key, value
    # end def get_field_key_value

    @classmethod
    def get_init_method_param_document(cls, parameters, space_length, version, is_optional=False):
        """
        | Get the ``__init__`` method documentation format
        | Example: 0x0007 Device Friendly Name::
        |    [1] getFriendlyName(byteIndex) -> byteIndex, nameChunk
        | GetFriendlyName.__init__ documentation::
        |    : param byte_index: Byte Index
        |    : type byte_index: ``int | HexList``
        | GetFriendlyNameResponse.__init__ documentation::
        |    : param byte_index: Byte Index
        |    : type byte_index: ``int | HexList``
        |    : param name_chunk: Name Chunk
        |    : type name_chunk: ``str | HexList``

        :param parameters: Parameter information
        :type parameters: ``list[Parameter | SubParameter]``
        :param space_length: Space length
        :type space_length: ``int``
        :param version: Version information
        :type version: ``int``
        :param is_optional: Flag indicating if optional text is appended - OPTIONAL
        :type is_optional: ``bool``

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        for parameter in parameters:
            if not parameter.is_given_version_present(version):
                continue
            # end if
            if parameter.exclusion:
                # Rationale: Some functions are deprecated even if this information is not written in the specification.
                # Example: x1815 - HostInfo - GetFeatureInfoResponseV1ToV2.__init__()
                # 'moveHost' and 'deleteHost' are forbidden.
                # That's why the capability bits 'Move Host' and 'Delete Host' were not exposed in the request API.
                # In the same way, 'eQuad HD' and 'USB HD' were never used by our firmwares.
                # Refer column P in tab 'API Info' in sheet:
                # https://docs.google.com/spreadsheets/d/1dQIU9SQnbkZG91g7vb5xZtRfm_G2EPyemC0dn6Lt2Mg
                continue
            # end if

            if parameter.data_type == DataType.RESERVED:
                # ignore reserved field
                continue
            # end if

            if parameter.has_sub_parameters():
                txt = cls.get_init_method_param_document(parameter.sub_parameters, space_length, version, is_optional)
                output.append(txt)
                continue
            # end if
            data_type, name = cls._get_name_and_data_type(parameter, space_length, is_optional)
            name_lower = parameter.get_name_lower_underscore()
            space = " " * space_length

            output.append(Template(CommonTemplate.DOC_PARAM_TYPE).substitute(dict(
                NameLower=name_lower,
                Name=name,
                Type=data_type,
                Space=space
            )))
        # end for
        return "".join(output)
    # end def get_init_method_param_document

    @classmethod
    def _get_name_and_data_type(cls, parameter, space_length, is_optional):
        """
        Get name and the data type
        :param parameter: Parameter information
        :type parameter: ``Parameter | SubParameter``
        :param space_length: Space length
        :type space_length: ``int``
        :param is_optional: Flag indicating if optional text is appended - OPTIONAL
        :type is_optional: ``bool``

        :return: Formatted output
        :rtype: ``tuple[str, str]``
        """
        data_type = "``HexList``" if parameter.data_type == "HexList" \
            else f"``{parameter.data_type} | HexList``"
        name = cls.get_field_name(parameter, space_length)
        if is_optional:
            # remove full stop at the end (if any)
            if name[-1] == ".":
                name = name[:-1]
            # end if
            if not name.endswith(ConstantTextManager.OPTIONAL):
                name += ConstantTextManager.OPTIONAL
            # end if
            data_type = data_type[:-2] + " | None``"
        # end if
        return data_type, name
    # end def _get_name_and_data_type

    @classmethod
    def get_field_name(cls, parameter, space_length):
        """
        Get field name from the parameter name/comment

        Example => :param set_os_version: getHostOsVersion() and setHostOsVersion() supported by the device - OPTIONAL

        :param parameter: Parameter information
        :type parameter: ``Parameter | SubParameter``
        :param space_length: Space length
        :type space_length: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        name = cls.get_formatted_name(parameter)

        # Wrap text
        text = f"{' ' * space_length}:param {parameter.name.lower()}: "
        space = " " * len(text)
        wrap_length = ConstantTextManager.LINE_WRAP_AT_CHAR - len(text)
        if len(name) > wrap_length:
            count = name.find(". ")
            delimiter = " "
            if count > 0 and name.find("=>") > 0:
                delimiter = ". "
            # end if
            name = cls.get_wrapped_text(content=name, space=space, wrap_length=wrap_length, delimiter=delimiter)
        # end if

        return name
    # end def get_field_name

    @classmethod
    def get_formatted_name(cls, parameter):
        """
        Get field name from the parameter name/comment

        Example => :param set_os_version: getHostOsVersion() and setHostOsVersion() supported by the device - OPTIONAL

        :param parameter: Parameter information
        :type parameter: ``Parameter | SubParameter``

        :return: Formatted output
        :rtype: ``str``
        """
        # default: use the field name as comment
        # explicit: comment is provided in test design document (spreadsheet)
        name = parameter.name if parameter.comment is None else parameter.comment
        if parameter.default_value is not None:
            # remove full stop at the end (if any)
            if name[-1] == ".":
                name = name[:-1]
            # end if
            if not name.endswith(ConstantTextManager.OPTIONAL):
                name += ConstantTextManager.OPTIONAL
            # end if
        # end if

        # replace : with => to avoid confusion in documentation text
        name = name.replace(":", "=>")

        # remove extra \n (if any)
        items = name.split("\n")
        if len(items) > 1:
            for i in range(len(items)):
                # add full stop in the end
                if len(items[i]) > 1 and items[i][-1] != ".":
                    items[i] += "."
                # end if
            # end for
            name = f" ".join(items)
        # end if

        # if multiline, add full stop in the end
        if name.find(". ") > 0 and name[-1] != ".":
            name += "."
        # end if
        return name
    # end def get_formatted_name

    @staticmethod
    def get_feature_class_param_document(parameters, version, output_value):
        """
        | Get the feature class's parameters documentation format
        | Example: 0x0007 Device Friendly Name::
        |    [1] getFriendlyName(byteIndex) -> byteIndex, nameChunk
        | ``DeviceFriendlyNameV0`` documentation request::
        |    byteIndex
        | ``DeviceFriendlyNameV0`` documentation response::
        |    byteIndex, nameChunk

        :param parameters: Parameter information
        :type parameters: ``list[Parameter | SubParameter]``
        :param version: Version information
        :type version: ``int``
        :param output_value: Output type
        :type output_value: ``bool``

        :return: Formatted output
        :rtype: ``str``
        """
        if len(parameters) == 0:
            return DataType.NONE if output_value else ""
        # end if
        output = []
        for parameter in parameters:
            if not parameter.is_given_version_present(version):
                continue
            # end if
            if parameter.data_type == DataType.RESERVED:
                # ignore reserved field
                continue
            # end if
            value = parameter.get_name_title(replace_bit_map=True)
            # make the first letter of the value to lower case
            value = value[0].lower() + value[1:]
            output.append(value)
        # end for
        if len(output) == 0:
            return DataType.NONE if output_value else ""
        # end if
        return ", ".join(output)
    # end def get_feature_class_param_document

    @classmethod
    def get_request_report_id_type(cls, api, version):
        """
        | Get report id type for request.
        | Example::
        |    0 < REPORT_ID_SHORT <= 24
        |    24 < REPORT_ID_LONG <= 128

        :param api: Function/Event information
        :type api: ``FunctionInfo | EventInfo``
        :param version: Version information
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        max_size = 0
        for parameter in api.request.parameters:
            max_size += parameter.get_size(version)
        # end for

        return cls.REPORT_ID_SHORT_NAME if max_size <= cls.REPORT_ID_SHORT_SIZE else cls.REPORT_ID_LONG_NAME
    # end def get_request_report_id_type

    @classmethod
    def get_request_padding_size(cls, parameters, version):
        """
        | Get request padding size
        | Example::
        |    0 < REPORT_ID_SHORT <= 24
        |    Padding = REPORT_ID_SHORT - sum(size of all parameters)
        |    24 < REPORT_ID_LONG <= 128
        |    Padding = REPORT_ID_LONG - sum(size of all parameters)

        :param parameters: Parameter information
        :type parameters: ``list[Parameter | SubParameter]``
        :param version: Version information
        :type version: ``int``

        :return: Padding size in bits
        :rtype: ``int``
        """
        padding_size = cls.REPORT_ID_LONG_SIZE
        for parameter in parameters:
            padding_size -= parameter.get_size(version)
        # end for

        # The default size is 24 bits (3 bytes).
        short_size = cls.REPORT_ID_LONG_SIZE - cls.REPORT_ID_SHORT_SIZE
        if padding_size == short_size:
            # The data is already 3 bytes. No padding is required.
            padding_size = 0
        elif (padding_size - short_size) > 0:
            # More than 3 bytes data in input
            padding_size -= short_size
        # end if
        return padding_size
    # end def get_request_padding_size

    @classmethod
    def get_response_padding_size(cls, parameters, version):
        """
        | Get response padding size
        | Example::
        |    0 < REPORT_ID_LONG <= 128
        |    Padding = REPORT_ID_LONG - sum(size of all parameters)

        :param parameters: Parameter information
        :type parameters: ``list[Parameter | SubParameter]``
        :param version: Version information
        :type version: ``int``

        :return: Padding size in bits
        :rtype: ``int``
        """
        padding_size = cls.REPORT_ID_LONG_SIZE
        for parameter in parameters:
            padding_size -= parameter.get_size(version)
        # end for

        return padding_size
    # end def get_response_padding_size

    @classmethod
    def get_subclass_function_data_format(cls, parameter, version):
        """
        | Get subclass function data format
        | Example: Returns the structure for the given subclass::
        |    Format:
        |    ============================  ==========
        |    Name                          Bit Count
        |    ============================  ==========
        |    Padding                       24
        |    ============================  ==========

        :param parameter: Parameter information
        :type parameter: ``Parameter``
        :param version: Version
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str | None``
        """
        output = []
        column_1_size = parameter.get_name_col_size(ConstantTextManager.COLUMN_ONE_SIZE)
        column_2_size = ConstantTextManager.COLUMN_TWO_SIZE
        for sub_parameter in parameter.sub_parameters:
            if not sub_parameter.is_given_version_present(version):
                continue
            # end if
            output.append(
                Template(FeatureTemplate.FUNCTION_DATA_VALUE_FORMAT).substitute(
                    dict(
                        Space=" " * 8,
                        Name=f"{sub_parameter.name:{column_1_size}}",
                        Size=sub_parameter.get_size(version),
                        DoubleSpace="  "
                    )
                )
            )
        # end for
        if len(output) > 0:
            return Template(FeatureTemplate.FUNCTION_DATA_FORMAT).substitute(dict(
                Space=" " * 8,
                Format="Format",
                NameHashLine="=" * column_1_size,
                BitCountHashLine="=" * column_2_size,
                DoubleSpace="  ",
                Name=f"{'Name':{column_1_size}}",
                BitCount="Bit count",
                FunctionParams="".join(output)
            ))
        # end if
    # end def get_subclass_function_data_format

    @classmethod
    def get_function_data_format(cls, info, category, version):
        """
        | Get function request/response documentation comment for data format
        | Example: Returns the structure (request/response/event) for the given api::
        |    Format:
        |    ============================  ==========
        |    Name                          Bit Count
        |    ============================  ==========
        |    Padding                       24
        |    ============================  ==========

        :param info: Function/Event information
        :type info: ``FunctionInfo | EventInfo``
        :param category: Request/Response/Event category
        :type category: ``str``
        :param version: Version information
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        parameters = None
        padding_size = None
        column_1_size = ConstantTextManager.COLUMN_ONE_SIZE
        column_2_size = ConstantTextManager.COLUMN_TWO_SIZE
        if category == "Request":
            if not info.request.is_this_version_applicable(version):
                return ""
            # end if
            parameters = info.request.parameters
            column_1_size = info.request.get_name_col_size(ConstantTextManager.COLUMN_ONE_SIZE)
            padding_size = cls.get_request_padding_size(parameters, version)
        elif category == "Response":
            if not info.response.is_this_version_applicable(version):
                return ""
            # end if
            parameters = info.response.parameters
            column_1_size = info.response.get_name_col_size(ConstantTextManager.COLUMN_ONE_SIZE)
            padding_size = cls.get_response_padding_size(parameters, version)
        elif category == "Event":
            if not info.event.is_this_version_applicable(version):
                return ""
            # end if
            parameters = info.event.parameters
            column_1_size = info.event.get_name_col_size(ConstantTextManager.COLUMN_ONE_SIZE)
            padding_size = cls.get_response_padding_size(parameters, version)
        # end if
        if len(parameters) == 0:
            return ""
        # end if
        SizeValidator.validate_negative_padding_size(padding_size, info.name)
        output = []
        for parameter in parameters:
            if not parameter.is_given_version_present(version):
                continue
            # end if
            name = parameter.get_name(replace_bit_map=True)
            output.append(
                Template(FeatureTemplate.FUNCTION_DATA_VALUE_FORMAT).substitute(
                    dict(
                        Space=" " * 4,
                        Name=f"{name:{column_1_size}}",
                        Size=parameter.get_size(version),
                        DoubleSpace="  "
                    )
                )
            )
        # end for

        if padding_size > 0:
            output.append(
                Template(FeatureTemplate.FUNCTION_DATA_VALUE_FORMAT).substitute(
                    dict(
                        Space=" " * 4,
                        Name=f"{'Padding':{column_1_size}}",
                        Size=padding_size,
                        DoubleSpace="  "
                    )
                )
            )
        # end if

        return Template(FeatureTemplate.FUNCTION_DATA_FORMAT).substitute(dict(
            Space=" " * 4,
            Format="Format",
            NameHashLine="=" * column_1_size,
            BitCountHashLine="=" * column_2_size,
            DoubleSpace="  ",
            Name=f"{'Name':{column_1_size}}",
            BitCount="Bit count",
            FunctionParams="".join(output)
        ))
    # end def get_function_data_format

    @classmethod
    def get_subclass_fid_info(cls, parameter, version):
        """
        | Get the subclass ``FID`` information
        | Example: Generate the FID class::
        |    class FID(Object):
        |        '''
        |        Define Field Identifiers
        |        '''
        |        X = 0xFF
        |        PADDING = X - 1
        |    # end class FID

        :param parameter: Parameter information
        :type parameter: ``Parameter``
        :param version: Version
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str | None``
        """
        output = []
        prev_value = None
        for sub_parameter in parameter.sub_parameters:
            if not sub_parameter.is_given_version_present(version):
                continue
            # end if
            name = sub_parameter.get_name_upper_underscore()
            if len(output) == 0:
                value = "0xFF"
            else:
                value = f"{prev_value} - 1"
            # end if
            output.append(
                Template(FeatureTemplate.NAME_VALUE_FORMAT).substitute(
                    dict(Name=name, Value=value, Space=cls.get_new_line_with_space(space_length=12),
                         EqualTo=ConstantTextManager.EQUAL_TO)
                )
            )
            prev_value = name
        # end for
        if len(output) > 0:
            return Template(FeatureTemplate.SUBCLASS_FID).substitute(dict(
                FidValue="".join(output)
            ))
        # end if
    # end def get_subclass_fid_info

    @classmethod
    def get_new_line_with_space(cls, space_length):
        """
        Get a new line with space text

        :param space_length: Space length
        :type space_length: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        return ConstantTextManager.NEW_LINE + " " * space_length
    # end def get_new_line_with_space

    @classmethod
    def get_class_fid_info(cls, info, category, base_class, version):
        """
        | Get ``FID`` class information
        | Example: Generate the FID class with respective base class::
        |    class FID(BaseClass.FID):
        |        # See ``BaseClass.FID``
        |        X = BaseClass.FID.SOFTWARE_ID - 1
        |        PADDING = X - 1
        |    # end class FID

        :param info: Function/Event information
        :type info: ``FunctionInfo | EventInfo``
        :param category: Request/Response/Event category
        :type category: ``str``
        :param base_class: Base class to FID
        :type base_class: ``str``
        :param version: Version information
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        parameters = None
        padding_size = 0
        if category == "Request":
            parameters = info.request.parameters
            padding_size = cls.get_request_padding_size(parameters, version)
        elif category == "Response":
            parameters = info.response.parameters
            padding_size = cls.get_response_padding_size(parameters, version)
        elif category == "Event":
            parameters = info.event.parameters
            padding_size = cls.get_response_padding_size(parameters, version)
        # end if
        if len(parameters) == 0:
            return ""
        # end if

        output = []
        prev_value = None
        for parameter in parameters:
            if not parameter.is_given_version_present(version):
                continue
            # end if
            name = parameter.get_name_upper_underscore(replace_bit_map=True)
            if prev_value is None:
                value = f"{base_class}.FID.SOFTWARE_ID - 1"
            else:
                value = f"{prev_value} - 1"
            # end if
            output.append(
                Template(FeatureTemplate.NAME_VALUE_FORMAT).substitute(
                    dict(Name=name, Value=value, Space=cls.get_new_line_with_space(space_length=8),
                         EqualTo=ConstantTextManager.EQUAL_TO)
                )
            )
            prev_value = name
        # end for

        if padding_size > 0:
            output.append(
                Template(FeatureTemplate.NAME_VALUE_FORMAT).substitute(
                    dict(Name=DataType.PADDING.upper(), Value=f"{prev_value} - 1",
                         Space=cls.get_new_line_with_space(space_length=8),
                         EqualTo=ConstantTextManager.EQUAL_TO)
                )
            )
        # end if
        return Template(FeatureTemplate.CLASS_FID).substitute(dict(
            Base=base_class,
            FidValue="".join(output)
        ))
    # end def get_class_fid_info

    @classmethod
    def get_bit_field_info(cls, parameter, version):
        """
        | Get ``BitField`` information
        | Example: Generate the BitField class::
        |            BitField(fid=FID.X, length=LEN.X,
        |                     title="X", name="x",
        |                     checks=(CheckHexList(LEN.X // 8), CheckByte(),)),
        |            BitField(fid=FID.PADDING, length=LEN.PADDING,
        |                     title="Padding", name="padding",
        |                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
        |                     default_value=DEFAULT.PADDING)

        :param parameter: Parameter information
        :type parameter: ``Parameter | SubParameter``
        :param version: Version information
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        dictionary = dict(
            NameLower=parameter.get_name_lower_underscore(),
            NameUpper=parameter.get_name_upper_underscore(),
            NameTitle=parameter.get_name_title(),
            DefaultValue=""
        )
        indent = " " * 4
        if parameter.settings_default_value is not None:
            dictionary["DefaultValue"] = f",\n{indent * 5} default_value=DEFAULT.{dictionary['NameUpper']}"
        # end if
        size = int(parameter.get_size(version))
        if parameter.data_type == "List":
            items = [ConstantTextManager.IMPORT_HEXLIST,
                     ConstantTextManager.IMPORT_CHECK_INT,
                     ConstantTextManager.IMPORT_CHECK_LIST]
            template = FeatureTemplate.BITFIELD_CHECK_LIST_SUB_LEVEL
        elif parameter.data_type == "HexList" or size % 8 == 0:
            if size == 8:
                items = [ConstantTextManager.IMPORT_HEXLIST]
                # Use CheckByte() in the checks only if the data size is 1 byte.
                dictionary["Check"] = " CheckByte(),"
            else:
                items = [ConstantTextManager.IMPORT_HEXLIST,
                         ConstantTextManager.IMPORT_CHECK_INT]
                dictionary["Check"] = \
                    f'{indent * 7} CheckInt(min_value=0, max_value=pow(2, LEN.{dictionary["NameUpper"]}) - 1),'
            # end if
            template = FeatureTemplate.BITFIELD_CHECK_HEX_LIST_SUB_LEVEL
        else:
            items = [ConstantTextManager.IMPORT_HEXLIST,
                     ConstantTextManager.IMPORT_CHECK_INT]
            template = FeatureTemplate.BITFIELD_CHECK_INT_SUB_LEVEL
        # end if
        cls._import_list.extend(items)
        return Template(template).substitute(dictionary)
    # end def get_bit_field_info

    @classmethod
    def get_subclass_fields_info(cls, parameter, version):
        """
        | Get subclass ``FIELDS`` information
        | Example: Generate the FIELDS class with respective base class::
        |    FIELDS = (
        |            BitField(fid=FID.X, length=LEN.X,
        |                     title="X", name="x",
        |                     checks=(CheckHexList(LEN.X // 8), CheckByte(),)),
        |            BitField(fid=FID.PADDING, length=LEN.PADDING,
        |                     title="Padding", name="padding",
        |                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
        |                     default_value=DEFAULT.PADDING)
        |            )

        :param parameter: Parameter information
        :type parameter: ``Parameter``
        :param version: Version
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str | None``
        """
        output = []
        for sub_parameter in parameter.sub_parameters:
            if not sub_parameter.is_given_version_present(version):
                continue
            # end if
            output.append(cls.get_bit_field_info(sub_parameter, version))
        # end for
        if len(output) > 0:
            return Template(FeatureTemplate.FIELDS_SUB_LEVEL).substitute(dict(Fields="".join(output)))
        # end if
    # end def get_subclass_fields_info

    @classmethod
    def get_class_fields_info(cls, parameters, base_class, padding_size, version):
        """
        | Get ``FIELDS`` information
        | Example: Generate the FIELDS class with respective base class::
        |    FIELDS = BaseClass.FIELDS + (
        |            BitField(fid=FID.X, length=LEN.X,
        |                     title="X", name="x",
        |                     checks=(CheckHexList(LEN.X // 8), CheckByte(),)),
        |            BitField(fid=FID.PADDING, length=LEN.PADDING,
        |                     title="Padding", name="padding",
        |                     checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
        |                     default_value=GpioAccess.DEFAULT.PADDING))

        :param parameters: Parameter information
        :type parameters: ``list[Parameter]``
        :param base_class: Base class information
        :type base_class: ``str``
        :param padding_size: Size of the padding
        :type padding_size: ``int``
        :param version: Version information
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        indent = " " * 4
        for parameter in parameters:
            if not parameter.is_given_version_present(version):
                continue
            # end if
            dictionary = dict(
                NameLower=parameter.get_name_lower_underscore(replace_bit_map=True),
                NameUpper=parameter.get_name_upper_underscore(replace_bit_map=True),
                NameTitle=parameter.get_name_title(replace_bit_map=True),
                DefaultValue=""
            )
            if parameter.data_type == DataType.RESERVED:
                # For reserved fields, use the default padding value
                dictionary["DefaultValue"] = f",\n{indent * 4} default_value={base_class}.DEFAULT.PADDING"
            # end if
            size = int(parameter.get_size(version))
            if parameter.data_type == "list":
                items = [ConstantTextManager.IMPORT_CHECK_INT,
                         ConstantTextManager.IMPORT_CHECK_LIST,
                         ConstantTextManager.IMPORT_HEXLIST,
                         ConstantTextManager.IMPORT_NUMERAL]
                template = FeatureTemplate.BITFIELD_CHECK_LIST
            elif parameter.data_type == "HexList" or size % 8 == 0:
                if size == 8:
                    items = [ConstantTextManager.IMPORT_HEXLIST]
                    # Use CheckByte() in the checks only if the data size is 1 byte.
                    dictionary["Check"] = " CheckByte(),"
                else:
                    items = [ConstantTextManager.IMPORT_HEXLIST,
                             ConstantTextManager.IMPORT_CHECK_INT]
                    dictionary["Check"] = f'\n{indent * 6} CheckInt(min_value=0, max_value=pow(2,' \
                                          f' LEN.{dictionary["NameUpper"]}) - 1),'
                # end if
                template = FeatureTemplate.BITFIELD_CHECK_HEX_LIST
            else:
                items = [ConstantTextManager.IMPORT_CHECK_INT,
                         ConstantTextManager.IMPORT_HEXLIST,
                         ConstantTextManager.IMPORT_NUMERAL]
                template = FeatureTemplate.BITFIELD_CHECK_INT
            # end if
            cls._import_list.extend(items)
            output.append(Template(template).substitute(dictionary))
        # end for

        if padding_size > 0:
            output.append(Template(FeatureTemplate.BITFIELD_PADDING).substitute(dict(Base=base_class)))
        # end if
        return Template(FeatureTemplate.FIELDS).substitute(dict(
            Base=base_class,
            Fields="".join(output)
        ))
    # end def get_class_fields_info

    @classmethod
    def get_subclass_default_info(cls, parameter, version):
        """
        | Get the subclass ``DEFAULT`` information
        | Example: Generate the DEFAULT class::
        |    class DEFAULT(Object):
        |        '''
        |        Field default values
        |        '''
        |        RESERVED = 0x0
        |    # end class DEFAULT

        :param parameter: Parameter information
        :type parameter: ``Parameter``
        :param version: Version information
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str | None``
        """
        output = []
        for sub_parameter in parameter.sub_parameters:
            if sub_parameter.settings_default_value is None:
                continue
            # end if
            if not sub_parameter.is_given_version_present(version):
                continue
            # end if
            value = sub_parameter.settings_default_value
            if isinstance(value, int):
                value = hex(value).upper().replace('0X', '0x')
            # end if
            output.append(
                Template(FeatureTemplate.NAME_VALUE_FORMAT).substitute(
                    dict(Name=sub_parameter.get_name_upper_underscore(),
                         Value=value,
                         Space=cls.get_new_line_with_space(space_length=12),
                         EqualTo=ConstantTextManager.EQUAL_TO)
                )
            )
        # end for
        if len(output) > 0:
            return Template(FeatureTemplate.SUBCLASS_DEFAULT).substitute(dict(DefaultValue="".join(output)))
        # end if
    # end def get_subclass_default_info

    @classmethod
    def is_multi_version(cls, parameters):
        """
        Check whether multi version is available for the parameter

        :param parameters: Parameter information
        :type parameters: ``list[Parameter | SubParameter]``

        :return: Flag indicating if parameter has multi version
        :rtype: ``bool``
        """
        for parameter in parameters:
            if parameter.version_info != "all versions":
                return True
            # end if
        # end for
    # end def is_multi_version

    @classmethod
    def get_subclass_len_info(cls, parameter, version):
        """
        | Get the subclass ``LEN`` information
        | Example: Generate the LEN class::
        |    class LEN(Object):
        |        '''
        |        Field length in bits
        |        '''
        |        X = 0x8
        |        PADDING = 0x10
        |    # end class LEN

        :param parameter: Parameter information
        :type parameter: ``Parameter``
        :param version: Version
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str | None``
        """
        output = []
        for sub_parameter in parameter.sub_parameters:
            if not sub_parameter.is_given_version_present(version):
                continue
            # end if
            output.append(
                Template(FeatureTemplate.NAME_VALUE_FORMAT).substitute(
                    dict(Name=sub_parameter.get_name_upper_underscore(),
                         Value=hex(sub_parameter.get_size(version)).upper().replace('0X', '0x'),
                         Space=cls.get_new_line_with_space(space_length=12),
                         EqualTo=ConstantTextManager.EQUAL_TO)
                )
            )
        # end for
        if len(output) > 0:
            return Template(FeatureTemplate.SUBCLASS_LEN).substitute(dict(LenValue="".join(output)))
        # end if
    # end def get_subclass_len_info

    @classmethod
    def get_class_len_info(cls, info, category, base_class, version):
        """
        | Get ``LEN`` class information
        | Example: Generate the LEN class with respective base class::
        |    class LEN(BaseClass.LEN):
        |        # See ``BaseClass.LEN``
        |        X = 0x8
        |        PADDING = 0x10
        |    # end class LEN

        :param info: Function/Event information
        :type info: ``FunctionInfo | EventInfo``
        :param category: Request/Response/Event category
        :type category: ``str``
        :param base_class: Base class to LEN
        :type base_class: ``str``
        :param version: Version information
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        if not info.is_this_version_applicable(version):
            return ""
        # end if
        parameters = None
        padding_size = 0
        if category == "Request":
            parameters = info.request.parameters
            padding_size = cls.get_request_padding_size(parameters, version)
        elif category == "Response":
            parameters = info.response.parameters
            padding_size = cls.get_response_padding_size(parameters, version)
        elif category == "Event":
            parameters = info.event.parameters
            padding_size = cls.get_response_padding_size(parameters, version)
        # end if
        if len(parameters) == 0:
            return ""
        # end if

        output = []
        for parameter in parameters:
            if not parameter.is_given_version_present(version):
                continue
            # end if
            output.append(
                Template(FeatureTemplate.NAME_VALUE_FORMAT).substitute(
                    dict(Name=parameter.get_name_upper_underscore(replace_bit_map=True),
                         Value=hex(parameter.get_size(version)).upper().replace('0X', '0x'),
                         Space=cls.get_new_line_with_space(space_length=8),
                         EqualTo=ConstantTextManager.EQUAL_TO)
                )
            )
        # end for

        if padding_size > 0:
            output.append(
                Template(FeatureTemplate.NAME_VALUE_FORMAT).substitute(
                    dict(Name=DataType.PADDING.upper(),
                         Value=hex(padding_size).upper().replace('0X', '0x'),
                         Space=cls.get_new_line_with_space(space_length=8),
                         EqualTo=ConstantTextManager.EQUAL_TO)
                )
            )
        # end if
        return Template(FeatureTemplate.CLASS_LEN).substitute(dict(Base=base_class, LenValue="".join(output)))
    # end def get_class_len_info

    @classmethod
    def get_mixed_container(cls, api, dictionary, version=None):
        """
        | Generate the mixed container class structure
        | Example: Few request and response parameter can share the same data format.
        | In such cases, generate a base class with FID, LEN, FIELDS and documentation.
        | This container will be used many times to avoid duplicate.::
        |    class MixedContainer(BaseClass):
        |        <Documentation>
        |        class FID(BaseClass.FID):
        |            <FieldInfo>
        |        # end class FID
        |        class LEN(BaseClass.LEN):
        |            <LengthInfo>
        |        # end class LEN
        |        FIELDS = BaseClass.FIELDS + <BitFieldsInfo>
        |    # end class MixedContainer

        :param api: API information
        :type api: ``dict``
        :param dictionary: List of values to replace
        :type dictionary: ``dict``
        :param version: Version information
        :type version: ``int | None``

        :return: Formatted output
        :rtype: ``str``
        """
        parameters = None
        padding_size = 0
        info = api["Api"]
        category = api["Category"]
        if category == "Request":
            parameters = info.request.parameters
            padding_size = cls.get_request_padding_size(parameters, version)
        elif category == "Response":
            parameters = info.response.parameters
            padding_size = cls.get_response_padding_size(parameters, version)
        elif category == "Event":
            parameters = info.event.parameters
            padding_size = cls.get_response_padding_size(parameters, version)
        # end if

        dictionary["FunctionName"] = api["Base"]
        dictionary["Base"] = dictionary["FeatureNameTitleCaseWithoutSpace"]
        dictionary["FidParams"] = cls.get_class_fid_info(info, category, dictionary["Base"], version)
        dictionary["LenParams"] = cls.get_class_len_info(info, category, dictionary["Base"], version)
        if len(parameters) == 0:
            dictionary["FieldParams"] = ""
        else:
            dictionary["FieldParams"] = cls.get_class_fields_info(parameters, dictionary["Base"], padding_size, version)
        # end if
        dictionary["FunctionParams"] = cls.get_function_data_format(info, category, version)
        return Template(FeatureTemplate.MIXED_PACKET_DATA_FORMAT).substitute(dictionary)
    # end def get_mixed_container

    @classmethod
    def get_class_structure(cls, info, base_class, category, template, version):
        """
        | Generate the request/response class structure
        | Example: 0x0007 Device Friendly Name::
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen
        | request::
        |    class SetFriendlyName(DeviceFriendlyName):
        |        <body>
        |    # end class SetFriendlyName
        | response::
        |    class SetFriendlyNameResponse(DeviceFriendlyName):
        |        <body>
        |    # end class SetFriendlyNameResponse
        | event::
        |    class XyzEvent(BaseClass):
        |        <body>
        |    # end class xyzEvent

        :param info: Function/Event information
        :type info: ``FunctionInfo | EventInfo``
        :param base_class: Base class information
        :type base_class: ``str``
        :param category: Request/Response/Event category
        :type category: ``str``
        :param template: Template to use
        :type template: ``str``
        :param version: Version information
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        if not info.is_this_version_applicable(version):
            return ""
        # end if
        function_name = info.get_name_without_space()
        hex_name = info.get_name_without_space()
        version_text = ""
        version_list = ", ".join([str(v) for v in AutoInput.get_version_list()])
        if info.check_multi_version():
            version_text = AutoInput.get_version_text(version)
            version_list = version
        # end if

        dictionary = dict(
            Base=base_class,
            FeatureNameTitleCaseWithoutSpace="".join(AutoInput.HIDPP_FEATURE_NAME.split()),
            FidParams="",
            FieldParams="",
            FunctionIndex=info.index,
            FunctionName=function_name,
            FunctionParams="",
            HidppFeatureVersion=AutoInput.HIDPP_FEATURE_VERSION,
            InitBody="",
            InitParams="self, device_index, feature_index, **kwargs",
            InitParamsDoc="",
            LenParams="",
            NewLine="",
            Response="Response",
            SubClass="",
            Version=version_list,
            VersionText=version_text,
        )

        parameters = None
        padding_size = 0
        if category == "Event":
            dictionary["RequestList"] = ""
            dictionary["ResponseOrEvent"] = category
            dictionary["ResponseOrEventUpper"] = category.upper()
            dictionary["ReportIdType"] = cls.REPORT_ID_LONG_NAME
            parameters = info.event.parameters
            padding_size = cls.get_response_padding_size(parameters, version)
            hex_name += f"Event{version_text}"
        elif category == "Response":
            dictionary["ResponseOrEvent"] = category
            dictionary["ResponseOrEventUpper"] = category.upper()
            dictionary["RequestList"] = f"\n    REQUEST_LIST = ({function_name}{version_text},)"
            dictionary["ReportIdType"] = cls.REPORT_ID_LONG_NAME
            parameters = info.response.parameters
            padding_size = cls.get_response_padding_size(parameters, version)
            hex_name += f"Response{version_text}"
        elif category == "Request":
            dictionary["RequestList"] = f"\n    REQUEST_LIST = ({function_name}{version_text},)"
            dictionary["ReportIdType"] = cls.get_request_report_id_type(info, version)
            parameters = info.request.parameters
            padding_size = cls.get_request_padding_size(parameters, version)
        # end if

        # override the base class
        if base_class == "FeatureNameTitleCaseWithoutSpace":
            dictionary["Base"] = dictionary[base_class]
            dictionary["FidParams"] = cls.get_class_fid_info(info, category, dictionary["Base"], version)
            dictionary["LenParams"] = cls.get_class_len_info(info, category, dictionary["Base"], version)
            if len(parameters) > 0:
                dictionary["FieldParams"] = cls.get_class_fields_info(
                    parameters, dictionary["Base"], padding_size, version)
            # end if
            dictionary["FunctionParams"] = cls.get_function_data_format(info, category, version)
            dictionary["NewLine"] = ConstantTextManager.NEW_LINE
        # end if
        dictionary["FromHexList"] = cls.get_from_hexlist_body(parameters, hex_name, version)

        if len(parameters) <= 0:
            return Template(template).substitute(dictionary)
        # end if

        formatted_param = cls.get_formatted_method_param(parameters, version)
        params = "self, device_index, feature_index, **kwargs"
        if len(formatted_param) > 0:
            params = f"self, device_index, feature_index, {formatted_param}, **kwargs"
        # end if

        # Wrap text
        space = " " * len(f"    def __init__(")
        wrap_length = ConstantTextManager.LINE_WRAP_AT_CHAR - len(space) - 3
        if len(params) > wrap_length:
            params = cls.get_wrapped_text(
                content=params, space=space, wrap_length=wrap_length, delimiter=", ")
        # end if

        dictionary["InitParams"] = params
        dictionary["InitParamsDoc"] = cls.get_init_method_param_document(
            parameters=parameters, space_length=8, version=version)
        dictionary["InitBody"] = cls.get_init_method_body(parameters, version)
        return Template(template).substitute(dictionary)
    # end def get_class_structure

    @classmethod
    def get_wrapped_text(cls, content, space, wrap_length, delimiter=",", decorator=""):
        """
        Get wrapped text if the content is more than wrap length

        :param content: The content to wrap
        :type content: ``str``
        :param space: Prefix space
        :type space: ``str``
        :param wrap_length: Position to line wrap
        :type wrap_length: ``int``
        :param delimiter: Delimiter to split - OPTIONAL
        :type delimiter: ``str``
        :param decorator: Decorator before and after content - OPTIONAL
        :type decorator: ``str``

        :return: Formatted output
        :rtype: ``str``
        """
        txt = ""
        final_text = ""
        trailing_text = delimiter
        if delimiter[-1] == " ":
            # remove the trailing space
            trailing_text = delimiter[:-1]
        # end if
        for value in content.split(delimiter):
            if len(txt + value) >= wrap_length:
                if len(final_text) == 0:
                    final_text = f"{decorator}{txt}{decorator}"
                else:
                    final_text = f"{final_text}{trailing_text}\n{space}{decorator}{txt}{decorator}"
                # end if
                txt = ""
            # end if
            if len(txt) == 0:
                txt = value
            else:
                txt = f"{txt}{delimiter}{value}"
            # end if
        # end for
        if len(final_text) == 0:
            final_text = f"{decorator}{txt}{decorator}"
        else:
            final_text = f"{final_text}{trailing_text}\n{space}{decorator}{txt}{decorator}"
        # end if
        return final_text
    # end def get_wrapped_text

    @classmethod
    def get_subclass_structure(cls, parameters):
        """
        Get the class structure for sub parameters

        :param parameters: Parameter information
        :type parameters: ``list[Parameter]``

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        for parameter in parameters:
            if not parameter.has_sub_parameters():
                continue
            # end if
            for text in cls.get_subclass_structure_per_version(parameter):
                output.append(text)
            # end for
        # end for
        output = CommonFileGenerator.uniquify_list(output)
        return "".join(output)
    # end def get_subclass_structure

    @classmethod
    def get_subclass_structure_per_version(cls, parameter):
        """
        Get the class structure for sub parameters

        :param parameter: Parameter information
        :type parameter: ``Parameter``

        :return: Formatted output
        :rtype: ``list[str]``
        """
        output = []
        version_values = dict()
        version_output = []
        for version in AutoInput.get_version_list():
            fid_params = cls.get_subclass_fid_info(parameter, version)
            if fid_params is None:
                continue
            # end if
            # Use the SubclassName without version suffix
            sub_class_name = parameter.get_name_without_space()
            version_values[version] = dict(
                Version=version,
                SubclassName=sub_class_name,
                FidParams=fid_params,
                LenParams=cls.get_subclass_len_info(parameter, version),
                FieldParams=cls.get_subclass_fields_info(parameter, version),
                FunctionParams=cls.get_subclass_function_data_format(parameter, version),
                DefaultParams=cls.get_subclass_default_info(parameter, version),
                NewLine=ConstantTextManager.NEW_LINE
            )
            text = Template(FeatureTemplate.SUBCLASS_STRUCTURE).substitute(version_values[version])
            if text not in version_output:
                version_output.append(text)
            # end if
        # end for
        # Check all the version have the single common output
        if len(version_output) == 1:
            output.append(version_output[0])

        # Check if multiple version available. Suffix the Version number to the class name.
        elif len(version_output) > 1:
            for version, value in version_values.items():
                value["SubclassName"] = f'{parameter.get_name_without_space()}V{version}'
                output.append(Template(FeatureTemplate.SUBCLASS_STRUCTURE).substitute(value))
            # end for
        # end if

        output = CommonFileGenerator.uniquify_list(output)
        return output
    # end def get_subclass_structure_per_version

    @classmethod
    def get_structure(cls, version, previous_version):
        """
        | Generate the request/response/event list structure
        | The below generated request/response/event is used {FeatureName}V0.__init__
        | request::
        |    self.{function_name}_cls = {FeatureName}Model.get_request_cls(
        |        self.VERSION, index.{FUNCTION_NAME})
        | response::
        |    self.{function_name}_response_cls = {FeatureName}Model.get_response_cls(
        |        self.VERSION, index.{FUNCTION_NAME})
        | event::
        |    self.{event_name}_event_cls = {FeatureName}Model.get_report_cls(
        |        self.VERSION, index.{EVENT_NAME})

        :param version: Version information
        :type version: ``int``
        :param previous_version: Version information
        :type previous_version: ``int | None``

        :return: Formatted output
        :rtype: ``tuple[str, str, str]``
        """
        request = []
        response = []
        for function_info in AutoInput.FUNCTION_LIST:
            if not function_info.is_this_version_applicable(version):
                continue
            # end if
            if previous_version is not None:
                if not function_info.check_multi_version():
                    continue
                # end if
                if not function_info.check_since_version(version):
                    continue
                # end if
            # end if

            dictionary = dict(
                FunctionNameLower=function_info.get_name_lower_underscore(),
                FunctionNameUpper=function_info.get_name_upper_underscore(),
                Ext="_cls",
                RRR="get_request_cls",
                Model="Model",
                FeatureNameTitleCaseWithoutSpace="".join(AutoInput.HIDPP_FEATURE_NAME.split())
            )
            request.append(Template(FeatureTemplate.NAME_VALUE_RRR_STRUCTURE).substitute(dictionary))

            dictionary = dict(
                FunctionNameLower=function_info.get_name_lower_underscore(),
                FunctionNameUpper=function_info.get_name_upper_underscore(),
                Ext="_response_cls",
                RRR="get_response_cls",
                Model="Model",
                FeatureNameTitleCaseWithoutSpace="".join(AutoInput.HIDPP_FEATURE_NAME.split())
            )
            response.append(Template(FeatureTemplate.NAME_VALUE_RRR_STRUCTURE).substitute(dictionary))
        # end for

        return "".join(request), "".join(response), cls.get_event_text(version, previous_version)
    # end def get_structure

    @classmethod
    def get_event_text(cls, version, previous_version):
        """
        | Generate the event list structure
        | The below generated event is used {FeatureName}V0.__init__
        | event::
        |    self.{event_name}_event_cls = {FeatureName}Model.get_report_cls(
        |        self.VERSION, index.{EVENT_NAME})

        :param version: Version information
        :type version: ``int``
        :param previous_version: Version information
        :type previous_version: ``int | None``

        :return: Formatted output
        :rtype: ``str``
        """
        event = []
        for event_info in AutoInput.EVENT_LIST:
            if not event_info.is_this_version_applicable(version):
                continue
            # end if
            if previous_version is not None:
                if not event_info.check_multi_version():
                    continue
                # end if
                if event_info.check_since_version(version):
                    continue
                # end if
            # end if
            event.append(Template(FeatureTemplate.NAME_VALUE_RRR_STRUCTURE).substitute(dict(
                FunctionNameLower=event_info.get_name_lower_underscore(),
                FunctionNameUpper=event_info.get_name_upper_underscore(),
                Ext="_event_cls",
                RRR="get_report_cls",
                Model="Model",
                FeatureNameTitleCaseWithoutSpace="".join(AutoInput.HIDPP_FEATURE_NAME.split())
            )))
        # end for

        return "" if len(event) == 0 else "\n\n        # Events" + "".join(event)
    # end def get_event_text

    @classmethod
    def get_helper_class(cls, version=None):
        """
        Generate helper class for the function

        :param version: Version information
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        response = []
        for function_info in AutoInput.FUNCTION_LIST:
            text = cls.get_hidpp_function_info(function_info, version)
            if len(text) > 0 and text not in response:
                response.append(text)
            # end if
            text = cls.get_hidpp_function_info_with_error_handling(function_info, version)
            if len(text) > 0 and text not in response:
                response.append(text)
            # end if
        # end for

        event = []
        for event_info in AutoInput.EVENT_LIST:
            if not event_info.event.is_this_version_applicable(version):
                continue
            # end if
            if len(event_info.event.parameters) > 0:
                name = f"{event_info.name} Event"
                name_lower = f"{event_info.get_name_lower_underscore()}_event"
                event.append(Template(UtilsTemplate.GET_HIDPP_EVENT).substitute(dict(
                    CommonBaseTestCase=cls.get_common_base_test_case_name(),
                    FunctionLower=name_lower,
                    FunctionName="".join(name.split()),
                    ReqCls="_cls",
                    FIDLower=AutoInput.HIDPP_FEATURE_ID.lower()
                )))
            # end if
        # end for

        return "\n".join([cls.get_message_checker_class(),
                          Template(UtilsTemplate.CLASS_HIDPP_HELPER).substitute(dict(
                              FeatureName="".join(AutoInput.HIDPP_FEATURE_NAME.split()),
                              FeatureNameFactory="".join(AutoInput.HIDPP_FEATURE_NAME.split()) + "Factory",
                              HidppFunction="\n".join(response),
                              HidppEvent="".join(event)
                          ))])
    # end def get_helper_class

    @classmethod
    def get_message_checker_class(cls):
        """
        | Generate message checker class for the function
        | Example: 0x0007 Device Friendly Name:
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen
        | Message Checker which validates the output parameters::
        |    nameLen

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        for item in cls.get_message_checker_input():
            name = item[0]
            name_without_space = item[1]
            parameters = item[2]
            is_multi_version = item[3]
            category = item[4]
            for parameter in parameters:
                if parameter.has_sub_parameters():
                    default_check_map = cls.get_check_map_methods(
                        parameter.name, parameter.sub_parameters, is_multi_version)
                    if len(default_check_map) > 0:
                        txt = Template(UtilsTemplate.CLASS_MESSAGE_CHECKER).substitute(dict(
                            FunctionName=parameter.get_name_without_space(),
                            Ext="Checker",
                            DefaultCheckMap=default_check_map,
                        ))
                        output.append(txt)
                    # end if
                # end if
            # end for

            default_check_map = cls.get_check_map_methods(name, parameters, is_multi_version, category)
            if len(default_check_map) > 0:
                output.append(Template(UtilsTemplate.CLASS_MESSAGE_CHECKER).substitute(dict(
                    FunctionName=name_without_space + category,
                    Ext="Checker",
                    DefaultCheckMap=default_check_map,
                )))
            # end if
        # end for

        return "".join(CommonFileGenerator.uniquify_list(output))
    # end def get_message_checker_class

    @classmethod
    def get_message_checker_input(cls):
        """
        Get message checker class input items

        :return: Input values for the message checker class
        :rtype: ``list[tuple(str, str, str, str)]``
        """
        items = []
        for function_info in AutoInput.FUNCTION_LIST:
            if len(function_info.response.parameters) == 0:
                continue
            # end if
            items.append((function_info.name, function_info.get_name_without_space(), function_info.response.parameters,
                          function_info.response.check_multi_version(), "Response"))
        # end for
        for event_info in AutoInput.EVENT_LIST:
            items.append((event_info.name, event_info.get_name_without_space(), event_info.event.parameters,
                          event_info.event.check_multi_version(), "Event"))
        # end for
        return items
    # end def get_message_checker_input

    @classmethod
    def get_check_map_methods(cls, name, parameters, is_multi_version, ext=""):
        """
        Generate check map class methods

        :param name: Name
        :type name: ``str``
        :param parameters: Parameter information
        :type parameters: ``list[Parameter | SubParameter]``
        :param is_multi_version: Flag indicating if multi version is applicable
        :type is_multi_version: ``bool``
        :param ext: Extension - OPTIONAL
        :type ext: ``str``

        :return: Formatted output
        :rtype: ``str``
        """
        rv, config, error_text = cls.get_default_check_map_return_values(
            parameters=parameters,
            is_multi_version=is_multi_version)
        if len(rv) == 0:
            return ""
        # end if
        error_doc = ""
        if len(error_text) > 0:
            error_doc = """\n\n            :raise ``NotImplementedError``: Version that raise an exception"""
        # end if
        output = [Template(UtilsTemplate.GET_DEFAULT_CHECK_MAP).substitute(dict(
            CommonBaseTestCase=cls.get_common_base_test_case_name(),
            ErrorText=error_text,
            ErrorDoc=error_doc,
            ReturnValues=rv,
            Config=config,
            HidppCategoryUpper=AutoInput.HIDPP_CATEGORY.upper(),
            FeatureNameUpperCaseWithUnderscore="_".join(AutoInput.HIDPP_FEATURE_NAME.upper().split())
        ))]

        response = ext.lower() if len(ext) > 0 else "bitmap"
        for parameter in parameters:
            field_data_type = parameter.get_field_data_type()
            field_lower = parameter.get_name_lower_underscore(replace_bit_map=True)
            dictionary = dict(
                CommonBaseTestCase=cls.get_common_base_test_case_name(),
                FieldLowerCase=field_lower,
                FunctionName="".join(name.split()) + ext,
                ResponseName=cls.get_response_name(ext, name, parameter),
                Response=response,
                FieldDataType=field_data_type
            )

            if parameter.has_sub_parameters():
                dictionary["Utils"] = f'{"".join(AutoInput.HIDPP_FEATURE_NAME.split())}TestUtils'
                dictionary["Checker"] = f'{parameter.get_name_without_space()}Checker'
                dictionary["ClassName"] = f'{"".join(AutoInput.HIDPP_FEATURE_NAME.split())}'
                dictionary["FieldDataType"] = "``dict``"

                config_text, items = cls.get_check_map_items(config, dictionary, parameter)

                dictionary["VersionConfig"] = config_text
                dictionary["Items"] = "".join(CommonFileGenerator.uniquify_list(items))
                output.append(Template(UtilsTemplate.GET_CHECK_MAP_FUNCTION_SUB_LEVEL).substitute(dictionary))
            else:
                dictionary["Obtained"] = f"{response}.{field_lower},  # TODO: verify this data type ({field_data_type})"
                dictionary["Expected"] = "expected,"
                if parameter.data_type in ["int", "Reserved"]:
                    dictionary["Obtained"] = f"to_int({response}.{field_lower}),"
                    dictionary["Expected"] = "to_int(expected),"
                elif parameter.data_type in ["str", "HexList", "bool"]:
                    dictionary["Obtained"] = f"HexList({response}.{field_lower}),"
                    dictionary["Expected"] = "HexList(expected),"
                # end if
                output.append(Template(UtilsTemplate.GET_CHECK_MAP_FUNCTION).substitute(dictionary))
            # end if
        # end for
        return "".join(CommonFileGenerator.uniquify_list(output))
    # end def get_check_map_methods

    @classmethod
    def get_check_map_items(cls, config, dictionary, parameter):
        """
        Get check map items

        :param config: Config text
        :type config: ``str``
        :param dictionary: Dictionary
        :type dictionary: ``dict``
        :param parameter: Parameter information
        :type parameter: ``Parameter | SubParameter``

        :return: Formatted output
        :rtype: ``tuple[str, list[str]]``
        """
        items = []
        config_text = ""
        raise_text = ""
        indent = " " * 4
        for version in AutoInput.get_version_list():
            if not parameter.is_given_version_present(version):
                continue
            # end if
            if parameter.check_multi_version():
                version_text = AutoInput.get_version_text(version)
                config_text = config
                raise_text = f'\n{indent * 3}raise NotImplementedError(f"Version {version} is not implemented")'
                dictionary["MaskBitMap"] = f'{parameter.get_name_without_space()}{version_text}'
                dictionary["Space"] = indent * 4
                item = Template(UtilsTemplate.GET_SUB_LEVEL_SINGLE_ITEM).substitute(dictionary)
                items.append(f"\n{indent * 3}if version == cls.Version.{cls._version_map[version]}:"
                             f"\n{item}\n{indent * 3}# end if")
            else:
                dictionary["Space"] = indent * 3
                dictionary["MaskBitMap"] = f"{parameter.get_name_without_space()}"
                item = Template(UtilsTemplate.GET_SUB_LEVEL_SINGLE_ITEM).substitute(dictionary)
                if item not in items:
                    items.append(f"\n{item}")
                # end if
            # end if
        # end for
        if len(raise_text) > 0:
            items.append(raise_text)
        # end if
        return config_text, items
    # end def get_check_map_items

    @classmethod
    def get_response_name(cls, ext, name, parameter):
        """
        Get response name

        :param ext: Extension
        :type ext: ``str``
        :param name: Name
        :type name: ``str``
        :param parameter: Parameter information
        :type parameter: ``Parameter | SubParameter``

        :return: Response name
        :rtype: ``str``
        """
        response = ext.lower() if len(ext) > 0 else "bitmap"
        output = []
        for version in AutoInput.get_version_list():
            if not parameter.is_given_version_present(version):
                continue
            # end if
            version_text = ""
            if parameter.check_multi_version():
                version_text = AutoInput.get_version_text(version)
            # end if
            response_name = f'{"".join(name.split())}{ext}{version_text}'
            if response == "bitmap":
                response_name = f'{"".join(AutoInput.HIDPP_FEATURE_NAME.split())}.{response_name}'
            elif AutoInput.ARGS_OBJECT_REFERENCE == ConstantTextManager.ARGS_OBJ_REF_NAME_WITH_PATH:
                response_name = f'pyhid.hidpp.features.{AutoInput.HIDPP_CATEGORY.lower()}.' \
                                f'{"".join(AutoInput.HIDPP_FEATURE_NAME.lower().split())}.' \
                                f'{response_name}'
            # end if
            if response_name not in output:
                output.append(response_name)
            # end if
        # end for
        return " | ".join(output)
    # end def get_response_name

    @staticmethod
    def get_inner_check_map(test_util, function_info, version, space):
        """
        Generate inner check_map return values

        :param test_util: Test util name
        :type test_util: ``str``
        :param function_info: Function information
        :type function_info: ``FunctionInfo``
        :param version: Version information
        :type version: ``int``
        :param space: Space
        :type space: ``str``

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        open_brace = "{"
        close_brace = "}"
        for parameter in function_info.response.parameters:
            if not parameter.has_sub_parameters():
                continue
            # end if
            result = ReqResGenerator.get_inner_check_map_text(parameter, version, space)
            if len(result) > 0:
                output.append(f"checker = {test_util}.{parameter.get_name_without_space()}Checker")
                value = ",".join(result)
                output.append(f"{parameter.get_name_lower_underscore(replace_bit_map=True)} = "
                              f"{open_brace}{value}\n{space}{close_brace}")
            # end if
        # end for
        return f"\n{space}".join(output)
    # end def get_inner_check_map

    @staticmethod
    def get_inner_check_map_text(parameter, version, space):
        """
        Get inner check map text

        :param parameter: Parameter information
        :type parameter: ``Parameter``
        :param version: Version information
        :type version: ``int``
        :param space: Space
        :type space: ``str``

        :return: Formatted output
        :rtype: ``str``
        """
        indent = " " * 4
        result = []
        for sub_parameter in parameter.sub_parameters:
            if not sub_parameter.is_given_version_present(version):
                continue
            # end if
            if sub_parameter.data_type == DataType.RESERVED:
                # ignore reserved field
                continue
            # end if
            name = sub_parameter.get_name_lower_underscore()
            if name == DataType.PADDING:
                continue
            # end if
            if sub_parameter.settings_data_type in ["int", "str"]:
                # this field is already in utils default_check_map
                continue
            # end if
            result.append(f'\n{space}{indent}"{name}": (checker.check_{name}, {name})')
        # end for
        return result
    # end def get_inner_check_map_text

    @staticmethod
    def get_override_check_map(function_info, template, version, include_device_feature=False):
        """
        Generate check_map override return values

        :param function_info: Function information
        :type function_info: ``FunctionInfo``
        :param template: CheckMap template
        :type template: ``str``
        :param version: Version information
        :type version: ``int``
        :param include_device_feature: Flag indicating if the device/feature index are included in the check map
        - OPTIONAL
        :type include_device_feature: ``bool``

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        for parameter in function_info.response.parameters:
            if not parameter.is_given_version_present(version):
                continue
            # end if
            if parameter.data_type == DataType.RESERVED:
                # ignore reserved field
                continue
            # end if
            name = parameter.get_name_lower_underscore(replace_bit_map=True)
            if name == DataType.PADDING:
                continue
            # end if
            if parameter.settings_data_type in ["int", "str"]:
                # this field is already in utils default_check_map
                continue
            # end if
            output.append(Template(template).substitute(dict(Field1=name, Field2=name, Field3=name)))
        # end for

        # Inject deviceIndex and featureIndex
        if include_device_feature:
            # Insert device_index at 1st position
            output.insert(0, Template(template).substitute(
                    dict(Field1="device_index",
                         Field2="device_index",
                         Field3="HexList(self.original_device_index)")))
            # Insert feature_index at 2nd position
            output.insert(1, Template(template).substitute(
                dict(Field1="feature_index",
                     Field2="feature_index",
                     Field3=f"HexList(self.feature_{AutoInput.HIDPP_FEATURE_ID.lower()}_index)")))
        # end if
        return ",".join(output)
    # end def get_override_check_map

    @classmethod
    def get_default_check_map_return_values(cls, parameters, is_multi_version, class_name=None):
        """
        Generate ``default_check_map`` return values

        :param parameters: Parameter information
        :type parameters: ``list[Parameter | SubParameter]``
        :param is_multi_version: Flag indicating if multi version is applicable
        :type is_multi_version: ``bool``
        :param class_name: Class name - OPTIONAL
        :type class_name: ``str | None``

        :return: Formatted output
        :rtype: ``tuple[str, str, str]``
        """
        if is_multi_version:
            indent = 5
        else:
            indent = 4
        # end if

        version_output = []
        config = ""
        config_text = f'\n            config = test_case.f.PRODUCT.FEATURES.{AutoInput.HIDPP_CATEGORY.upper()}.' \
                      f'{"_".join(AutoInput.HIDPP_FEATURE_NAME.upper().split())}'
        version_text = ""
        assertion_text = ""
        if is_multi_version:
            version_text = f'\n            version = test_case.config_manager.get_feature_version(config)'
            assertion_text = '\n            raise NotImplementedError(f"Version {version} is not implemented")'
        # end if
        for version in AutoInput.get_version_list():
            has_config, output = cls.get_check_map_return_value(class_name, parameters, indent, version)
            if has_config:
                config = config_text
            # end if
            if len(output) == 0:
                continue
            # end if
            if is_multi_version:
                version_output.append(f"\n            if version == cls.Version.{cls._version_map[version]}:"
                                      + "\n                return {"
                                      + ",".join(output)
                                      + "\n                }"
                                      + "\n            # end if")
            else:
                version_output.append("\n            return {"
                                      + ",".join(output)
                                      + "\n            }")
            # end if
        # end for
        return f"".join(CommonFileGenerator.uniquify_list(version_output)), config + version_text, assertion_text
    # end def get_default_check_map_return_values

    @classmethod
    def get_check_map_return_value(cls, class_name, parameters, indent, version):
        """
        Get check map return value

        :param class_name: Class name
        :type class_name: ``str``
        :param parameters: Parameters information
        :type parameters: ``list[Parameter]``
        :param indent: Number of indents
        :type indent: ``int``
        :param version: Version information
        :type version: ``int``

        :return: Value containing check map
        :rtype: ``tuple[bool, list[str]]``
        """
        has_config = False
        output = []
        for parameter in parameters:
            if not parameter.is_given_version_present(version):
                continue
            # end if
            name = parameter.get_name_lower_underscore(replace_bit_map=True)
            if parameter.has_sub_parameters():
                data = f'{"".join(AutoInput.HIDPP_FEATURE_NAME.split())}TestUtils.' \
                       f'{parameter.get_name_without_space()}Checker.get_default_check_map(test_case)'
                output.append(cls.get_default_check_map_text(dict(
                    ClassName=class_name,
                    FieldLowerCase=name,
                    Data=data,
                    Space=" " * 4 * indent
                )))
                continue
            # end if
            has_config = True
            data = DataType.NONE
            if parameter.settings_data_type in ["int", "str", "HexList", "bool"]:
                field_name = parameter.get_name_title()
                data = f"config.F_{field_name}"
            elif parameter.settings_default_value is not None:
                data = parameter.settings_default_value
            # end if
            if name == DataType.PADDING or parameter.data_type == DataType.RESERVED:
                data = "0"
            # end if
            output.append(cls.get_default_check_map_text(dict(
                ClassName=class_name,
                FieldLowerCase=name,
                Data=data,
                Space=" " * 4 * indent
            )))
        # end for
        return has_config, output
    # end def get_check_map_return_value

    @classmethod
    def get_default_check_map_text(cls, dictionary):
        """
        Get the default check map text in single/double/triple line(s)

        :param dictionary: Dictionary to substitute
        :type dictionary: ``dict``

        :return: Formatted output
        :rtype: ``str``
        """
        text = Template(UtilsTemplate.GET_DEFAULT_CHECK_MAP_SINGLE_LINE).substitute(dictionary)
        if len(text) > ConstantTextManager.LINE_WRAP_AT_CHAR:
            line2 = Template(UtilsTemplate.GET_DEFAULT_CHECK_MAP_DOUBLE_LINE_2).substitute(dictionary)
            if len(line2) > ConstantTextManager.LINE_WRAP_AT_CHAR:
                text = Template(UtilsTemplate.GET_DEFAULT_CHECK_MAP_TRIPLE_LINE).substitute(dictionary)
            else:
                line1 = Template(UtilsTemplate.GET_DEFAULT_CHECK_MAP_DOUBLE_LINE_1).substitute(dictionary)
                text = line1 + line2
            # end if
        # end if
        return text
    # end def get_default_check_map_text

    @classmethod
    def get_hidpp_function_info(cls, function_info, version):
        """
        | Generate hid++ function for the api
        | Example: 0x0007 Device Friendly Name::
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen
        | HID++ Helper which helps in read/write operations::
        |        set_friendly_name

        :param function_info: Function information
        :type function_info: ``FunctionInfo``
        :param version: Version information
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        response_name_output = []
        for version_value in AutoInput.get_version_list():
            if not function_info.is_this_version_applicable(version_value):
                continue
            # end if
            version_text = ""
            if function_info.check_multi_version():
                version_text = AutoInput.get_version_text(version_value)
            # end if
            response_name = f'{"".join(function_info.name.split())}Response{version_text}'
            if AutoInput.ARGS_OBJECT_REFERENCE == ConstantTextManager.ARGS_OBJ_REF_NAME_WITH_PATH:
                response_name = f'pyhid.hidpp.features.{AutoInput.HIDPP_CATEGORY.lower()}.' \
                                f'{"".join(AutoInput.HIDPP_FEATURE_NAME.lower().split())}.{response_name}'
            # end if
            response_name_output.append(response_name)
        # end for
        response_name = " | ".join(CommonFileGenerator.uniquify_list(response_name_output))

        name_lower = function_info.get_name_lower_underscore()

        padding_code = ""
        padding_param = ""
        padding_param_doc = ""
        if ReqResGenerator.get_request_padding_size(function_info.request.parameters, version) > 0:
            padding_param = ", padding=None"
            padding_param_doc = UtilsTemplate.GET_HIDPP_FUNCTION_PADDING_DOC
            padding_code = UtilsTemplate.GET_HIDPP_FUNCTION_PADDING_CODE
        # end if

        reserved_code = ""
        reserved_param = ""
        reserved_param_doc = ""
        if function_info.request.check_data_type(version, ["Reserved"]):
            reserved_param = ", reserved=None"
            reserved_param_doc = UtilsTemplate.GET_HIDPP_FUNCTION_RESERVED_DOC
            reserved_code = UtilsTemplate.GET_HIDPP_FUNCTION_RESERVED_CODE
        # end if

        if len(function_info.request.parameters) > 0:
            is_optional = function_info.request.check_multi_version()
            params = "cls, test_case, " \
                     + cls.get_formatted_method_param(parameters=function_info.request.parameters,
                                                      version=version,
                                                      is_optional=is_optional) \
                     + f", device_index=None, port_index=None, software_id=None{padding_param}{reserved_param}"

            # Wrap text
            space = " " * len(f"        def {name_lower}(")
            wrap_length = ConstantTextManager.LINE_WRAP_AT_CHAR - len(space) - 4
            if len(params) > wrap_length:
                params = cls.get_wrapped_text(content=params, space=space, wrap_length=wrap_length, delimiter=", ")
            # end if

            separator = ",\n                "
            params_key_value = separator + cls.get_formatted_method_param(
                function_info.request.parameters, version, format_type="KeyAndValueWithHexList", separator=separator)
            params_doc = cls.get_init_method_param_document(
                parameters=function_info.request.parameters, space_length=12, version=version, is_optional=is_optional)
        else:
            params = f"cls, test_case, device_index=None, port_index=None, software_id=None{padding_param}"
            # Wrap text
            space = " " * len(f"        def {name_lower}(")
            wrap_length = ConstantTextManager.LINE_WRAP_AT_CHAR - len(space) - 4
            if len(params) > wrap_length:
                params = cls.get_wrapped_text(content=params, space=space, wrap_length=wrap_length, delimiter=", ")
            # end if
            params_key_value = ""
            params_doc = ""
        # end if

        return Template(UtilsTemplate.GET_HIDPP_FUNCTION).substitute(dict(
            CommonBaseTestCase=cls.get_common_base_test_case_name(),
            FIDLower=AutoInput.HIDPP_FEATURE_ID.lower(),
            FunctionLower=name_lower,
            FunctionName=function_info.get_name_without_space(),
            Index="_index",
            PaddingCode=padding_code,
            PaddingParamsDoc=padding_param_doc,
            Params=params,
            ParamsDoc=params_doc,
            ParamsKeyValue=params_key_value,
            Queue=AutoInput.HIDPP_CATEGORY.upper(),
            ReqCls="_cls",
            ResCls="_response_cls",
            ReservedCode=reserved_code,
            ReservedParamsDoc=reserved_param_doc,
            Response="Response",
            ResponseName=response_name,
        ))
    # end def get_hidpp_function_info

    @classmethod
    def get_hidpp_function_info_with_error_handling(cls, function_info, version):
        """
        | Generate hid++ function for the api
        | Example: 0x0007 Device Friendly Name::
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen
        | HID++ Helper which helps in read/write operations::
        |        set_friendly_name_and_check_error

        :param function_info: Function information
        :type function_info: ``FunctionInfo``
        :param version: Version information
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        indent = " " * 4
        response_name_output = []
        for version_value in AutoInput.get_version_list():
            if not function_info.is_this_version_applicable(version_value):
                continue
            # end if
            version_text = ""
            if function_info.check_multi_version():
                version_text = AutoInput.get_version_text(version_value)
            # end if
            response_name = f'{"".join(function_info.name.split())}Response{version_text}'
            if AutoInput.ARGS_OBJECT_REFERENCE == ConstantTextManager.ARGS_OBJ_REF_NAME_WITH_PATH:
                response_name = f'pyhid.hidpp.features.{AutoInput.HIDPP_CATEGORY.lower()}.' \
                                f'{"".join(AutoInput.HIDPP_FEATURE_NAME.lower().split())}.{response_name}'
            # end if
            response_name_output.append(response_name)
        # end for
        response_name = " | ".join(CommonFileGenerator.uniquify_list(response_name_output))

        name_lower = function_info.get_name_lower_underscore()
        suffix = "_and_check_error"

        if len(function_info.request.parameters) > 0:
            is_optional = function_info.request.check_multi_version()
            params = f"\n{indent*4}cls, test_case, error_codes, " \
                     + cls.get_formatted_method_param(parameters=function_info.request.parameters,
                                                      version=version,
                                                      is_optional=is_optional) \
                     + ", function_index=None, device_index=None, port_index=None"

            # Wrap text
            space = f"{indent * 4}"
            wrap_length = ConstantTextManager.LINE_WRAP_AT_CHAR - len(space) - 4
            if len(params) > wrap_length:
                params = cls.get_wrapped_text(content=params, space=space, wrap_length=wrap_length, delimiter=", ")
            # end if

            separator = ",\n                "
            params_key_value = separator + cls.get_formatted_method_param(
                function_info.request.parameters, version, format_type="KeyAndValueWithHexList", separator=separator)
            params_doc = cls.get_init_method_param_document(
                parameters=function_info.request.parameters, space_length=12, version=version, is_optional=is_optional)
        else:
            params = f"\n{indent*4}cls, test_case, error_codes, function_index=None, device_index=None, port_index=None"
            params_key_value = ""
            params_doc = ""
        # end if

        return Template(UtilsTemplate.GET_HIDPP_FUNCTION_WITH_ERROR_CASE).substitute(dict(
            Suffix=suffix,
            CommonBaseTestCase=cls.get_common_base_test_case_name(),
            FIDLower=AutoInput.HIDPP_FEATURE_ID.lower(),
            FunctionLower=name_lower,
            FunctionName=function_info.get_name_without_space(),
            Index="_index",
            Params=params,
            ParamsDoc=params_doc,
            ParamsKeyValue=params_key_value,
            ReqCls="_cls",
            ResponseName=response_name,
        ))
    # end def get_hidpp_function_info_with_error_handling

    @staticmethod
    def get_sys_import_structure():
        """
        | Generate the import section for the python library
        | Example: 0x0007 Device Friendly Name:
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen
        | This below generated output is used in import structure
        | Here the nameChunk is a string, hence a random value will be generated.::
        |    from random import choices
        |    from string import ascii_uppercase
        |    from string import digits

        :return: Import structure
        :rtype: ``list[str]``
        """
        for function_info in AutoInput.FUNCTION_LIST:
            for version in AutoInput.get_version_list():
                if function_info.check_data_type(version, ["str"]):
                    return [
                        ConstantTextManager.IMPORT_ASCII_UPPER_CASE,
                        ConstantTextManager.IMPORT_DIGITS,
                        ConstantTextManager.IMPORT_CHOICES
                    ]
                # end if
            # end for
        # end for
        return []
    # end def get_sys_import_structure

    @staticmethod
    def get_subclass_import_structure():
        """
        | Generate the import section for subclass
        | Example: 0x4220 Get Lock Key State::
        |    [0] getLockKeyState() -> lockKeyStateFormat
        | This below generated output is used in import structure::
        |    from pyhid.bitfieldcontainermixin import BitFieldContainerMixin

        :return: Import structure
        :rtype: ``list[str]``
        """
        hex_list = []
        for obj in AutoInput.FUNCTION_LIST:
            hex_list.extend(obj.request.parameters)
            hex_list.extend(obj.response.parameters)
        # end for

        for obj in AutoInput.EVENT_LIST:
            hex_list.extend(obj.event.parameters)
        # end for

        output = []
        for parameter in hex_list:
            if parameter.has_sub_parameters():
                output.append(ConstantTextManager.IMPORT_BIT_FIELD_CONTAINER_MIXIN)
                break
            # end if
        # end for

        return output
    # end def get_subclass_import_structure

    @classmethod
    def get_import_structure(cls):
        """
        | Generate the import section for used classes
        | Example: 0x0007 Device Friendly Name::
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen
        | This below generated output is used in import structure::
        |    from pyhid.hidpp.features.common.devicefriendlyname import SetFriendlyName

        :return: Formatted output
        :rtype: ``list[str]``
        """
        output = []
        dictionary = dict(
            FeatureNameLowerCaseWithoutSpace="".join(AutoInput.HIDPP_FEATURE_NAME.lower().split()),
            HidppCategory=AutoInput.HIDPP_CATEGORY,
        )

        # add import 1: from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyName
        dictionary["Name"] = "".join(AutoInput.HIDPP_FEATURE_NAME.split())
        output.append(Template(FeatureTestTemplate.IMPORT_ITEM).substitute(dictionary))

        # add import 2: from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyNameFactory
        dictionary["Name"] = "".join(AutoInput.HIDPP_FEATURE_NAME.split()) + "Factory"
        output.append(Template(FeatureTestTemplate.IMPORT_ITEM).substitute(dictionary))

        # add import 3: from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyNameV0
        for version in AutoInput.get_all_version():
            dictionary["Name"] = "".join(AutoInput.HIDPP_FEATURE_NAME.split()) + f"V{version}"
            output.append(Template(FeatureTestTemplate.IMPORT_ITEM).substitute(dictionary))
        # end for

        # add import for HexList (if any)
        output.append(cls._get_import_hex_list())

        # add import for request/response/event
        output.extend(cls._get_import_request_response())
        output.extend(cls._get_import_event())

        return output
    # end def get_import_structure

    @classmethod
    def _get_import_event(cls):
        """
        Get import statements for event

        :return: Event import statements
        :rtype: ``list[str]``
        """
        output = []
        dictionary = dict(
            FeatureNameLowerCaseWithoutSpace="".join(AutoInput.HIDPP_FEATURE_NAME.lower().split()),
            HidppCategory=AutoInput.HIDPP_CATEGORY,
        )
        for event_info in AutoInput.EVENT_LIST:
            for version in AutoInput.get_version_list():
                if not event_info.is_this_version_applicable(version):
                    continue
                # end if
                version_text = ""
                if event_info.check_multi_version():
                    version_text = AutoInput.get_version_text(version)
                # end if
                # Example: from pyhid.hidpp.features.peripheral.ads1231 import MonitorReportEvent
                dictionary["Name"] = f"{event_info.get_name_without_space()}Event{version_text}"
                output.append(Template(FeatureTestTemplate.IMPORT_ITEM).substitute(dictionary))
            # end for
        # end for
        return output
    # end def _get_import_event

    @classmethod
    def _get_import_request_response(cls):
        """
        Get import statements for request/response

        :return: Request/Response import statements
        :rtype: ``list[str]``
        """
        output = []
        dictionary = dict(
            FeatureNameLowerCaseWithoutSpace="".join(AutoInput.HIDPP_FEATURE_NAME.lower().split()),
            HidppCategory=AutoInput.HIDPP_CATEGORY,
        )
        for function_info in AutoInput.FUNCTION_LIST:
            for version in AutoInput.get_version_list():
                if not function_info.is_this_version_applicable(version):
                    continue
                # end if
                version_text = ""
                if function_info.check_multi_version():
                    version_text = AutoInput.get_version_text(version)
                # end if

                # Example: from pyhid.hidpp.features.common.devicefriendlyname import SetFriendlyName
                dictionary["Name"] = f"{function_info.get_name_without_space()}{version_text}"
                output.append(Template(FeatureTestTemplate.IMPORT_ITEM).substitute(dictionary))

                # Example: from pyhid.hidpp.features.common.devicefriendlyname import SetFriendlyNameResponse
                dictionary["Name"] = f"{function_info.get_name_without_space()}Response{version_text}"
                output.append(Template(FeatureTestTemplate.IMPORT_ITEM).substitute(dictionary))
            # end for
        # end for
        return output
    # end def _get_import_request_response

    @classmethod
    def get_import_numeral(cls):
        """
        Get import statement for Numeral if available

        :return: Numeral import statement
        :rtype: ``str``
        """
        for version in AutoInput.get_version_list():
            for function_info in AutoInput.FUNCTION_LIST:
                if function_info.request.check_settings_data_type(version, ["int"]):
                    return ConstantTextManager.IMPORT_NUMERAL
                # end if
            # end for
        # end for
        return ""
    # end def get_import_numeral

    @classmethod
    def _get_import_hex_list(cls):
        """
        Get import statement for HexList if available

        :return: HexList import statement
        :rtype: ``str``
        """
        for version in AutoInput.get_version_list():
            for function_info in AutoInput.FUNCTION_LIST:
                if function_info.check_data_type(version, ["HexList"]):
                    return ConstantTextManager.IMPORT_HEXLIST
                # end if
            # end for
            for event_info in AutoInput.EVENT_LIST:
                if event_info.check_data_type(version, ["HexList"]):
                    return ConstantTextManager.IMPORT_HEXLIST
                # end if
            # end for
        # end for
        return ""
    # end def _get_import_hex_list

    @staticmethod
    def get_interfaces_structure(version):
        """
        | Generate the interface list for test case
        | Example: 0x0007 Device Friendly Name:
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen
        | This below generated output is used in interface structure in setUpClass::
        |    "set_friendly_name_cls": SetFriendlyName,
        |    "set_friendly_name_response_cls": SetFriendlyNameResponse,

        :param version: Version
        :type version: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        for function_info in AutoInput.FUNCTION_LIST:
            if not function_info.is_this_version_applicable(version):
                continue
            # end if

            version_text = ""
            if function_info.check_multi_version():
                version_text = AutoInput.get_version_text(version)
            # end if

            # Request
            name = f"{function_info.get_name_without_space()}{version_text}"
            output.append(Template(FeatureTestTemplate.NAME_VALUE_STRUCTURE).substitute(dict(
                RightSideValue=name,
                LeftSideValue=f"{function_info.get_name_lower_underscore()}_cls",
            )))

            # Response
            name = f"{function_info.get_name_without_space()}Response{version_text}"
            output.append(Template(FeatureTestTemplate.NAME_VALUE_STRUCTURE).substitute(dict(
                RightSideValue=name,
                LeftSideValue=f"{function_info.get_name_lower_underscore()}_response_cls",
            )))
        # end for
        for event_info in AutoInput.EVENT_LIST:
            if not event_info.event.is_this_version_applicable(version):
                continue
            # end if

            version_text = ""
            if event_info.check_multi_version():
                version_text = AutoInput.get_version_text(version)
            # end if

            # Event
            name = f"{event_info.get_name_without_space()}Event{version_text}"
            output.append(Template(FeatureTestTemplate.NAME_VALUE_STRUCTURE).substitute(dict(
                RightSideValue=name,
                LeftSideValue=f"{event_info.get_name_lower_underscore()}_event_cls",
            )))
        # end for
        return "".join(output)
    # end def get_interfaces_structure

    @classmethod
    def get_test_request_name(cls, function_info, version):
        """
        Get request name

        :param function_info: Function information
        :type function_info: ``FunctionInfo``
        :param version: Version information
        :type version: ``int``

        :return: Request name
        :rtype: ``tuple[str, str]``
        """
        version_text = ""
        version_text_lower = ""
        if function_info.check_multi_version():
            version_text = AutoInput.get_version_text(version)
            version_text_lower = f"_{version_text.lower()}"
        # end if
        name_req = f"{function_info.get_name_without_space()}{version_text}"
        name_lower_req = f"{function_info.get_name_lower_underscore()}{version_text_lower}"
        return name_lower_req, name_req
    # end def get_test_request_name

    @classmethod
    def get_test_response_name(cls, function_info, version):
        """
        Get request name

        :param function_info: Function information
        :type function_info: ``FunctionInfo``
        :param version: Version information
        :type version: ``int``

        :return: Response name
        :rtype: ``tuple[str, str]``
        """
        version_text = ""
        version_text_lower = ""
        if function_info.check_multi_version():
            version_text = AutoInput.get_version_text(version)
            version_text_lower = f"_{version_text.lower()}"
        # end if
        name_res = f"{function_info.get_name_without_space()}Response{version_text}"
        name_lower_res = f"{function_info.get_name_lower_underscore()}_response{version_text_lower}"
        return name_lower_res, name_res
    # end def get_test_response_name

    @classmethod
    def get_test_event_name(cls, event_info, version):
        """
        Get event name

        :param event_info: Event information
        :type event_info: ``EventInfo``
        :param version: Version information
        :type version: ``int``

        :return: Event name
        :rtype: ``tuple[str, str]``
        """
        version_text = ""
        version_text_lower = ""
        if event_info.check_multi_version():
            version_text = AutoInput.get_version_text(version)
            version_text_lower = f"_{version_text.lower()}"
        # end if
        name = f"{event_info.get_name_without_space()}Event{version_text}"
        name_lower = f"{event_info.get_name_lower_underscore()}_event{version_text_lower}"
        return name, name_lower
    # end def get_test_event_name

    @classmethod
    def get_request_test_structure(cls):
        """
        | Generate the request/response test structure
        | Example: 0x0007 Device Friendly Name::
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen
        | This below generated output is used in unit test
        | request::
        |    @staticmethod
        |    def test_set_friendly_name():
        |        <body>
        |    # end def test_set_friendly_name

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        for function_info in AutoInput.FUNCTION_LIST:
            for version in AutoInput.get_version_list():
                if not function_info.is_this_version_applicable(version):
                    continue
                # end if
                name_lower_req, name_req = cls.get_test_request_name(function_info, version)
                space_length = len(f"        my_class = {name_req}(")
                space = f',\n{" " * space_length}'
                report_id_type = cls.get_request_report_id_type(function_info, version).lower()
                text = Template(FeatureTestTemplate.API_TEST_STRUCTURE).substitute(dict(
                    FunctionNameLower=name_lower_req,
                    FunctionName=name_req,
                    ReportIdType=f"_{report_id_type}_function_class_checker",
                    ParamsMinValue=cls.get_method_param_min_value(
                        parameters=function_info.request.parameters, space=space, equal_to="=",
                        template=FeatureTestTemplate.NAME_VALUE_FORMAT,
                        name=name_req, version=version),
                    ParamsMaxValue=cls.get_method_param_max_value(
                        parameters=function_info.request.parameters, space=space, equal_to="=",
                        name=name_req, version=version)
                ))
                if text not in output:
                    output.append(text)
                # end if
            # end for
        # end for
        return "".join(output)
    # end def get_request_test_structure

    @classmethod
    def get_response_test_structure(cls):
        """
        | Generate the response test structure
        | Example: 0x0007 Device Friendly Name::
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen
        | This below generated output is used in unit test
        | response::
        |    @staticmethod
        |    def test_set_friendly_name_response():
        |        <body>
        |    # end def test_set_friendly_name_response

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        for function_info in AutoInput.FUNCTION_LIST:
            for version in AutoInput.get_version_list():
                if not function_info.is_this_version_applicable(version):
                    continue
                # end if
                name_lower_res, name_res = cls.get_test_response_name(function_info, version)
                space_length = len(f"        my_class = {name_res}(")
                space = f',\n{" " * space_length}'
                text = Template(FeatureTestTemplate.API_TEST_STRUCTURE).substitute(dict(
                    FunctionNameLower=name_lower_res,
                    FunctionName=name_res,
                    ReportIdType=f"_long_function_class_checker",
                    ParamsMinValue=cls.get_method_param_min_value(
                        parameters=function_info.response.parameters, space=space, equal_to="=",
                        template=FeatureTestTemplate.NAME_VALUE_FORMAT,
                        name=name_res, version=version),
                    ParamsMaxValue=cls.get_method_param_max_value(
                        parameters=function_info.response.parameters, space=space, equal_to="=",
                        name=name_res, version=version)
                ))
                if text not in output:
                    output.append(text)
                # end if
            # end for
        # end for
        return "".join(output)
    # end def get_response_test_structure

    @classmethod
    def get_event_test_structure(cls):
        """
        | Generate the event test structure
        | event::
        |    @staticmethod
        |    def test_xyz_report():
        |        <body>
        |    # end def test_xyz_report

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        for event_info in AutoInput.EVENT_LIST:
            for version in AutoInput.get_version_list():
                if not event_info.is_this_version_applicable(version):
                    continue
                # end if
                name, name_lower = cls.get_test_event_name(event_info, version)
                space_length = len(f"        my_class = {name}(")
                space = f',\n{" " * space_length}'
                text = Template(FeatureTestTemplate.API_TEST_STRUCTURE).substitute(
                    dict(
                        FunctionNameLower=name_lower,
                        FunctionName=name,
                        ReportIdType="_long_function_class_checker",
                        ParamsMinValue=cls.get_method_param_min_value(
                            parameters=event_info.event.parameters, space=space, equal_to="=",
                            template=FeatureTestTemplate.NAME_VALUE_FORMAT,
                            name=name, version=version),
                        ParamsMaxValue=cls.get_method_param_max_value(
                            parameters=event_info.event.parameters, space=space, equal_to="=",
                            name=name, version=version)
                    )
                )
                if text not in output:
                    output.append(text)
                # end if
            # end for
        # end for
        return "".join(output)
    # end def get_event_test_structure

    @classmethod
    def get_api_test_structure(cls):
        """
        | Generate the api test structure
        """
        output = [
            cls.get_request_test_structure(),
            cls.get_response_test_structure(),
            cls.get_event_test_structure()
        ]
        return "".join(output)
    # end def get_api_test_structure

    @classmethod
    def get_api_structure(cls, version, previous_version):
        """
        | Generate the api documentation structure
        | Example: 0x0007 Device Friendly Name:
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen
        | This below generated output is used in documentation structure in ``DeviceFriendlyNameV0``::
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen

        :param version: Version information
        :type version: ``int``
        :param previous_version: Version information
        :type previous_version: ``int | None``

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        output.extend(cls.get_api_structure_for_function_info(version, previous_version))
        for event_info in AutoInput.EVENT_LIST:
            if not event_info.event.is_this_version_applicable(version):
                continue
            # end if
            if previous_version is not None and not event_info.check_multi_version():
                continue
            # end if
            out_param = cls.get_feature_class_param_document(event_info.event.parameters, version, True)
            # make the first letter of the function lower case
            name = event_info.get_name_without_space()
            value = Template(FeatureTemplate.API_STRUCTURE).substitute(dict(
                Space=" " * 4,
                Index=f"Event {event_info.index}",
                Name=f"{name}Event",
                InputParam="",
                OutputParam=out_param
            ))
            if len(value) > ConstantTextManager.LINE_WRAP_AT_CHAR:
                space = " " * 4
                wrap_length = ConstantTextManager.LINE_WRAP_AT_CHAR - len(space) - 3
                value = cls.get_wrapped_text(content=value, space=space, wrap_length=wrap_length, delimiter=", ")
            # end if
            output.append(value)
        # end for
        return "".join(output)
    # end def get_api_structure

    @classmethod
    def get_api_structure_for_function_info(cls, version, previous_version):
        """
        | Generate the api documentation structure
        | Example: 0x0007 Device Friendly Name:
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen
        | This below generated output is used in documentation structure in ``DeviceFriendlyNameV0``::
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen

        :param version: Version information
        :type version: ``int``
        :param previous_version: Version information
        :type previous_version: ``int``

        :return: List of information
        :rtype: ``list[str]``
        """
        output = []
        for function_info in AutoInput.FUNCTION_LIST:
            if not function_info.is_this_version_applicable(version):
                continue
            # end if
            if previous_version is not None and not function_info.check_multi_version():
                continue
            # end if
            value = cls.get_one_api_format_with_input_and_output(function_info=function_info, version=version, indent=1)
            if value not in output:
                output.append(value)
            # end if
        # end for
        return output
    # end def get_api_structure_for_function_info

    @classmethod
    def get_one_api_format_with_input_and_output(cls, function_info, version, indent):
        """
        | Get single api format with input and output parameters
        | Example: 0x0007 Device Friendly Name:
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen
        | This below generated output is used in documentation structure in ``DeviceFriendlyNameV0``::
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen

        :param function_info: FunctionInfo information
        :type function_info: ``FunctionInfo``
        :param version: Version information
        :type version: ``int``
        :param indent: Number of indents
        :type indent: ``int``

        :return: Formatted output
        :rtype: ``str``
        """
        in_param = cls.get_feature_class_param_document(function_info.request.parameters, version, False)
        out_param = cls.get_feature_class_param_document(function_info.response.parameters, version, True)
        # make the first letter of the function lower case
        name = function_info.get_name_without_space()
        name = name[0].lower() + name[1:]
        value = Template(FeatureTemplate.API_STRUCTURE).substitute(dict(
            Space=" " * (4 * indent),
            Index=function_info.index,
            Name=name,
            InputParam=f"({in_param})",
            OutputParam=out_param
        ))
        if len(value) > ConstantTextManager.LINE_WRAP_AT_CHAR:
            space = " " * (4 * indent)
            wrap_length = ConstantTextManager.LINE_WRAP_AT_CHAR - len(space) - 3
            value = cls.get_wrapped_text(content=value, space=space, wrap_length=wrap_length, delimiter=", ")
        # end if
        return value
    # end def get_one_api_format_with_input_and_output

    @staticmethod
    def get_feature_interface_structure():
        """
        | Get the feature interface structure
        | Example: 0x0007 Device Friendly Name::
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen
        | The below generated request/response is used ``DeviceFriendlyNameInterface.__init__``.
        | request::
        |    self.set_friendly_name_cls = None
        | response::
        |    self.set_friendly_name_response_cls = None

        :return: Formatted output
        :rtype: ``tuple[str, str, str]``
        """
        request = []
        response = []
        event = []
        for function_info in AutoInput.FUNCTION_LIST:
            dictionary = dict(
                FunctionName=function_info.get_name_lower_underscore(),
                Ext="_cls",
            )
            request.append(Template(FeatureTemplate.FEATURE_INTERFACE_STRUCTURE).substitute(dictionary))

            dictionary["Ext"] = "_response_cls"
            response.append(Template(FeatureTemplate.FEATURE_INTERFACE_STRUCTURE).substitute(dictionary))
        # end for
        for event_info in AutoInput.EVENT_LIST:
            event.append(Template(FeatureTemplate.FEATURE_INTERFACE_STRUCTURE).substitute(dict(
                FunctionName=event_info.get_name_lower_underscore(),
                Ext="_event_cls",
            )))
        # end for

        return "".join(request), \
               "".join(response), \
               "" if len(event) == 0 else "\n\n        # Events" + "".join(event)
    # end def get_feature_interface_structure

    @classmethod
    def get_request_structure(cls):
        """
        | Get the request information
        | Example: 0x0007 Device Friendly Name::
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen
        | request::
        |    class SetFriendlyName(DeviceFriendlyName):
        |        <body>
        |    # end class SetFriendlyName

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        for function_info in AutoInput.FUNCTION_LIST:
            for version in AutoInput.get_version_list():
                if not function_info.is_this_version_applicable(version):
                    continue
                # end if
                output.append(cls.get_class_structure(function_info, function_info.request.get_base_class(), "Request",
                                                      FeatureTemplate.CLASS_REQ_STRUCTURE, version))
            # end for
        # end for
        output = CommonFileGenerator.uniquify_list(output)
        return "".join(output)
    # end def get_request_structure

    @classmethod
    def get_response_structure(cls):
        """
        | Get the response information
        | Example: 0x0007 Device Friendly Name::
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen
        | response::
        |    class SetFriendlyNameResponse(DeviceFriendlyName):
        |        <body>
        |    # end class SetFriendlyNameResponse

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        for function_info in AutoInput.FUNCTION_LIST:
            for version in AutoInput.get_version_list():
                if not function_info.is_this_version_applicable(version):
                    continue
                # end if
                output.append(
                    cls.get_class_structure(function_info, function_info.response.get_base_class(), "Response",
                                            FeatureTemplate.CLASS_RES_STRUCTURE, version))
            # end for
        # end for
        output = CommonFileGenerator.uniquify_list(output)
        return "".join(output)
    # end def get_response_structure

    @classmethod
    def get_event_structure(cls):
        """
        | Get the event information
        | Example: 0x0007 Device Friendly Name::
        |    [3] setFriendlyName(byteIndex, nameChunk) -> nameLen
        | response::
        |    class SetFriendlyNameResponse(DeviceFriendlyName):
        |        <body>
        |    # end class SetFriendlyNameResponse

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        for event_info in AutoInput.EVENT_LIST:
            for version in AutoInput.get_version_list():
                if not event_info.is_this_version_applicable(version):
                    continue
                # end if
                output.append(cls.get_class_structure(event_info, event_info.event.get_base_class(), "Event",
                                                      FeatureTemplate.CLASS_RES_STRUCTURE, version))
            # end for
        # end for
        output = CommonFileGenerator.uniquify_list(output)
        return "".join(output)
    # end def get_event_structure

    @classmethod
    def get_short_empty_packet_format(cls):
        """
        | Get ``ShortEmptyPacketDataFormat`` information
        | Example: Generate containers::
        |    class ShortEmptyPacketDataFormat(DeviceFriendlyName):
        |        <Padding 24 body>
        |    # end class ShortEmptyPacketDataFormat

        :return: Formatted output
        :rtype: ``str``
        """
        indent = " " * 4
        container = []
        for function_info in AutoInput.FUNCTION_LIST:
            for version in AutoInput.get_version_list():
                if not function_info.is_this_version_applicable(version):
                    continue
                # end if
                version_text = ""
                if function_info.check_multi_version():
                    version_text = AutoInput.get_version_text(version)
                # end if
                if not function_info.request.check_parameters(version):
                    container.append(f"\n{indent*2}- {function_info.get_name_without_space()}{version_text}")
                # end if
            # end for
        # end for
        container = CommonFileGenerator.uniquify_list(container)
        if len(container) > 0:
            container.sort()
            return Template(FeatureTemplate.EMPTY_PACKET_DATA_FORMAT).substitute(dict(
                EmptyPacketDataFormat="ShortEmptyPacketDataFormat",
                BitCount=cls.REPORT_ID_SHORT_SIZE,
                PaddingSize=hex(cls.REPORT_ID_SHORT_SIZE).upper().replace('0X', '0x'),
                FeatureNameTitleCaseWithoutSpace="".join(AutoInput.HIDPP_FEATURE_NAME.split()),
                Container="".join(container)
            ))
        # end if
        return ""
    # end def get_short_empty_packet_format

    @classmethod
    def get_long_empty_packet_format(cls):
        """
        | Get ``LongEmptyPacketDataFormat`` information
        | Example: Generate container::
        |    class ShortEmptyPacketDataFormat(DeviceFriendlyName):
        |        <Padding 24 body>
        |    # end class ShortEmptyPacketDataFormat

        :return: Formatted output
        :rtype: ``str``
        """
        container = []
        for function_info in AutoInput.FUNCTION_LIST:
            for version in AutoInput.get_version_list():
                if not function_info.is_this_version_applicable(version):
                    continue
                # end if
                version_text = ""
                if function_info.check_multi_version():
                    version_text = AutoInput.get_version_text(version)
                # end if
                if not function_info.response.check_parameters(version):
                    container.append(f"\n        - {function_info.get_name_without_space()}Response{version_text}")
                # end if
            # end for
        # end for
        container = CommonFileGenerator.uniquify_list(container)
        if len(container) > 0:
            container.sort()
            return Template(FeatureTemplate.EMPTY_PACKET_DATA_FORMAT).substitute(dict(
                EmptyPacketDataFormat="LongEmptyPacketDataFormat",
                BitCount=cls.REPORT_ID_LONG_SIZE,
                PaddingSize=hex(cls.REPORT_ID_LONG_SIZE).upper().replace('0X', '0x'),
                FeatureNameTitleCaseWithoutSpace="".join(AutoInput.HIDPP_FEATURE_NAME.split()),
                Container="".join(container)
            ))
        # end if
        return ""
    # end def get_long_empty_packet_format

    @classmethod
    def get_all_common_packet_format(cls):
        """
        | Get the request/response/event information
        | Example: Generate Short/Long/Mixed containers::
        |    class MixedContainer(DeviceFriendlyName):
        |        <body>
        |    # end class MixedContainer

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        dictionary = dict(
            FeatureNameTitleCaseWithoutSpace="".join(AutoInput.HIDPP_FEATURE_NAME.split()),
            HidppFeatureVersion=AutoInput.HIDPP_FEATURE_VERSION
        )
        index = 1
        for key, value in cls.count_common_parameters_key().items():
            if value["Count"] > 1:
                if value.get("Base") is None:
                    # if the user didn't specify the name in the spreadsheet, provide the default one.
                    value["Base"] = f"MixedContainer{index}"
                    cls.update_base_info(value)
                    index += 1
                # end if
                dictionary["Container"] = cls.get_mixed_container_for_info(value)
                output.append(cls.get_mixed_container(value, dictionary))
            # end if
        # end for
        output = CommonFileGenerator.uniquify_list(output)
        return "".join(output)
    # end def get_all_common_packet_format

    @staticmethod
    def update_base_info(dictionary):
        """
        Update the base class information in function info list

        :param dictionary: Dictionary to check
        :type dictionary: ``dict``
        """
        for name in dictionary["FunctionName"]:
            for function_info in AutoInput.FUNCTION_LIST:
                if name == function_info.name:
                    function_info.request.base = dictionary["Base"]
                    break
                elif name == f"{function_info.name} Response":
                    function_info.response.base = dictionary["Base"]
                    break
                # end if
            # end for
            for function_info in AutoInput.EVENT_LIST:
                if name == f"{function_info.name} Event":
                    function_info.event.base = dictionary["Base"]
                    break
                # end if
            # end for
        # end for
    # end def update_base_info

    @classmethod
    def count_common_parameters_key(cls):
        """
        Count the number of times the parameters are generic for all api

        :return: Mixed value types dictionary
        :rtype: ``dict``
        """
        dictionary = dict()
        for function_info in AutoInput.FUNCTION_LIST:
            cls.update_request_value(function_info, dictionary)
            cls.update_response_value(function_info, dictionary)
        # end for
        for event_info in AutoInput.EVENT_LIST:
            cls.update_event_value(event_info, dictionary)
        # end for
        return dictionary
    # end def count_common_parameters_key

    @classmethod
    def update_request_value(cls, function_info, dictionary):
        """
        Update the request values for a single api

        :param function_info: Function information
        :type function_info: ``FunctionInfo``
        :param dictionary: Values dictionary
        :type dictionary: ``dict``
        """
        for version in AutoInput.get_version_list():
            if not function_info.is_this_version_applicable(version):
                continue
            # end if
            if len(function_info.request.parameters) == 0:
                continue
            # end if
            param_data = cls.get_formatted_method_param(function_info.request.parameters, version)
            size_data = cls.get_request_padding_size(function_info.request.parameters, version)
            report_data = cls.get_request_report_id_type(function_info, version)
            key = f"{param_data}, {size_data}, {report_data}"

            version_text = ""
            if function_info.check_multi_version():
                version_text = AutoInput.get_version_text(version)
            # end if
            if key in dictionary:
                text = f"{function_info.name}{version_text}"
                if text not in dictionary[key]["FunctionName"]:
                    dictionary[key]["Count"] += 1
                    dictionary[key]["FunctionName"].append(text)
                # end if
            else:
                dictionary[key] = dict(Count=1,
                                       FunctionIndex=function_info.index,
                                       Category="Request",
                                       FunctionName=[f"{function_info.name}{version_text}"],
                                       Api=function_info)
            # end if

            if function_info.request.base is not None:
                dictionary[key]["Base"] = function_info.request.base
            # end if
        # end for
    # end def update_request_value

    @classmethod
    def update_response_value(cls, function_info, dictionary):
        """
        Update the response values for a single api

        :param function_info: Function information
        :type function_info: ``FunctionInfo``
        :param dictionary: Values dictionary
        :type dictionary: ``dict``
        """
        for version in AutoInput.get_version_list():
            if not function_info.is_this_version_applicable(version):
                continue
            # end if
            if len(function_info.response.parameters) == 0:
                continue
            # end if
            param_data = cls.get_formatted_method_param(function_info.response.parameters, version)
            size_data = cls.get_response_padding_size(function_info.response.parameters, version)
            key = f"{param_data}, {size_data}, {cls.REPORT_ID_LONG_NAME}"
            version_text = ""
            if function_info.check_multi_version():
                version_text = AutoInput.get_version_text(version)
            # end if
            if key in dictionary:
                text = f"{function_info.name}Response{version_text}"
                if text not in dictionary[key]["FunctionName"]:
                    dictionary[key]["Count"] += 1
                    dictionary[key]["FunctionName"].append(text)
                # end if
            else:
                dictionary[key] = dict(Count=1,
                                       FunctionIndex=function_info.index,
                                       Category="Response",
                                       FunctionName=[f"{function_info.name}Response{version_text}"],
                                       Api=function_info)
            # end if

            if function_info.response.base is not None:
                dictionary[key]["Base"] = function_info.response.base
            # end if
        # end for
    # end def update_response_value

    @classmethod
    def update_event_value(cls, event_info, dictionary):
        """
        Update event values for a single api

        :param event_info: Event information
        :type event_info: ``EventInfo``
        :param dictionary: Values dictionary
        :type dictionary: ``dict``
        """
        for version in AutoInput.get_version_list():
            if not event_info.is_this_version_applicable(version):
                continue
            # end if
            if len(event_info.event.parameters) == 0:
                continue
            # end if
            param_data = cls.get_formatted_method_param(event_info.event.parameters, version)
            size_data = cls.get_response_padding_size(event_info.event.parameters, version)
            key = f"{param_data}, {size_data}, {cls.REPORT_ID_LONG_NAME}"
            version_text = ""
            if event_info.check_multi_version():
                version_text = AutoInput.get_version_text(version)
            # end if
            if key in dictionary:
                text = f"{event_info.name}Event{version_text}"
                if text not in dictionary[key]["FunctionName"]:
                    dictionary[key]["Count"] += 1
                    dictionary[key]["FunctionName"].append(text)
                # end if
            else:
                dictionary[key] = dict(Count=1,
                                       FunctionIndex=event_info.index,
                                       Category="Event",
                                       FunctionName=[f"{event_info.name}Event{version_text}"],
                                       Api=event_info)
            # end if

            if event_info.event.base is not None:
                dictionary[key]["Base"] = event_info.event.base
            # end if
        # end for
    # end def update_event_value

    @staticmethod
    def get_mixed_container_for_info(dictionary):
        """
        | Get the mixed container info
        | Example:
        | This class is to be used as a base class for several messages in this feature.::
        |    - xRequest
        |    - yRequest
        |    - zResponse

        :param dictionary: Mixed container details
        :type dictionary: ``dict``

        :return: Formatted output
        :rtype: ``str``
        """
        output = []
        for item in dictionary["FunctionName"]:
            output.append(f"\n        - {''.join(item.split())}")
        # end for
        output = CommonFileGenerator.uniquify_list(output)
        output.sort()
        return "".join(output)
    # end def get_mixed_container_for_info

    @classmethod
    def get_min_value(cls, function_info, version, include_response=True):
        """
        Get minimum initialization value

        :param function_info: Function information
        :type function_info: ``FunctionInfo``
        :param version: Version information
        :type version: ``int``
        :param include_response: Flag indicating if the response parameters are included
        :type include_response: `bool``

        :return: Formatted output
        :rtype: ``str``
        """
        min_value_req = []
        if len(function_info.request.parameters) > 0:
            min_value_req = cls.get_method_param_settings_value(
                parameters=function_info.request.parameters, space=cls.get_new_line_with_space(space_length=8),
                equal_to=ConstantTextManager.EQUAL_TO,
                template=RobustnessTemplate.NAME_VALUE_FORMAT, skip_settings_values=False,
                result=[],
                version=version)

        if not include_response or len(function_info.response.parameters) == 0:
            return "".join(min_value_req)
        # end if

        min_value_res = cls.get_method_param_settings_value(
            parameters=function_info.response.parameters, space=cls.get_new_line_with_space(space_length=8),
            equal_to=ConstantTextManager.EQUAL_TO,
            template=RobustnessTemplate.NAME_VALUE_FORMAT,
            skip_settings_values=True,
            result=min_value_req,
            version=version)

        return "".join(min_value_res)
    # end def get_min_value

    @classmethod
    def get_check_map_and_fields(cls, dictionary, function_info, template, space_length, version,
                                 include_device_feature=False):
        """
        Get check map and fields for validation

        :param dictionary: Input dictionary
        :type dictionary: ``dict``
        :param function_info: Function information
        :type function_info: ``FunctionInfo``
        :param template: Template to use
        :type template: ``str``
        :param space_length: Space length
        :type space_length: ``int``
        :param version: Version information
        :type version: ``int``
        :param include_device_feature: Flag indicating if the device/feature index are included in the check map
        - OPTIONAL
        :type include_device_feature: ``bool``

        :return: Formatted output
        :rtype: ``str``
        """
        name = function_info.get_name_without_space()
        name_lower = function_info.get_name_lower_underscore()
        space = " " * space_length
        test_util = f"{dictionary['FeatureNameTitleCaseWithoutSpace']}TestUtils"
        fid_lower = dictionary['HidppFIDLower']

        check_fields = f"{space}checker.check_fields(self, response, " \
                       f"self.feature_{fid_lower}.{name_lower}_response_cls, check_map)"
        # line wrap
        if len(check_fields) > ConstantTextManager.LINE_WRAP_AT_CHAR:
            check_fields = f"{space}checker.check_fields(\n{space}    self, response, "\
                f"self.feature_{fid_lower}.{name_lower}_response_cls, check_map)"
        # end if

        output = []
        open_brace = "{"
        close_brace = "}"
        if len(function_info.response.parameters) > 0:
            value = cls.get_inner_check_map(test_util=test_util,
                                            function_info=function_info, version=version, space=space)
            if len(value) > 0:
                output.append(value)
                output.append(f"\n{space}")
            # end if
            output.append(f"checker = {test_util}.{name}ResponseChecker")
            output.append(f"\n{space}check_map = checker.get_default_check_map(self)\n")
            value = cls.get_override_check_map(
                function_info=function_info,
                template=template,
                version=version,
                include_device_feature=include_device_feature)
            if len(value) > 0:
                output.append(f"{space}check_map.update({open_brace}")
                output.append(value)
                output.append(f"\n{space}{close_brace})\n")
            # end if
            output.append(check_fields)
        else:
            value = cls.get_override_check_map(
                    function_info=function_info,
                    template=template,
                    version=version,
                    include_device_feature=include_device_feature)
            if len(value) > 0:
                output.append(f"checker = {test_util}.MessageChecker")
                output.append(f"\n{space}check_map = {open_brace}")
                output.append(value)
                output.append(f"\n{space}{close_brace}\n")
                output.append(check_fields)
            else:
                output.append(f"{test_util}.MessageChecker.check_fields(\n{space}    self, response, self.feature_"
                              f"{fid_lower}.{name_lower}_response_cls, {open_brace}{close_brace})")
            # end if
        # end if
        return "".join(output)
    # end def get_check_map_and_fields

    @classmethod
    def get_test_case_item(cls, test_case_info, level):
        """
        Get test case item format

        :param test_case_info: TestCaseInfo
        :type test_case_info: ``TestCaseInfo``
        :param level: Feature level of the test case
        :type level: ``str``

        :return: Formatted output of the test case
        :rtype: ``str``
        """
        return Template(ErrorHandlingTemplate.SINGLE_TEST_CASE_ITEM).substitute(dict(
            FeatureId=cls.get_feature_list(test_case_info),
            Level=level,
            Identifier=test_case_info.identifier.replace("\n", ", "),
            Name=test_case_info.name,
            Synopsis=cls.get_synopsis(test_case_info),
            LogTypeAndText=cls.get_description(test_case_info)
        ))
    # end def get_test_case_item

    @classmethod
    def get_feature_list(cls, test_case_info):
        """
        Get the list of features used in the test case

        Example:
            @features("Feature0005")
            @features("Feature0007")

        :param test_case_info: TestCaseInfo of Interface/Business/Functionality/Robustness/ErrorHandling/Security
        :type test_case_info: ``TestCaseInfo``

        :return: Formatted output of features
        :rtype: ``str``
        """
        feature_list = []
        for line in test_case_info.description.split("\n"):
            first_match = re.search(pattern="feature 0x\w+ ", string=line)
            if first_match:
                feature_list.append(f'@features("Feature{first_match.group()[-5:-1].upper()}")')
            # end if
        # end for

        for line in test_case_info.synopsis.split("\n"):
            if not line.startswith("Require "):
                continue
            # end if
            for value in line.replace("Require ", "").split(", "):
                # Ex: Require 0x2201, Mouse
                if value.lower().startswith("0x") and len(value) == 6:
                    text = value.upper().replace("0X", "")
                    feature_list.append(f'@features("Feature{text}")')
                # Ex: Require PowerSupply
                elif value.lower() in ["powersupply", "power supply"]:
                    feature_list.append('@services("PowerSupply")')
                # Ex: Require 0x8071, LED analyzer/spy
                # Ex: Require button emulator
                elif value.lower() not in ["button emulator", "mouse", "led analyzer/spy"]:
                    sys.stdout.write(f"\nTODO: Yet to handle this requirement: {value}")
                # end if
            # end for
        # end for

        feature_list.sort()
        # always place the current feature in the top place
        feature_list.insert(0, f'@features("Feature{AutoInput.HIDPP_FEATURE_ID.upper()}")')
        feature_list = CommonFileGenerator.uniquify_list(feature_list)
        return "\n    ".join(feature_list)
    # end def get_feature_list

    @classmethod
    def get_description(cls, test_case_info):
        """
        Get test case descriptions one by one

        Example:
            LogHelper.log_prerequisite(self, 'text')
            LogHelper.log_step(self, 'text')
            LogHelper.log_check(self, 'text')
            LogHelper.log_info(self, 'text')
            LogHelper.log_post_requisite(self, 'text')

        :param test_case_info: TestCaseInfo of Interface/Business/Functionality/Robustness/ErrorHandling/Security
        :type test_case_info: ``TestCaseInfo``

        :return: Formatted output of description
        :rtype: ``str``
        """
        description = []
        hyphen = "-"
        space = " "
        indentation = 8
        tab_size = 4
        hyphen_size = 120 - indentation - len("# ")
        for line in test_case_info.description.split("\n"):
            if cls.get_ignore_state(line):
                continue
            # end if
            space_len = len(f"{space * indentation}LogHelper.log_(self, ")
            log_text, log_type = cls.get_log_type_and_text(line, space_len)
            # skip empty text line
            if log_text == '""':
                continue
            elif log_text == '"TODO: Check the test case document and fill the description"':
                description.append(f"\n\n{space * indentation}# {log_text[1:-1]}\n")
                continue
            # end if

            if log_type == "info" and log_text.lower().startswith('"end test loop'):
                indentation -= tab_size
                hyphen_size += tab_size
                description.append(f"{space * indentation}# end for")
            # end if

            description.append(f"\n{space * indentation}# {hyphen * hyphen_size}")
            description.append(f"\n{space * indentation}LogHelper.log_{log_type}(self, {log_text})")
            description.append(f"\n{space * indentation}# {hyphen * hyphen_size}\n")

            if log_text == ' "Restart device"':
                description.append(f"{space * indentation}self.reset(hardware_reset=True)\n")
            # end if

            if log_type == "info" and log_text.lower().startswith('"test loop'):
                description.append(f"{space * indentation}for _ in []:  # TODO: fill this condition")
                indentation += tab_size
                hyphen_size -= tab_size
            # end if
        # end for

        return "".join(description)
    # end def get_description

    @classmethod
    def get_synopsis(cls, test_case_info):
        """
        Get synopsis information

        :param test_case_info: TestCaseInfo of Interface/Business/Functionality/Robustness/ErrorHandling/Security
        :type test_case_info: ``TestCaseInfo``

        :return: Formatted output of synopsis
        :rtype: ``str``
        """
        new_lines = []
        space = " " * 8
        wrap_length = ConstantTextManager.LINE_WRAP_AT_CHAR - len(space) - 3
        for line in test_case_info.synopsis.split("\n"):
            if len(line) < wrap_length:
                new_lines.append(f"\n{space}{line}" if len(line) > 0 else "\n")
            else:
                modified_line = cls.get_wrapped_text(content=line, space=space, delimiter=" ", wrap_length=wrap_length)
                new_lines.append(f"\n{space}{modified_line}")
            # end if
        # end for
        return "".join(new_lines)
    # end def get_synopsis

    @classmethod
    def get_log_type_and_text(cls, line, space_len):
        """
        Get log type and text information from the given description

        :param line: The description text
        :type line: ``str``
        :param space_len: The space length before text
        :type space_len: ``int``

        :return: Log type and text
        :rtype: ``tuple[str, str]``
        """
        log_type = "info"
        log_text = line.strip()
        for item in [("prerequisite", "Pre-[Rr]equisite#[0-9]+:"), ("prerequisite", "Pre-[Rr]equisite:"),
                     ("step", "Test [Ss]tep [0-9]+:"), ("step", "Test [Ss]tep:"),
                     ("check", "Test [Cc]heck [0-9]+:"), ("check", "Test [Cc]heck:"),
                     ("post_requisite", "Post-[Rr]equisite#[0-9]+:"), ("post_requisite", "Post-[Rr]equisite:")]:
            first_match = re.search(pattern=item[1], string=line)
            if first_match:
                log_type = item[0]
                log_text = line[first_match.end():].strip()
                break
            # end if
        # end for

        space = " " * (space_len + len(log_type))
        wrap_length = ConstantTextManager.LINE_WRAP_AT_CHAR - len(space) - len('" ")')
        if len(log_text) <= wrap_length:
            return f'"{log_text}"', log_type
        # end if

        # Wrap the line
        log_text = cls.get_wrapped_text(
            content=log_text, delimiter=" ", space=space, wrap_length=wrap_length, decorator="\"")

        return log_text, log_type
    # end def get_log_type_and_text

    @classmethod
    def get_ignore_state(cls, line):
        """
        Get whether this line can be ignored by finding few pattern text

        Example lines:
            Pre-requisite#1: Backup NVS
            Pre-requisite#2: Enable Hidden Feature
            Pre-requisite#3: Get feature 0x0007 index
            Post-requisite#1: Restore NVS

        :param line: The log description text
        :type line: ``str``

        :return: Flag indicating if this line is ignored
        :rtype: ``bool``
        """
        # Ignore few pre-requisites & post-requisites
        for pattern in [("Pre-requisite", "Backup NVS"),
                        ("Post-requisite", "Restore NVS"),
                        ("Post-requisite", "Reload NVS"),
                        ("Pre-requisite", "Backup [Ii]nitial NVS"),
                        ("Post-requisite", "Reload [Ii]nitial NVS"),
                        ("Pre-requisite", "Enable [Hh]idden [Ff]eature"),
                        ("Post-requisite", "Disable [Hh]idden [Ff]eature"),
                        ("Pre-requisite", "Enable [Mm]anufacturing [Ff]eature"),
                        ("Pre-requisite", "Activate [Ff]eature"),
                        ("Pre-requisite", f"Get [Ff]eature 0x{AutoInput.HIDPP_FEATURE_ID.upper()}"),
                        ("Pre-requisite", f"GetFeature\(0x{AutoInput.HIDPP_FEATURE_ID.upper()}\)")
                        ]:
            first_match = re.search(pattern=pattern[0], string=line)
            if first_match:
                second_match = re.search(pattern=pattern[1], string=line)
                if second_match:
                    return True
                # end if
            # end if
        # end for
        return False
    # end def get_ignore_state
# end class ReqResGenerator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
