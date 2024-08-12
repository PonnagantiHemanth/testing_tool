#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.manager.engine
:brief: Manager engine
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/05/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import sys


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
# Refer: https://docs.google.com/spreadsheets/d/1TO4UOiJ7zWza0wuIIOrqqig43kEY-Tm2O0cgQmEQ-TU/view#gid=1693694472
_TOOL_VERSION = "1.3"
_HASH_LINE_COUNT = 118


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ConstantTextManager(object):
    """
    Define reusable constant texts
    """
    ARGS_OBJ_REF_IMPORT_SECTION = "IMPORT_SECTION"
    ARGS_OBJ_REF_NAME_WITH_PATH = "NAME_WITH_PATH"
    ASSIGNMENT = " = "
    AUTHOR_KEY = ":author: "
    BRIEF_KEY = ":brief: "
    COLUMN_ONE_SIZE = 28
    COLUMN_TWO_SIZE = 10
    CONSTANTS = "# constants"
    DATE_KEY = ":date: "
    DOUBLE_QUOTE = '"'
    EMPTY_STRING = ""
    END_OF_FILE = "# END OF FILE"
    ENVIRONMENT = "#!/usr/bin/env python"
    EQUAL_TO = " = "
    HASH_LINE = "# " + "-" * _HASH_LINE_COUNT
    IMPLEMENTATION = "# implementation"
    IMPORTS = "# imports"
    IMPORT_ABC = "\nfrom abc import ABC"
    IMPORT_ASCII_UPPER_CASE = "\nfrom string import ascii_uppercase"
    IMPORT_BASE_COMMUNICATION_CHANNEL = "\n# noinspection PyUnresolvedReferences" \
                                        "\nfrom pychannel.channelinterfaceclasses import BaseCommunicationChannel\n"
    IMPORT_BIT_FIELD = "\nfrom pyhid.bitfield import BitField"
    IMPORT_BIT_FIELD_CONTAINER_MIXIN = "\nfrom pyhid.bitfieldcontainermixin import BitFieldContainerMixin"
    IMPORT_CHANNEL_UTILS = "\nfrom pytestbox.base.channelutils import ChannelUtils"
    IMPORT_CHECK_BYTE = "\nfrom pyhid.field import CheckByte"
    IMPORT_CHECK_HEXLIST = "\nfrom pyhid.field import CheckHexList"
    IMPORT_CHECK_INT = "\nfrom pyhid.field import CheckInt"
    IMPORT_CHECK_LIST = "\nfrom pyhid.field import CheckList"
    IMPORT_CHOICES = "\nfrom random import choices"
    IMPORT_COMMON_BASE_TEST_UTILS = "\nfrom pytestbox.base.basetest import CommonBaseTestCase"
    IMPORT_COMPUTE_INF_VALUES = "\nfrom pylibrary.tools.util import compute_inf_values"
    IMPORT_COMPUTE_SUP_VALUES = "\nfrom pylibrary.tools.util import compute_sup_values"
    IMPORT_COMPUTE_WRONG_RANGE = "\nfrom pylibrary.tools.util import compute_wrong_range"
    IMPORT_DEVICE_BASE_TEST_CASE = "\nfrom pytestbox.base.basetest import DeviceBaseTestCase"
    IMPORT_DEVICE_BASE_TEST_UTILS = "\nfrom pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils"
    IMPORT_DEVICE_TEST_UTILS = "\nfrom pytestbox.device.base.devicetestutils import DeviceTestUtils"
    IMPORT_DIGITS = "\nfrom string import digits"
    IMPORT_FEATURES = "\nfrom pyharness.selector import features"
    IMPORT_FEATURE_FACTORY = "\nfrom pyhid.hidpp.features.basefeature import FeatureFactory"
    IMPORT_FEATURE_INTERFACE = "\nfrom pyhid.hidpp.features.basefeature import FeatureInterface"
    IMPORT_FEATURE_MODEL = "\nfrom pyhid.hidpp.features.basefeature import FeatureModel"
    IMPORT_HEXLIST = "\nfrom pylibrary.tools.hexlist import HexList"
    IMPORT_HIDPP_2_ERROR_CODES = "\nfrom pyhid.hidpp.features.error import Hidpp2ErrorCodes"
    IMPORT_HIDPP_MESSAGE = "\nfrom pyhid.hidpp.hidppmessage import HidppMessage"
    IMPORT_HID_DISPATCHER = "\nfrom pyhid.hiddispatcher import HIDDispatcher"
    IMPORT_LEVEL = "\nfrom pyharness.extensions import level"
    IMPORT_LOG_HELPER = "\nfrom pytestbox.base.loghelper import LogHelper"
    IMPORT_NUMERAL = "\nfrom pylibrary.tools.numeral import Numeral"
    IMPORT_ROOT_TEST_CASE = "\nfrom pyhid.hidpp.features.test.root_test import RootTestCase"
    IMPORT_TEST_CASE = "\nfrom unittest import TestCase"
    IMPORT_TO_INT = "\nfrom pylibrary.tools.numeral import to_int"
    IMPORT_TYPE = "\nfrom pyhid.hidpp.hidppmessage import TYPE"
    LINE_WRAP_AT_CHAR = 120
    LOOP_END = '\n_LOOP_END = "End Test Loop"'
    LOOP_START_FID = '\n_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"'
    LOOP_START_PADDING = '\n_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"'
    LOOP_START_RESERVED = '\n_LOOP_START_RESERVED = "Test loop over reserved range (several interesting values)"'
    LOOP_START_SW_ID = '\n_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"'
    MAIN = "# main"
    NEW_LINE = "\n"
    OPTIONAL = " - OPTIONAL"
    PACKAGE_KEY = ":package: "
    PY_TEST_BOX = "# Python Test Box"
    PY_TEST_HARNESS = "# Python Test Harness"
    SINGLE_QUOTE = "'"
    TAB = "    "
    TOOL_VERSION = _TOOL_VERSION
    TOOL_VERSION_INFO = f":tool: This file has been generated using 'code generator tool version {_TOOL_VERSION}'"
    TRIPLE_QUOTE = '"""'
    UTF_FORMAT = "# -*- coding: utf-8 -*-"
# end class ConstantTextManager


class FileManager(object):
    """
    Define reusable file operations
    """

    @staticmethod
    def write_file(file_name, data):
        """
        Write operation on a file

        :param file_name: Name of the file
        :type file_name: ``str``
        :param data: Data to write
        :type data: ``list[str]``

        :return: Flag indicating if the write operation is successful
        :rtype: ``bool``
        """
        with open(file_name, "w", encoding="utf-8") as writer:
            sys.stdout.write(f"\nWrite file: {file_name}")
            for line in data:
                try:
                    writer.write(line)
                except Exception as e:
                    sys.stdout.write(f"\nFile write failed with error: {type(e).__name__}: {e}")
                    return False
                # end try
            # end for
        # end with
        return True
    # end def write_file
# end class FileManager

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
