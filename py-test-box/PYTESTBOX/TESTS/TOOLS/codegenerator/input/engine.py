#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.input.engine
:brief: Input engine
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/07/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
ALL_VERSIONS = "all versions"
EMPTY = ""
SINCE_VERSION = "since v"
UPTO_VERSION = "up to v"
VERSION_ONLY = " only"
VERSION_V = "v"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TestCaseInfo(object):
    """
    Define test case information
    """
    def __init__(self, identifier, name, synopsis, description):
        """
        :param identifier: Test case identifier
        :type identifier: ``str``
        :param name: Test case name
        :type name: ``str``
        :param synopsis: Test case synopsis
        :type synopsis: ``str``
        :param description: Test case description
        :type description: ``str``
        """
        self.identifier = identifier
        self.name = name
        self.synopsis = synopsis
        self.description = description
    # end def __init__
# end class TestCaseInfo


class CommonName(object):
    """
    Define common name information
    """
    def __init__(self, name):
        """
        :param name: Name
        :type name: ``str``
        """
        self.name = name
    # end def __init__

    def get_name(self, replace_bit_map=False):
        """
        Get name

        :param replace_bit_map: Flag indicating if text is altered - OPTIONAL
        :type replace_bit_map: ``bool``

        :return: Formatted name
        :rtype: ``str``
        """
        value = self.name
        if replace_bit_map:
            value = value.replace("Mask Bit Map", EMPTY).replace(" Bit Map", EMPTY)
        # end if
        return value
    # end def get_name

    def get_name_lower_underscore(self, replace_bit_map=False):
        """
        Get name with underscore in lower case

        :param replace_bit_map: Flag indicating if text is altered - OPTIONAL
        :type replace_bit_map: ``bool``

        :return: Formatted name
        :rtype: ``str``
        """
        value = "_".join(self.name.lower().split())
        if replace_bit_map:
            value = value.replace("_mask_bit_map", EMPTY).replace("_bit_map", EMPTY)
        # end if
        return value
    # end def get_name_lower_underscore

    def get_name_upper_underscore(self, replace_bit_map=False):
        """
        Get name with underscore in upper case

        :param replace_bit_map: Flag indicating if text is altered - OPTIONAL
        :type replace_bit_map: ``bool``

        :return: Formatted name
        :rtype: ``str``
        """
        value = "_".join(self.name.upper().split())
        if replace_bit_map:
            value = value.replace("_MASK_BIT_MAP", EMPTY).replace("_BIT_MAP", EMPTY)
        # end if
        return value
    # end def get_name_upper_underscore

    def get_name_without_space(self, replace_bit_map=False):
        """
        Get name without space

        :param replace_bit_map: Flag indicating if text is altered - OPTIONAL
        :type replace_bit_map: ``bool``

        :return: Formatted name
        :rtype: ``str``
        """
        value = "".join(self.name.split())
        if replace_bit_map:
            value = value.replace("MaskBitMap", EMPTY).replace("BitMap", EMPTY)
        # end if
        return value
    # end def get_name_without_space

    def get_name_title(self, replace_bit_map=False):
        """
        | Get name title in capitalized text
        | Example 1: eQuad Id => EquadId
        | Example 2: BLE HD => BleHd

        :param replace_bit_map: Flag indicating if text is altered - OPTIONAL
        :type replace_bit_map: ``bool``

        :return: Formatted output
        :rtype: ``str``
        """
        value = ""
        for title in self.name.split():
            value += title.capitalize()
        # end for
        if replace_bit_map:
            value = value.replace("MaskBitMap", EMPTY).replace("BitMap", EMPTY)
        # end if
        return value
    # end def get_name_title
# end class CommonName


class CommonParameter(CommonName):
    """
    Define common class for parameter information
    """
    def __init__(self, index, size, data_type, name, comment, settings_data_type, settings_default_value, prefix,
                 exclusion, default_value, version_info):
        """
        :param index: Index
        :type index: ``int``
        :param size: Size (in bits)
        :type size: ``int``
        :param data_type: Data type
        :type data_type: ``str``
        :param name: Name
        :type name: ``str``
        :param comment: Documentation comment
        :type comment: ``str | None``
        :param settings_data_type: Settings.ini field data type
        :type settings_data_type: ``str | None``
        :param settings_default_value: Settings default value
        :type settings_default_value: ``int | tuple | str | bool | None``
        :param prefix: Prefix
        :type prefix: ``str | None``
        :param exclusion: Flag to exclude the parameter
        :type exclusion: ``bool``
        :param default_value: Default value
        :type default_value: ``bool | str | int | None``
        :param version_info: Version
        :type version_info: ``str``
        """
        super().__init__(name)
        self.index = index
        self.size = size
        self.data_type = data_type
        self.comment = comment
        self.settings_data_type = settings_data_type
        self.settings_default_value = settings_default_value
        self.prefix = prefix
        self.exclusion = exclusion
        self.default_value = default_value
        self.version_info = version_info
    # end def __init__

    def get_field_data_type(self):
        """
        Get field data type

        :return: Field data type
        :rtype: ``str``
        """
        field_data_type = f"``{self.data_type} | HexList``"
        if self.data_type == "HexList":
            field_data_type = "``HexList``"
        elif self.data_type == "Reserved":
            field_data_type = "``int | HexList``"
        # end if
        return field_data_type
    # end def get_field_data_type

    def has_sub_parameters(self):
        """
        Find this parameter class has sub parameters

        :return: Flag indicating if sub parameters are present
        :rtype: ``bool``
        """
        sub_parameters = hasattr(self, "sub_parameters")
        if sub_parameters:
            values = getattr(self, "sub_parameters")
            return values and len(values) > 0
        # end if
        return False
    # end def has_sub_parameters

    def is_given_version_present(self, version):
        """
        Check the given version number is present

        :param version: Version
        :type version: ``int``

        :return: Flag indicating if the given version is present
        :rtype: ``bool``
        """
        if version is None:
            return True
        # end if

        # Ex: all versions
        if self.version_info == ALL_VERSIONS:
            return True
        # if

        # Ex: since v2
        if self.version_info.startswith(SINCE_VERSION)\
                and version >= int(self.version_info.replace(SINCE_VERSION, EMPTY)):
            return True
        # end if

        # Ex: v2 only
        if self.version_info.endswith(VERSION_ONLY)\
                and version == int(self.version_info.replace(VERSION_ONLY, EMPTY).replace(VERSION_V, EMPTY)):
            return True
        # end if

        # Ex: up to v2
        if self.version_info.startswith(UPTO_VERSION)\
                and version <= int(self.version_info.replace(UPTO_VERSION, EMPTY)):
            return True
        # end if

        return False
    # end def is_given_version_present

    def check_settings_data_type(self, version, data_types):
        """
        Find the given field presence for the given version

        :param version: Version information
        :type version: ``int``
        :param data_types: Data type to check
        :type data_types: ``list[str]``

        :return: Flag indicating if the reserved field is present
        :rtype: ``bool``
        """
        return self.is_given_version_present(version) and self.settings_data_type in data_types
    # end def check_settings_data_type

    def check_data_type(self, version, data_types):
        """
        Find the given field presence for the given version

        :param version: Version information
        :type version: ``int``
        :param data_types: Data type to check
        :type data_types: ``list[str]``

        :return: Flag indicating if the reserved field is present
        :rtype: ``bool``
        """
        return self.is_given_version_present(version) and self.data_type in data_types
    # end def check_data_type
# end class CommonParameter


class SubParameter(CommonParameter):
    """
    Define subclass request/response/event parameter format
    """
    def get_size(self, version):
        """
        Get the size of the parameter for the given version

        :return: 0 (if version is not supported) or size (if version is supported)
        :rtype: ``int``
        """
        if self.is_given_version_present(version):
            return int(self.size)
        # end if
        return 0
    # end def get_size

    def is_given_version_present(self, version):
        """
        Check the given version number is present

        :param version: Version
        :type version: ``int``

        :return: Flag indicating if the given version is present
        :rtype: ``bool``

        :raise ``ValueError``: The version_info is mandatory
        """
        if self.version_info is None:
            raise ValueError(f"Version information field is mandatory for sub parameter ({self.name})")
        # end if
        return super().is_given_version_present(version)
    # end def is_given_version_present

    def check_since_version(self, version):
        """
        Check if since version available

        :param version: Version information
        :type version: ``int``

        :return: Flag indicating if since version is applicable
        :rtype: ``bool``
        """
        # Ex: since v2
        if self.version_info.startswith(SINCE_VERSION) \
                and version == int(self.version_info.replace(SINCE_VERSION, EMPTY)):
            return True
        # end if

        return False
    # end def check_since_version

    def check_bigger_than_upto_version(self, version):
        """
        Check if bigger than upto version

        :param version: Version information
        :type version: ``int``

        :return: Flag indicating if upto version is smaller
        :rtype: ``bool``
        """
        # Ex: upto v2
        if self.version_info and self.version_info.startswith(UPTO_VERSION) \
                and version > int(self.version_info.replace(UPTO_VERSION, EMPTY)):
            return True
        # end if

        return False
    # end def check_bigger_than_upto_version

    def check_bigger_than_only_version(self, version):
        """
        Check if bigger than only version

        :param version: Version information
        :type version: ``int``

        :return: Flag indicating if only version is smaller
        :rtype: ``bool``
        """
        # Ex: v2 only
        if self.version_info and self.version_info.endswith(VERSION_ONLY) \
                and version > int(self.version_info.replace(VERSION_ONLY, EMPTY).replace(VERSION_V, EMPTY)):
            return True
        # end if

        return False
    # end def check_bigger_than_only_version

    def check_multi_version(self):
        """
        Check if multi version available

        :return: Flag indicating if multi version is applicable
        :rtype: ``bool``
        """
        return self.version_info != ALL_VERSIONS
    # end def check_multi_version
# end class SubParameter


class Parameter(CommonParameter):
    """
    Define request/response/event parameter format
    """
    def __init__(self, index, size, data_type, name, comment, settings_data_type, settings_default_value, prefix,
                 exclusion, default_value, sub_parameters, version_info):
        """
        :param index: Index
        :type index: ``int``
        :param size: Size (in bits)
        :type size: ``int``
        :param data_type: Data type
        :type data_type: ``str``
        :param name: Name
        :type name: ``str``
        :param comment: Documentation comment
        :type comment: ``str | None``
        :param settings_data_type: Settings.ini field data type
        :type settings_data_type: ``str | None``
        :param settings_default_value: Settings default value
        :type settings_default_value: ``int | None``
        :param prefix: Prefix
        :type prefix: ``str | None``
        :param exclusion: Flag to exclude the parameter
        :type exclusion: ``bool``
        :param default_value: Default value
        :type default_value: ``int | None``
        :param sub_parameters: Subclass parameters - OPTIONAL
        :type sub_parameters: ``list[SubParameter] | None``
        :param version_info: Version
        :type version_info: ``str``
        """
        super().__init__(index, size, data_type, name, comment, settings_data_type, settings_default_value, prefix,
                         exclusion, default_value, version_info)
        self.sub_parameters = sub_parameters
    # end def __init__

    def is_given_version_present(self, version):
        """
        Check the given version number is present

        :param version: Version
        :type version: ``int``

        :return: Flag indicating if the given version is present
        :rtype: ``bool``
        """
        if self.version_info is None:
            valid_version = False
            for sub_parameter in self.sub_parameters:
                valid_version = sub_parameter.is_given_version_present(version)
                if valid_version:
                    break
                # end if
            # end for
            return valid_version
        # end if
        return super().is_given_version_present(version)
    # end def is_given_version_present

    def get_size(self, version):
        """
        Get the size of the parameter for the given version

        :return: size or 0 (if version is not supported)
        :rtype: ``int``

        :raise ``ValueError``: The size is mandatory
        """
        if self.has_sub_parameters():
            size = 0
            for sub_parameter in self.sub_parameters:
                size += sub_parameter.get_size(version)
            # end for
            return size
        # end if

        if self.is_given_version_present(version):
            return int(self.size)
        # end if

        return 0
    # end def get_size

    def get_name_col_size(self, max_size):
        """
        Get name column size

        :param max_size: Maximum default size
        :type max_size: ``int``

        :return: Column max size
        :rtype: ``int``
        """
        for sub_parameter in self.sub_parameters:
            if len(sub_parameter.name) > max_size:
                # increase the column size to field name size
                max_size = len(sub_parameter.name)
            # end if
        # end for
        return max_size
    # end def get_name_col_size

    def check_since_version(self, version):
        """
        Check if since version available

        :param version: Version information
        :type version: ``int``

        :return: Flag indicating if since version is applicable
        :rtype: ``bool``
        """
        if self.sub_parameters and len(self.sub_parameters) > 0:
            for sub_parameter in self.sub_parameters:
                if sub_parameter.check_since_version(version):
                    return True
                # end if
            # end for
        # end if

        # Ex: since v2
        if self.version_info and self.version_info.startswith(SINCE_VERSION) \
                and version == int(self.version_info.replace(SINCE_VERSION, EMPTY)):
            return True
        # end if

        return False
    # end def check_since_version

    def check_bigger_than_upto_version(self, version):
        """
        Check if bigger than upto version

        :param version: Version information
        :type version: ``int``

        :return: Flag indicating if upto version is smaller
        :rtype: ``bool``
        """
        if self.sub_parameters and len(self.sub_parameters) > 0:
            for sub_parameter in self.sub_parameters:
                if sub_parameter.check_bigger_than_upto_version(version):
                    return True
                # end if
            # end for
        # end if

        # Ex: upto v2
        if self.version_info and self.version_info.startswith(UPTO_VERSION) \
                and version > int(self.version_info.replace(UPTO_VERSION, EMPTY)):
            return True
        # end if

        return False
    # end def check_bigger_than_upto_version

    def check_bigger_than_only_version(self, version):
        """
        Check if bigger than only version

        :param version: Version information
        :type version: ``int``

        :return: Flag indicating if only version is smaller
        :rtype: ``bool``
        """
        if self.sub_parameters and len(self.sub_parameters) > 0:
            for sub_parameter in self.sub_parameters:
                if sub_parameter.check_bigger_than_only_version(version):
                    return True
                # end if
            # end for
        # end if

        # Ex: v2 only
        if self.version_info and self.version_info.endswith(VERSION_ONLY) \
                and version > int(self.version_info.replace(VERSION_ONLY, EMPTY).replace(VERSION_V, EMPTY)):
            return True
        # end if

        return False
    # end def check_bigger_than_only_version

    def check_multi_version(self):
        """
        Check if multi version available

        :return: Flag indicating if multi version is applicable
        :rtype: ``bool``
        """
        if self.sub_parameters and len(self.sub_parameters) > 0:
            version_info = []
            for sub_parameter in self.sub_parameters:
                if sub_parameter.version_info not in version_info:
                    version_info.append(sub_parameter.version_info)
                # end if
            # end for
            return len(version_info) > 1
        # end if

        return self.version_info != ALL_VERSIONS
    # end def check_multi_version

    def get_name_lower_underscore_with_prefix(self, replace_bit_map=False):
        """
        Get name with underscore in lower case including prefix

        :param replace_bit_map: Flag indicating if text is altered - OPTIONAL
        :type replace_bit_map: ``bool``

        :return: Formatted name
        :rtype: ``str``
        """
        if self.sub_parameters and len(self.sub_parameters) > 0 and self.sub_parameters[0].prefix:
            value = f"{self.sub_parameters[0].prefix.lower()}_{self.get_name_lower_underscore()}"
        elif self.prefix:
            value = f"{self.prefix.lower()}_{self.get_name_lower_underscore()}"
        else:
            value = self.get_name_lower_underscore()
        # end if
        if replace_bit_map:
            value = value.replace("_mask_bit_map", EMPTY).replace("_bit_map", EMPTY)
        # end if
        return value
    # end def get_name_lower_underscore_with_prefix

    def get_version_text(self, version):
        """
        Get version text information

        :param version: Version information
        :type version: ``int``

        :return: Version text
        :rtype: ``str``
        """
        if self.check_multi_version():
            return f"V{version}"
        # end if
        return ""
    # end def get_version_text
# end class Parameter


class RequestResponseEvent(object):
    """
    Define request/response/event format for the given api
    """
    def __init__(self, base=None, parameters=None):
        """
        :param base: Name of the base class
        :type base: ``str``
        :param parameters: Parameter information
        :type parameters: ``list[Parameter]``
        """
        self.base = base
        self.parameters = parameters
    # end def __init__

    def is_this_version_applicable(self, version):
        """
        Check the given version is found in the parameters

        :param version: Version
        :type version: ``int``

        :return: Flag indicating if the given version is present
        :rtype: ``bool``
        """
        for parameter in self.parameters:
            valid_version = parameter.is_given_version_present(version)
            if valid_version:
                return True
            # end if
        # end for
        return False
    # end def is_this_version_applicable

    def get_name_col_size(self, max_size):
        """
        Get name column size

        :param max_size: Maximum default size
        :type max_size: ``int``

        :return: Column max size
        :rtype: ``int``
        """
        for parameter in self.parameters:
            name = parameter.name.replace(" Mask Bit Map", EMPTY).replace(" Bit Map", EMPTY)
            if len(name) > max_size:
                # increase the default size to maximum size
                max_size = len(name)
            # end if
        # end for
        return max_size
    # end def get_name_col_size

    def check_settings_data_type(self, version, data_types):
        """
        Check the settings data type presence for the given version

        :param version: Version information
        :type version: ``int``
        :param data_types: Data types to check
        :type data_types: ``list[str]``

        :return: Flag indicating if at least one expected data type is present
        :rtype: ``bool``
        """
        for parameter in self.parameters:
            if parameter.check_settings_data_type(version, data_types):
                return True
            # end if
        # end if
        return False
    # end def check_settings_data_type

    def check_data_type(self, version, data_types):
        """
        Check the data type presence for the given version

        :param version: Version information
        :type version: ``int``
        :param data_types: Data types to check
        :type data_types: ``list[str]``

        :return: Flag indicating if at least one expected data type is present
        :rtype: ``bool``
        """
        for parameter in self.parameters:
            if parameter.check_data_type(version, data_types):
                return True
            # end if
        # end if
        return False
    # end def check_data_type

    def check_parameters(self, version):
        """
        Check parameters present for the given version

        :param version: Version information
        :type version: ``int``

        :return: Flag indicating if at least one parameter is present
        :rtype: ``bool``
        """
        for parameter in self.parameters:
            if parameter.is_given_version_present(version):
                return True
            # end if
        # end for
        return False
    # end def check_parameters

    def check_since_version(self, version):
        """
        Check if since version available

        :param version: Version information
        :type version: ``int``

        :return: Flag indicating if since version is applicable
        :rtype: ``bool``
        """
        for parameter in self.parameters:
            if parameter.check_since_version(version):
                return True
            # end if
        # end for
        return False
    # end def check_since_version

    def check_bigger_than_upto_version(self, version):
        """
        Check if bigger than upto version

        :param version: Version information
        :type version: ``int``

        :return: Flag indicating if upto version is smaller
        :rtype: ``bool``
        """
        for parameter in self.parameters:
            if parameter.check_bigger_than_upto_version(version):
                return True
            # end if
        # end for
        return False
    # end def check_bigger_than_upto_version

    def check_bigger_than_only_version(self, version):
        """
        Check if bigger than only version

        :param version: Version information
        :type version: ``int``

        :return: Flag indicating if only version is smaller
        :rtype: ``bool``
        """
        for parameter in self.parameters:
            if parameter.check_bigger_than_only_version(version):
                return True
            # end if
        # end for
        return False
    # end def check_bigger_than_only_version

    def check_multi_version(self):
        """
        Check if multi version available

        :return: Flag indicating if multi version is applicable
        :rtype: ``bool``
        """
        for parameter in self.parameters:
            if parameter.check_multi_version():
                return True
            # end if
        # end for
        return False
    # end def check_multi_version
# end class RequestResponseEvent


class Request(RequestResponseEvent):
    """
    Define request format for the given api
    """
    def get_base_class(self):
        """
        Get base class information

        :return: Base class information
        :rtype: ``str``
        """
        base_class = "FeatureNameTitleCaseWithoutSpace"
        if len(self.parameters) == 0:
            base_class = "ShortEmptyPacketDataFormat"
        elif self.base is not None:
            base_class = self.base
        # end if
        return base_class
    # end def get_base_class
# end class


class Response(RequestResponseEvent):
    """
    Define response format for the given api
    """
    def get_base_class(self):
        """
        Get base class information

        :return: Base class information
        :rtype: ``str``
        """
        base_class = "FeatureNameTitleCaseWithoutSpace"
        if len(self.parameters) == 0:
            base_class = "LongEmptyPacketDataFormat"
        elif self.base is not None:
            base_class = self.base
        # end if
        return base_class
    # end def get_base_class
# end class


class Event(RequestResponseEvent):
    """
    Define event format for the given api
    """
    def get_base_class(self):
        """
        Get base class information

        :return: Base class information
        :rtype: ``str``
        """
        base_class = "FeatureNameTitleCaseWithoutSpace"
        if len(self.parameters) == 0:
            base_class = "LongEmptyPacketDataFormat"
        elif self.base is not None:
            base_class = self.base
        # end if
        return base_class
    # end def get_base_class
# end class


class FunctionInfo(CommonName):
    """
    Define function information for the given api
    """
    def __init__(self, index, name, request, response, nvs_backup_required, version_info):
        """
        :param index: Index
        :type index: ``int``
        :param name: Name
        :type name: ``str``
        :param request: Request
        :type request: ``Request``
        :param response: Response
        :type response: ``Response``
        :param nvs_backup_required: Flag indicating if NVS backup is required
        :type nvs_backup_required: ``bool``
        :param version_info: Version
        :type version_info: ``str``
        """
        super().__init__(name)
        self.index = index
        self.request = request
        self.response = response
        self.nvs_backup_required = nvs_backup_required
        self.version_info = version_info
    # end def __init__

    def is_this_version_applicable(self, version):
        """
        Check the given version is found in the parameters

        :param version: Version
        :type version: ``int``

        :return: Flag indicating if the given version is present
        :rtype: ``bool``
        """
        if self.version_info is None:
            return self.request.is_this_version_applicable(version) or self.response.is_this_version_applicable(version)
        # end if

        # Ex: all versions
        if self.version_info == ALL_VERSIONS:
            return True
        # if

        # Ex: since v2
        if self.version_info.startswith(SINCE_VERSION)\
                and version >= int(self.version_info.replace(SINCE_VERSION, EMPTY)):
            return True
        # end if

        # Ex: v2 only
        if self.version_info.endswith(VERSION_ONLY)\
                and version == int(self.version_info.replace(VERSION_ONLY, EMPTY).replace(VERSION_V, EMPTY)):
            return True
        # end if

        # Ex: up to v2
        if self.version_info.startswith(UPTO_VERSION)\
                and version <= int(self.version_info.replace(UPTO_VERSION, EMPTY)):
            return True
        # end if

        return False
    # end def is_this_version_applicable

    def check_since_version(self, version):
        """
        Check if since version available

        :param version: Version information
        :type version: ``int``

        :return: Flag indicating if since version is applicable
        :rtype: ``bool``
        """
        if self.version_info is not None:
            # Ex: since v2
            if self.version_info.startswith(SINCE_VERSION) \
                    and version == int(self.version_info.replace(SINCE_VERSION, EMPTY)):
                return True
            # end if
        # end if
        return self.request.check_since_version(version) or self.response.check_since_version(version)
    # end def check_since_version

    def check_bigger_than_upto_version(self, version):
        """
        Check if bigger than upto version

        :param version: Version information
        :type version: ``int``

        :return: Flag indicating if upto version is smaller
        :rtype: ``bool``
        """
        if self.version_info is not None:
            # Ex: upto v2
            if self.version_info.startswith(UPTO_VERSION) \
                    and version > int(self.version_info.replace(UPTO_VERSION, EMPTY)):
                return True
            # end if
        # end if
        return self.request.check_bigger_than_upto_version(version) or self.response.check_bigger_than_upto_version(
            version)
    # end def check_bigger_than_upto_version

    def check_bigger_than_only_version(self, version):
        """
        Check if bigger than only version

        :param version: Version information
        :type version: ``int``

        :return: Flag indicating if only version is smaller
        :rtype: ``bool``
        """
        if self.version_info is not None:
            # Ex: v2 only
            if self.version_info.endswith(VERSION_ONLY) \
                    and version > int(self.version_info.replace(VERSION_ONLY, EMPTY).replace(VERSION_V, EMPTY)):
                return True
            # end if
        # end if
        return self.request.check_bigger_than_only_version(version) or self.response.check_bigger_than_only_version(
            version)
    # end def check_bigger_than_only_version

    def check_multi_version(self):
        """
        Check if multi version available

        :return: Flag indicating if multi version is applicable
        :rtype: ``bool``
        """
        if self.version_info is not None:
            return self.version_info != ALL_VERSIONS
        # end if
        return self.request.check_multi_version() or self.response.check_multi_version()
    # end def check_multi_version

    def check_data_type(self, version, data_types):
        """
        Check the data type presence for the given version

        :param version: Version information
        :type version: ``int``
        :param data_types: Data types to check
        :type data_types: ``list[str]``

        :return: Flag indicating if at least one expected data type is present
        :rtype: ``bool``
        """
        return self.request.check_data_type(version, data_types) or self.response.check_data_type(version, data_types)
    # end def check_data_type
# end class FunctionInfo


class EventInfo(CommonName):
    """
    Define event information for the given api
    """
    def __init__(self, index, name, event, nvs_backup_required, version_info):
        """
        :param index: Index
        :type index: ``int``
        :param name: Name
        :type name: ``str``
        :param event: Event
        :type event: ``Event``
        :param nvs_backup_required: Flag indicating if NVS backup is required
        :type nvs_backup_required: ``bool``
        :param version_info: Version
        :type version_info: ``str``
        """
        super().__init__(name)
        self.index = index
        self.event = event
        self.nvs_backup_required = nvs_backup_required
        self.version_info = version_info
    # end def __init__

    def is_this_version_applicable(self, version):
        """
        Check the given version is found in the parameters

        :param version: Version
        :type version: ``int``

        :return: Flag indicating if the given version is present
        :rtype: ``bool``
        """
        if self.version_info is None:
            return self.event.is_this_version_applicable(version)
        # end if

        # Ex: all versions
        if self.version_info == ALL_VERSIONS:
            return True
        # if

        # Ex: since v2
        if self.version_info.startswith(SINCE_VERSION) \
                and version >= int(self.version_info.replace(SINCE_VERSION, EMPTY)):
            return True
        # end if

        # Ex: v2 only
        if self.version_info.endswith(VERSION_ONLY) \
                and version == int(self.version_info.replace(VERSION_ONLY, EMPTY).replace(VERSION_V, EMPTY)):
            return True
        # end if

        # Ex: up to v2
        if self.version_info.startswith(UPTO_VERSION) \
                and version <= int(self.version_info.replace(UPTO_VERSION, EMPTY)):
            return True
        # end if

        return False
    # end def is_this_version_applicable

    def check_since_version(self, version):
        """
        Check if since version available

        :param version: Version information
        :type version: ``int``

        :return: Flag indicating if since version is applicable
        :rtype: ``bool``
        """
        return self.event.check_since_version(version)
    # end def check_since_version

    def check_bigger_than_upto_version(self, version):
        """
        Check if bigger than upto version

        :param version: Version information
        :type version: ``int``

        :return: Flag indicating if upto version is smaller
        :rtype: ``bool``
        """
        return self.event.check_bigger_than_upto_version(version)
    # end def check_bigger_than_upto_version

    def check_bigger_than_only_version(self, version):
        """
        Check if bigger than only version

        :param version: Version information
        :type version: ``int``

        :return: Flag indicating if only version is smaller
        :rtype: ``bool``
        """
        return self.event.check_bigger_than_only_version(version)
    # end def check_bigger_than_only_version

    def check_multi_version(self):
        """
        Check if multi version available

        :return: Flag indicating if multi version is applicable
        :rtype: ``bool``
        """
        return self.event.check_multi_version()
    # end def check_multi_version

    def check_data_type(self, version, data_types):
        """
        Check the data type presence for the given version

        :param version: Version information
        :type version: ``int``
        :param data_types: Data types to check
        :type data_types: ``list[str]``

        :return: Flag indicating if at least one expected data type is present
        :rtype: ``bool``
        """
        return self.event.check_data_type(version, data_types)
    # end def check_data_type
# end class EventInfo

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
