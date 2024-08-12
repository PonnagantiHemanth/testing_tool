#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.input.autoinput
:brief: Auto inputs for the code generation
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/05/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from codegenerator.input.engine import Parameter
from codegenerator.input.engine import SubParameter
from codegenerator.input.userinput import UserInput
from codegenerator.manager.engine import ConstantTextManager


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AutoInput(UserInput):
    """
    Define input data for generators
    """
    @classmethod
    def get_feature_location(cls):
        """
        Get the feature location

        :return: Feature location
        :rtype: ``str``
        """
        return f"output/TESTS/TESTSUITES/pytestbox/{cls.HIDPP_TYPE.lower()}/hidpp20/{cls.HIDPP_CATEGORY.lower()}" \
               f"/feature_{cls.HIDPP_FEATURE_ID.lower()}"
    # end def get_feature_location

    @classmethod
    def get_all_version(cls):
        """
        Get all version information

        :return: All version information
        :rtype: ``list | range``

        :raise ``AssertionError``: Assert version that raise an exception
        """
        if isinstance(cls.HIDPP_FEATURE_VERSION, str):
            return [int(version) for version in cls.HIDPP_FEATURE_VERSION.split(",")]
        elif isinstance(cls.HIDPP_FEATURE_VERSION, int):
            return range(cls.HIDPP_FEATURE_VERSION + 1)
        # end if

        return AssertionError("Feature Version must be number or comma separated string")
    # end def get_all_version

    @classmethod
    def get_max_version(cls):
        """
        Get maximum version information

        :return: Max version
        :rtype: ``int``

        :raise ``AssertionError``: Assert version that raise an exception
        """
        if isinstance(cls.HIDPP_FEATURE_VERSION, str):
            return max([int(version) for version in cls.HIDPP_FEATURE_VERSION.split(",")])
        elif isinstance(cls.HIDPP_FEATURE_VERSION, int):
            return cls.HIDPP_FEATURE_VERSION
        # end if
        return AssertionError("Feature Version must be number or comma separated string")
    # end def _get_max_version

    @classmethod
    def get_max_function_index(cls):
        """
        Get MAX_FUNCTION_INDEX for the feature

        :return: Max function index
        :rtype: ``str``
        """
        output = []
        for version in cls.get_version_list():
            max_index = -1
            for function_info in cls.FUNCTION_LIST:
                if function_info.is_this_version_applicable(version):
                    max_index += 1
                # end if
            # end for
            output.append(f"MAX_FUNCTION_INDEX_V{version} = {max_index}")
        # end for

        return "\n    ".join(output)
    # end def get_max_function_index

    @classmethod
    def get_max_function_index_number(cls, version):
        """
        Get MAX_FUNCTION_INDEX number for the version

        :param version: Version
        :type version: ``int``

        :return: Max function index number
        :rtype: ``str``
        """
        max_index = -1
        for function_info in cls.FUNCTION_LIST:
            if function_info.is_this_version_applicable(version):
                max_index += 1
            # end if
        # end for

        return max_index
    # end def get_max_function_index_number

    @classmethod
    def get_version_list(cls):
        """
        Get version list information

        :return: Version information
        :rtype: ``list[int]``
        """
        version_list = None
        if isinstance(cls.HIDPP_FEATURE_VERSION, str):
            version_list = [int(version) for version in cls.HIDPP_FEATURE_VERSION.split(",")]
        elif isinstance(cls.HIDPP_FEATURE_VERSION, int):
            version_list = list(range(cls.HIDPP_FEATURE_VERSION + 1))
        # end if
        return version_list
    # end def get_version_list

    @classmethod
    def get_version_text(cls, version):
        """
        Check the feature has multi version

        :param version: Version information
        :type version: ``int``

        :return: Version text
        :rtype: ``str``
        """
        if str(cls.HIDPP_FEATURE_VERSION).__contains__(","):
            return f"V{version}"
        # end if
        return ""
    # end def get_version_text

    @classmethod
    def get_common_dictionary(cls):
        """
        Get the common inputs in dictionary format

        :return: Template substitute values
        :rtype: ``dict``
        """
        # User may provide the prefix. Remove it.
        if cls.HIDPP_FEATURE_ID.lower().startswith("0x"):
            cls.HIDPP_FEATURE_ID = cls.HIDPP_FEATURE_ID.replace("0x", "").replace("0X", "")
        # end if

        # Dictionary format is mandatory to use in string:Template object.
        return dict(
            # Author Info
            AuthorEmailId=cls.AUTHOR_EMAIL_ID,
            AuthorName=cls.AUTHOR_NAME,

            # HIDPP info
            HidppCategory=cls.HIDPP_CATEGORY,
            HidppCategoryCapitalized=cls.HIDPP_CATEGORY.capitalize(),
            HidppCategoryUpper=cls.HIDPP_CATEGORY.upper(),
            HidppFIDUpper=cls.HIDPP_FEATURE_ID.upper(),
            HidppFIDLower=cls.HIDPP_FEATURE_ID.lower(),
            HidppFeatureComment=cls.HIDPP_FEATURE_COMMENT,
            HidppFeatureVersion=cls.HIDPP_FEATURE_VERSION,
            HidppType=cls.HIDPP_TYPE,
            HidppTypeTitleCase=cls.HIDPP_TYPE.capitalize(),
            HidppVersion=cls.HIDPP_VERSION,
            FeaturesSubSystem=f"{cls.HIDPP_CATEGORY.capitalize()}FeatureSubSystem",

            # Day info
            Day=cls.DAY,
            Month=cls.MONTH,
            Year=cls.YEAR,

            NvsBackupRestore=cls.NVS_BACKUP_RESTORE,

            # "Device Friendly Name" => "Device Friendly Name"
            FeatureNameTitleCaseWithSpace=cls.HIDPP_FEATURE_NAME,

            # "Device Friendly Name" => "DeviceFriendlyName"
            FeatureNameTitleCaseWithoutSpace="".join(cls.HIDPP_FEATURE_NAME.split()),

            # "Device Friendly Name" => "DeviceFriendlyNameTestCase"
            FeatureNameTestCase="".join(cls.HIDPP_FEATURE_NAME.split()) + "TestCase",

            # "Device Friendly Name" => "DeviceFriendlyNameTestUtils"
            FeatureNameUtils="".join(cls.HIDPP_FEATURE_NAME.split()) + "TestUtils",

            # "Device Friendly Name" => "DeviceFriendlyNameFactory"
            FeatureNameFactory="".join(cls.HIDPP_FEATURE_NAME.split()) + "Factory",

            # "Device Friendly Name" => "devicefriendlyname"
            FeatureNameLowerCaseWithoutSpace="".join(cls.HIDPP_FEATURE_NAME.lower().split()),

            # "Device Friendly Name" => "device_friendly_name"
            FeatureNameLowerCaseWithUnderscore="_".join(cls.HIDPP_FEATURE_NAME.lower().split()),

            # "Device Friendly Name" => "DEVICE_FRIENDLY_NAME"
            FeatureNameUpperCaseWithUnderscore="_".join(cls.HIDPP_FEATURE_NAME.upper().split()),

            # Extra fixed values required by the program (do not edit)
            TestWithUnderscore="_test",
            Utils="utils",
            Model="Model",
            Interface="Interface",
            V="V",
            TestCase="TestCase",
            MaxVersion=cls.get_max_version()
        )
    # end def get_common_dictionary

    @classmethod
    def get_import_text(cls, text):
        """
        Get the import text with word wrap

        :param text: The text to split
        :type text: ``str``

        :return: The text with word wrap
        :rtype: ``str``
        """
        if len(text) > ConstantTextManager.LINE_WRAP_AT_CHAR:
            return text.replace("import", "\\\n    import")
        # end if
        return text
    # end def get_import_text
# end class AutoInput

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
