#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.features.keyboard.disablekeysbyusage
    :brief: HID++ 2.0 Disable Keys by Usage command interface definition
    :author: Roy Luo
    :date: 2020/04/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from enum import IntEnum
from enum import unique
from pyhid.bitfield import BitField
from pyhid.hidpp.hidppmessage import HidppMessage, TYPE
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DisableKeysByUsage(HidppMessage):
    """
    DisableKeysByUsage implementation class

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Params                        24
    ============================  ==========
    """

    FEATURE_ID = 0x4522
    MAX_FUNCTION_INDEX = 3

    @unique
    class GameMode(IntEnum):
        """
        Modes values
        """
        DO_NOT_CHANGE = 0
        DISABLE = 1
        ENABLE = 2
    # end class GameMode

    def __init__(self, device_index, feature_index):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Feature Index
        :type feature_index: ``int``
        """
        super().__init__()

        self.deviceIndex = device_index
        self.featureIndex = feature_index
    # end def __init__
# end class DisableKeysByUsage

class DisableKeysByUsageModel(FeatureModel):
    """
    Disable keys by usage feature model
    """
    class INDEX:
        """
        Functions indexes
        """
        GET_CAPABILITIES = 0
        DISABLE_KEYS = 1
        ENABLE_KEYS = 2
        ENABLE_ALL_KEYS = 3
    # end class

    @classmethod
    def _get_data_model(cls):
        """
        Disable Keys by Usage feature data model
        """
        return {
            "feature_base": DisableKeysByUsage,
            "versions": {
                0: {
                    "main_cls": DisableKeysByUsageV0,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_CAPABILITIES: {"request": GetCapabilities,
                                                         "response": GetCapabilitiesResponse},
                            cls.INDEX.DISABLE_KEYS: {"request": DisableKeys, "response": DisableKeysResponse},
                            cls.INDEX.ENABLE_KEYS: {"request": EnableKeys, "response": EnableKeysResponse},
                            cls.INDEX.ENABLE_ALL_KEYS: {"request": EnableAllKeys, "response": EnableAllKeysResponse},
                        }
                    },
                },
            }
        }
    # end def _get_data_model
# end class DisableKeysByUsageModel

class DisableKeysByUsageFactory(FeatureFactory):
    """
    Disable keys by usage factory creates an object from a given version
    """
    @staticmethod
    def create(version):
        """
        Disable keys by usage object creation from version number
        :param version: Disable keys by usage feature version
        :type version: ``int``
        :return: Disable keys by usage object
        :rtype: ``DisableKeysByUsageInterface``
        """
        return DisableKeysByUsageModel.get_main_cls(version)()
    # end def create
# end class DisableKeysByUsageFactory

class DisableKeysByUsageInterface(FeatureInterface, ABC):
    """
    Interface to disable keys by usage feature
    Defines required interfaces for disable keys by usage classes
    """
    def __init__(self):
        """
        Constructor
        """
        self.get_capabilities_cls = None
        self.get_capabilities_response_cls = None
        self.disable_keys_cls = None
        self.disable_keys_response_cls = None
        self.enable_keys_cls = None
        self.enable_keys_response_cls = None
        self.enable_all_keys_cls = None
        self.enable_all_keys_response_cls = None
    # end def __init__
# end class DisableKeysByUsageInterface

class DisableKeysByUsageV0(DisableKeysByUsageInterface):
    """
    DisableKeysByUsage
    [0] getCapabilities() => usageCount
    [1] disableKeys(keysToDisable)
    [2] enableKeys(keysToEnable)
    [3] enableAllKeys()
    """
    VERSION = 0

    def __init__(self):
        super().__init__()
        self.get_capabilities_cls = DisableKeysByUsageModel.get_request_cls(
            self.VERSION, DisableKeysByUsageModel.INDEX.GET_CAPABILITIES)
        self.get_capabilities_response_cls = DisableKeysByUsageModel.get_response_cls(
            self.VERSION, DisableKeysByUsageModel.INDEX.GET_CAPABILITIES)
        self.disable_keys_cls = self.disable_keys_cls = DisableKeysByUsageModel.get_request_cls(
            self.VERSION, DisableKeysByUsageModel.INDEX.DISABLE_KEYS)
        self.disable_keys_response_cls = DisableKeysByUsageModel.get_response_cls(
            self.VERSION, DisableKeysByUsageModel.INDEX.DISABLE_KEYS)
        self.enable_keys_cls = self.enable_keys_cls = DisableKeysByUsageModel.get_request_cls(
            self.VERSION, DisableKeysByUsageModel.INDEX.ENABLE_KEYS)
        self.enable_keys_response_cls = DisableKeysByUsageModel.get_response_cls(
            self.VERSION, DisableKeysByUsageModel.INDEX.ENABLE_KEYS)
        self.enable_all_keys_cls = DisableKeysByUsageModel.get_request_cls(
            self.VERSION, DisableKeysByUsageModel.INDEX.ENABLE_ALL_KEYS)
        self.enable_all_keys_response_cls = DisableKeysByUsageModel.get_response_cls(
            self.VERSION, DisableKeysByUsageModel.INDEX.ENABLE_ALL_KEYS)

    # end def __init__

    def get_max_function_index(self):
        """
        See :any:`DisableKeysByUsageInterface.get_max_function_index`
        """
        return DisableKeysByUsageModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class DisableKeysByUsageV0

class GetCapabilities(DisableKeysByUsage):
    """
    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Padding                       24
    ============================  ==========
    """

    class FID(DisableKeysByUsage.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(DisableKeysByUsage.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = DisableKeysByUsage.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DisableKeysByUsage.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Feature Index
        :type feature_index: ``int``
        """
        super().__init__(device_index, feature_index)
        self.functionIndex = GetCapabilitiesResponse.FUNCTION_INDEX
    # end def __init__
# end class GetCapabilities

class GetCapabilitiesResponse(DisableKeysByUsage):
    """
    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    MaxDisabledUsages             8
    Padding                       120
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilities)
    VERSION = (0, )
    FUNCTION_INDEX = 0

    class FID(DisableKeysByUsage.FID):
        """
        Field Identifiers
        """
        MAX_DISABLED_USAGES = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(DisableKeysByUsage.LEN):
        """
        Field Lengths
        """
        MAX_DISABLED_USAGES = 0x08
        PADDING = 0x78
    # end class LEN

    FIELDS = DisableKeysByUsage.FIELDS + (
                BitField(FID.MAX_DISABLED_USAGES,
                         LEN.MAX_DISABLED_USAGES,
                         0x00,
                         0x00,
                         title='MaxDisabledUsages',
                         name='max_disabled_usages',
                         checks=(CheckHexList(LEN.MAX_DISABLED_USAGES // 8),
                                 CheckByte(),),
                         conversions={HexList: Numeral}, ),
                BitField(FID.PADDING,
                         LEN.PADDING,
                         0x00,
                         0x00,
                         title='Padding',
                         name='padding',
                         checks=(CheckHexList(LEN.PADDING // 8),
                                 CheckByte(),),
                         default_value=DisableKeysByUsage.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, max_disabled_keys):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Feature Index
        :type feature_index: ``int``
        :param max_disabled_keys: Maximum Disabled Keys
        :type max_disabled_keys: ``int``
        """
        super().__init__(device_index, feature_index)

        self.functionIndex = self.FUNCTION_INDEX
        self.max_disabled_usages = max_disabled_keys
    # end def __init__
# end class GetCapabilitiesResponse

class DisableKeys(DisableKeysByUsage):
    """
    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    KeysToDisable                 128
    ============================  ==========
    """

    class FID(DisableKeysByUsage.FID):
        """
        Field Identifiers
        """
        KEYS_TO_DISABLE = 0xFA
    # end class FID

    class LEN(DisableKeysByUsage.LEN):
        """
        Field Lengths
        """
        KEYS_TO_DISABLE = 0x80
    # end class LEN

    FIELDS = DisableKeysByUsage.FIELDS + (
        BitField(FID.KEYS_TO_DISABLE,
                 LEN.KEYS_TO_DISABLE,
                 0x00,
                 0x00,
                 title='KeysToDisable',
                 name='keys_to_disable',
                 checks=(CheckHexList(LEN.KEYS_TO_DISABLE // 8),
                         CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, keys_to_disable):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Feature Index
        :type feature_index: ``int``
        :param keys_to_disable: List of Disabled Keys
        :type keys_to_disable: ``list``
        """
        super(DisableKeys, self).__init__(device_index, feature_index)
        self.reportId = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.functionIndex = DisableKeysResponse.FUNCTION_INDEX
        for i in range(16-len(keys_to_disable)):
            keys_to_disable.append(0)
        # end for
        self.keys_to_disable = HexList(keys_to_disable)
    # end def __init__
# end class DisableKeys

class DisableKeysResponse(DisableKeysByUsage):
    """
    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Padding                       128
    ============================  ==========
    """

    FUNCTION_INDEX = 1
    VERSION = (0,)
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (DisableKeys)

    class FID(DisableKeysByUsage.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(DisableKeysByUsage.LEN):
        """
        Field Lengths
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = DisableKeysByUsage.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=DisableKeysByUsage.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Feature Index
        :type feature_index: ``int``
        """
        super().__init__(device_index, feature_index)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class DisableKeysResponse

class EnableKeys(DisableKeysByUsage):
    """
    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    KeysToEnable                  128
    ============================  ==========
    """

    class FID(DisableKeysByUsage.FID):
        """
        Field Identifiers
        """
        KEYS_TO_ENABLE = 0xFA
    # end class FID

    class LEN(DisableKeysByUsage.LEN):
        """
        Field Lengths
        """
        KEYS_TO_ENABLE = 0x80
    # end class LEN

    FIELDS = DisableKeysByUsage.FIELDS + (
        BitField(FID.KEYS_TO_ENABLE,
                 LEN.KEYS_TO_ENABLE,
                 0x00,
                 0x00,
                 title='KeysToEnable',
                 name='keys_to_enable',
                 checks=(CheckHexList(LEN.KEYS_TO_ENABLE // 8),
                         CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, keys_to_enable):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Feature Index
        :type feature_index: ``int``
        :param keys_to_enable: List of Enabled Keys
        :type keys_to_enable: ``list``
        """
        super(EnableKeys, self).__init__(device_index, feature_index)
        self.reportId = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.functionIndex = EnableKeysResponse.FUNCTION_INDEX
        for i in range(16-len(keys_to_enable)):
            keys_to_enable.append(0)
        # end for
        self.keys_to_enable = HexList(keys_to_enable)

    # end def __init__
# end class EnableKeys

class EnableKeysResponse(DisableKeysByUsage):
    """
    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Padding                       128
    ============================  ==========
    """
    FUNCTION_INDEX = 2
    VERSION = (0,)
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (EnableKeys)

    class FID(DisableKeysByUsage.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(DisableKeysByUsage.LEN):
        """
        Field Lengths
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = DisableKeysByUsage.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=DisableKeysByUsage.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Feature Index
        :type feature_index: ``int``
        """
        super().__init__(device_index, feature_index)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class EnableKeysResponse

class EnableAllKeys(DisableKeysByUsage):
    """
    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Padding                       24
    ============================  ==========
    """

    class FID(DisableKeysByUsage.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(DisableKeysByUsage.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = DisableKeysByUsage.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DisableKeysByUsage.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Feature Index
        :type feature_index: ``int``
        """
        super().__init__(device_index, feature_index)
        self.functionIndex = EnableAllKeysResponse.FUNCTION_INDEX
    # end def __init__
# end class EnableAllKeys

class EnableAllKeysResponse(DisableKeysByUsage):
    """
    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Padding                       128
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (EnableAllKeys)
    VERSION = (0, )
    FUNCTION_INDEX = 3

    class FID(DisableKeysByUsage.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(DisableKeysByUsage.LEN):
        """
        Field Lengths
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = DisableKeysByUsage.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=DisableKeysByUsage.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Feature Index
        :type feature_index: ``int``
        """
        super().__init__(device_index, feature_index)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class EnableAllKeysResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
