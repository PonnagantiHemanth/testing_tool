#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.common.backlight
:brief: HID++ 2.0 ``Backlight`` command interface definition
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/09/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from enum import IntEnum

from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class Backlight(HidppMessage):
    """
    Define the feature which gives the possibility to play various effects or waveforms.
    The configuration enables / disables the backlight.
    An event is generated whenever user changes the backlight.
    This feature also can be used by keyboard that has similar backlight system.
    """

    FEATURE_ID = 0x1982
    MAX_FUNCTION_INDEX_V1 = 2
    MAX_FUNCTION_INDEX_V2ToV3 = 3

    class Configuration(IntEnum):
        """
        Define 'bcklEn' parameter configuration
        """
        DISABLE = 0x00
        ENABLE = 0x01
    # end class Configuration

    class Wow(IntEnum):
        """
        Define 'supportedOptions' byte values to enable and disable the 'wow' effect
        """
        DISABLE = 0x00
        ENABLE = 0x01
    # end class Wow

    class Crown(IntEnum):
        """
        Define 'supportedOptions' byte values to enable and disable the 'crown' effect
        """
        DISABLE = 0x00
        ENABLE = 0x02
    # end class Crown

    class PwrSave(IntEnum):
        """
        Define 'supportedOptions' byte values to enable and disable the 'pwrSave' effect
        """
        DISABLE = 0x00
        ENABLE = 0x04
    # end class PwrSave

    class SupportedOptionsMask(IntEnum):
        """
        Define the 'getBacklightConfig.supportedOptions' parameter masked values
        """
        NONE = 0x00
        WOW = 0x0100
        CROWN = 0x0200
        PWR_SAVE = 0x0400
        BCKL_MODE = 0x1800
        ALL = 0x1FFF
        DEFAULT_OPTIONS = 0xFF00
        WOW_S = 0x0001
        CROWN_S = 0x0002
        PWR_SAVE_S = 0x0004
        # Since v3
        AUTO_MODE_S = 0x0008
        TEMP_MANUAL_MODE_S = 0x0010
        PERM_MANUAL_MODE_S = 0x0020
    # end class SupportedOptionsMask

    class SupportedBacklightEffectMask(IntEnum):
        """
        Define the 'getBacklightConfig.backlightEffectList' parameter masked values
        """
        STATIC = 0x0100
        NONE = 0x0200
        BREATHING_LIGHT = 0x0400
        CONTRAST = 0x0800
        REACTION = 0x1000
        RANDOM = 0x2000
        WAVES = 0x4000
    # end class SupportedBacklightEffectMask

    class BacklightEffect(IntEnum):
        """
        Define 'backlightEffect' parameter possible values
        """
        STATIC_EFFECT = 0x00
        NONE_EFFECT = 0x01
        BREATHING_LIGHT_EFFECT = 0X02
        CONTRAST_EFFECT = 0x03
        REACTION_EFFECT = 0x04
        RANDOM_EFFECT = 0x05
        WAVES_EFFECT = 0x06
        # Only for SetBacklightConfig and SetBacklightEffect
        CURRENT_EFFECT = 0xFF
    # end class BacklightEffect

    class Options(IntEnum):
        """
        Define the 'setBacklightConfig.options' parameter possible values
        """
        NONE = 0x00
        WOW = 0x01
        CROWN = 0x02
        PWR_SAVE = 0x04
        # Since v3
        NO_BACKLIGHT_MODE_SELECTED = 0x00
        AUTOMATIC_MODE = 0x08
        TEMPORARY_MANUAL_MODE = 0x10
        PERMANENT_MANUAL_MODE = 0x18
        ALL = 0x1F
    # end class Options

    class BacklightStatus(IntEnum):
        """
        Define backlight status parameter possible values
        """
        DISABLED_BY_SW = 0x00
        DISABLED_BY_CRITICAL_BATTERY = 0x01
        ALS_AUTOMATIC_MODE = 0x02
        ALS_MODE_SATURATED = 0x03
        MANUAL_MODE = 0x04
        # Since v3
        PERMANENT_MANUAL_MODE = 0x05
    # end class BacklightStatus

    class CurrentLevel(IntEnum):
        """
        Define the current backlight intensity level parameter possible values
        """
        CURRENT_LEVEL_0 = 0
        CURRENT_LEVEL_1 = 1
        CURRENT_LEVEL_2 = 2
        CURRENT_LEVEL_3 = 3
        CURRENT_LEVEL_4 = 4
        CURRENT_LEVEL_5 = 5
        CURRENT_LEVEL_6 = 6
        CURRENT_LEVEL_7 = 7
    # end class CurrentLevel

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__
# end class Backlight


class BacklightModel(FeatureModel):
    """
    Define ``Backlight`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_BACKLIGHT_CONFIG = 0
        SET_BACKLIGHT_CONFIG = 1
        GET_BACKLIGHT_INFO = 2
        SET_BACKLIGHT_EFFECT = 3

        # Event index
        BACKLIGHT_INFO = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``Backlight`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v1 = {
            "functions": {
                cls.INDEX.GET_BACKLIGHT_CONFIG: {
                    "request": GetBacklightConfig,
                    "response": GetBacklightConfigResponseV1
                },
                cls.INDEX.SET_BACKLIGHT_CONFIG: {
                    "request": SetBacklightConfigV1,
                    "response": SetBacklightConfigResponse
                },
                cls.INDEX.GET_BACKLIGHT_INFO: {
                    "request": GetBacklightInfo,
                    "response": GetBacklightInfoResponseV1
                },
            },
            "events": {
                cls.INDEX.BACKLIGHT_INFO: {"report": BacklightInfoEventV1}
            }
        }

        function_map_v2 = {
            "functions": {
                cls.INDEX.GET_BACKLIGHT_CONFIG: {
                    "request": GetBacklightConfig,
                    "response": GetBacklightConfigResponseV2
                },
                cls.INDEX.SET_BACKLIGHT_CONFIG: {
                    "request": SetBacklightConfigV2,
                    "response": SetBacklightConfigResponse
                },
                cls.INDEX.GET_BACKLIGHT_INFO: {
                    "request": GetBacklightInfo,
                    "response": GetBacklightInfoResponseV2
                },
                cls.INDEX.SET_BACKLIGHT_EFFECT: {
                    "request": SetBacklightEffect,
                    "response": SetBacklightEffectResponse
                }
            },
            "events": {
                cls.INDEX.BACKLIGHT_INFO: {"report": BacklightInfoEventV2ToV4}
            }
        }

        function_map_v3 = {
            "functions": {
                cls.INDEX.GET_BACKLIGHT_CONFIG: {
                    "request": GetBacklightConfig,
                    "response": GetBacklightConfigResponseV3
                },
                cls.INDEX.SET_BACKLIGHT_CONFIG: {
                    "request": SetBacklightConfigV3,
                    "response": SetBacklightConfigResponse
                },
                cls.INDEX.GET_BACKLIGHT_INFO: {
                    "request": GetBacklightInfo,
                    "response": GetBacklightInfoResponseV3
                },
                cls.INDEX.SET_BACKLIGHT_EFFECT: {
                    "request": SetBacklightEffect,
                    "response": SetBacklightEffectResponse
                }
            },
            "events": {
                cls.INDEX.BACKLIGHT_INFO: {"report": BacklightInfoEventV2ToV4}
            }
        }

        function_map_v4 = {
            "functions": {
                cls.INDEX.GET_BACKLIGHT_CONFIG: {
                    "request": GetBacklightConfig,
                    "response": GetBacklightConfigResponseV4
                },
                cls.INDEX.SET_BACKLIGHT_CONFIG: {
                    "request": SetBacklightConfigV4,
                    "response": SetBacklightConfigResponse
                },
                cls.INDEX.GET_BACKLIGHT_INFO: {
                    "request": GetBacklightInfo,
                    "response": GetBacklightInfoResponseV4
                },
                cls.INDEX.SET_BACKLIGHT_EFFECT: {
                    "request": SetBacklightEffect,
                    "response": SetBacklightEffectResponse
                }
            },
            "events": {
                cls.INDEX.BACKLIGHT_INFO: {"report": BacklightInfoEventV2ToV4}
            }
        }

        return {
            "feature_base": Backlight,
            "versions": {
                BacklightV1.VERSION: {
                    "main_cls": BacklightV1,
                    "api": function_map_v1
                },
                BacklightV2.VERSION: {
                    "main_cls": BacklightV2,
                    "api": function_map_v2
                },
                BacklightV3.VERSION: {
                    "main_cls": BacklightV3,
                    "api": function_map_v3
                },
                BacklightV4.VERSION: {
                    "main_cls": BacklightV4,
                    "api": function_map_v4
                }
            }
        }
    # end def _get_data_model
# end class BacklightModel


class BacklightFactory(FeatureFactory):
    """
    Get ``Backlight`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``Backlight`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``BacklightInterface``
        """
        return BacklightModel.get_main_cls(version)()
    # end def create
# end class BacklightFactory


class BacklightInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``Backlight``
    """

    def __init__(self):
        # Requests
        self.get_backlight_config_cls = None
        self.set_backlight_config_cls = None
        self.get_backlight_info_cls = None
        self.set_backlight_effect_cls = None

        # Responses
        self.get_backlight_config_response_cls = None
        self.set_backlight_config_response_cls = None
        self.get_backlight_info_response_cls = None
        self.set_backlight_effect_response_cls = None

        # Events
        self.backlight_info_event_cls = None
    # end def __init__
# end class BacklightInterface


class BacklightV1(BacklightInterface):
    """
    Define ``BacklightV1`` feature

    This feature provides model and unit specific information for version 1

    [0] getBacklightConfig() -> configuration, supportedOptions

    [1] setBacklightConfig(configuration, options) -> None

    [2] getBacklightInfo() -> numberOfLevel, currentLevel, backlightStatus

    [Event 0] backlightInfoEvent -> numberOfLevel, currentLevel, backlightStatus
    """

    VERSION = 1

    def __init__(self):
        # See ``Backlight.__init__``
        super().__init__()
        index = BacklightModel.INDEX

        # Requests
        self.get_backlight_config_cls = BacklightModel.get_request_cls(
            self.VERSION, index.GET_BACKLIGHT_CONFIG)
        self.set_backlight_config_cls = BacklightModel.get_request_cls(
            self.VERSION, index.SET_BACKLIGHT_CONFIG)
        self.get_backlight_info_cls = BacklightModel.get_request_cls(
            self.VERSION, index.GET_BACKLIGHT_INFO)

        # Responses
        self.get_backlight_config_response_cls = BacklightModel.get_response_cls(
            self.VERSION, index.GET_BACKLIGHT_CONFIG)
        self.set_backlight_config_response_cls = BacklightModel.get_response_cls(
            self.VERSION, index.SET_BACKLIGHT_CONFIG)
        self.get_backlight_info_response_cls = BacklightModel.get_response_cls(
            self.VERSION, index.GET_BACKLIGHT_INFO)

        # Events
        self.backlight_info_event_cls = BacklightModel.get_report_cls(
            self.VERSION, index.BACKLIGHT_INFO)
    # end def __init__

    def get_max_function_index(self):
        # See ``BacklightInterface.get_max_function_index``
        return BacklightModel.get_base_cls().MAX_FUNCTION_INDEX_V1
    # end def get_max_function_index
# end class BacklightV1


class BacklightV2(BacklightV1):
    """
    Define ``BacklightV2`` feature

    This feature provides model and unit specific information for version 2

    [0] getBacklightConfig() -> configuration, supportedOptions, backlightEffectList

    [1] setBacklightConfig(configuration, options, backlightEffect) -> None

    [2] getBacklightInfo() -> numberOfLevel, currentLevel, backlightStatus, backlightEffect

    [3] setBacklightEffect(backlightEffect) -> None

    [Event 0] backlightInfoEvent -> numberOfLevel, currentLevel, backlightStatus, backlightEffect
    """

    VERSION = 2

    def __init__(self):
        # See ``Backlight.__init__``
        super().__init__()
        index = BacklightModel.INDEX

        # Requests
        self.set_backlight_effect_cls = BacklightModel.get_request_cls(
            self.VERSION, index.SET_BACKLIGHT_EFFECT)

        # Responses
        self.set_backlight_effect_response_cls = BacklightModel.get_response_cls(
            self.VERSION, index.SET_BACKLIGHT_EFFECT)
    # end def __init__

    def get_max_function_index(self):
        # See ``BacklightInterface.get_max_function_index``
        return BacklightModel.get_base_cls().MAX_FUNCTION_INDEX_V2ToV3
    # end def get_max_function_index
# end class BacklightV2


class BacklightV3(BacklightV2):
    """
    Define ``BacklightV3`` feature

    This feature provides model and unit specific information for version 3

    [0] getBacklightConfig() -> configuration, supportedOptions, backlightEffectList, currentBacklightLevel,
                                currDurationHandsOUT, currDurationHandsIN, currDurationPowered

    [1] setBacklightConfig(configuration, options, backlightEffect, currentBacklightLevel, currDurationHandsOUT,
                           currDurationHandsIN, currDurationPowered) -> None

    [2] getBacklightInfo() -> numberOfLevel, currentLevel, backlightStatus, backlightEffect, OOBDurationHandsOUT,
                              OOBDurationHandsIN, OOBDurationPowered

    [3] setBacklightEffect(backlightEffect) -> None

    [Event 0] backlightInfoEvent -> numberOfLevel, currentLevel, backlightStatus, backlightEffect
    """

    VERSION = 3
# end class BacklightV3


class BacklightV4(BacklightV3):
    """
    Define ``BacklightV4`` feature

    This feature provides model and unit specific information for version 3

    [0] getBacklightConfig() -> configuration, supportedOptions, backlightEffectList, currentBacklightLevel,
                                currDurationHandsOUT, currDurationHandsIN, currDurationPowered, currDurationNotPowered

    [1] setBacklightConfig(configuration, options, backlightEffect, currentBacklightLevel, currDurationHandsOUT,
                           currDurationHandsIN, currDurationPowered, currDurationNotPowered) -> None

    [2] getBacklightInfo() -> numberOfLevel, currentLevel, backlightStatus, backlightEffect, OOBDurationHandsOUT,
                              OOBDurationHandsIN, OOBDurationPowered, OOBDurationNotPowered

    [3] setBacklightEffect(backlightEffect) -> None

    [Event 0] backlightInfoEvent -> numberOfLevel, currentLevel, backlightStatus, backlightEffect
    """

    VERSION = 4
# end class BacklightV4


class GetBacklightConfigResponseData1(Backlight):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetBacklightConfigResponseData2
        - GetBacklightConfigResponseData3
        - GetBacklightConfigResponseV1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Configuration                 8
    SupportedOptions              16
    ============================  ==========
    """

    class FID(Backlight.FID):
        # See ``Backlight.FID``
        CONFIGURATION = Backlight.FID.SOFTWARE_ID - 1
        SUPPORTED_OPTIONS = CONFIGURATION - 1
    # end class FID

    class LEN(Backlight.LEN):
        # See ``Backlight.LEN``
        CONFIGURATION = 0x8
        SUPPORTED_OPTIONS = 0x10
    # end class LEN

    FIELDS = Backlight.FIELDS + (
        BitField(fid=FID.CONFIGURATION, length=LEN.CONFIGURATION,
                 title="Configuration", name="configuration",
                 checks=(CheckHexList(LEN.CONFIGURATION // 8),
                         CheckByte(),)),
        BitField(fid=FID.SUPPORTED_OPTIONS, length=LEN.SUPPORTED_OPTIONS,
                 title="SupportedOptions", name="supported_options",
                 checks=(CheckHexList(LEN.SUPPORTED_OPTIONS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.SUPPORTED_OPTIONS) - 1),)),
    )
# end class GetBacklightConfigResponseData1


class GetBacklightConfigResponseData2(GetBacklightConfigResponseData1):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetBacklightConfigResponseData3
        - GetBacklightConfigResponseV2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Configuration                 8
    SupportedOptions              16
    BacklightEffectList           16
    ============================  ==========
    """

    class FID(GetBacklightConfigResponseData1.FID):
        # See ``GetBacklightConfigResponseData1.FID``
        BACKLIGHT_EFFECT_LIST = GetBacklightConfigResponseData1.FID.SUPPORTED_OPTIONS - 1
    # end class FID

    class LEN(GetBacklightConfigResponseData1.LEN):
        # See ``GetBacklightConfigResponseData1.LEN``
        BACKLIGHT_EFFECT_LIST = 0x10
    # end class LEN

    FIELDS = GetBacklightConfigResponseData1.FIELDS + (
        BitField(fid=FID.BACKLIGHT_EFFECT_LIST, length=LEN.BACKLIGHT_EFFECT_LIST,
                 title="BacklightEffectList", name="backlight_effect_list",
                 checks=(CheckHexList(LEN.BACKLIGHT_EFFECT_LIST // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.BACKLIGHT_EFFECT_LIST) - 1),)),
    )
# end class GetBacklightConfigResponseData2


class GetBacklightConfigResponseData3(GetBacklightConfigResponseData2):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetBacklightConfigResponseV3

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Configuration                 8
    SupportedOptions              16
    BacklightEffectList           16
    CurrentBacklightLevel         8
    CurrDurationHandsOUT          16
    CurrDurationHandsIN           16
    CurrDurationPowered           16
    ============================  ==========
    """

    class FID(GetBacklightConfigResponseData2.FID):
        # See ``GetBacklightConfigResponseData2.FID``
        CURRENT_BACKLIGHT_LEVEL = GetBacklightConfigResponseData2.FID.BACKLIGHT_EFFECT_LIST - 1
        CURR_DURATION_HANDS_OUT = CURRENT_BACKLIGHT_LEVEL - 1
        CURR_DURATION_HANDS_IN = CURR_DURATION_HANDS_OUT - 1
        CURR_DURATION_POWERED = CURR_DURATION_HANDS_IN - 1
    # end class FID

    class LEN(GetBacklightConfigResponseData2.LEN):
        # See ``GetBacklightConfigResponseData2.LEN``
        CURRENT_BACKLIGHT_LEVEL = 0x8
        CURR_DURATION_HANDS_OUT = 0x10
        CURR_DURATION_HANDS_IN = 0x10
        CURR_DURATION_POWERED = 0x10
    # end class LEN

    FIELDS = GetBacklightConfigResponseData2.FIELDS + (
        BitField(fid=FID.CURRENT_BACKLIGHT_LEVEL, length=LEN.CURRENT_BACKLIGHT_LEVEL,
                 title="CurrentBacklightLevel", name="current_backlight_level",
                 checks=(CheckHexList(LEN.CURRENT_BACKLIGHT_LEVEL // 8),
                         CheckByte(),)),
        BitField(fid=FID.CURR_DURATION_HANDS_OUT, length=LEN.CURR_DURATION_HANDS_OUT,
                 title="CurrDurationHandsOut", name="curr_duration_hands_out",
                 checks=(CheckHexList(LEN.CURR_DURATION_HANDS_OUT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CURR_DURATION_HANDS_OUT) - 1),)),
        BitField(fid=FID.CURR_DURATION_HANDS_IN, length=LEN.CURR_DURATION_HANDS_IN,
                 title="CurrDurationHandsIn", name="curr_duration_hands_in",
                 checks=(CheckHexList(LEN.CURR_DURATION_HANDS_IN // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CURR_DURATION_HANDS_IN) - 1),)),
        BitField(fid=FID.CURR_DURATION_POWERED, length=LEN.CURR_DURATION_POWERED,
                 title="CurrDurationPowered", name="curr_duration_powered",
                 checks=(CheckHexList(LEN.CURR_DURATION_POWERED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CURR_DURATION_POWERED) - 1),)),
    )
# end class GetBacklightConfigResponseData3


class GetBacklightConfigResponseData4(GetBacklightConfigResponseData3):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetBacklightConfigResponseV4

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Configuration                 8
    SupportedOptions              16
    BacklightEffectList           16
    CurrentBacklightLevel         8
    CurrDurationHandsOUT          16
    CurrDurationHandsIN           16
    CurrDurationPowered           16
    CurrDurationNotPowered        16
    ============================  ==========
    """

    class FID(GetBacklightConfigResponseData3.FID):
        # See ``GetBacklightConfigResponseData3.FID``
        CURR_DURATION_NOT_POWERED = GetBacklightConfigResponseData3.FID.CURR_DURATION_POWERED - 1
    # end class FID

    class LEN(GetBacklightConfigResponseData3.LEN):
        # See ``GetBacklightConfigResponseData3.LEN``
        CURR_DURATION_NOT_POWERED = 0x10
    # end class LEN

    FIELDS = GetBacklightConfigResponseData3.FIELDS + (
        BitField(fid=FID.CURR_DURATION_NOT_POWERED, length=LEN.CURR_DURATION_NOT_POWERED,
                 title="CurrDurationNotPowered", name="curr_duration_not_powered",
                 checks=(CheckHexList(LEN.CURR_DURATION_NOT_POWERED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CURR_DURATION_NOT_POWERED) - 1),)),
    )
# end class GetBacklightConfigResponseData4


class SetBacklightConfigData1(Backlight):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetBacklightConfigData2
        - SetBacklightConfigData3
        - SetBacklightConfigV1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Configuration                 8
    Options                       8
    ============================  ==========
    """

    class FID(Backlight.FID):
        # See ``Backlight.FID``
        CONFIGURATION = Backlight.FID.SOFTWARE_ID - 1
        OPTIONS = CONFIGURATION - 1
    # end class FID

    class LEN(Backlight.LEN):
        # See ``Backlight.LEN``
        CONFIGURATION = 0x8
        OPTIONS = 0x8
    # end class LEN

    FIELDS = Backlight.FIELDS + (
        BitField(fid=FID.CONFIGURATION, length=LEN.CONFIGURATION,
                 title="Configuration", name="configuration",
                 checks=(CheckHexList(LEN.CONFIGURATION // 8),
                         CheckByte(),)),
        BitField(fid=FID.OPTIONS, length=LEN.OPTIONS,
                 title="Options", name="options",
                 checks=(CheckHexList(LEN.OPTIONS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.OPTIONS) - 1),)),
    )
# end class SetBacklightConfigData1


class SetBacklightConfigData2(SetBacklightConfigData1):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetBacklightConfigData3
        - SetBacklightConfigV2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Configuration                 8
    Options                       8
    BacklightEffect               8
    ============================  ==========
    """

    class FID(SetBacklightConfigData1.FID):
        # See ``SetBacklightConfigData1.FID``
        BACKLIGHT_EFFECT = SetBacklightConfigData1.FID.OPTIONS - 1
    # end class FID

    class LEN(SetBacklightConfigData1.LEN):
        # See ``SetBacklightConfigData1.LEN``
        BACKLIGHT_EFFECT = 0x8
    # end class LEN

    FIELDS = SetBacklightConfigData1.FIELDS + (
        BitField(fid=FID.BACKLIGHT_EFFECT, length=LEN.BACKLIGHT_EFFECT,
                 title="BacklightEffect", name="backlight_effect",
                 checks=(CheckHexList(LEN.BACKLIGHT_EFFECT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.BACKLIGHT_EFFECT) - 1),)),
    )
# end class SetBacklightConfigData2


class SetBacklightConfigData3(SetBacklightConfigData2):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetBacklightConfigV3

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Configuration                 8
    Options                       8
    BacklightEffect               8
    CurrentBacklightLevel         8
    CurrDurationHandsOUT          16
    CurrDurationHandsIN           16
    CurrDurationHandsPowered      16
    ============================  ==========
    """

    class FID(SetBacklightConfigData2.FID):
        # See ``SetBacklightConfigData2.FID``
        CURRENT_BACKLIGHT_LEVEL = SetBacklightConfigData2.FID.BACKLIGHT_EFFECT - 1
        CURR_DURATION_HANDS_OUT = CURRENT_BACKLIGHT_LEVEL - 1
        CURR_DURATION_HANDS_IN = CURR_DURATION_HANDS_OUT - 1
        CURR_DURATION_POWERED = CURR_DURATION_HANDS_IN - 1
    # end class FID

    class LEN(SetBacklightConfigData2.LEN):
        # See ``SetBacklightConfigData2.LEN``
        CURRENT_BACKLIGHT_LEVEL = 0x8
        CURR_DURATION_HANDS_OUT = 0x10
        CURR_DURATION_HANDS_IN = 0x10
        CURR_DURATION_POWERED = 0x10
    # end class LEN

    FIELDS = SetBacklightConfigData2.FIELDS + (
        BitField(fid=FID.CURRENT_BACKLIGHT_LEVEL, length=LEN.CURRENT_BACKLIGHT_LEVEL,
                 title="CurrentBacklightLevel", name="current_backlight_level",
                 checks=(CheckHexList(LEN.CURRENT_BACKLIGHT_LEVEL // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CURRENT_BACKLIGHT_LEVEL) - 1),)),
        BitField(fid=FID.CURR_DURATION_HANDS_OUT, length=LEN.CURR_DURATION_HANDS_OUT,
                 title="CurrDurationHandsOut", name="curr_duration_hands_out",
                 checks=(CheckHexList(LEN.CURR_DURATION_HANDS_OUT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CURR_DURATION_HANDS_OUT) - 1),)),
        BitField(fid=FID.CURR_DURATION_HANDS_IN, length=LEN.CURR_DURATION_HANDS_IN,
                 title="CurrDurationHandsIn", name="curr_duration_hands_in",
                 checks=(CheckHexList(LEN.CURR_DURATION_HANDS_IN // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CURR_DURATION_HANDS_IN) - 1),)),
        BitField(fid=FID.CURR_DURATION_POWERED, length=LEN.CURR_DURATION_POWERED,
                 title="CurrDurationPowered", name="curr_duration_powered",
                 checks=(CheckHexList(LEN.CURR_DURATION_POWERED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CURR_DURATION_POWERED) - 1),)),
    )
# end class SetBacklightConfigData3


class SetBacklightConfigData4(SetBacklightConfigData3):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetBacklightConfigV4

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Configuration                 8
    Options                       8
    BacklightEffect               8
    CurrentBacklightLevel         8
    CurrDurationHandsOUT          16
    CurrDurationHandsIN           16
    CurrDurationHandsPowered      16
    CurrDurationHandsNotPowered   16
    ============================  ==========
    """

    class FID(SetBacklightConfigData3.FID):
        # See ``SetBacklightConfigData3.FID``
        CURR_DURATION_NOT_POWERED = SetBacklightConfigData3.FID.CURR_DURATION_POWERED - 1
    # end class FID

    class LEN(SetBacklightConfigData3.LEN):
        # See ``SetBacklightConfigData3.LEN``
        CURR_DURATION_NOT_POWERED = 0x10
    # end class LEN

    FIELDS = SetBacklightConfigData3.FIELDS + (
        BitField(fid=FID.CURR_DURATION_NOT_POWERED, length=LEN.CURR_DURATION_NOT_POWERED,
                 title="CurrDurationNotPowered", name="curr_duration_not_powered",
                 checks=(CheckHexList(LEN.CURR_DURATION_NOT_POWERED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CURR_DURATION_NOT_POWERED) - 1),)),
    )
# end class SetBacklightConfigData4


class GetBacklightInfoResponseData1(Backlight):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetBacklightInfoResponseData2
        - GetBacklightInfoResponseData3
        - GetBacklightInfoResponseV1
        - BacklightInfoEventV1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    NbLevels                      8
    CurrentLevel                  8
    BacklightStatus               8
    ============================  ==========
    """

    class FID(Backlight.FID):
        # See ``Backlight.FID``
        NUMBER_OF_LEVEL = Backlight.FID.SOFTWARE_ID - 1
        CURRENT_LEVEL = NUMBER_OF_LEVEL - 1
        BACKLIGHT_STATUS = CURRENT_LEVEL - 1
    # end class FID

    class LEN(Backlight.LEN):
        # See ``Backlight.LEN``
        NUMBER_OF_LEVEL = 0x8
        CURRENT_LEVEL = 0x8
        BACKLIGHT_STATUS = 0x8
    # end class LEN

    FIELDS = Backlight.FIELDS + (
        BitField(fid=FID.NUMBER_OF_LEVEL, length=LEN.NUMBER_OF_LEVEL,
                 title="NumberOfLevel", name="number_of_level",
                 checks=(CheckHexList(LEN.NUMBER_OF_LEVEL // 8),
                         CheckByte(),)),
        BitField(fid=FID.CURRENT_LEVEL, length=LEN.CURRENT_LEVEL,
                 title="CurrentLevel", name="current_level",
                 checks=(CheckHexList(LEN.CURRENT_LEVEL // 8),
                         CheckByte(),)),
        BitField(fid=FID.BACKLIGHT_STATUS, length=LEN.BACKLIGHT_STATUS,
                 title="BacklightStatus", name="backlight_status",
                 checks=(CheckHexList(LEN.BACKLIGHT_STATUS // 8),
                         CheckByte(),)),
    )
# end class GetBacklightInfoResponseData1


class GetBacklightInfoResponseData2(GetBacklightInfoResponseData1):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetBacklightInfoResponseData3
        - GetBacklightInfoResponseV2
        - BacklightInfoEvent

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    NbLevels                      8
    CurrentLevel                  8
    BacklightStatus               8
    BacklightEffect               8
    ============================  ==========
    """

    class FID(GetBacklightInfoResponseData1.FID):
        # See ``GetBacklightInfoResponseData1.FID``
        BACKLIGHT_EFFECT = GetBacklightInfoResponseData1.FID.BACKLIGHT_STATUS - 1
    # end class FID

    class LEN(GetBacklightInfoResponseData1.LEN):
        # See ``GetBacklightInfoResponseData1.LEN``
        BACKLIGHT_EFFECT = 0x8
    # end class LEN

    FIELDS = GetBacklightInfoResponseData1.FIELDS + (
        BitField(fid=FID.BACKLIGHT_EFFECT, length=LEN.BACKLIGHT_EFFECT,
                 title="BacklightEffect", name="backlight_effect",
                 checks=(CheckHexList(LEN.BACKLIGHT_EFFECT // 8),
                         CheckByte(),)),
    )
# end class GetBacklightInfoResponseData2


class GetBacklightInfoResponseData3(GetBacklightInfoResponseData2):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetBacklightInfoResponseV3

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    NbLevels                      8
    CurrentLevel                  8
    BacklightStatus               8
    BacklightEffect               8
    OOBDurationHandsOUT           16
    OOBDurationHandsIN            16
    OOBDurationPowered            16
    ============================  ==========
    """

    class FID(GetBacklightInfoResponseData2.FID):
        # See ``GetBacklightInfoResponseData2.FID``
        OOB_DURATION_HANDS_OUT = GetBacklightInfoResponseData2.FID.BACKLIGHT_EFFECT - 1
        OOB_DURATION_HANDS_IN = OOB_DURATION_HANDS_OUT - 1
        OOB_DURATION_POWERED = OOB_DURATION_HANDS_IN - 1
    # end class FID

    class LEN(GetBacklightInfoResponseData2.LEN):
        # See ``GetBacklightInfoResponseData2.LEN``
        OOB_DURATION_HANDS_OUT = 0x10
        OOB_DURATION_HANDS_IN = 0x10
        OOB_DURATION_POWERED = 0x10
    # end class LEN

    FIELDS = GetBacklightInfoResponseData2.FIELDS + (
        BitField(fid=FID.OOB_DURATION_HANDS_OUT, length=LEN.OOB_DURATION_HANDS_OUT,
                 title="OobDurationHandsOut", name="oob_duration_hands_out",
                 checks=(CheckHexList(LEN.OOB_DURATION_HANDS_OUT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.OOB_DURATION_HANDS_OUT) - 1),)),
        BitField(fid=FID.OOB_DURATION_HANDS_IN, length=LEN.OOB_DURATION_HANDS_IN,
                 title="OobDurationHandsIn", name="oob_duration_hands_in",
                 checks=(CheckHexList(LEN.OOB_DURATION_HANDS_IN // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.OOB_DURATION_HANDS_IN) - 1),)),
        BitField(fid=FID.OOB_DURATION_POWERED, length=LEN.OOB_DURATION_POWERED,
                 title="OobDurationPowered", name="oob_duration_powered",
                 checks=(CheckHexList(LEN.OOB_DURATION_POWERED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.OOB_DURATION_POWERED) - 1),)),
    )
# end class GetBacklightInfoResponseData3


class GetBacklightInfoResponseData4(GetBacklightInfoResponseData3):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetBacklightInfoResponseV4

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    NbLevels                      8
    CurrentLevel                  8
    BacklightStatus               8
    BacklightEffect               8
    OOBDurationHandsOUT           16
    OOBDurationHandsIN            16
    OOBDurationPowered            16
    OOBDurationNotPowered         16
    ============================  ==========
    """

    class FID(GetBacklightInfoResponseData3.FID):
        # See ``GetBacklightInfoResponseData3.FID``
        OOB_DURATION_NOT_POWERED = GetBacklightInfoResponseData3.FID.OOB_DURATION_POWERED - 1
    # end class FID

    class LEN(GetBacklightInfoResponseData3.LEN):
        # See ``GetBacklightInfoResponseData3.LEN``
        OOB_DURATION_NOT_POWERED = 0x10
    # end class LEN

    FIELDS = GetBacklightInfoResponseData3.FIELDS + (
        BitField(fid=FID.OOB_DURATION_NOT_POWERED, length=LEN.OOB_DURATION_NOT_POWERED,
                 title="OobDurationNotPowered", name="oob_duration_not_powered",
                 checks=(CheckHexList(LEN.OOB_DURATION_NOT_POWERED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.OOB_DURATION_NOT_POWERED) - 1),)),
    )
# end class GetBacklightInfoResponseData4


class ShortEmptyPacketDataFormat(Backlight):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetBacklightConfig
        - GetBacklightInfo

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(Backlight.FID):
        # See ``Backlight.FID``
        PADDING = Backlight.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(Backlight.LEN):
        # See ``Backlight.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = Backlight.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Backlight.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(Backlight):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetBacklightConfigResponse
        - SetBacklightEffectResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(Backlight.FID):
        # See ``Backlight.FID``
        PADDING = Backlight.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(Backlight.LEN):
        # See ``Backlight.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = Backlight.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Backlight.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class GetBacklightConfig(ShortEmptyPacketDataFormat):
    """
    Define ``GetBacklightConfig`` implementation class for version 2
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetBacklightConfigResponseV2.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT, **kwargs)
    # end def __init__
# end class GetBacklightConfig


class GetBacklightConfigResponseV1(GetBacklightConfigResponseData1):
    """
    Define ``GetBacklightConfigResponse`` implementation class for version 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Configuration                 8
    SupportedOptions              16
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetBacklightConfig,)
    VERSION = (1,)
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, configuration, supported_options, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param configuration: Configuration
        :type configuration: ``int`` or ``HexList``
        :param supported_options: Supported Options
        :type supported_options: ``int`` or ``HexList``
        :param backlight_effect_list: Backlight Effect List
        :type backlight_effect_list: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT, **kwargs)
        self.configuration = configuration
        self.supported_options = supported_options
    # end def __init__
# end class GetBacklightConfigResponseV1


class GetBacklightConfigResponseV2(GetBacklightConfigResponseData2):
    """
    Define ``GetBacklightConfigResponse`` implementation class for version 2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Configuration                 8
    SupportedOptions              16
    BacklightEffectList           16
    Reserved                      88
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetBacklightConfig,)
    VERSION = (2,)
    FUNCTION_INDEX = 0

    class FID(GetBacklightConfigResponseData2.FID):
        # See ``GetBacklightInfoData2.FID``
        RESERVED = GetBacklightConfigResponseData2.FID.BACKLIGHT_EFFECT_LIST - 1
    # end class FID

    class LEN(GetBacklightConfigResponseData2.LEN):
        # See ``GetBacklightInfoData2.LEN``
        RESERVED = 0x58
    # end class LEN

    FIELDS = GetBacklightConfigResponseData2.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                 default_value=Backlight.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, configuration, supported_options, backlight_effect_list, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param configuration: Configuration
        :type configuration: ``int`` or ``HexList``
        :param supported_options: Supported Options
        :type supported_options: ``int`` or ``HexList``
        :param backlight_effect_list: Backlight Effect List
        :type backlight_effect_list: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG, **kwargs)
        self.configuration = configuration
        self.supported_options = supported_options
        self.backlight_effect_list = backlight_effect_list
    # end def __init__
# end class GetBacklightConfigResponseV2


class GetBacklightConfigResponseV3(GetBacklightConfigResponseData3):
    """
    Define ``GetBacklightConfigResponse`` implementation class for version 3

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Configuration                 8
    SupportedOptions              16
    BacklightEffectList           16
    CurrentBacklightLevel         8
    CurrDurationHandsOUT          16
    CurrDurationHandsIN           16
    CurrDurationPowered           16
    Reserved                      32
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetBacklightConfig,)
    VERSION = (3,)
    FUNCTION_INDEX = 0

    class FID(GetBacklightConfigResponseData3.FID):
        # See ``GetBacklightConfigResponseData3.FID``
        RESERVED = GetBacklightConfigResponseData3.FID.CURR_DURATION_POWERED - 1
    # end class FID

    class LEN(GetBacklightConfigResponseData3.LEN):
        # See ``GetBacklightConfigResponseData3.LEN``
        RESERVED = 0x20
    # end class LEN

    FIELDS = GetBacklightConfigResponseData3.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                 default_value=Backlight.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, configuration, supported_options, backlight_effect_list,
                 current_backlight_level, curr_duration_hands_out, curr_duration_hands_in, curr_duration_powered,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param configuration: Configuration
        :type configuration: ``int`` or ``HexList``
        :param supported_options: Supported Options
        :type supported_options: ``int`` or ``HexList``
        :param backlight_effect_list: Backlight Effect List
        :type backlight_effect_list: ``int`` or ``HexList``
        :param current_backlight_level: The current backlight brightness level set by the SW or HW in
                                        "Permanent Manual Mode".
        :type current_backlight_level: ``int`` or ``HexList``
        :param curr_duration_hands_out: The needed time to start the FADE-OUT effect after the last keystroke and no
                                        proximity detection.
        :type curr_duration_hands_out: ``int`` or ``HexList``
        :param curr_duration_hands_in: The needed time to start the FADE-OUT effect after the last interaction with
                                       the device while keeping the object/hands in the detection zone.
        :type curr_duration_hands_in: ``int`` or ``HexList``
        :param curr_duration_powered: The needed time to start the FADE-OUT effect after the last interaction with
                                      a device externally powered.
        :type curr_duration_powered: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG, **kwargs)
        self.configuration = configuration
        self.supported_options = supported_options
        self.backlight_effect_list = backlight_effect_list
        self.current_backlight_level = current_backlight_level
        self.curr_duration_hands_out = curr_duration_hands_out
        self.curr_duration_hands_in = curr_duration_hands_in
        self.curr_duration_powered = curr_duration_powered
    # end def __init__
# end class GetBacklightConfigResponseV3


class GetBacklightConfigResponseV4(GetBacklightConfigResponseData4):
    """
    Define ``GetBacklightConfigResponse`` implementation class for version 4

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Configuration                 8
    SupportedOptions              16
    BacklightEffectList           16
    CurrentBacklightLevel         8
    CurrDurationHandsOUT          16
    CurrDurationHandsIN           16
    CurrDurationPowered           16
    CurrDurationNotPowered        16
    Reserved                      16
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetBacklightConfig,)
    VERSION = (4,)
    FUNCTION_INDEX = 0

    class FID(GetBacklightConfigResponseData4.FID):
        # See ``GetBacklightConfigResponseData4.FID``
        RESERVED = GetBacklightConfigResponseData4.FID.CURR_DURATION_NOT_POWERED - 1
    # end class FID

    class LEN(GetBacklightConfigResponseData4.LEN):
        # See ``GetBacklightConfigResponseData4.LEN``
        RESERVED = 0x10
    # end class LEN

    FIELDS = GetBacklightConfigResponseData4.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                 default_value=Backlight.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, configuration, supported_options, backlight_effect_list,
                 current_backlight_level, curr_duration_hands_out, curr_duration_hands_in, curr_duration_powered,
                 curr_duration_not_powered, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param configuration: Configuration
        :type configuration: ``int`` or ``HexList``
        :param supported_options: Supported Options
        :type supported_options: ``int`` or ``HexList``
        :param backlight_effect_list: Backlight Effect List
        :type backlight_effect_list: ``int`` or ``HexList``
        :param current_backlight_level: The current backlight brightness level set by the SW or HW in
                                        "Permanent Manual Mode".
        :type current_backlight_level: ``int`` or ``HexList``
        :param curr_duration_hands_out: The needed time to start the FADE-OUT effect after the last keystroke and no
                                        proximity detection.
        :type curr_duration_hands_out: ``int`` or ``HexList``
        :param curr_duration_hands_in: The needed time to start the FADE-OUT effect after the last interaction with
                                       the device while keeping the object/hands in the detection zone.
        :type curr_duration_hands_in: ``int`` or ``HexList``
        :param curr_duration_powered: The needed time to start the FADE-OUT effect after the last interaction with
                                      a device externally powered.
        :type curr_duration_powered: ``int`` or ``HexList``
        :param curr_duration_not_powered: The needed time to start the FADE-OUT effect after the last interaction with
                                          a not externally powered device which has no proximity sensor.
        :type curr_duration_not_powered: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG, **kwargs)
        self.configuration = configuration
        self.supported_options = supported_options
        self.backlight_effect_list = backlight_effect_list
        self.current_backlight_level = current_backlight_level
        self.curr_duration_hands_out = curr_duration_hands_out
        self.curr_duration_hands_in = curr_duration_hands_in
        self.curr_duration_powered = curr_duration_powered
        self.curr_duration_not_powered = curr_duration_not_powered
    # end def __init__
# end class GetBacklightConfigResponseV4


class SetBacklightConfigV1(SetBacklightConfigData1):
    """
    Define ``SetBacklightConfig`` implementation class for version 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Configuration                 8
    Options                       8
    Padding                       8
    ============================  ==========
    """

    class FID(SetBacklightConfigData1.FID):
        # See ``SetBacklightInfoData1.FID``
        PADDING = SetBacklightConfigData1.FID.OPTIONS - 1
    # end class FID

    class LEN(SetBacklightConfigData1.LEN):
        # See ``SetBacklightInfoData1.LEN``
        PADDING = 0x8
    # end class LEN

    FIELDS = SetBacklightConfigData1.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Backlight.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, configuration, options, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param configuration: Configuration
        :type configuration: ``int`` or ``HexList``
        :param options: Options
        :type options: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetBacklightConfigResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT, **kwargs)
        self.configuration = configuration
        self.options = options
    # end def __init__
# end class SetBacklightConfigV1


class SetBacklightConfigV2(SetBacklightConfigData2):
    """
    Define ``SetBacklightConfig`` implementation class for version 2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Configuration                 8
    Options                       8
    BacklightEffect               8
    ============================  ==========
    """

    def __init__(self, device_index, feature_index, configuration, options, backlight_effect, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param configuration: Configuration
        :type configuration: ``int`` or ``HexList``
        :param options: Options
        :type options: ``int`` or ``HexList``
        :param backlight_effect: Backlight Effect
        :type backlight_effect: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetBacklightConfigResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT, **kwargs)
        self.configuration = configuration
        self.options = options
        self.backlight_effect = backlight_effect
    # end def __init__
# end class SetBacklightConfigV2


class SetBacklightConfigV3(SetBacklightConfigData3):
    """
    Define ``SetBacklightConfig`` implementation class for version 3

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Configuration                 8
    Options                       8
    BacklightEffect               8
    CurrentBacklightLevel         8
    CurrDurationHandsOUT          16
    CurrDurationHandsIN           16
    CurrDurationHandsPowered      16
    Padding                       48
    ============================  ==========
    """

    class FID(SetBacklightConfigData3.FID):
        # See ``SetBacklightInfoData3.FID``
        PADDING = SetBacklightConfigData3.FID.CURR_DURATION_POWERED - 1
    # end class FID

    class LEN(SetBacklightConfigData3.LEN):
        # See ``SetBacklightInfoData3.LEN``
        PADDING = 0x30
    # end class LEN

    FIELDS = SetBacklightConfigData3.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Backlight.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, configuration, options, backlight_effect, current_backlight_level,
                 curr_duration_hands_out, curr_duration_hands_in, curr_duration_powered, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param configuration: Configuration
        :type configuration: ``int`` or ``HexList``
        :param options: Options
        :type options: ``int`` or ``HexList``
        :param backlight_effect: Backlight Effect
        :type backlight_effect: ``int`` or ``HexList``
        :param current_backlight_level: The current backlight brightness level set by the SW or HW in
                                        "Permanent Manual Mode".
        :type current_backlight_level: ``int`` or ``HexList``
        :param curr_duration_hands_out: The needed time to start the FADE-OUT effect after the last keystroke and no
                                        proximity detection.
        :type curr_duration_hands_out: ``int`` or ``HexList``
        :param curr_duration_hands_in: The needed time to start the FADE-OUT effect after the last interaction with
                                       the device while keeping the object/hands in the detection zone.
        :type curr_duration_hands_in: ``int`` or ``HexList``
        :param curr_duration_powered: The needed time to start the FADE-OUT effect after the last interaction with
                                      a device externally powered.
        :type curr_duration_powered: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetBacklightConfigResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG, **kwargs)
        self.configuration = configuration
        self.options = options
        self.backlight_effect = backlight_effect
        self.current_backlight_level = current_backlight_level
        self.curr_duration_hands_out = curr_duration_hands_out
        self.curr_duration_hands_in = curr_duration_hands_in
        self.curr_duration_powered = curr_duration_powered
    # end def __init__
# end class SetBacklightConfigV3


class SetBacklightConfigV4(SetBacklightConfigData4):
    """
    Define ``SetBacklightConfig`` implementation class for version 4

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Configuration                 8
    Options                       8
    BacklightEffect               8
    CurrentBacklightLevel         8
    CurrDurationHandsOUT          16
    CurrDurationHandsIN           16
    CurrDurationHandsPowered      16
    CurrDurationHandsNotPowered   16
    Padding                       32
    ============================  ==========
    """

    class FID(SetBacklightConfigData4.FID):
        # See ``SetBacklightInfoData3.FID``
        PADDING = SetBacklightConfigData4.FID.CURR_DURATION_NOT_POWERED - 1
    # end class FID

    class LEN(SetBacklightConfigData4.LEN):
        # See ``SetBacklightInfoData3.LEN``
        PADDING = 0x20
    # end class LEN

    FIELDS = SetBacklightConfigData4.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Backlight.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, configuration, options, backlight_effect, current_backlight_level,
                 curr_duration_hands_out, curr_duration_hands_in, curr_duration_powered, curr_duration_not_powered,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param configuration: Configuration
        :type configuration: ``int`` or ``HexList``
        :param options: Options
        :type options: ``int`` or ``HexList``
        :param backlight_effect: Backlight Effect
        :type backlight_effect: ``int`` or ``HexList``
        :param current_backlight_level: The current backlight brightness level set by the SW or HW in
                                        "Permanent Manual Mode".
        :type current_backlight_level: ``int`` or ``HexList``
        :param curr_duration_hands_out: The needed time to start the FADE-OUT effect after the last keystroke and no
                                        proximity detection.
        :type curr_duration_hands_out: ``int`` or ``HexList``
        :param curr_duration_hands_in: The needed time to start the FADE-OUT effect after the last interaction with
                                       the device while keeping the object/hands in the detection zone.
        :type curr_duration_hands_in: ``int`` or ``HexList``
        :param curr_duration_powered: The needed time to start the FADE-OUT effect after the last interaction with
                                      a device externally powered.
        :type curr_duration_powered: ``int`` or ``HexList``
        :param curr_duration_not_powered: The needed time to start the FADE-OUT effect after the last interaction with
                                          a not externally powered device which has no proximity sensor.
        :type curr_duration_not_powered: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetBacklightConfigResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG, **kwargs)
        self.configuration = configuration
        self.options = options
        self.backlight_effect = backlight_effect
        self.current_backlight_level = current_backlight_level
        self.curr_duration_hands_out = curr_duration_hands_out
        self.curr_duration_hands_in = curr_duration_hands_in
        self.curr_duration_powered = curr_duration_powered
        self.curr_duration_not_powered = curr_duration_not_powered
    # end def __init__
# end class SetBacklightConfigV4


class SetBacklightConfigResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetBacklightConfigResponse`` implementation class for version 2, 3 and 4
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetBacklightConfigV2,)
    VERSION = (1, 2, 3, 4)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG, **kwargs)
    # end def __init__
# end class SetBacklightConfigResponse


class GetBacklightInfo(ShortEmptyPacketDataFormat):
    """
    Define ``GetBacklightInfo`` implementation class for version 2
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetBacklightInfoResponseV2.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT, **kwargs)
    # end def __init__
# end class GetBacklightInfo


class GetBacklightInfoResponseV1(GetBacklightInfoResponseData1):
    """
    Define ``GetBacklightInfoResponse`` implementation class for version 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    NbLevels                      8
    CurrentLevel                  8
    BacklightStatus               8
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetBacklightInfo,)
    VERSION = (1,)
    FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, number_of_level, current_level, backlight_status, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param number_of_level: Number of levels
        :type number_of_level: ``int`` or ``HexList``
        :param current_level: Current Level
        :type current_level: ``int`` or ``HexList``
        :param backlight_status: Backlight Status
        :type backlight_status: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT, **kwargs)
        self.number_of_level = number_of_level
        self.current_level = current_level
        self.backlight_status = backlight_status
    # end def __init__
# end class GetBacklightInfoResponseV1


class GetBacklightInfoResponseV2(GetBacklightInfoResponseData2):
    """
    Define ``GetBacklightInfoResponse`` implementation class for version 2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    NbLevels                      8
    CurrentLevel                  8
    BacklightStatus               8
    BacklightEffect               8
    Reserved                      96
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetBacklightInfo,)
    VERSION = (2,)
    FUNCTION_INDEX = 2

    class FID(GetBacklightInfoResponseData2.FID):
        # See ``GetBacklightInfoResponseData2.FID``
        RESERVED = GetBacklightInfoResponseData2.FID.BACKLIGHT_EFFECT - 1
    # end class FID

    class LEN(GetBacklightInfoResponseData2.LEN):
        # See ``GetBacklightInfoResponseData2.LEN``
        RESERVED = 0x60
    # end class LEN

    FIELDS = GetBacklightInfoResponseData2.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                 default_value=Backlight.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, number_of_level, current_level, backlight_status, backlight_effect,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param number_of_level: Number of levels
        :type number_of_level: ``int`` or ``HexList``
        :param current_level: Current Level
        :type current_level: ``int`` or ``HexList``
        :param backlight_status: Backlight Status
        :type backlight_status: ``int`` or ``HexList``
        :param backlight_effect: Backlight Effect
        :type backlight_effect: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG, **kwargs)
        self.number_of_level = number_of_level
        self.current_level = current_level
        self.backlight_status = backlight_status
        self.backlight_effect = backlight_effect
    # end def __init__
# end class GetBacklightInfoResponseV2


class GetBacklightInfoResponseV3(GetBacklightInfoResponseData3):
    """
    Define ``GetBacklightInfoResponse`` implementation class for version 3

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    NbLevels                      8
    CurrentLevel                  8
    BacklightStatus               8
    BacklightEffect               8
    OOBDurationHandsOUT           16
    OOBDurationHandsIN            16
    OOBDurationPowered            16
    Reserved                      48
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetBacklightInfo,)
    VERSION = (3,)
    FUNCTION_INDEX = 2

    class FID(GetBacklightInfoResponseData3.FID):
        # See ``GetBacklightInfoResponseData3.FID``
        RESERVED = GetBacklightInfoResponseData3.FID.OOB_DURATION_POWERED - 1
    # end class FID

    class LEN(GetBacklightInfoResponseData3.LEN):
        # See ``GetBacklightInfoResponseData3.LEN``
        RESERVED = 0x30
    # end class LEN

    FIELDS = GetBacklightInfoResponseData3.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                 default_value=Backlight.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, number_of_level, current_level, backlight_status, backlight_effect,
                 oob_duration_hands_out, oob_duration_hands_in, oob_duration_powered, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param number_of_level: Number of levels
        :type number_of_level: ``int`` or ``HexList``
        :param current_level: Current Level
        :type current_level: ``int`` or ``HexList``
        :param backlight_status: Backlight Status
        :type backlight_status: ``int`` or ``HexList``
        :param backlight_effect: Backlight Effect
        :type backlight_effect: ``int`` or ``HexList``
        :param oob_duration_hands_out: The default OOB duration when hands are OUT of the detection zone.
        :type oob_duration_hands_out: ``int`` or ``HexList``
        :param oob_duration_hands_in: The default OOB duration when hands are IN the detection zone.
        :type oob_duration_hands_in: ``int`` or ``HexList``
        :param oob_duration_powered: The default OOB duration when hands are IN the detection zone.
        :type oob_duration_powered: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG, **kwargs)
        self.number_of_level = number_of_level
        self.current_level = current_level
        self.backlight_status = backlight_status
        self.backlight_effect = backlight_effect
        self.oob_duration_hands_out = oob_duration_hands_out
        self.oob_duration_hands_in = oob_duration_hands_in
        self.oob_duration_powered = oob_duration_powered
    # end def __init__
# end class GetBacklightInfoResponseV3


class GetBacklightInfoResponseV4(GetBacklightInfoResponseData4):
    """
    Define ``GetBacklightInfoResponse`` implementation class for version 4

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    NbLevels                      8
    CurrentLevel                  8
    BacklightStatus               8
    BacklightEffect               8
    OOBDurationHandsOUT           16
    OOBDurationHandsIN            16
    OOBDurationPowered            16
    OOBDurationNotPowered         16
    Reserved                      32
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetBacklightInfo,)
    VERSION = (4,)
    FUNCTION_INDEX = 2

    class FID(GetBacklightInfoResponseData4.FID):
        # See ``GetBacklightInfoResponseData4.FID``
        RESERVED = GetBacklightInfoResponseData4.FID.OOB_DURATION_NOT_POWERED - 1
    # end class FID

    class LEN(GetBacklightInfoResponseData4.LEN):
        # See ``GetBacklightInfoResponseData4.LEN``
        RESERVED = 0x20
    # end class LEN

    FIELDS = GetBacklightInfoResponseData4.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                 default_value=Backlight.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, number_of_level, current_level, backlight_status, backlight_effect,
                 oob_duration_hands_out, oob_duration_hands_in, oob_duration_powered, oob_duration_not_powered,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param number_of_level: Number of levels
        :type number_of_level: ``int`` or ``HexList``
        :param current_level: Current Level
        :type current_level: ``int`` or ``HexList``
        :param backlight_status: Backlight Status
        :type backlight_status: ``int`` or ``HexList``
        :param backlight_effect: Backlight Effect
        :type backlight_effect: ``int`` or ``HexList``
        :param oob_duration_hands_out: The default OOB duration when hands are OUT of the detection zone.
        :type oob_duration_hands_out: ``int`` or ``HexList``
        :param oob_duration_hands_in: The default OOB duration when hands are IN the detection zone.
        :type oob_duration_hands_in: ``int`` or ``HexList``
        :param oob_duration_powered: The default OOB duration when device is powered.
        :type oob_duration_powered: ``int`` or ``HexList``
        :param oob_duration_not_powered: The default OOB duration when device is not powered.
        :type oob_duration_not_powered: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG, **kwargs)
        self.number_of_level = number_of_level
        self.current_level = current_level
        self.backlight_status = backlight_status
        self.backlight_effect = backlight_effect
        self.oob_duration_hands_out = oob_duration_hands_out
        self.oob_duration_hands_in = oob_duration_hands_in
        self.oob_duration_powered = oob_duration_powered
        self.oob_duration_not_powered = oob_duration_not_powered
    # end def __init__
# end class GetBacklightInfoResponseV4


class SetBacklightEffect(Backlight):
    """
    Define ``SetBacklightEffect`` implementation class for version 2 and 3

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    BacklightEffect               8
    Padding                       16
    ============================  ==========
    """

    class FID(Backlight.FID):
        # See ``Backlight.FID``
        BACKLIGHT_EFFECT = Backlight.FID.SOFTWARE_ID - 1
        PADDING = BACKLIGHT_EFFECT - 1
    # end class FID

    class LEN(Backlight.LEN):
        # See ``Backlight.LEN``
        BACKLIGHT_EFFECT = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = Backlight.FIELDS + (
        BitField(fid=FID.BACKLIGHT_EFFECT, length=LEN.BACKLIGHT_EFFECT,
                 title="BacklightEffect", name="backlight_effect",
                 checks=(CheckHexList(LEN.BACKLIGHT_EFFECT // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Backlight.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, backlight_effect, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param backlight_effect: Backlight Effect
        :type backlight_effect: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetBacklightEffectResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT, **kwargs)
        self.backlight_effect = backlight_effect
    # end def __init__
# end class SetBacklightEffect


class SetBacklightEffectResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetBacklightEffectResponse`` implementation class for version 2, 3 and 4
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetBacklightEffect,)
    VERSION = (2, 3, 4)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG, **kwargs)
    # end def __init__
# end class SetBacklightEffectResponse


class BacklightInfoEventV1(GetBacklightInfoResponseData1):
    """
    Define ``BacklightInfoEvent`` implementation class for version 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    NbLevels                      8
    CurrentLevel                  8
    BacklightStatus               8
    ============================  ==========
    """

    MSG_TYPE = TYPE.EVENT
    VERSION = (1,)
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, number_of_level, current_level, backlight_status, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param number_of_level: Number of levels
        :type number_of_level: ``int`` or ``HexList``
        :param current_level: Current Level
        :type current_level: ``int`` or ``HexList``
        :param backlight_status: Backlight Status
        :type backlight_status: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT, **kwargs)
        self.number_of_level = number_of_level
        self.current_level = current_level
        self.backlight_status = backlight_status
    # end def __init__
# end class BacklightInfoEventV1


class BacklightInfoEventV2ToV4(GetBacklightInfoResponseData2):
    """
    Define ``BacklightInfoEvent`` implementation class for version 2, 3 and 4

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    NbLevels                      8
    CurrentLevel                  8
    BacklightStatus               8
    BacklightEffect               8
    Reserved                      96
    ============================  ==========
    """

    MSG_TYPE = TYPE.EVENT
    VERSION = (2, 3, 4)
    FUNCTION_INDEX = 0

    class FID(GetBacklightInfoResponseData2.FID):
        # See ``GetBacklightInfoResponseData2.FID``
        RESERVED = GetBacklightInfoResponseData2.FID.BACKLIGHT_EFFECT - 1
    # end class FID

    class LEN(GetBacklightInfoResponseData2.LEN):
        # See ``GetBacklightInfoResponseData2.LEN``
        RESERVED = 0x60
    # end class LEN

    FIELDS = GetBacklightInfoResponseData2.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                 default_value=Backlight.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, number_of_level, current_level, backlight_status, backlight_effect,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param number_of_level: Number Of Level
        :type number_of_level: ``int`` or ``HexList``
        :param current_level: Current Level
        :type current_level: ``int`` or ``HexList``
        :param backlight_status: Backlight Status
        :type backlight_status: ``int`` or ``HexList``
        :param backlight_effect: Backlight Effect
        :type backlight_effect: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG, **kwargs)
        self.number_of_level = number_of_level
        self.current_level = current_level
        self.backlight_status = backlight_status
        self.backlight_effect = backlight_effect
    # end def __init__
# end class BacklightInfoEventV2ToV4

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
