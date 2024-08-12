#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.gaming.rgbeffects
:brief: HID++ 2.0 ``RGBEffects`` command interface definition
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/11/03
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import time
from abc import ABC
from enum import IntEnum
from enum import unique

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
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RGBEffects(HidppMessage):
    """
    Manage RGB effects configurations and play
    """
    FEATURE_ID = 0x8071
    MAX_FUNCTION_INDEX_V0_TO_V3 = 8
    MAX_FUNCTION_INDEX_V4 = 9

    class DEFAULT(HidppMessage.DEFAULT):
        """
        Fields Default values
        """
        OPTION = 0
    # end class DEFAULT

    class RGBEffectID:
        """
        RGB Effect ID
        """
        # V2 to V3
        DISABLED = 0x0000
        FIXED = 0x0001
        PULSING_BREATHING = 0x0002
        CYCLING = 0x0003
        COLOR_WAVE = 0x0004
        STARLIGHT = 0x0005
        LIGHT_ON_PRESS = 0x0006
        AUDIO_VISUALIZER = 0x0007
        BOOT_UP = 0x0008
        DEMO_MODE = 0x0009
        PULSING_BREATHING_WAVEFORM = 0x000A
        RIPPLE = 0x000B
        CUSTOM_ONBOARD_STORED = 0x000C
        KITT_LIGHTING = 0x000D
        COLOR_DECOMPOSITION = 0x000E
        SNIPE_PULSE_CYAN_PINK = 0x000F
        NEURAL_WAVE_CYAN_PINK = 0x0010
        SNIPE_PULSE_CONFIGURABLE_COLOR = 0x0011
        NEURAL_WAVE_CONFIGURABLE_COLOR = 0x0012
        HOST_STREAMING = 0x0013
        HSV_PULSING_BREATHING = 0x0014
        COLOR_CYCLING_CONFIGURABLE_S = 0x0015
        COLOR_WAVE_CONFIGURABLE_S = 0x0016
        RIPPLE_CONFIGURATION_S = 0x0017
        SMOOTH_STAR_BREATHING = 0x0018
        SMOOTH_WAVE = 0x0019

        # V4
        FRAME_BASED_SIGNATURE_EFFECT_ACTIVE = 0x000F
        FRAME_BASED_SIGNATURE_EFFECT_PASSIVE = 0x0010
        FORMULA_BASED_SIGNATURE_EFFECT_ACTIVE = 0x0018
        FORMULA_BASED_SIGNATURE_EFFECT_PASSIVE = 0x0019
    # end class RGBEffectID

    class NvCapability:
        """
        Supported RGB effects in non-volatile capability
        """
        BOOT_UP_EFFECT = 0x0001
        DEMO = 0x0002
        USER_DEMO_MODE = 0x0004
        EVENTS_DISPLAY = 0x0008
        ACTIVE_DIMMING = 0x0010
        RAMP_DOWN_TO_OFF = 0x0020
        SHUTDOWN_EFFECT = 0x0040
    # en class NvCapability

    class CapabilityState:
        """
        The possible state of NvCapability
        """
        NO_CHANGE = 0
        ENABLED = 1
        DISABLED = 2
    # end class CapabilityState

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(deviceIndex=device_index, featureIndex=feature_index, **kwargs)
    # end def __init__
# end class RGBEffects


class RGBEffectsModel(FeatureModel):
    """
    ``RGBEffects`` feature model
    """
    class INDEX(object):
        """
        Function/Event index
        """
        # Function index
        GET_INFO = 0
        SET_RGB_CLUSTER_EFFECT = 1
        SET_MULTI_LED_RGB_CLUSTER_PATTERN = 2
        MANAGE_NV_CONFIG = 3
        MANAGE_RGB_LED_BIN_INFO = 4
        MANAGE_SW_CONTROL = 5
        SET_EFFECT_SYNC_CORRECTION = 6
        MANAGE_RGB_POWER_MODE_CONFIG = 7
        MANAGE_RGB_POWER_MODE = 8
        SHUTDOWN = 9

        # Event index
        EFFECT_SYNC = 0
        USER_ACTIVITY = 1
        RGB_CLUSTER_CHANGED_EVENT = 2
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        ``RGBEffects`` feature data model
        """
        return {
            "feature_base": RGBEffects,
            "versions": {
                RGBEffectsV0.VERSION: {
                    "main_cls": RGBEffectsV0,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_INFO: {
                                "request": GetInfoV0,
                                "response": GetInfoResponse
                            },
                            cls.INDEX.SET_RGB_CLUSTER_EFFECT: {
                                "request": SetRgbClusterEffectV0,
                                "response": SetRgbClusterEffectResponse
                            },
                            cls.INDEX.SET_MULTI_LED_RGB_CLUSTER_PATTERN: {
                                "request": SetMultiLedRgbClusterPattern,
                                "response": SetMultiLedRgbClusterPatternResponse
                            },
                            cls.INDEX.MANAGE_NV_CONFIG: {
                                "request": ManageNvConfigV0ToV2,
                                "response": ManageNvConfigResponseV0ToV2
                            },
                            cls.INDEX.MANAGE_RGB_LED_BIN_INFO: {
                                "request": ManageRgbLedBinInfo,
                                "response": ManageRgbLedBinInfoResponse
                            },
                            cls.INDEX.MANAGE_SW_CONTROL: {
                                "request": ManageSWControl,
                                "response": ManageSWControlResponse
                            },
                            cls.INDEX.SET_EFFECT_SYNC_CORRECTION: {
                                "request": SetEffectSyncCorrection,
                                "response": SetEffectSyncCorrectionResponse
                            },
                            cls.INDEX.MANAGE_RGB_POWER_MODE_CONFIG: {
                                "request": ManageRgbPowerModeConfig,
                                "response": ManageRgbPowerModeConfigResponse
                            },
                            cls.INDEX.MANAGE_RGB_POWER_MODE: {
                                "request": ManageRgbPowerMode,
                                "response": ManageRgbPowerModeResponse
                            }
                        },
                        "events": {
                            cls.INDEX.EFFECT_SYNC: {
                                "report": EffectSyncEvent
                            },
                            cls.INDEX.USER_ACTIVITY: {
                                "report": UserActivityEvent
                            }
                        }
                    }
                },
                RGBEffectsV1.VERSION: {
                    "main_cls": RGBEffectsV1,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_INFO: {
                                "request": GetInfoV1ToV4,
                                "response": GetInfoResponse
                            },
                            cls.INDEX.SET_RGB_CLUSTER_EFFECT: {
                                "request": SetRgbClusterEffectV1ToV4,
                                "response": SetRgbClusterEffectResponse
                            },
                            cls.INDEX.SET_MULTI_LED_RGB_CLUSTER_PATTERN: {
                                "request": SetMultiLedRgbClusterPattern,
                                "response": SetMultiLedRgbClusterPatternResponse
                            },
                            cls.INDEX.MANAGE_NV_CONFIG: {
                                "request": ManageNvConfigV0ToV2,
                                "response": ManageNvConfigResponseV0ToV2
                            },
                            cls.INDEX.MANAGE_RGB_LED_BIN_INFO: {
                                "request": ManageRgbLedBinInfo,
                                "response": ManageRgbLedBinInfoResponse
                            },
                            cls.INDEX.MANAGE_SW_CONTROL: {
                                "request": ManageSWControl,
                                "response": ManageSWControlResponse
                            },
                            cls.INDEX.SET_EFFECT_SYNC_CORRECTION: {
                                "request": SetEffectSyncCorrection,
                                "response": SetEffectSyncCorrectionResponse
                            },
                            cls.INDEX.MANAGE_RGB_POWER_MODE_CONFIG: {
                                "request": ManageRgbPowerModeConfig,
                                "response": ManageRgbPowerModeConfigResponse
                            },
                            cls.INDEX.MANAGE_RGB_POWER_MODE: {
                                "request": ManageRgbPowerMode,
                                "response": ManageRgbPowerModeResponse
                            }
                        },
                        "events": {
                            cls.INDEX.EFFECT_SYNC: {
                                "report": EffectSyncEvent
                            },
                            cls.INDEX.USER_ACTIVITY: {
                                "report": UserActivityEvent
                            }
                        }
                    }
                },
                RGBEffectsV2.VERSION: {
                    "main_cls": RGBEffectsV2,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_INFO: {
                                "request": GetInfoV1ToV4,
                                "response": GetInfoResponse
                            },
                            cls.INDEX.SET_RGB_CLUSTER_EFFECT: {
                                "request": SetRgbClusterEffectV1ToV4,
                                "response": SetRgbClusterEffectResponse
                            },
                            cls.INDEX.SET_MULTI_LED_RGB_CLUSTER_PATTERN: {
                                "request": SetMultiLedRgbClusterPattern,
                                "response": SetMultiLedRgbClusterPatternResponse
                            },
                            cls.INDEX.MANAGE_NV_CONFIG: {
                                "request": ManageNvConfigV0ToV2,
                                "response": ManageNvConfigResponseV0ToV2
                            },
                            cls.INDEX.MANAGE_RGB_LED_BIN_INFO: {
                                "request": ManageRgbLedBinInfo,
                                "response": ManageRgbLedBinInfoResponse
                            },
                            cls.INDEX.MANAGE_SW_CONTROL: {
                                "request": ManageSWControl,
                                "response": ManageSWControlResponse
                            },
                            cls.INDEX.SET_EFFECT_SYNC_CORRECTION: {
                                "request": SetEffectSyncCorrection,
                                "response": SetEffectSyncCorrectionResponse
                            },
                            cls.INDEX.MANAGE_RGB_POWER_MODE_CONFIG: {
                                "request": ManageRgbPowerModeConfig,
                                "response": ManageRgbPowerModeConfigResponse
                            },
                            cls.INDEX.MANAGE_RGB_POWER_MODE: {
                                "request": ManageRgbPowerMode,
                                "response": ManageRgbPowerModeResponse
                            }
                        },
                        "events": {
                            cls.INDEX.EFFECT_SYNC: {
                                "report": EffectSyncEvent
                            },
                            cls.INDEX.USER_ACTIVITY: {
                                "report": UserActivityEvent
                            }
                        }
                    }
                },
                RGBEffectsV3.VERSION: {
                    "main_cls": RGBEffectsV3,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_INFO: {
                                "request": GetInfoV1ToV4,
                                "response": GetInfoResponse
                            },
                            cls.INDEX.SET_RGB_CLUSTER_EFFECT: {
                                "request": SetRgbClusterEffectV1ToV4,
                                "response": SetRgbClusterEffectResponse
                            },
                            cls.INDEX.SET_MULTI_LED_RGB_CLUSTER_PATTERN: {
                                "request": SetMultiLedRgbClusterPattern,
                                "response": SetMultiLedRgbClusterPatternResponse
                            },
                            cls.INDEX.MANAGE_NV_CONFIG: {
                                "request": ManageNvConfigV3ToV4,
                                "response": ManageNvConfigResponseV3ToV4
                            },
                            cls.INDEX.MANAGE_RGB_LED_BIN_INFO: {
                                "request": ManageRgbLedBinInfo,
                                "response": ManageRgbLedBinInfoResponse
                            },
                            cls.INDEX.MANAGE_SW_CONTROL: {
                                "request": ManageSWControl,
                                "response": ManageSWControlResponse
                            },
                            cls.INDEX.SET_EFFECT_SYNC_CORRECTION: {
                                "request": SetEffectSyncCorrection,
                                "response": SetEffectSyncCorrectionResponse
                            },
                            cls.INDEX.MANAGE_RGB_POWER_MODE_CONFIG: {
                                "request": ManageRgbPowerModeConfig,
                                "response": ManageRgbPowerModeConfigResponse
                            },
                            cls.INDEX.MANAGE_RGB_POWER_MODE: {
                                "request": ManageRgbPowerMode,
                                "response": ManageRgbPowerModeResponse
                            }
                        },
                        "events": {
                            cls.INDEX.EFFECT_SYNC: {
                                "report": EffectSyncEvent
                            },
                            cls.INDEX.USER_ACTIVITY: {
                                "report": UserActivityEvent
                            }
                        }
                    }
                },
                RGBEffectsV4.VERSION: {
                    "main_cls": RGBEffectsV4,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_INFO: {
                                "request": GetInfoV1ToV4,
                                "response": GetInfoResponse
                            },
                            cls.INDEX.SET_RGB_CLUSTER_EFFECT: {
                                "request": SetRgbClusterEffectV1ToV4,
                                "response": SetRgbClusterEffectResponse
                            },
                            cls.INDEX.SET_MULTI_LED_RGB_CLUSTER_PATTERN: {
                                "request": SetMultiLedRgbClusterPattern,
                                "response": SetMultiLedRgbClusterPatternResponse
                            },
                            cls.INDEX.MANAGE_NV_CONFIG: {
                                "request": ManageNvConfigV3ToV4,
                                "response": ManageNvConfigResponseV3ToV4
                            },
                            cls.INDEX.MANAGE_RGB_LED_BIN_INFO: {
                                "request": ManageRgbLedBinInfo,
                                "response": ManageRgbLedBinInfoResponse
                            },
                            cls.INDEX.MANAGE_SW_CONTROL: {
                                "request": ManageSWControl,
                                "response": ManageSWControlResponse
                            },
                            cls.INDEX.SET_EFFECT_SYNC_CORRECTION: {
                                "request": SetEffectSyncCorrection,
                                "response": SetEffectSyncCorrectionResponse
                            },
                            cls.INDEX.MANAGE_RGB_POWER_MODE_CONFIG: {
                                "request": ManageRgbPowerModeConfig,
                                "response": ManageRgbPowerModeConfigResponse
                            },
                            cls.INDEX.MANAGE_RGB_POWER_MODE: {
                                "request": ManageRgbPowerMode,
                                "response": ManageRgbPowerModeResponse
                            },
                            cls.INDEX.SHUTDOWN: {
                                "request": Shutdown,
                                "response": ShutdownResponse
                            }
                        },
                        "events": {
                            cls.INDEX.EFFECT_SYNC: {
                                "report": EffectSyncEvent
                            },
                            cls.INDEX.USER_ACTIVITY: {
                                "report": UserActivityEvent
                            },
                            cls.INDEX.RGB_CLUSTER_CHANGED_EVENT: {
                                "report": RgbClusterChangedEvent
                            }
                        }
                    }
                }
            }
        }
    # end def _get_data_model
# end class RGBEffectsModel


class RGBEffectsFactory(FeatureFactory):
    """
    Factory which creates a ``RGBEffects`` object from a given version
    """
    @staticmethod
    def create(version):
        """
        ``RGBEffects`` object creation from version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``RGBEffectsInterface``
        """
        return RGBEffectsModel.get_main_cls(version)()
    # end def create
# end class RGBEffectsFactory


class RGBEffectsInterface(FeatureInterface, ABC):
    """
    Defines required interfaces for ``RGBEffects`` classes
    """
    def __init__(self):
        # Requests
        self.get_info_cls = None
        self.set_rgb_cluster_effect_cls = None
        self.set_multi_led_rgb_cluster_pattern_cls = None
        self.manage_nv_config_cls = None
        self.manage_rgb_led_bin_info_cls = None
        self.manage_sw_control_cls = None
        self.set_effect_sync_correction_cls = None
        self.manage_rgb_power_mode_config_cls = None
        self.manage_rgb_power_mode_cls = None
        self.shutdown_cls = None

        # Responses
        self.get_info_response_cls = None
        self.set_rgb_cluster_effect_response_cls = None
        self.set_multi_led_rgb_cluster_pattern_response_cls = None
        self.manage_nv_config_response_cls = None
        self.manage_rgb_led_bin_info_response_cls = None
        self.manage_sw_control_response_cls = None
        self.set_effect_sync_correction_response_cls = None
        self.manage_rgb_power_mode_config_response_cls = None
        self.manage_rgb_power_mode_response_cls = None
        self.shutdown_response_cls = None

        # Events
        self.effect_sync_event_cls = None
        self.user_activity_event_cls = None
        self.rgb_cluster_changed_event_cls = None
    # end def __init__

    def get_effect_dictionary(self):
        """
        Get the effect dictionary for the current feature version
        """
        raise NotImplementedError("Effect dictionary getter is not implemented in current version")
    # end def get_effect_dictionary
# end class RGBEffectsInterface


class RGBEffectsV0(RGBEffectsInterface):
    """
    ``RGBEffectsV0``

    This feature provides model and unit specific information for version 0

    [0] getInfo(rgbClusterIndex, rgbClusterEffectIndex) -> rgbClusterIndex, rgbClusterEffectIndex, param1..14

    [1] setRgbClusterEffect(rgbClusterIndex, rgbClusterEffectIndex, param1..10, persistence) -> None

    [2] setMultiLedRgbClusterPattern(rgbClusterIndex, pattern) -> None

    [3] manageNvConfig(getOrSet, nVCapabilities, capabilityState, param1, param2) ->
            getOrSet, nVCapabilities, capabilityState, param1, param2

    [4] manageRgbLedBinInfo(getOrSet, rgbClusterIndex, ledBinIndex, param1..8) ->
            getOrSet, rgbClusterIndex, ledBinIndex, param1..8

    [5] manageSWControl(getOrSet, swControlFlags, eventsNotificationFlags) ->
            getOrSet, swControlFlags, eventsNotificationFlags

    [6] setEffectSyncCorrection(rgbClusterIndex, driftValue) -> None

    [7] manageRgbPowerModeConfig(getOrSet, rgbPowerModeFlags, rgbNoActTimeoutToSave, rgbNoActTimeoutToOff) ->
            getOrSet, rgbPowerModeFlags, rgbNoActTimeoutToSave, rgbNoActTimeoutToOff

    [8] manageRgbPowerMode(getOrSet, rgbPowerMode) -> getOrSet, rgbPowerMode

    [Event 0] effectSyncEvent -> rgbClusterIndex, effectCounter

    [Event 1] userActivityEvent -> activityEventType
    """
    VERSION = 0

    def __init__(self):
        # See ``RGBEffects.__init__``
        super().__init__()
        index = RGBEffectsModel.INDEX

        # Requests
        self.get_info_cls = RGBEffectsModel.get_request_cls(
            self.VERSION, index.GET_INFO)
        self.set_rgb_cluster_effect_cls = RGBEffectsModel.get_request_cls(
            self.VERSION, index.SET_RGB_CLUSTER_EFFECT)
        self.set_multi_led_rgb_cluster_pattern_cls = RGBEffectsModel.get_request_cls(
            self.VERSION, index.SET_MULTI_LED_RGB_CLUSTER_PATTERN)
        self.manage_nv_config_cls = RGBEffectsModel.get_request_cls(
            self.VERSION, index.MANAGE_NV_CONFIG)
        self.manage_rgb_led_bin_info_cls = RGBEffectsModel.get_request_cls(
            self.VERSION, index.MANAGE_RGB_LED_BIN_INFO)
        self.manage_sw_control_cls = RGBEffectsModel.get_request_cls(
            self.VERSION, index.MANAGE_SW_CONTROL)
        self.set_effect_sync_correction_cls = RGBEffectsModel.get_request_cls(
            self.VERSION, index.SET_EFFECT_SYNC_CORRECTION)
        self.manage_rgb_power_mode_config_cls = RGBEffectsModel.get_request_cls(
            self.VERSION, index.MANAGE_RGB_POWER_MODE_CONFIG)
        self.manage_rgb_power_mode_cls = RGBEffectsModel.get_request_cls(
            self.VERSION, index.MANAGE_RGB_POWER_MODE)

        # Responses
        self.get_info_response_cls = RGBEffectsModel.get_response_cls(
            self.VERSION, index.GET_INFO)
        self.set_rgb_cluster_effect_response_cls = RGBEffectsModel.get_response_cls(
            self.VERSION, index.SET_RGB_CLUSTER_EFFECT)
        self.set_multi_led_rgb_cluster_pattern_response_cls = RGBEffectsModel.get_response_cls(
            self.VERSION, index.SET_MULTI_LED_RGB_CLUSTER_PATTERN)
        self.manage_nv_config_response_cls = RGBEffectsModel.get_response_cls(
            self.VERSION, index.MANAGE_NV_CONFIG)
        self.manage_rgb_led_bin_info_response_cls = RGBEffectsModel.get_response_cls(
            self.VERSION, index.MANAGE_RGB_LED_BIN_INFO)
        self.manage_sw_control_response_cls = RGBEffectsModel.get_response_cls(
            self.VERSION, index.MANAGE_SW_CONTROL)
        self.set_effect_sync_correction_response_cls = RGBEffectsModel.get_response_cls(
            self.VERSION, index.SET_EFFECT_SYNC_CORRECTION)
        self.manage_rgb_power_mode_config_response_cls = RGBEffectsModel.get_response_cls(
            self.VERSION, index.MANAGE_RGB_POWER_MODE_CONFIG)
        self.manage_rgb_power_mode_response_cls = RGBEffectsModel.get_response_cls(
            self.VERSION, index.MANAGE_RGB_POWER_MODE)

        # Events
        self.effect_sync_event_cls = RGBEffectsModel.get_report_cls(
            self.VERSION, index.EFFECT_SYNC)
        self.user_activity_event_cls = RGBEffectsModel.get_report_cls(
            self.VERSION, index.USER_ACTIVITY)
    # end def __init__

    def get_max_function_index(self):
        # See ``RGBEffectsInterface.get_max_function_index``
        return RGBEffectsModel.get_base_cls().MAX_FUNCTION_INDEX_V0_TO_V3
    # end def get_max_function_index

    def get_effect_dictionary(self):
        # See ``RGBEffectsInterface.get_effect_dictionary``
        return EFFECT_ID_TO_CLASS_MAP_V0_V1
    # end def get_effect_dictionary
# end class RGBEffectsV0


class RGBEffectsV1(RGBEffectsV0):
    """
    ``RGBEffectsV1``

    This feature provides model and unit specific information for version 1

    M [0] getInfo(rgbClusterIndex, rgbClusterEffectIndex) -> rgbClusterIndex, rgbClusterEffectIndex, param1..14
    M [1] setRgbClusterEffect(rgbClusterIndex, rgbClusterEffectIndex, param1..10, persistence, powerMode)
    M [3] manageNvConfig(getOrSet, nVCapabilities, capabilityState, param1, param2) ->
            getOrSet, nVCapabilities, capabilityState, param1, param2
    """
    VERSION = 1
# end class RGBEffectsV1


class RGBEffectsV2(RGBEffectsV0):
    """
    ``RGBEffectsV2``

    This feature provides model and unit specific information for version 2

    M [0] getInfo(rgbClusterIndex, rgbClusterEffectIndex) -> rgbClusterIndex, rgbClusterEffectIndex, param1..14
    M [1] setRgbClusterEffect(rgbClusterIndex, rgbClusterEffectIndex, param1..10, persistence, powerMode)
    M [3] manageNvConfig(getOrSet, nVCapabilities, capabilityState, param1, param2) ->
            getOrSet, nVCapabilities, capabilityState, param1, param2
    """
    VERSION = 2

    def get_effect_dictionary(self):
        # See ``RGBEffectsInterface.get_effect_dictionary``
        return EFFECT_ID_TO_CLASS_MAP_V2
    # end def get_effect_dictionary
# end class RGBEffectsV2


class RGBEffectsV3(RGBEffectsV0):
    """
    ``RGBEffectsV2``

    This feature provides model and unit specific information for version 3

    M [0] getInfo(rgbClusterIndex, rgbClusterEffectIndex, typeOfInfo, param1..13) → rgbClusterCount / nvCapabilities /
                                                                                    effectCapabilities
    M [1] setRgbClusterEffect(rgbClusterIndex, rgbClusterEffectIndex, param1..10, persistence, powerMode)
    M [3] manageNvConfig(getOrSet, nVCapabilities, capabilityState, param1, param2) ->
            getOrSet, nVCapabilities, capabilityState, param1, param2
    """
    VERSION = 3

    def get_effect_dictionary(self):
        # See ``RGBEffectsInterface.get_effect_dictionary``
        return EFFECT_ID_TO_CLASS_MAP_V3
    # end def get_effect_dictionary
# end class RGBEffectsV3


class RGBEffectsV4(RGBEffectsV0):
    """
    ``RGBEffectsV4``

    This feature provides model and unit specific information for version 4

    Following interfaces are added in version 4

    [9] shutdown() -> None

    [Event 2] rgbClusterChangedEvent -> rgbClusterIndex, rgbClusterEffectIndex, param1..10, powerMode, persistence
    """
    VERSION = 4

    def __init__(self):
        # See ``BrightnessControl.__init__``
        super().__init__()
        index = RGBEffectsModel.INDEX

        # Requests
        self.shutdown_cls = RGBEffectsModel.get_request_cls(
            self.VERSION, index.SHUTDOWN)

        # Responses
        self.shutdown_response_cls = RGBEffectsModel.get_response_cls(
            self.VERSION, index.SHUTDOWN)

        # Events
        self.rgb_cluster_changed_event = RGBEffectsModel.get_report_cls(
            self.VERSION, index.RGB_CLUSTER_CHANGED_EVENT)
    # end def __init__

    def get_max_function_index(self):
        # See ``RGBEffectsInterface.get_max_function_index``
        return RGBEffectsModel.get_base_cls().MAX_FUNCTION_INDEX_V4
    # end def get_max_function_index

    def get_effect_dictionary(self):
        # See ``RGBEffectsInterface.get_effect_dictionary``
        return EFFECT_ID_TO_CLASS_MAP_V4
    # end def get_effect_dictionary
# end class RGBEffectsV4


class ShortEmptyPacketDataFormat(RGBEffects):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - Shutdown

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """
    class FID(RGBEffects.FID):
        # See ``RGBEffects.FID``
        PADDING = RGBEffects.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(RGBEffects.LEN):
        # See ``RGBEffects.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = RGBEffects.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(RGBEffects):
    """
    This class is to be used as a base class for several messages in this feature
        - SetRgbClusterEffectResponse
        - SetMultiLedRgbClusterPatternResponse
        - SetEffectSyncCorrectionResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """
    class FID(RGBEffects.FID):
        # See ``RGBEffects.FID``
        PADDING = RGBEffects.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(RGBEffects.LEN):
        # See ``RGBEffects.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = RGBEffects.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class RgbClusterInfoHead(RGBEffects):
    """
    This class is to be used as a base class for several messages in this feature.
        - InfoAboutDeviceV0ToV1
        - InfoAboutRGBClusterV0
        - InfoAboutEffectGeneralInfo
        - EffectInfoHead
        - GetInfoV0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    ============================  ==========
    """
    class FID(RGBEffects.FID):
        # See ``RGBEffects.FID``
        RGB_CLUSTER_INDEX = RGBEffects.FID.SOFTWARE_ID - 1
        RGB_CLUSTER_EFFECT_INDEX = RGB_CLUSTER_INDEX - 1
    # end class FID

    class LEN(RGBEffects.LEN):
        # See ``RGBEffects.LEN``
        RGB_CLUSTER_INDEX = 0x8
        RGB_CLUSTER_EFFECT_INDEX = 0x8
    # end class LEN

    FIELDS = RGBEffects.FIELDS + (
        BitField(fid=FID.RGB_CLUSTER_INDEX, length=LEN.RGB_CLUSTER_INDEX,
                 title="RgbClusterIndex", name="rgb_cluster_index",
                 conversions={HexList: Numeral},
                 checks=(CheckHexList(LEN.RGB_CLUSTER_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_CLUSTER_EFFECT_INDEX, length=LEN.RGB_CLUSTER_EFFECT_INDEX,
                 title="RgbClusterEffectIndex", name="rgb_cluster_effect_index",
                 checks=(CheckHexList(LEN.RGB_CLUSTER_EFFECT_INDEX // 8),
                         CheckByte(),)),
    )
# end class RgbClusterInfoHead


class InfoAboutDeviceV0ToV1(RgbClusterInfoHead):
    """
    ``InfoAboutDeviceV0ToV1`` implementation class for re-format response data structure from
        - GetInfo V0 with RgbClusterIndex = 0xFF, RgbClusterEffectIndex = 0xFF
        - GetInfo V1 with RgbClusterIndex = 0xFF, RgbClusterEffectIndex = 0xFF, TypeOfInfo = 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    RgbClusterCount               8
    NVCapabilities                16
    EXTCapabilities               16
    Reserved                      72
    ============================  ==========
    """
    class FID(RgbClusterInfoHead.FID):
        # See ``RgbClusterInfoHead.FID``
        RGB_CLUSTER_COUNT = RgbClusterInfoHead.FID.RGB_CLUSTER_EFFECT_INDEX - 1
        NV_CAPABILITIES = RGB_CLUSTER_COUNT - 1
        EXT_CAPABILITIES = NV_CAPABILITIES - 1
        RESERVED = EXT_CAPABILITIES - 1
    # end class FID

    class LEN(RgbClusterInfoHead.LEN):
        # See ``RgbClusterInfoHead.LEN``
        RGB_CLUSTER_COUNT = 0x8
        NV_CAPABILITIES = 0x10
        EXT_CAPABILITIES = 0x10
        RESERVED = 0x48
    # end class LEN

    FIELDS = RgbClusterInfoHead.FIELDS + (
        BitField(fid=FID.RGB_CLUSTER_COUNT, length=LEN.RGB_CLUSTER_COUNT,
                 title="RgbClusterCount", name="rgb_cluster_count",
                 checks=(CheckHexList(LEN.RGB_CLUSTER_COUNT // 8),
                         CheckByte(),)),
        BitField(fid=FID.NV_CAPABILITIES, length=LEN.NV_CAPABILITIES,
                 title="NVCapabilities", name="nv_capabilities",
                 checks=(CheckHexList(LEN.NV_CAPABILITIES // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.NV_CAPABILITIES) - 1),)),
        BitField(fid=FID.EXT_CAPABILITIES, length=LEN.EXT_CAPABILITIES,
                 title="EXTCapabilities", name="ext_capabilities",
                 checks=(CheckHexList(LEN.EXT_CAPABILITIES // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.EXT_CAPABILITIES) - 1),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=RGBEffects.DEFAULT.RESERVED),
    )
# end class InfoAboutDeviceV0ToV1


class InfoAboutDeviceV2ToV4(InfoAboutDeviceV0ToV1):
    """
    ``InfoAboutDeviceV2ToV4`` implementation class for re-format response data structure from
        - GetInfo V2 to V4 with RgbClusterIndex = 0xFF, RgbClusterEffectIndex = 0xFF, TypeOfInfo = 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    RgbClusterCount               8
    NVCapabilities                16
    EXTCapabilities               16
    NumberOfMultiClusterEffects   8
    Reserved                      64
    ============================  ==========
    """
    class FID(InfoAboutDeviceV0ToV1.FID):
        # See ``InfoAboutDeviceV0ToV1.FID``
        NUMBER_OF_MULTI_CLUSTER_EFFECTS = InfoAboutDeviceV0ToV1.FID.EXT_CAPABILITIES - 1
        RESERVED = NUMBER_OF_MULTI_CLUSTER_EFFECTS - 1
    # end class FID

    class LEN(InfoAboutDeviceV0ToV1.LEN):
        # See ``InfoAboutDeviceV0ToV1.LEN``
        NUMBER_OF_MULTI_CLUSTER_EFFECTS = 0x08
        RESERVED = 0x40
    # end class LEN

    FIELDS = InfoAboutDeviceV0ToV1.FIELDS[:-1] + (
        BitField(fid=FID.NUMBER_OF_MULTI_CLUSTER_EFFECTS, length=LEN.NUMBER_OF_MULTI_CLUSTER_EFFECTS,
                 title="NumberOfMultiClusterEffects", name="number_of_multi_cluster_effects",
                 checks=(CheckHexList(LEN.NUMBER_OF_MULTI_CLUSTER_EFFECTS // 8),
                         CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=RGBEffects.DEFAULT.RESERVED),
    )
# end class InfoAboutDeviceV2ToV4


class InfoAboutRGBClusterV0(RgbClusterInfoHead):
    """
    ``InfoAboutRGBClusterV0`` implementation class for re-format response data structure from
        - GetInfo V0 with RgbClusterEffectIndex = 0xFF

    Format:
    ===============================  ==========
    Name                             Bit count
    ===============================  ==========
    RgbClusterIndex                  8
    RgbClusterEffectIndex            8
    LocationEffect                   16
    EffectsNumber                    8
    DisplayPersistencyCapabilities   8
    Reserved                         80
    ===============================  ==========
    """
    class FID(RgbClusterInfoHead.FID):
        # See ``RgbClusterInfoHead.FID``
        LOCATION_EFFECT = RgbClusterInfoHead.FID.RGB_CLUSTER_EFFECT_INDEX - 1
        EFFECTS_NUMBER = LOCATION_EFFECT - 1
        DISPLAY_PERSISTENCY_CAPABILITIES = EFFECTS_NUMBER - 1
        RESERVED = DISPLAY_PERSISTENCY_CAPABILITIES - 1
    # end class FID

    class LEN(RgbClusterInfoHead.LEN):
        # See ``RgbClusterInfoHead.LEN``
        LOCATION_EFFECT = 0x10
        EFFECTS_NUMBER = 0x8
        DISPLAY_PERSISTENCY_CAPABILITIES = 0x8
        RESERVED = 0x50
    # end class LEN

    FIELDS = RgbClusterInfoHead.FIELDS + (
        BitField(fid=FID.LOCATION_EFFECT, length=LEN.LOCATION_EFFECT,
                 title="LocationEffect", name="location_effect",
                 checks=(CheckHexList(LEN.LOCATION_EFFECT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.LOCATION_EFFECT) - 1),)),
        BitField(fid=FID.EFFECTS_NUMBER, length=LEN.EFFECTS_NUMBER,
                 title="EffectsNumber", name="effects_number",
                 checks=(CheckHexList(LEN.EFFECTS_NUMBER // 8),
                         CheckByte(),)),
        BitField(fid=FID.DISPLAY_PERSISTENCY_CAPABILITIES, length=LEN.DISPLAY_PERSISTENCY_CAPABILITIES,
                 title="DisplayPersistencyCapabilities", name="display_persistency_capabilities",
                 checks=(CheckHexList(LEN.DISPLAY_PERSISTENCY_CAPABILITIES // 8),
                         CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=RGBEffects.DEFAULT.RESERVED),
    )
# end class InfoAboutRGBClusterV0


class InfoAboutRGBClusterV1ToV4(InfoAboutRGBClusterV0):
    """
    ``InfoAboutRGBClusterV1ToV4`` implementation class for re-format response data structure from
        - GetInfo V1 ~ V4 with RgbClusterEffectIndex = 0xFF, TypeOfInfo = 0

    Format:
    ===============================  ==========
    Name                             Bit count
    ===============================  ==========
    RgbClusterIndex                  8
    RgbClusterEffectIndex            8
    LocationEffect                   16
    EffectsNumber                    8
    DisplayPersistencyCapabilities   8
    EffectPersistencyCapabilities    8
    MultiLedPatternCapabilities      8
    Reserved                         64
    ===============================  ==========
    """
    class FID(InfoAboutRGBClusterV0.FID):
        # See ``InfoAboutRGBClusterV0.FID``
        EFFECT_PERSISTENCY_CAPABILITIES = InfoAboutRGBClusterV0.FID.DISPLAY_PERSISTENCY_CAPABILITIES - 1
        MULTI_LED_PATTERN_CAPABILITIES = EFFECT_PERSISTENCY_CAPABILITIES - 1
        RESERVED = MULTI_LED_PATTERN_CAPABILITIES - 1
    # end class FID

    class LEN(InfoAboutRGBClusterV0.LEN):
        # See ``InfoAboutRGBClusterV0.LEN``
        EFFECT_PERSISTENCY_CAPABILITIES = 0x8
        MULTI_LED_PATTERN_CAPABILITIES = 0X08
        RESERVED = 0x40
    # end class LEN

    FIELDS = InfoAboutRGBClusterV0.FIELDS[:-1] + (
        BitField(fid=FID.EFFECT_PERSISTENCY_CAPABILITIES, length=LEN.EFFECT_PERSISTENCY_CAPABILITIES,
                 title="EffectPersistencyCapabilities", name="effect_persistency_capabilities",
                 checks=(CheckHexList(LEN.EFFECT_PERSISTENCY_CAPABILITIES // 8),
                         CheckByte(),)),
        BitField(fid=FID.MULTI_LED_PATTERN_CAPABILITIES, length=LEN.MULTI_LED_PATTERN_CAPABILITIES,
                 title="MultiLedPatternCapabilities", name="multi_led_pattern_capabilities",
                 checks=(CheckHexList(LEN.MULTI_LED_PATTERN_CAPABILITIES // 8),
                         CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=RGBEffects.DEFAULT.RESERVED),
    )
# end class InfoAboutRGBClusterV1ToV4


class InfoAboutEffectGeneralInfo(RgbClusterInfoHead):
    """
    ``InfoAboutEffectGeneralInfo`` implementation class for re-format response data structure from
        - GetInfo V0
        - GetInfo V1 ~ V4 with TypeOfInfo = 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    EffectId                      16
    EffectCapabilities            16
    EffectPeriod                  16
    Reserved                      64
    ============================  ==========
    """
    class FID(RgbClusterInfoHead.FID):
        # See ``RgbClusterInfoHead.FID``
        EFFECT_ID = RgbClusterInfoHead.FID.RGB_CLUSTER_EFFECT_INDEX - 1
        EFFECT_CAPABILITIES = EFFECT_ID - 1
        EFFECT_PERIOD = EFFECT_CAPABILITIES - 1
        RESERVED = EFFECT_PERIOD - 1
    # end class FID

    class LEN(RgbClusterInfoHead.LEN):
        # See ``RgbClusterInfoHead.LEN``
        EFFECT_ID = 0x10
        EFFECT_CAPABILITIES = 0x10
        EFFECT_PERIOD = 0x10
        RESERVED = 0x40
    # end class LEN

    FIELDS = RgbClusterInfoHead.FIELDS + (
        BitField(fid=FID.EFFECT_ID, length=LEN.EFFECT_ID,
                 title="EffectId", name="effect_id",
                 checks=(CheckHexList(LEN.EFFECT_ID // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.EFFECT_ID) - 1),)),
        BitField(fid=FID.EFFECT_CAPABILITIES, length=LEN.EFFECT_CAPABILITIES,
                 title="EffectCapabilities", name="effect_capabilities",
                 checks=(CheckHexList(LEN.EFFECT_CAPABILITIES // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.EFFECT_CAPABILITIES) - 1),)),
        BitField(fid=FID.EFFECT_PERIOD, length=LEN.EFFECT_PERIOD,
                 title="EffectPeriod", name="effect_period",
                 checks=(CheckHexList(LEN.EFFECT_PERIOD // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.EFFECT_PERIOD) - 1),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=RGBEffects.DEFAULT.RESERVED),
    )
# end class InfoAboutEffectGeneralInfo


class EffectInfoHead(RgbClusterInfoHead):
    """
    This class is to be used as a base class for several messages in this feature.
        - CustomOnboardStoredEffectInfoHead
        - GetInfoV1ToV4

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    TypeOfInfo                    8
    ============================  ==========
    """
    class FID(RgbClusterInfoHead.FID):
        # See ``RgbClusterInfoHead.FID``
        TYPE_OF_INFO = RgbClusterInfoHead.FID.RGB_CLUSTER_EFFECT_INDEX - 1
    # end class FID

    class LEN(RgbClusterInfoHead.LEN):
        # See ``RgbClusterInfoHead.LEN``
        TYPE_OF_INFO = 0x8
    # end class LEN

    FIELDS = RgbClusterInfoHead.FIELDS + (
        BitField(fid=FID.TYPE_OF_INFO, length=LEN.TYPE_OF_INFO,
                 title="TypeOfInfo", name="type_of_info",
                 checks=(CheckHexList(LEN.TYPE_OF_INFO // 8),
                         CheckByte(),)),
    )
# end class EffectInfoHead


class CustomOnboardStoredEffectInfoHead(EffectInfoHead):
    """
    This class is to be used as a base class for several messages in this feature.
        - InfoAboutCustomOnboardStoredEffect0
        - InfoAboutCustomOnboardStoredEffect1
        - InfoAboutCustomOnboardStoredEffect2
        - InfoAboutCustomOnboardStoredEffect3
        - InfoAboutCustomOnboardStoredEffect4
        - InfoAboutCustomOnboardStoredEffect5
        - InfoAboutCustomOnboardStoredEffect6

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    TypeOfInfo                    8
    Slot                          8
    SlotInfoType                  8
    ============================  ==========
    """
    class FID(EffectInfoHead.FID):
        # See ``EffectInfoHead.FID``
        SLOT = EffectInfoHead.FID.TYPE_OF_INFO - 1
        SLOT_INFO_TYPE = SLOT - 1
    # end class FID

    class LEN(EffectInfoHead.LEN):
        # See ``EffectInfoHead.LEN``
        SLOT = 0x8
        SLOT_INFO_TYPE = 0x8
    # end class LEN

    FIELDS = EffectInfoHead.FIELDS + (
        BitField(fid=FID.SLOT, length=LEN.SLOT,
                 title="slot", name="slot",
                 checks=(CheckHexList(LEN.SLOT // 8),
                         CheckByte(),)),
        BitField(fid=FID.SLOT_INFO_TYPE, length=LEN.SLOT_INFO_TYPE,
                 title="SlotInfoType", name="slot_info_type",
                 checks=(CheckHexList(LEN.SLOT_INFO_TYPE // 8),
                         CheckByte(),)),
    )
# end class CustomOnboardStoredEffectInfoHead


class InfoAboutCustomOnboardStoredEffect0(CustomOnboardStoredEffectInfoHead):
    """
    ``InfoAboutCustomOnboardStoredEffect0`` implementation class for re-format response data structure from
        - GetInfo V1 ~ V4 with RgbClusterIndex = 0xFF,
                               RgbClusterEffectIndex = Custom Onboard Effect Index, TypeOfInfo = 1,
                               SlotInfoType = Slot State

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    TypeOfInfo                    8
    Slot                          8
    SlotInfoType                  8
    DataValidity                  8
    LengthFrames                  16
    Reserved                      64
    ============================  ==========
    """
    class FID(CustomOnboardStoredEffectInfoHead.FID):
        # See ``CustomOnboardStoredEffectInfoHead.FID``
        DATA_VALIDITY = CustomOnboardStoredEffectInfoHead.FID.SLOT_INFO_TYPE - 1
        LENGTH_FRAMES = DATA_VALIDITY - 1
        RESERVED = LENGTH_FRAMES - 1
    # end class FID

    class LEN(CustomOnboardStoredEffectInfoHead.LEN):
        # See ``CustomOnboardStoredEffectInfoHead.LEN``
        DATA_VALIDITY = 0x8
        LENGTH_FRAMES = 0x10
        RESERVED = 0x40
    # end class LEN

    FIELDS = CustomOnboardStoredEffectInfoHead.FIELDS + (
        BitField(fid=FID.DATA_VALIDITY, length=LEN.DATA_VALIDITY,
                 title="DataValidity", name="data_validity",
                 checks=(CheckHexList(LEN.DATA_VALIDITY // 8),
                         CheckByte(),)),
        BitField(fid=FID.LENGTH_FRAMES, length=LEN.LENGTH_FRAMES,
                 title="LengthFrame", name="length_frame",
                 checks=(CheckHexList(LEN.LENGTH_FRAMES // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.LENGTH_FRAMES) - 1),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                 default_value=RGBEffects.DEFAULT.RESERVED),
    )
# end InfoAboutCustomOnboardStoredEffect0


class InfoAboutCustomOnboardStoredEffect1(CustomOnboardStoredEffectInfoHead):
    """
    ``InfoAboutCustomOnboardStoredEffect1`` implementation class for re-format response data structure from
        - GetInfo V1 ~ V4 with RgbClusterIndex = 0xFF,
                               RgbClusterEffectIndex = Custom Onboard Effect Index, TypeOfInfo = 1,
                               SlotInfoType = Defaults

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    TypeOfInfo                    8
    Slot                          8
    SlotInfoType                  8
    InitFrame                     16
    LengthFramesToPlay            16
    FramePeriodMs                 16
    Intensity                     8
    Reserved                      32
    ============================  ==========
    """
    class FID(CustomOnboardStoredEffectInfoHead.FID):
        # See ``CustomOnboardStoredEffectInfoHead.FID``
        INIT_FRAME = CustomOnboardStoredEffectInfoHead.FID.SLOT_INFO_TYPE - 1
        LENGTH_FRAMES_TO_PLAY = INIT_FRAME - 1
        FRAME_PERIOD_MS = LENGTH_FRAMES_TO_PLAY - 1
        INTENSITY = FRAME_PERIOD_MS - 1
        RESERVED = INTENSITY - 1
    # end class FID

    class LEN(CustomOnboardStoredEffectInfoHead.LEN):
        # See ``CustomOnboardStoredEffectInfoHead.LEN``
        INIT_FRAME = 0x10
        LENGTH_FRAMES_TO_PLAY = 0x10
        FRAME_PERIOD_MS = 0x10
        INTENSITY = 0x8
        RESERVED = 0x20
    # end class LEN

    FIELDS = CustomOnboardStoredEffectInfoHead.FIELDS + (
        BitField(fid=FID.INIT_FRAME, length=LEN.INIT_FRAME,
                 title="InitFrame", name="init_frame",
                 checks=(CheckHexList(LEN.INIT_FRAME // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.INIT_FRAME) - 1),)),
        BitField(fid=FID.LENGTH_FRAMES_TO_PLAY, length=LEN.LENGTH_FRAMES_TO_PLAY,
                 title="LengthFramesToPlay", name="length_frames_to_play",
                 checks=(CheckHexList(LEN.LENGTH_FRAMES_TO_PLAY // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.LENGTH_FRAMES_TO_PLAY) - 1),)),
        BitField(fid=FID.FRAME_PERIOD_MS, length=LEN.FRAME_PERIOD_MS,
                 title="FramePeriodMs", name="frame_period_ms",
                 checks=(CheckHexList(LEN.FRAME_PERIOD_MS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FRAME_PERIOD_MS) - 1),)),
        BitField(fid=FID.INTENSITY, length=LEN.INTENSITY,
                 title="Intensity", name="intensity",
                 checks=(CheckHexList(LEN.INTENSITY // 8),
                         CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                 default_value=RGBEffects.DEFAULT.RESERVED),
    )
# end class InfoAboutCustomOnboardStoredEffect1


class InfoAboutCustomOnboardStoredEffect2(CustomOnboardStoredEffectInfoHead):
    """
    ``InfoAboutCustomOnboardStoredEffect2`` implementation class for re-format response data structure from
        - GetInfo V1 ~ V4 with RgbClusterIndex = 0xFF,
                               RgbClusterEffectIndex = Custom Onboard Effect Index, TypeOfInfo = 1,
                               SlotInfoType = UUID_0_10

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    TypeOfInfo                    8
    Slot                          8
    SlotInfoType                  8
    UUID_0_10                     88
    ============================  ==========
    """
    class FID(CustomOnboardStoredEffectInfoHead.FID):
        # See ``CustomOnboardStoredEffectInfoHead.FID``
        UUID_0_10 = CustomOnboardStoredEffectInfoHead.FID.SLOT_INFO_TYPE - 1
    # end class FID

    class LEN(CustomOnboardStoredEffectInfoHead.LEN):
        # See ``CustomOnboardStoredEffectInfoHead.LEN``
        UUID_0_10 = 0x58
    # end class LEN

    FIELDS = CustomOnboardStoredEffectInfoHead.FIELDS + (
        BitField(fid=FID.UUID_0_10, length=LEN.UUID_0_10,
                 title="UUID_0_10", name="uuid_0_10",
                 checks=(CheckHexList(LEN.UUID_0_10 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.UUID_0_10) - 1),)),
    )
# end class InfoAboutCustomOnboardStoredEffect2


class InfoAboutCustomOnboardStoredEffect3(CustomOnboardStoredEffectInfoHead):
    """
    ``InfoAboutCustomOnboardStoredEffect3`` implementation class for re-format response data structure from
        - GetInfo V1 ~ V4 with RgbClusterIndex = 0xFF,
                               RgbClusterEffectIndex = Custom Onboard Effect Index, TypeOfInfo = 1,
                               SlotInfoType = UUID_11_16

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    TypeOfInfo                    8
    Slot                          8
    SlotInfoType                  8
    UUID_11_16                    48
    Reserved                      40
    ============================  ==========
    """
    class FID(CustomOnboardStoredEffectInfoHead.FID):
        # See ``CustomOnboardStoredEffectInfoHead.FID``
        UUID_11_16 = CustomOnboardStoredEffectInfoHead.FID.SLOT_INFO_TYPE - 1
        RESERVED = UUID_11_16 - 1
    # end class FID

    class LEN(CustomOnboardStoredEffectInfoHead.LEN):
        # See ``CustomOnboardStoredEffectInfoHead.LEN``
        UUID_11_16 = 0x30
        RESERVED = 0x28
    # end class LEN

    FIELDS = CustomOnboardStoredEffectInfoHead.FIELDS + (
        BitField(fid=FID.UUID_11_16, length=LEN.UUID_11_16,
                 title="UUID_11_16", name="uuid_11_16",
                 checks=(CheckHexList(LEN.UUID_11_16 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.UUID_11_16) - 1),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                 default_value=RGBEffects.DEFAULT.RESERVED),
    )
# end class InfoAboutCustomOnboardStoredEffect3


class InfoAboutCustomOnboardStoredEffect4(CustomOnboardStoredEffectInfoHead):
    """
    ``InfoAboutCustomOnboardStoredEffect4`` implementation class for re-format response data structure from
        - GetInfo V1 ~ V4 with RgbClusterIndex = 0xFF,
                               RgbClusterEffectIndex = Custom Onboard Effect Index, TypeOfInfo = 1,
                               SlotInfoType = EffectName_0_10

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    TypeOfInfo                    8
    Slot                          8
    SlotInfoType                  8
    EffectName_0_10               88
    ============================  ==========
    """
    class FID(CustomOnboardStoredEffectInfoHead.FID):
        # See ``CustomOnboardStoredEffectInfoHead.FID``
        EFFECT_NAME_0_10 = CustomOnboardStoredEffectInfoHead.FID.SLOT_INFO_TYPE - 1
    # end class FID

    class LEN(CustomOnboardStoredEffectInfoHead.LEN):
        # See ``CustomOnboardStoredEffectInfoHead.LEN``
        EFFECT_NAME_0_10 = 0x58
    # end class LEN

    FIELDS = CustomOnboardStoredEffectInfoHead.FIELDS + (
        BitField(fid=FID.EFFECT_NAME_0_10, length=LEN.EFFECT_NAME_0_10,
                 title="EffectName_0_10", name="effect_name_0_10",
                 checks=(CheckHexList(LEN.EFFECT_NAME_0_10 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.EFFECT_NAME_0_10) - 1),)),
    )
# end class InfoAboutCustomOnboardStoredEffect4


class InfoAboutCustomOnboardStoredEffect5(CustomOnboardStoredEffectInfoHead):
    """
    ``InfoAboutCustomOnboardStoredEffect5`` implementation class for re-format response data structure from
        - GetInfo V1 ~ V4 with RgbClusterIndex = 0xFF,
                               RgbClusterEffectIndex = Custom Onboard Effect Index, TypeOfInfo = 1,
                               SlotInfoType = EffectName_11_21

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    TypeOfInfo                    8
    Slot                          8
    SlotInfoType                  8
    EffectName_11_21              88
    ============================  ==========
    """
    class FID(CustomOnboardStoredEffectInfoHead.FID):
        # See ``CustomOnboardStoredEffectInfoHead.FID``
        EFFECT_NAME_11_21 = CustomOnboardStoredEffectInfoHead.FID.SLOT_INFO_TYPE - 1
    # end class FID

    class LEN(CustomOnboardStoredEffectInfoHead.LEN):
        # See ``CustomOnboardStoredEffectInfoHead.LEN``
        EFFECT_NAME_11_21 = 0x58
    # end class LEN

    FIELDS = CustomOnboardStoredEffectInfoHead.FIELDS + (
        BitField(fid=FID.EFFECT_NAME_11_21, length=LEN.EFFECT_NAME_11_21,
                 title="EffectName_11_21", name="effect_name_11_21",
                 checks=(CheckHexList(LEN.EFFECT_NAME_11_21 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.EFFECT_NAME_11_21) - 1),)),
    )
# end class InfoAboutCustomOnboardStoredEffect5


class InfoAboutCustomOnboardStoredEffect6(CustomOnboardStoredEffectInfoHead):
    """
    ``InfoAboutCustomOnboardStoredEffect6`` implementation class for re-format response data structure from
        - GetInfo V1 ~ V4 with RgbClusterIndex = 0xFF,
                               RgbClusterEffectIndex = Custom Onboard Effect Index, TypeOfInfo = 1,
                               SlotInfoType = EffectName_22_31

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    TypeOfInfo                    8
    Slot                          8
    SlotInfoType                  8
    EffectName_22_31              80
    Reserved                      8
    ============================  ==========
    """
    class FID(CustomOnboardStoredEffectInfoHead.FID):
        # See ``CustomOnboardStoredEffectInfoHead.FID``
        EFFECT_NAME_22_31 = CustomOnboardStoredEffectInfoHead.FID.SLOT_INFO_TYPE - 1
        RESERVED = EFFECT_NAME_22_31 - 1
    # end class FID

    class LEN(CustomOnboardStoredEffectInfoHead.LEN):
        # See ``CustomOnboardStoredEffectInfoHead.LEN``
        EFFECT_NAME_22_31 = 0x50
        RESERVED = 0x8
    # end class LEN

    FIELDS = CustomOnboardStoredEffectInfoHead.FIELDS + (
        BitField(fid=FID.EFFECT_NAME_22_31, length=LEN.EFFECT_NAME_22_31,
                 title="EffectName_22_31", name="effect_name_22_31",
                 checks=(CheckHexList(LEN.EFFECT_NAME_22_31 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.EFFECT_NAME_22_31) - 1),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.RESERVED),
    )
# end class InfoAboutCustomOnboardStoredEffect6


class ManageHead(RGBEffects):
    """
    This class is to be used as a base class for several messages in this feature.
        - NvConfig
        - RgbLedBinInfoHead
        - SwControl
        - RgbPowerModeConfig
        - RgbPowerMode

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    GetOrSet                      8
    ============================  ==========
    """

    class FID(RGBEffects.FID):
        # See ``RGBEffects.FID``
        GET_OR_SET = RGBEffects.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(RGBEffects.LEN):
        # See ``RGBEffects.LEN``
        GET_OR_SET = 0x8
    # end class LEN

    FIELDS = RGBEffects.FIELDS + (
        BitField(fid=FID.GET_OR_SET, length=LEN.GET_OR_SET,
                 title="GetOrSet", name="get_or_set",
                 checks=(CheckHexList(LEN.GET_OR_SET // 8),
                         CheckByte(),)),
    )
# end class ManageHead


class NvConfig(ManageHead):
    """
    This class is to be used as a base class for several messages in this feature.
        - NvConfigExt
        - ManageNvConfigV0ToV2
        - ManageNvConfigResponseV0ToV2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    GetOrSet                      8
    NVCapabilities                16
    CapabilityState               8
    Param1                        8
    Param2                        8
    Padding                       80
    ============================  ==========
    """
    class FID(ManageHead.FID):
        # See ``ManageHead.FID``
        NV_CAPABILITIES = ManageHead.FID.GET_OR_SET - 1
        CAPABILITY_STATE = NV_CAPABILITIES - 1
        PARAM_1 = CAPABILITY_STATE - 1
        PARAM_2 = PARAM_1 - 1
        PADDING = PARAM_2 - 1
    # end class FID

    class LEN(ManageHead.LEN):
        # See ``ManageHead.LEN``
        NV_CAPABILITIES = 0x10
        CAPABILITY_STATE = 0x8
        PARAM_1 = 0x8
        PARAM_2 = 0x8
        PADDING = 0x50
    # end class LEN

    FIELDS = ManageHead.FIELDS + (
        BitField(fid=FID.NV_CAPABILITIES, length=LEN.NV_CAPABILITIES,
                 title="NVCapabilities", name="nv_capabilities",
                 checks=(CheckHexList(LEN.NV_CAPABILITIES // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.NV_CAPABILITIES) - 1),)),
        BitField(fid=FID.CAPABILITY_STATE, length=LEN.CAPABILITY_STATE,
                 title="CapabilityState", name="capability_state",
                 checks=(CheckHexList(LEN.CAPABILITY_STATE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_1, length=LEN.PARAM_1,
                 title="Param1", name="param_1",
                 checks=(CheckHexList(LEN.PARAM_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_2, length=LEN.PARAM_2,
                 title="Param2", name="param_2",
                 checks=(CheckHexList(LEN.PARAM_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.PADDING),
    )
# end class NvConfig


class NvConfigExt(NvConfig):
    """
    This class is to be used as a base class for several messages in this feature.
        - ManageNvConfigV3ToV4
        - ManageNvConfigResponseV3ToV4

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    GetOrSet                      8
    NVCapabilities                16
    CapabilityState               8
    Param1                        8
    Param2                        8
    Param3                        8
    Param4                        8
    Param5                        8
    Param6                        8
    Padding                       48
    ============================  ==========
    """
    class FID(NvConfig.FID):
        # See ``NvConfig.FID``
        PARAM_3 = NvConfig.FID.PARAM_2 - 1
        PARAM_4 = PARAM_3 - 1
        PARAM_5 = PARAM_4 - 1
        PARAM_6 = PARAM_5 - 1
        PADDING = PARAM_6 - 1
    # end class FID

    class LEN(NvConfig.LEN):
        # See ``NvConfig.LEN``
        PARAM_3 = 0x8
        PARAM_4 = 0x8
        PARAM_5 = 0x8
        PARAM_6 = 0x8
        PADDING = 0x30
    # end class LEN

    FIELDS = NvConfig.FIELDS[:-1] + (
        BitField(fid=FID.PARAM_3, length=LEN.PARAM_3,
                 title="Param3", name="param_3",
                 checks=(CheckHexList(LEN.PARAM_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_4, length=LEN.PARAM_4,
                 title="Param4", name="param_4",
                 checks=(CheckHexList(LEN.PARAM_4 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_5, length=LEN.PARAM_5,
                 title="Param5", name="param_5",
                 checks=(CheckHexList(LEN.PARAM_5 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_6, length=LEN.PARAM_6,
                 title="Param6", name="param_6",
                 checks=(CheckHexList(LEN.PARAM_6 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.PADDING),
    )
# end class NvConfigExt


class RgbLedBinInfoHead(ManageHead):
    """
    This class is to be used as a base class for several messages in this feature.
        - RgbLedBinInfo
        - LedBinIndex0
        - LedBinIndex1
        - LedBinIndex2
        - LedBinIndex3
        - LedBinIndex4
        - LedBinIndex5

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    GetOrSet                      8
    RgbClusterIndex               8
    LedBinIndex                   8
    ============================  ==========
    """
    class FID(ManageHead.FID):
        # See ``ManageHead.FID``
        RGB_CLUSTER_INDEX = ManageHead.FID.GET_OR_SET - 1
        LED_BIN_INDEX = RGB_CLUSTER_INDEX - 1
    # end class FID

    class LEN(ManageHead.LEN):
        # See ``ManageHead.LEN``
        RGB_CLUSTER_INDEX = 0x8
        LED_BIN_INDEX = 0x8
    # end class LEN

    FIELDS = ManageHead.FIELDS + (
        BitField(fid=FID.RGB_CLUSTER_INDEX, length=LEN.RGB_CLUSTER_INDEX,
                 title="RgbClusterIndex", name="rgb_cluster_index",
                 checks=(CheckHexList(LEN.RGB_CLUSTER_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.LED_BIN_INDEX, length=LEN.LED_BIN_INDEX,
                 title="LedBinIndex", name="led_bin_index",
                 checks=(CheckHexList(LEN.LED_BIN_INDEX // 8),
                         CheckByte(),)),
    )
# end class RgbLedBinInfoHead


class RgbLedBinInfo(RgbLedBinInfoHead):
    """
    This class is to be used as a base class for several messages in this feature.
        - ManageRgbLedBinInfo
        - ManageRgbLedBinInfoResponse

    The RgbLedBinInfo can be re-formatted to
    - LedBinIndex0
    - LedBinIndex1
    - LedBinIndex2
    - LedBinIndex3
    - LedBinIndex4
    - LedBinIndex5

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    GetOrSet                      8
    RgbClusterIndex               8
    LedBinIndex                   8
    Param1                        8
    Param2                        8
    Param3                        8
    Param4                        8
    Param5                        8
    Param6                        8
    Param7                        8
    Param8                        8
    Padding                       40
    ============================  ==========
    """
    class FID(RgbLedBinInfoHead.FID):
        # See ``RgbLedBinInfoHead.FID``
        PARAM_1 = RgbLedBinInfoHead.FID.LED_BIN_INDEX - 1
        PARAM_2 = PARAM_1 - 1
        PARAM_3 = PARAM_2 - 1
        PARAM_4 = PARAM_3 - 1
        PARAM_5 = PARAM_4 - 1
        PARAM_6 = PARAM_5 - 1
        PARAM_7 = PARAM_6 - 1
        PARAM_8 = PARAM_7 - 1
        PADDING = PARAM_8 - 1
    # end class FID

    class LEN(RgbLedBinInfoHead.LEN):
        # See ``RgbLedBinInfoHead.LEN``
        PARAM_1 = 0x8
        PARAM_2 = 0x8
        PARAM_3 = 0x8
        PARAM_4 = 0x8
        PARAM_5 = 0x8
        PARAM_6 = 0x8
        PARAM_7 = 0x8
        PARAM_8 = 0x8
        PADDING = 0x28
    # end class LEN

    FIELDS = RgbLedBinInfoHead.FIELDS + (
        BitField(fid=FID.PARAM_1, length=LEN.PARAM_1,
                 title="Param1", name="param_1",
                 checks=(CheckHexList(LEN.PARAM_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_2, length=LEN.PARAM_2,
                 title="Param2", name="param_2",
                 checks=(CheckHexList(LEN.PARAM_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_3, length=LEN.PARAM_3,
                 title="Param3", name="param_3",
                 checks=(CheckHexList(LEN.PARAM_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_4, length=LEN.PARAM_4,
                 title="Param4", name="param_4",
                 checks=(CheckHexList(LEN.PARAM_4 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_5, length=LEN.PARAM_5,
                 title="Param5", name="param_5",
                 checks=(CheckHexList(LEN.PARAM_5 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_6, length=LEN.PARAM_6,
                 title="Param6", name="param_6",
                 checks=(CheckHexList(LEN.PARAM_6 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_7, length=LEN.PARAM_7,
                 title="Param7", name="param_7",
                 checks=(CheckHexList(LEN.PARAM_7 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_8, length=LEN.PARAM_8,
                 title="Param8", name="param_8",
                 checks=(CheckHexList(LEN.PARAM_8 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.PADDING),
    )
# end class RgbLedBinInfo


class LedBinIndex0(RgbLedBinInfoHead):
    """
    ``LedBinIndex0`` implementation class for re-format response data structure from
        - ManageRgbLedBinInfo with GetOrSet = 0, LedBinIndex = 0 (Bin value brightness)

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    GetOrSet                      8
    RgbClusterIndex               8
    LedBinIndex                   8
    Combination1                  8
    Combination2                  8
    Combination3                  8
    Combination4                  8
    Combination5                  8
    Padding                       64
    ============================  ==========
    """
    class FID(RgbLedBinInfoHead.FID):
        # See ``RgbLedBinInfoHead.FID``
        COMBINATION_1 = RgbLedBinInfoHead.FID.LED_BIN_INDEX - 1
        COMBINATION_2 = COMBINATION_1 - 1
        COMBINATION_3 = COMBINATION_2 - 1
        COMBINATION_4 = COMBINATION_3 - 1
        COMBINATION_5 = COMBINATION_4 - 1
        PADDING = COMBINATION_5 - 1
    # end class FID

    class LEN(RgbLedBinInfoHead.LEN):
        # See ``RgbLedBinInfoHead.LEN``
        COMBINATION_1 = 0x8
        COMBINATION_2 = 0x8
        COMBINATION_3 = 0x8
        COMBINATION_4 = 0x8
        COMBINATION_5 = 0x8
        PADDING = 0x40
    # end class LEN

    FIELDS = RGBEffects.FIELDS + (
        BitField(fid=FID.COMBINATION_1, length=LEN.COMBINATION_1,
                 title="Combination1", name="combination_1",
                 checks=(CheckHexList(LEN.COMBINATION_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.COMBINATION_2, length=LEN.COMBINATION_2,
                 title="Combination2", name="combination_2",
                 checks=(CheckHexList(LEN.COMBINATION_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.COMBINATION_3, length=LEN.COMBINATION_3,
                 title="Combination3", name="combination_3",
                 checks=(CheckHexList(LEN.COMBINATION_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.COMBINATION_4, length=LEN.COMBINATION_4,
                 title="Combination4", name="combination_4",
                 checks=(CheckHexList(LEN.COMBINATION_4 // 8),
                         CheckByte(),)),
        BitField(fid=FID.COMBINATION_5, length=LEN.COMBINATION_5,
                 title="Combination5", name="combination_5",
                 checks=(CheckHexList(LEN.COMBINATION_5 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.PADDING),
    )
# end class LedBinIndex0


class LedBinIndex1(RgbLedBinInfoHead):
    """
    ``LedBinIndex1`` implementation class for re-format response data structure from
        - ManageRgbLedBinInfo with GetOrSet = 0, LedBinIndex = 1 (Bin value color)

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    GetOrSet                      8
    RgbClusterIndex               8
    LedBinIndex                   8
    BinCode1                      8
    BinCode2                      8
    Padding                       88
    ============================  ==========
    """
    class FID(RgbLedBinInfoHead.FID):
        # See ``RgbLedBinInfoHead.FID``
        BIN_CODE_1 = RgbLedBinInfoHead.FID.LED_BIN_INDEX - 1
        BIN_CODE_2 = BIN_CODE_1 - 1
        PADDING = BIN_CODE_2 - 1
    # end class FID

    class LEN(RgbLedBinInfoHead.LEN):
        # See ``RgbLedBinInfoHead.LEN``
        BIN_CODE_1 = 0x8
        BIN_CODE_2 = 0x8
        PADDING = 0x58
    # end class LEN

    FIELDS = RGBEffects.FIELDS + (
        BitField(fid=FID.BIN_CODE_1, length=LEN.BIN_CODE_1,
                 title="BinCode1", name="bin_code_1",
                 checks=(CheckHexList(LEN.BIN_CODE_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.BIN_CODE_2, length=LEN.BIN_CODE_2,
                 title="BinCode2", name="bin_code_2",
                 checks=(CheckHexList(LEN.BIN_CODE_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.PADDING),
    )
# end class LedBinIndex1


class LedBinIndex2(RgbLedBinInfoHead):
    """
    ``LedBinIndex2`` implementation class for re-format response data structure from
        - ManageRgbLedBinInfo with GetOrSet = 0, LedBinIndex = 2 (Calibration factors)

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    GetOrSet                      8
    RgbClusterIndex               8
    LedBinIndex                   8
    CaliFactor1                   8
    CaliFactor2                   8
    CaliFactor3                   8
    Padding                       80
    ============================  ==========
    """
    class FID(RgbLedBinInfoHead.FID):
        # See ``RgbLedBinInfoHead.FID``
        CALI_FACTOR_1 = RgbLedBinInfoHead.FID.LED_BIN_INDEX - 1
        CALI_FACTOR_2 = CALI_FACTOR_1 - 1
        CALI_FACTOR_3 = CALI_FACTOR_2 - 1
        PADDING = CALI_FACTOR_3 - 1
    # end class FID

    class LEN(RgbLedBinInfoHead.LEN):
        # See ``RgbLedBinInfoHead.LEN``
        CALI_FACTOR_1 = 0x8
        CALI_FACTOR_2 = 0x8
        CALI_FACTOR_3 = 0x8
        PADDING = 0x50
    # end class LEN

    FIELDS = RGBEffects.FIELDS + (
        BitField(fid=FID.CALI_FACTOR_1, length=LEN.CALI_FACTOR_1,
                 title="CaliFactor1", name="cali_factor_1",
                 checks=(CheckHexList(LEN.CALI_FACTOR_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.CALI_FACTOR_2, length=LEN.CALI_FACTOR_2,
                 title="CaliFactor2", name="cali_factor_2",
                 checks=(CheckHexList(LEN.CALI_FACTOR_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.CALI_FACTOR_3, length=LEN.CALI_FACTOR_3,
                 title="CaliFactor3", name="cali_factor_3",
                 checks=(CheckHexList(LEN.CALI_FACTOR_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.PADDING),
    )
# end class LedBinIndex2


class LedBinIndex3(RgbLedBinInfoHead):
    """
    ``LedBinIndex3`` implementation class for re-format response data structure from
        - ManageRgbLedBinInfo with GetOrSet = 0, LedBinIndex = 3 (Brightness)

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    GetOrSet                      8
    RgbClusterIndex               8
    LedBinIndex                   8
    RIntensity                    16
    GIntensity                    16
    BIntensity                    16
    Padding                       56
    ============================  ==========
    """
    class FID(RgbLedBinInfoHead.FID):
        # See ``RgbLedBinInfoHead.FID``
        R_INTENSITY = RgbLedBinInfoHead.FID.LED_BIN_INDEX - 1
        G_INTENSITY = R_INTENSITY - 1
        B_INTENSITY = G_INTENSITY - 1
        PADDING = B_INTENSITY - 1
    # end class FID

    class LEN(RgbLedBinInfoHead.LEN):
        # See ``RgbLedBinInfoHead.LEN``
        R_INTENSITY = 0x10
        G_INTENSITY = 0x10
        B_INTENSITY = 0x10
        PADDING = 0x38
    # end class LEN

    FIELDS = RGBEffects.FIELDS + (
        BitField(fid=FID.R_INTENSITY, length=LEN.R_INTENSITY,
                 title="RIntensity", name="r_intensity",
                 checks=(CheckHexList(LEN.R_INTENSITY // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.R_INTENSITY) - 1),)),
        BitField(fid=FID.G_INTENSITY, length=LEN.G_INTENSITY,
                 title="GIntensity", name="g_intensity",
                 checks=(CheckHexList(LEN.G_INTENSITY // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.G_INTENSITY) - 1),)),
        BitField(fid=FID.B_INTENSITY, length=LEN.B_INTENSITY,
                 title="BIntensity", name="b_intensity",
                 checks=(CheckHexList(LEN.B_INTENSITY // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.B_INTENSITY) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.PADDING),
    )
# end class LedBinIndex3


class LedBinIndex4(RgbLedBinInfoHead):
    """
    ``LedBinIndex4`` implementation class for re-format response data structure from
        - ManageRgbLedBinInfo with GetOrSet = 0, LedBinIndex = 4 (Colorimetric X)

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    GetOrSet                      8
    RgbClusterIndex               8
    LedBinIndex                   8
    RCx                           16
    GCx                           16
    BCx                           16
    WCx                           16
    Padding                       40
    ============================  ==========
    """
    class FID(RgbLedBinInfoHead.FID):
        # See ``RgbLedBinInfoHead.FID``
        R_CX = RgbLedBinInfoHead.FID.LED_BIN_INDEX - 1
        G_CX = R_CX - 1
        B_CX = G_CX - 1
        W_CX = B_CX - 1
        PADDING = W_CX - 1
    # end class FID

    class LEN(RgbLedBinInfoHead.LEN):
        # See ``RgbLedBinInfoHead.LEN``
        R_CX = 0x10
        G_CX = 0x10
        B_CX = 0x10
        W_CX = 0x10
        PADDING = 0x28
    # end class LEN

    FIELDS = RGBEffects.FIELDS + (
        BitField(fid=FID.R_CX, length=LEN.R_CX,
                 title="RCx", name="r_cx",
                 checks=(CheckHexList(LEN.R_CX // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.R_CX) - 1),)),
        BitField(fid=FID.G_CX, length=LEN.G_CX,
                 title="GCx", name="g_cx",
                 checks=(CheckHexList(LEN.G_CX // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.G_CX) - 1),)),
        BitField(fid=FID.B_CX, length=LEN.B_CX,
                 title="BCx", name="b_cx",
                 checks=(CheckHexList(LEN.B_CX // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.B_CX) - 1),)),
        BitField(fid=FID.W_CX, length=LEN.W_CX,
                 title="WCx", name="w_cx",
                 checks=(CheckHexList(LEN.W_CX // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.W_CX) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.PADDING),
    )
# end class LedBinIndex4


class LedBinIndex5(RgbLedBinInfoHead):
    """
    ``LedBinIndex5`` implementation class for re-format response data structure from
        - ManageRgbLedBinInfo with GetOrSet = 0, LedBinIndex = 5 (Colorimetric Y)

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    GetOrSet                      8
    RgbClusterIndex               8
    LedBinIndex                   8
    RCy                           16
    GCy                           16
    BCy                           16
    WCy                           16
    Padding                       40
    ============================  ==========
    """
    class FID(RgbLedBinInfoHead.FID):
        # See ``RgbLedBinInfoHead.FID``
        R_CY = RgbLedBinInfoHead.FID.LED_BIN_INDEX - 1
        G_CY = R_CY - 1
        B_CY = G_CY - 1
        W_CY = B_CY - 1
        PADDING = W_CY - 1
    # end class FID

    class LEN(RgbLedBinInfoHead.LEN):
        # See ``RgbLedBinInfoHead.LEN``
        R_CY = 0x10
        G_CY = 0x10
        B_CY = 0x10
        W_CY = 0x10
        PADDING = 0x28
    # end class LEN

    FIELDS = RGBEffects.FIELDS + (
        BitField(fid=FID.R_CY, length=LEN.R_CY,
                 title="RCy", name="r_cy",
                 checks=(CheckHexList(LEN.R_CY // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.R_CY) - 1),)),
        BitField(fid=FID.G_CY, length=LEN.G_CY,
                 title="GCy", name="g_cy",
                 checks=(CheckHexList(LEN.G_CY // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.G_CY) - 1),)),
        BitField(fid=FID.B_CY, length=LEN.B_CY,
                 title="BCy", name="b_cy",
                 checks=(CheckHexList(LEN.B_CY // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.B_CY) - 1),)),
        BitField(fid=FID.W_CY, length=LEN.W_CY,
                 title="WCy", name="w_cy",
                 checks=(CheckHexList(LEN.W_CY // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.W_CY) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.PADDING),
    )
# end class LedBinIndex5


class SwControl(ManageHead):
    """
    This class is to be used as a base class for several messages in this feature.
        - ManageSWControl
        - ManageSWControlResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    GetOrSet                      8
    SwControlFlags                8
    EventsNotificationFlags       8
    Reserved                      104
    ============================  ==========
    """
    class FID(ManageHead.FID):
        # See ``ManageHead.FID``
        SW_CONTROL_FLAGS = ManageHead.FID.GET_OR_SET - 1
        EVENTS_NOTIFICATION_FLAGS = SW_CONTROL_FLAGS - 1
        RESERVED = EVENTS_NOTIFICATION_FLAGS - 1
    # end class FID

    class LEN(ManageHead.LEN):
        # See ``ManageHead.LEN``
        SW_CONTROL_FLAGS = 0x8
        EVENTS_NOTIFICATION_FLAGS = 0x8
        RESERVED = 0x68
    # end class LEN

    FIELDS = ManageHead.FIELDS + (
        BitField(fid=FID.SW_CONTROL_FLAGS, length=LEN.SW_CONTROL_FLAGS,
                 title="SwControlFlags", name="sw_control_flags",
                 checks=(CheckHexList(LEN.SW_CONTROL_FLAGS // 8),
                         CheckByte(),)),
        BitField(fid=FID.EVENTS_NOTIFICATION_FLAGS, length=LEN.EVENTS_NOTIFICATION_FLAGS,
                 title="EventsNotificationFlags", name="events_notification_flags",
                 checks=(CheckHexList(LEN.EVENTS_NOTIFICATION_FLAGS // 8),
                         CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=RGBEffects.DEFAULT.RESERVED),
    )
# end class SwControl


class RgbPowerModeConfig(ManageHead):
    """
    This class is to be used as a base class for several messages in this feature.
        - ManageRgbPowerModeConfig
        - ManageRgbPowerModeConfigResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    GetOrSet                      8
    RgbPowerModeFlags             16
    RgbNoActTimeoutToPSave        16
    RgbNoActTimeoutToOff          16
    Reserved                      72
    ============================  ==========
    """
    class FID(ManageHead.FID):
        # See ``ManageHead.FID``
        RGB_POWER_MODE_FLAGS = ManageHead.FID.GET_OR_SET - 1
        RGB_NO_ACT_TIMEOUT_TO_PSAVE = RGB_POWER_MODE_FLAGS - 1
        RGB_NO_ACT_TIMEOUT_TO_OFF = RGB_NO_ACT_TIMEOUT_TO_PSAVE - 1
        RESERVED = RGB_NO_ACT_TIMEOUT_TO_OFF - 1
    # end class FID

    class LEN(ManageHead.LEN):
        # See ``ManageHead.LEN``
        RGB_POWER_MODE_FLAGS = 0x10
        RGB_NO_ACT_TIMEOUT_TO_PSAVE = 0x10
        RGB_NO_ACT_TIMEOUT_TO_OFF = 0x10
        RESERVED = 0x48
    # end class LEN

    FIELDS = ManageHead.FIELDS + (
        BitField(fid=FID.RGB_POWER_MODE_FLAGS, length=LEN.RGB_POWER_MODE_FLAGS,
                 title="RgbPowerModeFlags", name="rgb_power_mode_flags",
                 checks=(CheckHexList(LEN.RGB_POWER_MODE_FLAGS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RGB_POWER_MODE_FLAGS) - 1),)),
        BitField(fid=FID.RGB_NO_ACT_TIMEOUT_TO_PSAVE, length=LEN.RGB_NO_ACT_TIMEOUT_TO_PSAVE,
                 title="RgbNoActTimeoutToPSave", name="rgb_no_act_timeout_to_psave",
                 checks=(CheckHexList(LEN.RGB_NO_ACT_TIMEOUT_TO_PSAVE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RGB_NO_ACT_TIMEOUT_TO_PSAVE) - 1),)),
        BitField(fid=FID.RGB_NO_ACT_TIMEOUT_TO_OFF, length=LEN.RGB_NO_ACT_TIMEOUT_TO_OFF,
                 title="RgbNoActTimeoutToOff", name="rgb_no_act_timeout_to_off",
                 checks=(CheckHexList(LEN.RGB_NO_ACT_TIMEOUT_TO_OFF // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RGB_NO_ACT_TIMEOUT_TO_OFF) - 1),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=RGBEffects.DEFAULT.RESERVED),
    )
# end class RgbPowerModeConfig


class RgbPowerMode(ManageHead):
    """
    This class is to be used as a base class for several messages in this feature.
        - ManageRgbPowerMode
        - ManageRgbPowerModeResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    GetOrSet                      8
    RgbPowerMode                  8
    Reserved                      112
    ============================  ==========
    """
    class FID(ManageHead.FID):
        # See ``ManageHead.FID``
        RGB_POWER_MODE = ManageHead.FID.GET_OR_SET - 1
        RESERVED = RGB_POWER_MODE - 1
    # end class FID

    class LEN(ManageHead.LEN):
        # See ``ManageHead.LEN``
        RGB_POWER_MODE = 0x8
        RESERVED = 0x70
    # end class LEN

    FIELDS = ManageHead.FIELDS + (
        BitField(fid=FID.RGB_POWER_MODE, length=LEN.RGB_POWER_MODE,
                 title="RgbPowerMode", name="rgb_power_mode",
                 checks=(CheckHexList(LEN.RGB_POWER_MODE // 8),
                         CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=RGBEffects.DEFAULT.RESERVED),
    )
# end class RgbPowerMode


class GetInfoV0(RgbClusterInfoHead):
    """
    ``GetInfoV0`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    Padding                       8
    ============================  ==========
    """
    class FID(RgbClusterInfoHead.FID):
        # See ``RgbClusterInfoHead.FID``
        PADDING = RgbClusterInfoHead.FID.RGB_CLUSTER_EFFECT_INDEX - 1
    # end class FID

    class LEN(RgbClusterInfoHead.LEN):
        # See ``RgbClusterInfoHead.LEN``
        PADDING = 0x8
    # end class LEN

    FIELDS = RgbClusterInfoHead.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, rgb_cluster_index, rgb_cluster_effect_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param rgb_cluster_index: The index of the RGB cluster.
        :type rgb_cluster_index: ``int`` or ``HexList``
        :param rgb_cluster_effect_index: The index of the effect within that RGB cluster.
        :type rgb_cluster_effect_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetInfoResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.rgb_cluster_index = rgb_cluster_index
        self.rgb_cluster_effect_index = rgb_cluster_effect_index
    # end def __init__
# end class GetInfoV0


class GetInfoV1ToV4(EffectInfoHead):
    """
    ``GetInfoV1ToV4`` implementation class for versions 1, 2, 3 and 4

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    TypeOfInfo                    8
    Param1                        8
    Param2                        8
    Param3                        8
    Param4                        8
    Param5                        8
    Param6                        8
    Param7                        8
    Param8                        8
    Param9                        8
    Param10                       8
    Param11                       8
    Param12                       8
    Param13                       8
    ============================  ==========
    """
    class FID(EffectInfoHead.FID):
        # See ``EffectInfoHead.FID``
        PARAM_1 = EffectInfoHead.FID.TYPE_OF_INFO - 1
        PARAM_2 = PARAM_1 - 1
        PARAM_3 = PARAM_2 - 1
        PARAM_4 = PARAM_3 - 1
        PARAM_5 = PARAM_4 - 1
        PARAM_6 = PARAM_5 - 1
        PARAM_7 = PARAM_6 - 1
        PARAM_8 = PARAM_7 - 1
        PARAM_9 = PARAM_8 - 1
        PARAM_10 = PARAM_9 - 1
        PARAM_11 = PARAM_10 - 1
        PARAM_12 = PARAM_11 - 1
        PARAM_13 = PARAM_12 - 1
    # end class FID

    class LEN(EffectInfoHead.LEN):
        # See ``EffectInfoHead.LEN``
        PARAM_1 = 0x8
        PARAM_2 = 0x8
        PARAM_3 = 0x8
        PARAM_4 = 0x8
        PARAM_5 = 0x8
        PARAM_6 = 0x8
        PARAM_7 = 0x8
        PARAM_8 = 0x8
        PARAM_9 = 0x8
        PARAM_10 = 0x8
        PARAM_11 = 0x8
        PARAM_12 = 0x8
        PARAM_13 = 0x8
    # end class LEN

    FIELDS = EffectInfoHead.FIELDS + (
        BitField(fid=FID.PARAM_1, length=LEN.PARAM_1,
                 title="Param1", name="param_1",
                 checks=(CheckHexList(LEN.PARAM_1 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_2, length=LEN.PARAM_2,
                 title="Param2", name="param_2",
                 checks=(CheckHexList(LEN.PARAM_2 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_3, length=LEN.PARAM_3,
                 title="Param3", name="param_3",
                 checks=(CheckHexList(LEN.PARAM_3 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_4, length=LEN.PARAM_4,
                 title="Param4", name="param_4",
                 checks=(CheckHexList(LEN.PARAM_4 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_5, length=LEN.PARAM_5,
                 title="Param5", name="param_5",
                 checks=(CheckHexList(LEN.PARAM_5 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_6, length=LEN.PARAM_6,
                 title="Param6", name="param_6",
                 checks=(CheckHexList(LEN.PARAM_6 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_7, length=LEN.PARAM_7,
                 title="Param7", name="param_7",
                 checks=(CheckHexList(LEN.PARAM_7 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_8, length=LEN.PARAM_8,
                 title="Param8", name="param_8",
                 checks=(CheckHexList(LEN.PARAM_8 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_9, length=LEN.PARAM_9,
                 title="Param9", name="param_9",
                 checks=(CheckHexList(LEN.PARAM_9 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_10, length=LEN.PARAM_10,
                 title="Param10", name="param_10",
                 checks=(CheckHexList(LEN.PARAM_10 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_11, length=LEN.PARAM_11,
                 title="Param11", name="param_11",
                 checks=(CheckHexList(LEN.PARAM_11 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_12, length=LEN.PARAM_12,
                 title="Param12", name="param_12",
                 checks=(CheckHexList(LEN.PARAM_12 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_13, length=LEN.PARAM_13,
                 title="Param13", name="param_13",
                 checks=(CheckHexList(LEN.PARAM_13 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
    )

    def __init__(self, device_index, feature_index, rgb_cluster_index, rgb_cluster_effect_index, type_of_info,
                 param_1=0, param_2=0, param_3=0, param_4=0, param_5=0, param_6=0, param_7=0, param_8=0, param_9=0,
                 param_10=0, param_11=0, param_12=0, param_13=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param rgb_cluster_index: The index of the RGB cluster.
        :type rgb_cluster_index: ``int`` or ``HexList``
        :param rgb_cluster_effect_index: The index of the effect within that RGB cluster.
        :type rgb_cluster_effect_index: ``int`` or ``HexList``
        :param type_of_info: This parameter defines the type of information requested, depending on the type of request
        :type type_of_info: ``int`` or ``HexList``
        :param param_1: The parameters are definition for effect. - OPTIONAL
        :type param_1: ``int`` or ``HexList``
        :param param_2: The parameters are definition for effect. - OPTIONAL
        :type param_2: ``int`` or ``HexList``
        :param param_3: The parameters are definition for effect. - OPTIONAL
        :type param_3: ``int`` or ``HexList``
        :param param_4: The parameters are definition for effect. - OPTIONAL
        :type param_4: ``int`` or ``HexList``
        :param param_5: The parameters are definition for effect. - OPTIONAL
        :type param_5: ``int`` or ``HexList``
        :param param_6: The parameters are definition for effect. - OPTIONAL
        :type param_6: ``int`` or ``HexList``
        :param param_7: The parameters are definition for effect. - OPTIONAL
        :type param_7: ``int`` or ``HexList``
        :param param_8: The parameters are definition for effect. - OPTIONAL
        :type param_8: ``int`` or ``HexList``
        :param param_9: The parameters are definition for effect. - OPTIONAL
        :type param_9: ``int`` or ``HexList``
        :param param_10: The parameters are definition for effect. - OPTIONAL
        :type param_10: ``int`` or ``HexList``
        :param param_11: The parameters are definition for effect. - OPTIONAL
        :type param_11: ``int`` or ``HexList``
        :param param_12: The parameters are definition for effect. - OPTIONAL
        :type param_12: ``int`` or ``HexList``
        :param param_13: The parameters are definition for effect. - OPTIONAL
        :type param_13: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetInfoResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rgb_cluster_index = rgb_cluster_index
        self.rgb_cluster_effect_index = rgb_cluster_effect_index
        self.type_of_info = type_of_info
        self.param_1 = param_1
        self.param_2 = param_2
        self.param_3 = param_3
        self.param_4 = param_4
        self.param_5 = param_5
        self.param_6 = param_6
        self.param_7 = param_7
        self.param_8 = param_8
        self.param_9 = param_9
        self.param_10 = param_10
        self.param_11 = param_11
        self.param_12 = param_12
        self.param_13 = param_13
    # end def __init__
# end class GetInfoV1ToV4


class GetInfoResponse(RGBEffects):
    """
    ``GetInfoResponse`` implementation class for versions 0, 1, 2, 3 and 4

    Param1..Param14 are containers for GetInfo about device, RGB cluster, RGB effects and custom onboard effect.
    The GetInfoResponse can be re-formatted to
    - InfoAboutDeviceV0ToV1
    - InfoAboutDeviceV2ToV4
    - InfoAboutRGBClusterV0
    - InfoAboutRGBClusterV1ToV4
    - InfoAboutEffectGeneralInfo
    - InfoAboutCustomOnboardStoredEffect0
    - InfoAboutCustomOnboardStoredEffect1
    - InfoAboutCustomOnboardStoredEffect2
    - InfoAboutCustomOnboardStoredEffect3
    - InfoAboutCustomOnboardStoredEffect4
    - InfoAboutCustomOnboardStoredEffect5
    - InfoAboutCustomOnboardStoredEffect6

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    Param1                        8
    Param2                        8
    Param3                        8
    Param4                        8
    Param5                        8
    Param6                        8
    Param7                        8
    Param8                        8
    Param9                        8
    Param10                       8
    Param11                       8
    Param12                       8
    Param13                       8
    Param14                       8
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetInfoV0, GetInfoV1ToV4,)
    VERSION = (0, 1, 2, 3, 4,)
    FUNCTION_INDEX = 0

    class FID(RGBEffects.FID):
        # See ``RGBEffects.FID``
        RGB_CLUSTER_INDEX = RGBEffects.FID.SOFTWARE_ID - 1
        RGB_CLUSTER_EFFECT_INDEX = RGB_CLUSTER_INDEX - 1
        PARAM_1 = RGB_CLUSTER_EFFECT_INDEX - 1
        PARAM_2 = PARAM_1 - 1
        PARAM_3 = PARAM_2 - 1
        PARAM_4 = PARAM_3 - 1
        PARAM_5 = PARAM_4 - 1
        PARAM_6 = PARAM_5 - 1
        PARAM_7 = PARAM_6 - 1
        PARAM_8 = PARAM_7 - 1
        PARAM_9 = PARAM_8 - 1
        PARAM_10 = PARAM_9 - 1
        PARAM_11 = PARAM_10 - 1
        PARAM_12 = PARAM_11 - 1
        PARAM_13 = PARAM_12 - 1
        PARAM_14 = PARAM_13 - 1
    # end class FID

    class LEN(RGBEffects.LEN):
        # See ``RGBEffects.LEN``
        RGB_CLUSTER_INDEX = 0x8
        RGB_CLUSTER_EFFECT_INDEX = 0x8
        PARAM_1 = 0x8
        PARAM_2 = 0x8
        PARAM_3 = 0x8
        PARAM_4 = 0x8
        PARAM_5 = 0x8
        PARAM_6 = 0x8
        PARAM_7 = 0x8
        PARAM_8 = 0x8
        PARAM_9 = 0x8
        PARAM_10 = 0x8
        PARAM_11 = 0x8
        PARAM_12 = 0x8
        PARAM_13 = 0x8
        PARAM_14 = 0x8
    # end class LEN

    FIELDS = RGBEffects.FIELDS + (
        BitField(fid=FID.RGB_CLUSTER_INDEX, length=LEN.RGB_CLUSTER_INDEX,
                 title="RgbClusterIndex", name="rgb_cluster_index",
                 checks=(CheckHexList(LEN.RGB_CLUSTER_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_CLUSTER_EFFECT_INDEX, length=LEN.RGB_CLUSTER_EFFECT_INDEX,
                 title="RgbClusterEffectIndex", name="rgb_cluster_effect_index",
                 checks=(CheckHexList(LEN.RGB_CLUSTER_EFFECT_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_1, length=LEN.PARAM_1,
                 title="Param1", name="param_1",
                 checks=(CheckHexList(LEN.PARAM_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_2, length=LEN.PARAM_2,
                 title="Param2", name="param_2",
                 checks=(CheckHexList(LEN.PARAM_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_3, length=LEN.PARAM_3,
                 title="Param3", name="param_3",
                 checks=(CheckHexList(LEN.PARAM_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_4, length=LEN.PARAM_4,
                 title="Param4", name="param_4",
                 checks=(CheckHexList(LEN.PARAM_4 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_5, length=LEN.PARAM_5,
                 title="Param5", name="param_5",
                 checks=(CheckHexList(LEN.PARAM_5 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_6, length=LEN.PARAM_6,
                 title="Param6", name="param_6",
                 checks=(CheckHexList(LEN.PARAM_6 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_7, length=LEN.PARAM_7,
                 title="Param7", name="param_7",
                 checks=(CheckHexList(LEN.PARAM_7 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_8, length=LEN.PARAM_8,
                 title="Param8", name="param_8",
                 checks=(CheckHexList(LEN.PARAM_8 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_9, length=LEN.PARAM_9,
                 title="Param9", name="param_9",
                 checks=(CheckHexList(LEN.PARAM_9 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_10, length=LEN.PARAM_10,
                 title="Param10", name="param_10",
                 checks=(CheckHexList(LEN.PARAM_10 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_11, length=LEN.PARAM_11,
                 title="Param11", name="param_11",
                 checks=(CheckHexList(LEN.PARAM_11 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_12, length=LEN.PARAM_12,
                 title="Param12", name="param_12",
                 checks=(CheckHexList(LEN.PARAM_12 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_13, length=LEN.PARAM_13,
                 title="Param13", name="param_13",
                 checks=(CheckHexList(LEN.PARAM_13 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_14, length=LEN.PARAM_14,
                 title="Param14", name="param_14",
                 checks=(CheckHexList(LEN.PARAM_14 // 8),
                         CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, rgb_cluster_index, rgb_cluster_effect_index,
                 param_1, param_2, param_3, param_4, param_5, param_6, param_7, param_8, param_9, param_10, param_11,
                 param_12, param_13, param_14, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param rgb_cluster_index: The index of the RGB cluster.
        :type rgb_cluster_index: ``int`` or ``HexList``
        :param rgb_cluster_effect_index: The index of the effect within that RGB cluster.
        :type rgb_cluster_effect_index: ``int`` or ``HexList``
        :param param_1: The parameters are definition for effect.
        :type param_1: ``int`` or ``HexList``
        :param param_2: The parameters are definition for effect.
        :type param_2: ``int`` or ``HexList``
        :param param_3: The parameters are definition for effect.
        :type param_3: ``int`` or ``HexList``
        :param param_4: The parameters are definition for effect.
        :type param_4: ``int`` or ``HexList``
        :param param_5: The parameters are definition for effect.
        :type param_5: ``int`` or ``HexList``
        :param param_6: The parameters are definition for effect.
        :type param_6: ``int`` or ``HexList``
        :param param_7: The parameters are definition for effect.
        :type param_7: ``int`` or ``HexList``
        :param param_8: The parameters are definition for effect.
        :type param_8: ``int`` or ``HexList``
        :param param_9: The parameters are definition for effect.
        :type param_9: ``int`` or ``HexList``
        :param param_10: The parameters are definition for effect.
        :type param_10: ``int`` or ``HexList``
        :param param_11: The parameters are definition for effect.
        :type param_11: ``int`` or ``HexList``
        :param param_12: The parameters are definition for effect.
        :type param_12: ``int`` or ``HexList``
        :param param_13: The parameters are definition for effect.
        :type param_13: ``int`` or ``HexList``
        :param param_14: The parameters are definition for effect.
        :type param_14: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rgb_cluster_index = rgb_cluster_index
        self.rgb_cluster_effect_index = rgb_cluster_effect_index
        self.param_1 = param_1
        self.param_2 = param_2
        self.param_3 = param_3
        self.param_4 = param_4
        self.param_5 = param_5
        self.param_6 = param_6
        self.param_7 = param_7
        self.param_8 = param_8
        self.param_9 = param_9
        self.param_10 = param_10
        self.param_11 = param_11
        self.param_12 = param_12
        self.param_13 = param_13
        self.param_14 = param_14
    # end def __init__
# end class GetInfoResponse


class SetRgbClusterEffectV0(RGBEffects):
    """
    ``SetRgbClusterEffectV0`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    Param1                        8
    Param2                        8
    Param3                        8
    Param4                        8
    Param5                        8
    Param6                        8
    Param7                        8
    Param8                        8
    Param9                        8
    Param10                       8
    Reserved                      6
    Persistence                   2
    Padding                       24
    ============================  ==========
    """
    class FID(RGBEffects.FID):
        # See ``RGBEffects.FID``
        RGB_CLUSTER_INDEX = RGBEffects.FID.SOFTWARE_ID - 1
        RGB_CLUSTER_EFFECT_INDEX = RGB_CLUSTER_INDEX - 1
        PARAM_1 = RGB_CLUSTER_EFFECT_INDEX - 1
        PARAM_2 = PARAM_1 - 1
        PARAM_3 = PARAM_2 - 1
        PARAM_4 = PARAM_3 - 1
        PARAM_5 = PARAM_4 - 1
        PARAM_6 = PARAM_5 - 1
        PARAM_7 = PARAM_6 - 1
        PARAM_8 = PARAM_7 - 1
        PARAM_9 = PARAM_8 - 1
        PARAM_10 = PARAM_9 - 1
        RESERVED = PARAM_10 - 1
        PERSISTENCE = RESERVED - 1
        PADDING = PERSISTENCE - 1
    # end class FID

    class LEN(RGBEffects.LEN):
        # See ``RGBEffects.LEN``
        RGB_CLUSTER_INDEX = 0x8
        RGB_CLUSTER_EFFECT_INDEX = 0x8
        PARAM_1 = 0x8
        PARAM_2 = 0x8
        PARAM_3 = 0x8
        PARAM_4 = 0x8
        PARAM_5 = 0x8
        PARAM_6 = 0x8
        PARAM_7 = 0x8
        PARAM_8 = 0x8
        PARAM_9 = 0x8
        PARAM_10 = 0x8
        RESERVED = 0x6
        PERSISTENCE = 0x2
        PADDING = 0x18
    # end class LEN

    FIELDS = RGBEffects.FIELDS + (
        BitField(fid=FID.RGB_CLUSTER_INDEX, length=LEN.RGB_CLUSTER_INDEX,
                 title="RgbClusterIndex", name="rgb_cluster_index",
                 checks=(CheckHexList(LEN.RGB_CLUSTER_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_CLUSTER_EFFECT_INDEX, length=LEN.RGB_CLUSTER_EFFECT_INDEX,
                 title="RgbClusterEffectIndex", name="rgb_cluster_effect_index",
                 checks=(CheckHexList(LEN.RGB_CLUSTER_EFFECT_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_1, length=LEN.PARAM_1,
                 title="Param1", name="param_1",
                 checks=(CheckHexList(LEN.PARAM_1 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_2, length=LEN.PARAM_2,
                 title="Param2", name="param_2",
                 checks=(CheckHexList(LEN.PARAM_2 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_3, length=LEN.PARAM_3,
                 title="Param3", name="param_3",
                 checks=(CheckHexList(LEN.PARAM_3 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_4, length=LEN.PARAM_4,
                 title="Param4", name="param_4",
                 checks=(CheckHexList(LEN.PARAM_4 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_5, length=LEN.PARAM_5,
                 title="Param5", name="param_5",
                 checks=(CheckHexList(LEN.PARAM_5 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_6, length=LEN.PARAM_6,
                 title="Param6", name="param_6",
                 checks=(CheckHexList(LEN.PARAM_6 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_7, length=LEN.PARAM_7,
                 title="Param7", name="param_7",
                 checks=(CheckHexList(LEN.PARAM_7 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_8, length=LEN.PARAM_8,
                 title="Param8", name="param_8",
                 checks=(CheckHexList(LEN.PARAM_8 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_9, length=LEN.PARAM_9,
                 title="Param9", name="param_9",
                 checks=(CheckHexList(LEN.PARAM_9 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_10, length=LEN.PARAM_10,
                 title="Param10", name="param_10",
                 checks=(CheckHexList(LEN.PARAM_10 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PERSISTENCE, length=LEN.PERSISTENCE,
                 title="Persistence", name="persistence",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.PERSISTENCE) - 1),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index,
                 rgb_cluster_index, rgb_cluster_effect_index, persistence=0, param_1=0, param_2=0, param_3=0, param_4=0,
                 param_5=0, param_6=0, param_7=0, param_8=0, param_9=0, param_10=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param rgb_cluster_index: The index of the RGB cluster.
        :type rgb_cluster_index: ``int`` or ``HexList``
        :param rgb_cluster_effect_index: The index of the effect within that RGB cluster.
        :type rgb_cluster_effect_index: ``int`` or ``HexList``
        :param param_1: The parameters are definition for effect. - OPTIONAL
        :type param_1: ``int`` or ``HexList``
        :param param_2: The parameters are definition for effect. - OPTIONAL
        :type param_2: ``int`` or ``HexList``
        :param param_3: The parameters are definition for effect. - OPTIONAL
        :type param_3: ``int`` or ``HexList``
        :param param_4: The parameters are definition for effect. - OPTIONAL
        :type param_4: ``int`` or ``HexList``
        :param param_5: The parameters are definition for effect. - OPTIONAL
        :type param_5: ``int`` or ``HexList``
        :param param_6: The parameters are definition for effect. - OPTIONAL
        :type param_6: ``int`` or ``HexList``
        :param param_7: The parameters are definition for effect. - OPTIONAL
        :type param_7: ``int`` or ``HexList``
        :param param_8: The parameters are definition for effect. - OPTIONAL
        :type param_8: ``int`` or ``HexList``
        :param param_9: The parameters are definition for effect. - OPTIONAL
        :type param_9: ``int`` or ``HexList``
        :param param_10: The parameters are definition for effect. - OPTIONAL
        :type param_10: ``int`` or ``HexList``
        :param persistence: Determine how the settings persist through a power cycle - OPTIONAL
        :type persistence: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetRgbClusterEffectResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rgb_cluster_index = rgb_cluster_index
        self.rgb_cluster_effect_index = rgb_cluster_effect_index
        self.param_1 = param_1
        self.param_2 = param_2
        self.param_3 = param_3
        self.param_4 = param_4
        self.param_5 = param_5
        self.param_6 = param_6
        self.param_7 = param_7
        self.param_8 = param_8
        self.param_9 = param_9
        self.param_10 = param_10
        self.persistence = persistence
    # end def __init__
# end class SetRgbClusterEffectV0


class SetRgbClusterEffectV1ToV4(SetRgbClusterEffectV0):
    """
    ``SetRgbClusterEffectV1ToV4`` implementation class for versions 1, 2, 3 and 4

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    Param1                        8
    Param2                        8
    Param3                        8
    Param4                        8
    Param5                        8
    Param6                        8
    Param7                        8
    Param8                        8
    Param9                        8
    Param10                       8
    Reserved                      4
    PowerMode                     2
    Persistence                   2
    Padding                       24
    ============================  ==========
    """
    class FID(SetRgbClusterEffectV0.FID):
        # See ``SetRgbClusterEffectV0.FID``
        POWER_MODE = SetRgbClusterEffectV0.FID.RESERVED - 1
        PERSISTENCE = POWER_MODE - 1
        PADDING = PERSISTENCE - 1
    # end class FID

    class LEN(SetRgbClusterEffectV0.LEN):
        # See ``SetRgbClusterEffectV0.LEN``
        RESERVED = 0x4
        POWER_MODE = 0x2
        PERSISTENCE = 0x2
        PADDING = 0x18
    # end class LEN

    FIELDS = SetRgbClusterEffectV0.FIELDS[:-3] + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                 default_value=RGBEffects.DEFAULT.RESERVED),
        BitField(fid=FID.POWER_MODE, length=LEN.POWER_MODE,
                 title="PowerMode", name="power_mode",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.POWER_MODE) - 1),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PERSISTENCE, length=LEN.PERSISTENCE,
                 title="Persistence", name="persistence",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.PERSISTENCE) - 1),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index,
                 rgb_cluster_index, rgb_cluster_effect_index, param_1=0, param_2=0, param_3=0, param_4=0, param_5=0,
                 param_6=0, param_7=0, param_8=0, param_9=0, param_10=0, power_mode=0, persistence=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param rgb_cluster_index: The index of the RGB cluster.
        :type rgb_cluster_index: ``int`` or ``HexList``
        :param rgb_cluster_effect_index: The index of the effect within that RGB cluster.
        :type rgb_cluster_effect_index: ``int`` or ``HexList``
        :param param_1: The parameters are definition for effect. - OPTIONAL
        :type param_1: ``int`` or ``HexList``
        :param param_2: The parameters are definition for effect. - OPTIONAL
        :type param_2: ``int`` or ``HexList``
        :param param_3: The parameters are definition for effect. - OPTIONAL
        :type param_3: ``int`` or ``HexList``
        :param param_4: The parameters are definition for effect. - OPTIONAL
        :type param_4: ``int`` or ``HexList``
        :param param_5: The parameters are definition for effect. - OPTIONAL
        :type param_5: ``int`` or ``HexList``
        :param param_6: The parameters are definition for effect. - OPTIONAL
        :type param_6: ``int`` or ``HexList``
        :param param_7: The parameters are definition for effect. - OPTIONAL
        :type param_7: ``int`` or ``HexList``
        :param param_8: The parameters are definition for effect. - OPTIONAL
        :type param_8: ``int`` or ``HexList``
        :param param_9: The parameters are definition for effect. - OPTIONAL
        :type param_9: ``int`` or ``HexList``
        :param param_10: The parameters are definition for effect. - OPTIONAL
        :type param_10: ``int`` or ``HexList``
        :param power_mode: RGB Power mode to which the effect will be applied - OPTIONAL
        :type power_mode: ``int`` or ``HexList``
        :param persistence: Determine how the settings persist through a power cycle - OPTIONAL
        :type persistence: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         rgb_cluster_index=rgb_cluster_index, rgb_cluster_effect_index=rgb_cluster_effect_index,
                         param_1=param_1, param_2=param_2, param_3=param_3, param_4=param_4, param_5=param_5,
                         param_6=param_6, param_7=param_7, param_8=param_8, param_9=param_9, param_10=param_10,
                         power_mode=power_mode, persistence=persistence,
                         **kwargs)
        self.power_mode = power_mode
    # end def __init__
# end class SetRgbClusterEffectV1ToV4


class SetRgbClusterEffectResponse(LongEmptyPacketDataFormat):
    """
    ``SetRgbClusterEffectResponse`` implementation class for versions 0, 1, 2 and 3
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetRgbClusterEffectV0, SetRgbClusterEffectV1ToV4,)
    VERSION = (0, 1, 2, 3, 4,)
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
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetRgbClusterEffectResponse


class SetMultiLedRgbClusterPattern(RGBEffects):
    """
    ``SetMultiLedRgbClusterPattern`` implementation class for versions 0, 1, 2 and 3

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    Pattern                       8
    Padding                       8
    ============================  ==========
    """
    class FID(RGBEffects.FID):
        # See ``RGBEffects.FID``
        RGB_CLUSTER_INDEX = RGBEffects.FID.SOFTWARE_ID - 1
        PATTERN = RGB_CLUSTER_INDEX - 1
        PADDING = PATTERN - 1
    # end class FID

    class LEN(RGBEffects.LEN):
        # See ``RGBEffects.LEN``
        RGB_CLUSTER_INDEX = 0x8
        PATTERN = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = RGBEffects.FIELDS + (
        BitField(fid=FID.RGB_CLUSTER_INDEX, length=LEN.RGB_CLUSTER_INDEX,
                 title="RgbClusterIndex", name="rgb_cluster_index",
                 checks=(CheckHexList(LEN.RGB_CLUSTER_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PATTERN, length=LEN.PATTERN,
                 title="Pattern", name="pattern",
                 checks=(CheckHexList(LEN.PATTERN // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, rgb_cluster_index, pattern, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param rgb_cluster_index: The index of the RGB cluster.
        :type rgb_cluster_index: ``int`` or ``HexList``
        :param pattern: The code that has been arbitrarily assigned to a combination of ON and OFF LEDs, which is
                        known by both FW and SW. 0xFF means all LEDs ON and 0x00 means all LEDs OFF. Example: for 3
                        LEDs in a single RGB Cluster, code 0x01 could mean first LED ON, code 0x02 could mean first and
                        second LEDs ON, 0x03 all LEDs ON and 0x04 third and second LEDs ON.
        :type pattern: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetMultiLedRgbClusterPatternResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.rgb_cluster_index = rgb_cluster_index
        self.pattern = pattern
    # end def __init__
# end class SetMultiLedRgbClusterPattern


class SetMultiLedRgbClusterPatternResponse(LongEmptyPacketDataFormat):
    """
    ``SetMultiLedRgbClusterPatternResponse`` implementation class for versions 0, 1, 2 and 3
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetMultiLedRgbClusterPattern,)
    VERSION = (0, 1, 2, 3, 4,)
    FUNCTION_INDEX = 2

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
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetMultiLedRgbClusterPatternResponse


class ManageNvConfigV0ToV2(NvConfig):
    """
    ``ManageNvConfigV0ToV2`` implementation class for versions 0, 1 and 2
    """
    def __init__(self, device_index, feature_index,
                 get_or_set, nv_capabilities, capability_state=0, param_1=0, param_2=0,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param get_or_set: Determines the access type: read or modify
        :type get_or_set: ``int`` or ``HexList``
        :param nv_capabilities: One of the non-volatile capabilities. Only one must be provided.
        :type nv_capabilities: ``int`` or ``HexList``
        :param capability_state: Value only needed in case getOrSet parameter = 0x01 (Set) - OPTIONAL
        :type capability_state: ``int`` or ``HexList``
        :param param_1: Optional parameter 1 - OPTIONAL
        :type param_1: ``int`` or ``HexList``
        :param param_2: Optional parameter 2 - OPTIONAL
        :type param_2: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=ManageNvConfigResponseV0ToV2.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.get_or_set = get_or_set
        self.nv_capabilities = nv_capabilities
        self.capability_state = capability_state
        self.param_1 = param_1
        self.param_2 = param_2
    # end def __init__
# end class ManageNvConfigV0ToV2


class ManageNvConfigV3ToV4(NvConfigExt):
    """
    ``ManageNvConfigV3ToV4`` implementation class for version 3 and 4
    """
    def __init__(self, device_index, feature_index,
                 get_or_set, nv_capabilities, capability_state, param_1=0, param_2=0, param_3=0, param_4=0, param_5=0,
                 param_6=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param get_or_set: Determines the access type: read or modify
        :type get_or_set: ``int`` or ``HexList``
        :param nv_capabilities: One of the non-volatile capabilities. Only one must be provided.
        :type nv_capabilities: ``int`` or ``HexList``
        :param capability_state: Value only needed in case getOrSet parameter = 0x01 (Set)
        :type capability_state: ``int`` or ``HexList``
        :param param_1: Optional parameter 1 - OPTIONAL
        :type param_1: ``int`` or ``HexList``
        :param param_2: Optional parameter 2 - OPTIONAL
        :type param_2: ``int`` or ``HexList``
        :param param_3: Optional parameter 3 - OPTIONAL
        :type param_3: ``int`` or ``HexList``
        :param param_4: Optional parameter 4 - OPTIONAL
        :type param_4: ``int`` or ``HexList`
        :param param_5: Optional parameter 5 - OPTIONAL
        :type param_5: ``int`` or ``HexList``
        :param param_6: Optional parameter 6 - OPTIONAL
        :type param_6: ``int`` or ``HexList`
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=ManageNvConfigResponseV0ToV2.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.get_or_set = get_or_set
        self.nv_capabilities = nv_capabilities
        self.capability_state = capability_state
        self.param_1 = param_1
        self.param_2 = param_2
        self.param_3 = param_3
        self.param_4 = param_4
        self.param_5 = param_5
        self.param_6 = param_6
    # end def __init__
# end class ManageNvConfigV3ToV4


class ManageNvConfigResponseV0ToV2(NvConfig):
    """
    ``ManageNvConfigResponse`` implementation class for versions 0, 1 and 2
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ManageNvConfigV0ToV2,)
    VERSION = (0, 1, 2,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index,
                 get_or_set, nv_capabilities, capability_state, param_1, param_2,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param get_or_set: Determines the access type: read or modify
        :type get_or_set: ``int`` or ``HexList``
        :param nv_capabilities: nvCapability value passed in request.
        :type nv_capabilities: ``int`` or ``HexList``
        :param capability_state: Current non-volatile value. See following table for the values associated with each
                                 capability.
        :type capability_state: ``int`` or ``HexList``
        :param param_1: Optional parameter 1
        :type param_1: ``int`` or ``HexList``
        :param param_2: Optional parameter 2
        :type param_2: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.get_or_set = get_or_set
        self.nv_capabilities = nv_capabilities
        self.capability_state = capability_state
        self.param_1 = param_1
        self.param_2 = param_2
    # end def __init__
# end class ManageNvConfigResponseV0ToV2


class ManageNvConfigResponseV3ToV4(NvConfigExt):
    """
    ``ManageNvConfigResponseV3ToV4`` implementation class for version 3 and 4
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ManageNvConfigV3ToV4,)
    VERSION = (3, 4,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index,
                 get_or_set, nv_capabilities, capability_state, param_1, param_2, param_3, param_4, param_5, param_6,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param get_or_set: Determines the access type: read or modify
        :type get_or_set: ``int`` or ``HexList``
        :param nv_capabilities: nvCapability value passed in request.
        :type nv_capabilities: ``int`` or ``HexList``
        :param capability_state: Current non-volatile value. See following table for the values associated with each
                                 capability.
        :type capability_state: ``int`` or ``HexList``
        :param param_1: Optional parameter 1
        :type param_1: ``int`` or ``HexList``
        :param param_2: Optional parameter 2
        :type param_2: ``int`` or ``HexList``
        :param param_3: Optional parameter 3
        :type param_3: ``int`` or ``HexList``
        :param param_4: Optional parameter 4
        :type param_4: ``int`` or ``HexList``
        :param param_5: Optional parameter 5
        :type param_5: ``int`` or ``HexList``
        :param param_6: Optional parameter 6
        :type param_6: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.get_or_set = get_or_set
        self.nv_capabilities = nv_capabilities
        self.capability_state = capability_state
        self.param_1 = param_1
        self.param_2 = param_2
        self.param_3 = param_3
        self.param_4 = param_4
        self.param_5 = param_5
        self.param_6 = param_6
    # end def __init__
# end class ManageNvConfigResponseV3ToV4


class ManageRgbLedBinInfo(RgbLedBinInfo):
    """
    ``ManageRgbLedBinInfo`` implementation class for versions 0, 1, 2 and 3
    """
    def __init__(self, device_index, feature_index, get_or_set, rgb_cluster_index, led_bin_index,
                 param_1, param_2, param_3, param_4, param_5, param_6, param_7, param_8, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param get_or_set: Determines the access type: read or modify
        :type get_or_set: ``int`` or ``HexList``
        :param rgb_cluster_index: The index of the RGB cluster.
        :type rgb_cluster_index: ``int`` or ``HexList``
        :param led_bin_index: The index of the bin factor.
        :type led_bin_index: ``int`` or ``HexList``
        :param param_1: Those parameters help to define led bin information.
        :type param_1: ``int`` or ``HexList``
        :param param_2: Those parameters help to define led bin information.
        :type param_2: ``int`` or ``HexList``
        :param param_3: Those parameters help to define led bin information.
        :type param_3: ``int`` or ``HexList``
        :param param_4: Those parameters help to define led bin information.
        :type param_4: ``int`` or ``HexList``
        :param param_5: Those parameters help to define led bin information.
        :type param_5: ``int`` or ``HexList``
        :param param_6: Those parameters help to define led bin information.
        :type param_6: ``int`` or ``HexList``
        :param param_7: Those parameters help to define led bin information.
        :type param_7: ``int`` or ``HexList``
        :param param_8: Those parameters help to define led bin information.
        :type param_8: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=ManageRgbLedBinInfoResponse.FUNCTION_INDEX,
                         get_or_set=get_or_set, rgb_cluster_index=rgb_cluster_index, led_bin_index=led_bin_index,
                         **kwargs)
        self.param_1 = param_1
        self.param_2 = param_2
        self.param_3 = param_3
        self.param_4 = param_4
        self.param_5 = param_5
        self.param_6 = param_6
        self.param_7 = param_7
        self.param_8 = param_8
    # end def __init__
# end class ManageRgbLedBinInfo


class ManageRgbLedBinInfoResponse(RgbLedBinInfo):
    """
    ``ManageRgbLedBinInfoResponse`` implementation class for versions 0, 1, 2 and 3
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ManageRgbLedBinInfo,)
    VERSION = (0, 1, 2, 3, 4,)
    FUNCTION_INDEX = 4

    def __init__(self, device_index, feature_index,
                 get_or_set, rgb_cluster_index, led_bin_index, param_1, param_2, param_3, param_4, param_5, param_6,
                 param_7, param_8, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param get_or_set: Determines the access type: read, modify or read info from backup bank
        :type get_or_set: ``int`` or ``HexList``
        :param rgb_cluster_index: The index of the RGB cluster.
        :type rgb_cluster_index: ``int`` or ``HexList``
        :param led_bin_index: The index of the bin factor.
        :type led_bin_index: ``int`` or ``HexList``
        :param param_1: Those parameters help to define led bin information.
        :type param_1: ``int`` or ``HexList``
        :param param_2: Those parameters help to define led bin information.
        :type param_2: ``int`` or ``HexList``
        :param param_3: Those parameters help to define led bin information.
        :type param_3: ``int`` or ``HexList``
        :param param_4: Those parameters help to define led bin information.
        :type param_4: ``int`` or ``HexList``
        :param param_5: Those parameters help to define led bin information.
        :type param_5: ``int`` or ``HexList``
        :param param_6: Those parameters help to define led bin information.
        :type param_6: ``int`` or ``HexList``
        :param param_7: Those parameters help to define led bin information.
        :type param_7: ``int`` or ``HexList``
        :param param_8: Those parameters help to define led bin information.
        :type param_8: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.get_or_set = get_or_set
        self.rgb_cluster_index = rgb_cluster_index
        self.led_bin_index = led_bin_index
        self.param_1 = param_1
        self.param_2 = param_2
        self.param_3 = param_3
        self.param_4 = param_4
        self.param_5 = param_5
        self.param_6 = param_6
        self.param_7 = param_7
        self.param_8 = param_8
    # end def __init__
# end class ManageRgbLedBinInfoResponse


class ManageSWControl(SwControl):
    """
    ``ManageSWControl`` implementation class for versions 0, 1 ,2 and 3
    """
    def __init__(self, device_index, feature_index, get_or_set, sw_control_flags, events_notification_flags, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param get_or_set: Determines the access type: read or modify
        :type get_or_set: ``int`` or ``HexList``
        :param sw_control_flags: Software control flags
        :type sw_control_flags: ``int`` or ``HexList``
        :param events_notification_flags: Allow synchronization of the effect between devices.
        :type events_notification_flags: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=ManageSWControlResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.get_or_set = get_or_set
        self.sw_control_flags = sw_control_flags
        self.events_notification_flags = events_notification_flags
    # end def __init__
# end class ManageSWControl


class ManageSWControlResponse(SwControl):
    """
    ``ManageSWControlResponse`` implementation class for versions 0, 1, 2 and 3
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ManageSWControl,)
    VERSION = (0, 1, 2, 3, 4,)
    FUNCTION_INDEX = 5

    def __init__(self, device_index, feature_index, get_or_set, sw_control_flags, events_notification_flags, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param get_or_set: Determines the access type: read or modify
        :type get_or_set: ``int`` or ``HexList``
        :param sw_control_flags: Software control flags
        :type sw_control_flags: ``int`` or ``HexList``
        :param events_notification_flags: Allow synchronization of the effect between devices.
        :type events_notification_flags: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.get_or_set = get_or_set
        self.sw_control_flags = sw_control_flags
        self.events_notification_flags = events_notification_flags
    # end def __init__
# end class ManageSWControlResponse


class SetEffectSyncCorrection(RGBEffects):
    """
    ``SetEffectSyncCorrection`` implementation class for versions 0, 1, 2, and 3

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    DriftValue                    16
    Reserved                      104
    ============================  ==========
    """
    class FID(RGBEffects.FID):
        # See ``RGBEffects.FID``
        RGB_CLUSTER_INDEX = RGBEffects.FID.SOFTWARE_ID - 1
        DRIFT_VALUE = RGB_CLUSTER_INDEX - 1
        RESERVED = DRIFT_VALUE - 1
    # end class FID

    class LEN(RGBEffects.LEN):
        # See ``RGBEffects.LEN``
        RGB_CLUSTER_INDEX = 0x8
        DRIFT_VALUE = 0x10
        RESERVED = 0X68
    # end class LEN

    FIELDS = RGBEffects.FIELDS + (
        BitField(fid=FID.RGB_CLUSTER_INDEX, length=LEN.RGB_CLUSTER_INDEX,
                 title="RgbClusterIndex", name="rgb_cluster_index",
                 checks=(CheckHexList(LEN.RGB_CLUSTER_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.DRIFT_VALUE, length=LEN.DRIFT_VALUE,
                 title="DriftValue", name="drift_value",
                 checks=(CheckHexList(LEN.DRIFT_VALUE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DRIFT_VALUE) - 1),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=RGBEffects.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, rgb_cluster_index, drift_value, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param rgb_cluster_index: The index of the RGB cluster.
                                  0xFF can be used for all RGB clusters.
        :type rgb_cluster_index: ``int`` or ``HexList``
        :param drift_value: Phase correction value (in ms) to be applied to achieve synchronisation with SW. Device will
                            speed-up or slow down the current effect play to minimise the driftValue reported by SW.
        :type drift_value: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetEffectSyncCorrectionResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rgb_cluster_index = rgb_cluster_index
        self.drift_value = drift_value
    # end def __init__
# end class SetEffectSyncCorrection


class SetEffectSyncCorrectionResponse(LongEmptyPacketDataFormat):
    """
    ``SetEffectSyncCorrectionResponse`` implementation class for versions 0, 1, 2 and 3
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetEffectSyncCorrection,)
    VERSION = (0, 1, 2, 3, 4,)
    FUNCTION_INDEX = 6

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
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetEffectSyncCorrectionResponse


class ManageRgbPowerModeConfig(RgbPowerModeConfig):
    """
    ``ManageRgbPowerModeConfig`` implementation class for versions 0, 1, 2 and 3
    """
    def __init__(self, device_index, feature_index,
                 get_or_set, rgb_power_mode_flags, rgb_no_act_timeout_to_psave, rgb_no_act_timeout_to_off, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param get_or_set: Determines the access type: read or modify
        :type get_or_set: ``int`` or ``HexList``
        :param rgb_power_mode_flags: The power mode flags
        :type rgb_power_mode_flags: ``int`` or ``HexList``
        :param rgb_no_act_timeout_to_psave: Timeout (in seconds) since last user activity until Power Save mode is set
        :type rgb_no_act_timeout_to_psave: ``int`` or ``HexList``
        :param rgb_no_act_timeout_to_off: Timeout (in seconds) without any user activity since entering Power Save mode
                                          until Power Off mode is set
        :type rgb_no_act_timeout_to_off: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=ManageRgbPowerModeConfigResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.get_or_set = get_or_set
        self.rgb_power_mode_flags = rgb_power_mode_flags
        self.rgb_no_act_timeout_to_psave = rgb_no_act_timeout_to_psave
        self.rgb_no_act_timeout_to_off = rgb_no_act_timeout_to_off
    # end def __init__
# end class ManageRgbPowerModeConfig


class ManageRgbPowerModeConfigResponse(RgbPowerModeConfig):
    """
    ``ManageRgbPowerModeConfigResponse`` implementation class for versions 0, 1, 2 and 3
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ManageRgbPowerModeConfig,)
    VERSION = (0, 1, 2, 3, 4,)
    FUNCTION_INDEX = 7

    def __init__(self, device_index, feature_index,
                 get_or_set, rgb_power_mode_flags, rgb_no_act_timeout_to_psave, rgb_no_act_timeout_to_off, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param get_or_set: Determines the access type: read or modify
        :type get_or_set: ``int`` or ``HexList``
        :param rgb_power_mode_flags: The power mode flags
        :type rgb_power_mode_flags: ``int`` or ``HexList``
        :param rgb_no_act_timeout_to_psave: Timeout (in seconds) since last user activity until Power Save mode is set
        :type rgb_no_act_timeout_to_psave: ``int`` or ``HexList``
        :param rgb_no_act_timeout_to_off: Timeout (in seconds) without any user activity since entering Power Save mode
                                          until Power Off mode is set
        :type rgb_no_act_timeout_to_off: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.get_or_set = get_or_set
        self.rgb_power_mode_flags = rgb_power_mode_flags
        self.rgb_no_act_timeout_to_psave = rgb_no_act_timeout_to_psave
        self.rgb_no_act_timeout_to_off = rgb_no_act_timeout_to_off
    # end def __init__
# end class ManageRgbPowerModeConfigResponse


class ManageRgbPowerMode(RgbPowerMode):
    """
    ``ManageRgbPowerMode`` implementation class for versions 0, 1, 2 and 3
    """
    def __init__(self, device_index, feature_index, get_or_set, rgb_power_mode, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param get_or_set: Determines the access type: read or modify
        :type get_or_set: ``int`` or ``HexList``
        :param rgb_power_mode: The power mode
        :type rgb_power_mode: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=ManageRgbPowerModeResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.get_or_set = get_or_set
        self.rgb_power_mode = rgb_power_mode
    # end def __init__
# end class ManageRgbPowerMode


class ManageRgbPowerModeResponse(RgbPowerMode):
    """
    ``ManageRgbPowerModeResponse`` implementation class for versions 0, 1, 2 and 3
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ManageRgbPowerMode,)
    VERSION = (0, 1, 2, 3, 4,)
    FUNCTION_INDEX = 8

    def __init__(self, device_index, feature_index, get_or_set, rgb_power_mode, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param get_or_set: Determines the access type: read or modify
        :type get_or_set: ``int`` or ``HexList``
        :param rgb_power_mode: The power mode
        :type rgb_power_mode: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.get_or_set = get_or_set
        self.rgb_power_mode = rgb_power_mode
    # end def __init__
# end class ManageRgbPowerModeResponse


class Shutdown(ShortEmptyPacketDataFormat):
    """
    ``Shutdown`` implementation class for versions 4

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
                         functionIndex=ShutdownResponse.FUNCTION_INDEX, **kwargs)
    # end def __init__
# end class Shutdown


class ShutdownResponse(LongEmptyPacketDataFormat):
    """
    ``ShutdownResponse`` implementation class for versions 4

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
    REQUEST_LIST = (Shutdown,)
    VERSION = (4,)
    FUNCTION_INDEX = 9

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
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class ShutdownResponse


class EffectSyncEvent(RGBEffects):
    """
    ``EffectSyncEvent`` implementation class for versions 0, 1, 2 and 3

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    EffectCounter                 16
    Padding                       104
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1, 2, 3, 4,)
    FUNCTION_INDEX = 0

    class FID(RGBEffects.FID):
        # See ``RGBEffects.FID``
        RGB_CLUSTER_INDEX = RGBEffects.FID.SOFTWARE_ID - 1
        EFFECT_COUNTER = RGB_CLUSTER_INDEX - 1
        PADDING = EFFECT_COUNTER - 1
    # end class FID

    class LEN(RGBEffects.LEN):
        # See ``RGBEffects.LEN``
        RGB_CLUSTER_INDEX = 0x8
        EFFECT_COUNTER = 0x10
        PADDING = 0x68
    # end class LEN

    FIELDS = RGBEffects.FIELDS + (
        BitField(fid=FID.RGB_CLUSTER_INDEX, length=LEN.RGB_CLUSTER_INDEX,
                 title="RgbClusterIndex", name="rgb_cluster_index",
                 checks=(CheckHexList(LEN.RGB_CLUSTER_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.EFFECT_COUNTER, length=LEN.EFFECT_COUNTER,
                 title="EffectCounter", name="effect_counter",
                 checks=(CheckHexList(LEN.EFFECT_COUNTER // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.EFFECT_COUNTER) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, rgb_cluster_index, effect_counter, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param rgb_cluster_index: The index of the RGB cluster.
                                  0xFF can be used for all RGB clusters.
        :type rgb_cluster_index: ``int`` or ``HexList``
        :param effect_counter: Counter in ms of the period effect. When sent it provides the current timing in the
                               period effect. It is sent once during the period.
        :type effect_counter: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rgb_cluster_index = rgb_cluster_index
        self.effect_counter = effect_counter
    # end def __init__
# end class EffectSyncEvent


class UserActivityEvent(RGBEffects):
    """
    ``UserActivityEvent`` implementation class for versions 0, 1, 2 and 3

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ActivityEventType             8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1, 2, 3, 4,)
    FUNCTION_INDEX = 1

    class FID(RGBEffects.FID):
        # See ``RGBEffects.FID``
        ACTIVITY_EVENT_TYPE = RGBEffects.FID.SOFTWARE_ID - 1
        PADDING = ACTIVITY_EVENT_TYPE - 1
    # end class FID

    class LEN(RGBEffects.LEN):
        # See ``RGBEffects.LEN``
        ACTIVITY_EVENT_TYPE = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = RGBEffects.FIELDS + (
        BitField(fid=FID.ACTIVITY_EVENT_TYPE, length=LEN.ACTIVITY_EVENT_TYPE,
                 title="ActivityEventType", name="activity_event_type",
                 checks=(CheckHexList(LEN.ACTIVITY_EVENT_TYPE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, activity_event_type, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param activity_event_type: Which kind of event happened
        :type activity_event_type: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.activity_event_type = activity_event_type
    # end def __init__
# end class UserActivityEvent


class RgbClusterChangedEvent(RGBEffects):
    """
    ``RgbClusterChangedEvent`` implementation class for versions 4

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RgbClusterIndex               8
    RgbClusterEffectIndex         8
    Param1                        8
    Param2                        8
    Param3                        8
    Param4                        8
    Param5                        8
    Param6                        8
    Param7                        8
    Param8                        8
    Param9                        8
    Param10                       8
    Reserved                      4
    PowerMode                     2
    Persistence                   2
    Padding                       24
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (4,)
    FUNCTION_INDEX = 2

    class FID(RGBEffects.FID):
        # See ``RGBEffects.FID``
        RGB_CLUSTER_INDEX = RGBEffects.FID.SOFTWARE_ID - 1
        RGB_CLUSTER_EFFECT_INDEX = RGB_CLUSTER_INDEX - 1
        PARAM_1 = RGB_CLUSTER_EFFECT_INDEX - 1
        PARAM_2 = PARAM_1 - 1
        PARAM_3 = PARAM_2 - 1
        PARAM_4 = PARAM_3 - 1
        PARAM_5 = PARAM_4 - 1
        PARAM_6 = PARAM_5 - 1
        PARAM_7 = PARAM_6 - 1
        PARAM_8 = PARAM_7 - 1
        PARAM_9 = PARAM_8 - 1
        PARAM_10 = PARAM_9 - 1
        RESERVED = PARAM_10 - 1
        POWER_MODE = RESERVED - 1
        PERSISTENCE = POWER_MODE - 1
        PADDING = PERSISTENCE - 1
    # end class FID

    class LEN(RGBEffects.LEN):
        # See ``RGBEffects.LEN``
        RGB_CLUSTER_INDEX = 0x8
        RGB_CLUSTER_EFFECT_INDEX = 0x8
        PARAM_1 = 0x8
        PARAM_2 = 0x8
        PARAM_3 = 0x8
        PARAM_4 = 0x8
        PARAM_5 = 0x8
        PARAM_6 = 0x8
        PARAM_7 = 0x8
        PARAM_8 = 0x8
        PARAM_9 = 0x8
        PARAM_10 = 0x8
        RESERVED = 0x4
        POWER_MODE = 0x2
        PERSISTENCE = 0x2
        PADDING = 0x18
    # end class LEN

    FIELDS = RGBEffects.FIELDS + (
        BitField(fid=FID.RGB_CLUSTER_INDEX, length=LEN.RGB_CLUSTER_INDEX,
                 title="RgbClusterIndex", name="rgb_cluster_index",
                 checks=(CheckHexList(LEN.RGB_CLUSTER_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.RGB_CLUSTER_EFFECT_INDEX, length=LEN.RGB_CLUSTER_EFFECT_INDEX,
                 title="RgbClusterEffectIndex", name="rgb_cluster_effect_index",
                 checks=(CheckHexList(LEN.RGB_CLUSTER_EFFECT_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PARAM_1, length=LEN.PARAM_1,
                 title="Param1", name="param_1",
                 checks=(CheckHexList(LEN.PARAM_1 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_2, length=LEN.PARAM_2,
                 title="Param2", name="param_2",
                 checks=(CheckHexList(LEN.PARAM_2 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_3, length=LEN.PARAM_3,
                 title="Param3", name="param_3",
                 checks=(CheckHexList(LEN.PARAM_3 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_4, length=LEN.PARAM_4,
                 title="Param4", name="param_4",
                 checks=(CheckHexList(LEN.PARAM_4 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_5, length=LEN.PARAM_5,
                 title="Param5", name="param_5",
                 checks=(CheckHexList(LEN.PARAM_5 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_6, length=LEN.PARAM_6,
                 title="Param6", name="param_6",
                 checks=(CheckHexList(LEN.PARAM_6 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_7, length=LEN.PARAM_7,
                 title="Param7", name="param_7",
                 checks=(CheckHexList(LEN.PARAM_7 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_8, length=LEN.PARAM_8,
                 title="Param8", name="param_8",
                 checks=(CheckHexList(LEN.PARAM_8 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_9, length=LEN.PARAM_9,
                 title="Param9", name="param_9",
                 checks=(CheckHexList(LEN.PARAM_9 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PARAM_10, length=LEN.PARAM_10,
                 title="Param10", name="param_10",
                 checks=(CheckHexList(LEN.PARAM_10 // 8),
                         CheckByte(),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                 default_value=RGBEffects.DEFAULT.RESERVED),
        BitField(fid=FID.POWER_MODE, length=LEN.POWER_MODE,
                 title="PowerMode", name="power_mode",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.POWER_MODE) - 1),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PERSISTENCE, length=LEN.PERSISTENCE,
                 title="Persistence", name="persistence",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.PERSISTENCE) - 1),),
                 optional=True,
                 default_value=RGBEffects.DEFAULT.OPTION),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RGBEffects.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index,
                 rgb_cluster_index, rgb_cluster_effect_index, param_1=0, param_2=0, param_3=0, param_4=0, param_5=0,
                 param_6=0, param_7=0, param_8=0, param_9=0, param_10=0, power_mode=0, persistence=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param rgb_cluster_index: The index of the RGB cluster.
        :type rgb_cluster_index: ``int`` or ``HexList``
        :param rgb_cluster_effect_index: The index of the effect within that RGB cluster.
        :type rgb_cluster_effect_index: ``int`` or ``HexList``
        :param param_1: The parameters are definition for effect. - OPTIONAL
        :type param_1: ``int`` or ``HexList``
        :param param_2: The parameters are definition for effect. - OPTIONAL
        :type param_2: ``int`` or ``HexList``
        :param param_3: The parameters are definition for effect. - OPTIONAL
        :type param_3: ``int`` or ``HexList``
        :param param_4: The parameters are definition for effect. - OPTIONAL
        :type param_4: ``int`` or ``HexList``
        :param param_5: The parameters are definition for effect. - OPTIONAL
        :type param_5: ``int`` or ``HexList``
        :param param_6: The parameters are definition for effect. - OPTIONAL
        :type param_6: ``int`` or ``HexList``
        :param param_7: The parameters are definition for effect. - OPTIONAL
        :type param_7: ``int`` or ``HexList``
        :param param_8: The parameters are definition for effect. - OPTIONAL
        :type param_8: ``int`` or ``HexList``
        :param param_9: The parameters are definition for effect. - OPTIONAL
        :type param_9: ``int`` or ``HexList``
        :param param_10: The parameters are definition for effect. - OPTIONAL
        :type param_10: ``int`` or ``HexList``
        :param power_mode: RGB Power mode to which the effect will be applied - OPTIONAL
        :type power_mode: ``int`` or ``HexList``
        :param persistence: Determine how the settings persist through a power cycle - OPTIONAL
        :type persistence: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rgb_cluster_index = rgb_cluster_index
        self.rgb_cluster_effect_index = rgb_cluster_effect_index
        self.param_1 = param_1
        self.param_2 = param_2
        self.param_3 = param_3
        self.param_4 = param_4
        self.param_5 = param_5
        self.param_6 = param_6
        self.param_7 = param_7
        self.param_8 = param_8
        self.param_9 = param_9
        self.param_10 = param_10
        self.power_mode = power_mode
        self.persistence = persistence
    # end def __init__
# end class RgbClusterChangedEvent


class EffectClusterParams:
    """
    RGB effects cluster data class definition
    """
    PARAMS_COUNTS = 11

    def __init__(self, params):
        """
        :param params: Effect parameters
        :type params: ``HexList``
        """
        self.params = params
    # end def __init__
# end EffectClusterParams


class Disabled(EffectClusterParams):
    """
    RGB effect Disabled data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.DISABLED

    # Next comment is for Pycharm to remove unused warning
    # noinspection PyUnusedLocal
    def __init__(self, random_value=False):
        """
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        super().__init__(params=HexList([0] * self.PARAMS_COUNTS))
    # end def __init__
# end class Disabled


class Fixed(EffectClusterParams):
    """
    RGB effect Fixed data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.FIXED

    @unique
    class Mode(IntEnum):
        DEFAULT = 0
        RAMP_UP_DOWN = 1
        NO_EFFECT = 2
    # end class Mode

    def __init__(self, red=0, green=0, blue=0, mode=Mode.DEFAULT, random_value=False):
        """
        :param red: The light level of red - OPTIONAL
        :type red: ``int``
        :param green: The light level of green  - OPTIONAL
        :type green: ``int``
        :param blue: The light level of blue  - OPTIONAL
        :type blue: ``int``
        :param mode: The effect mode  - OPTIONAL
        :type mode: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            red = random_number % (2 ** 8)
            green = 0xFF - red
            blue = abs(red - green)
            mode = random_number % (self.Mode.NO_EFFECT + 1)
        # end if

        effect_params = [self.EFFECT_ID, red, green, blue, mode]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class Fixed


class PulsingBreathing(EffectClusterParams):
    """
    RGB effect PulsingBreathing data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.PULSING_BREATHING

    def __init__(self, red=0, green=0, blue=0, period=0, random_value=False):
        """
        :param red: The light level of red - OPTIONAL
        :type red: ``int``
        :param green: The light level of green - OPTIONAL
        :type green: ``int``
        :param blue: The light level of blue - OPTIONAL
        :type blue: ``int``
        :param period: Pulsing/Breathing period in ms
        :type period: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            red = random_number % (2 ** 8)
            green = 0xFF - red
            blue = abs(red - green)
            period = red
        # end if

        effect_params = [self.EFFECT_ID, red, green, blue, period]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class PulsingBreathing


class Cycling(EffectClusterParams):
    """
    RGB effect Cycling data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.CYCLING

    def __init__(self, period=0, intensity=0, random_value=False):
        """
        :param period: Cycling period in ms - OPTIONAL
        :type period: ``int``
        :param intensity: Intensity - OPTIONAL
        :type intensity: ``int
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            period = random_number % (2 ** 16)
            intensity = 0xFF - (random_number >> 8 & 0xFF)
        # end if

        effect_params = [self.EFFECT_ID] + [0] * 5 + [period >> 8 & 0xFF, period & 0xFF, intensity]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class Cycling


class ColorWave(EffectClusterParams):
    """
    RGB effect ColorWave data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.COLOR_WAVE

    @unique
    class Direction(IntEnum):
        DEFAULT = 0
        HORIZONTAL = 1
        VERTICAL = 2
        CENTER_OUT = 3
        INWARD = 4
        OUTWARD = 5
        REVERSE_HORIZONTAL = 6
        REVERSE_VERTICAL = 7
        CENTER_IN = 8
    # end class Direction

    def __init__(self, red_start=0, green_start=0, blue_start=0, red_stop=0, green_stop=0, blue_stop=0,
                 period=0, direction=Direction.DEFAULT, intensity=0, random_value=False):
        """
        :param red_start: The light level of red for start - OPTIONAL
        :type red_start: ``int``
        :param green_start: The light level of green for start - OPTIONAL
        :type green_start: ``int``
        :param blue_start: The light level of blue for start - OPTIONAL
        :type blue_start: ``int``
        :param red_stop: The light level of red for stop - OPTIONAL
        :type red_stop: ``int``
        :param green_stop: The light level of green for stop - OPTIONAL
        :type green_stop: ``int``
        :param blue_stop: The light level of blue for stop - OPTIONAL
        :type blue_stop: ``int``
        :param period: Color wave period in ms - OPTIONAL
        :type period: ``int``
        :param direction: The direction of wave - OPTIONAL
        :type direction: ``int | ColorWave.Direction``
        :param intensity: Intensity - OPTIONAL
        :type intensity: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            red_start = random_number % (2 ** 8)
            green_start = 0xFF - red_start
            blue_start = abs(red_start - green_start)
            red_stop = blue_start
            green_stop = red_start
            blue_stop = green_start
            period = random_number % (2 ** 16)
            intensity = red_start
            direction = random_number % (self.Direction.CENTER_IN + 1)
        # end if
        effect_params = [self.EFFECT_ID, red_start, green_start, blue_start, red_stop, green_stop, blue_stop,
                         period >> 8 & 0xFF, direction, intensity, period & 0xFF]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class ColorWave


class Starlight(EffectClusterParams):
    """
    RGB effect Starlight data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.STARLIGHT

    def __init__(self, red_sky=0, green_sky=0, blue_sky=0, red_star=0, green_star=0, blue_star=0, random_value=False):
        """
        :param red_sky: The light level of red for sky - OPTIONAL
        :type red_sky: ``int``
        :param green_sky: The light level of green for sky - OPTIONAL
        :type green_sky: ``int``
        :param blue_sky: The light level of blue for sky - OPTIONAL
        :type blue_sky: ``int``
        :param red_star: The light level of red for star - OPTIONAL
        :type red_star: ``int``
        :param green_star: The light level of green for star - OPTIONAL
        :type green_star: ``int``
        :param blue_star: The light level of blue for star - OPTIONAL
        :type blue_star: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            red_sky = random_number % (2 ** 8)
            green_sky = 0xFF - red_sky
            blue_sky = abs(red_sky - green_sky)
            red_star = blue_sky
            green_star = red_sky
            blue_star = green_sky
        # end if

        effect_params = [self.EFFECT_ID, red_sky, green_sky, blue_sky, red_star, green_star, blue_star]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class Starlight


class LightOnPress(EffectClusterParams):
    """
    RGB effect LightOnPress data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.LIGHT_ON_PRESS

    def __init__(self, red_press=0, green_press=0, blue_press=0, red_release=0, green_release=0, blue_release=0,
                 delay=0, random_value=False):
        """
        :param red_press: The light level of red for sky - OPTIONAL
        :type red_press: ``int``
        :param green_press: The light level of green for sky - OPTIONAL
        :type green_press: ``int``
        :param blue_press: The light level of blue for sky - OPTIONAL
        :type blue_press: ``int``
        :param red_release: The light level of red for star - OPTIONAL
        :type red_release: ``int``
        :param green_release: The light level of green for star - OPTIONAL
        :type green_release: ``int``
        :param blue_release: The light level of blue for star - OPTIONAL
        :type blue_release: ``int``
        :param delay: Delay time in ms - OPTIONAL
        :type delay: ``int
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            red_press = random_number % (2 ** 8)
            green_press = 0xFF - red_press
            blue_press = abs(red_press - green_press)
            red_release = blue_press
            green_release = red_press
            blue_release = green_press
            delay = random_number % (2 ** 16)
        # end if

        effect_params = [self.EFFECT_ID, red_press, green_press, blue_press,
                         red_release, green_release, blue_release, delay >> 8 & 0xFF, delay & 0xFF]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class LightOnPress


class AudioVisualizer(EffectClusterParams):
    """
    RGB effect AudioVisualizer data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.AUDIO_VISUALIZER

    # Next comment is for Pycharm to remove unused warning
    # noinspection PyUnusedLocal
    def __init__(self, random_value=False):
        """
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        effect_params = [self.EFFECT_ID]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class AudioVisualizer


class BootUp(EffectClusterParams):
    """
    RGB effect BootUp data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.BOOT_UP

    # Next comment is for Pycharm to remove unused warning
    # noinspection PyUnusedLocal
    def __init__(self, random_value=False):
        """
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        effect_params = [self.EFFECT_ID]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class BootUp


class DemoMode(EffectClusterParams):
    """
    RGB effect DemoMode data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.DEMO_MODE

    # Next comment is for Pycharm to remove unused warning
    # noinspection PyUnusedLocal
    def __init__(self, random_value=False):
        """
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        effect_params = [self.EFFECT_ID]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class DemoMode


class PulsingBreathingWaveform(EffectClusterParams):
    """
    RGB effect PulsingBreathingWaveform data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.PULSING_BREATHING_WAVEFORM

    @unique
    class Waveform(IntEnum):
        DEFAULT = 0
        SINE = 1
        SQUARE = 2
        TRIANGLE = 3
        SAW_TOOTH = 4
        SHARK_FIN = 5
        EXPONENTIAL = 6
    # end class Waveform

    def __init__(self, red=0, green=0, blue=0, period=0, waveform=Waveform.DEFAULT, intensity=0, random_value=False):
        """
        :param red: The light level of red - OPTIONAL
        :type red: ``int``
        :param green: The light level of green - OPTIONAL
        :type green: ``int``
        :param blue: The light level of blue - OPTIONAL
        :type blue: ``int``
        :param period: Pulsing/Breathing waveform period in ms - OPTIONAL
        :type period: ``int``
        :param waveform: Waveform - OPTIONAL
        :type waveform: ``int``
        :param intensity: Intensity - OPTIONAL
        :type intensity: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            red = random_number % (2 ** 8)
            green = 0xFF - red
            blue = abs(red - green)
            period = random_number % (2 ** 16)
            waveform = random_number % (self.Waveform.EXPONENTIAL + 1)
            intensity = 0xFF - (random_number >> 8 & 0xFF)
        # end if

        effect_params = [self.EFFECT_ID, red, green, blue, period >> 8 & 0xFF, period & 0xFF, waveform, intensity]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class PulsingBreathingWaveform


class Ripple(EffectClusterParams):
    """
    RGB effect Ripple data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.RIPPLE

    @unique
    class Animation(IntEnum):
        DEFAULT = 0
        SKIP_START_UP_ANIMATION = 1
    # end class Animation

    def __init__(self, red=0, green=0, blue=0, animation=Animation.DEFAULT, period=0, random_value=False):
        """
        :param red: The light level of red
        :type red: ``int``
        :param green: The light level of green
        :type green: ``int``
        :param blue: The light level of blue
        :type blue: ``int``
        :param animation: Animation
        :type animation: ``int``
        :param period: Ripple period in ms
        :type period: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            red = random_number % (2 ** 8)
            green = 0xFF - red
            blue = abs(red - green)
            animation = random_number % (self.Animation.SKIP_START_UP_ANIMATION + 1)
            period = random_number % (2 ** 16)
        # end if

        effect_params = [self.EFFECT_ID, red, green, blue, animation, period >> 8 & 0xFF, period & 0xFF]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class Ripple


class CustomOnboardStored(EffectClusterParams):
    """
    RGB effect CustomOnboardStored data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.CUSTOM_ONBOARD_STORED

    def __init__(self, effect_slot=0, init_frame=0, length=0, frame_period=0, intensity=0, random_value=False):
        """
        :param effect_slot: Effect slot- OPTIONAL
        :type effect_slot: ``int``
        :param init_frame: Init frame - OPTIONAL
        :type init_frame: ``int``
        :param length: Length - OPTIONAL
        :type length: ``int``
        :param frame_period: Period in ms/frame - OPTIONAL
        :type frame_period: ``int``
        :param intensity: Intensity - OPTIONAL
        :type intensity: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            effect_slot = random_number % (2 ** 8)
            init_frame = random_number % (2 ** 16)
            length = 0xFFFF - init_frame
            frame_period = abs(init_frame - frame_period)
            intensity = 0xFF - effect_slot
        # end if

        effect_params = [self.EFFECT_ID, effect_slot, init_frame >> 8 & 0xFF, init_frame & 0xFF,
                         length >> 8 & 0xFF, length & 0xFF, frame_period >> 8 & 0xFF, frame_period & 0xFF, intensity]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class CustomOnboardStored


class KittLighting(EffectClusterParams):
    """
    RGB effect KittLighting data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.KITT_LIGHTING

    def __init__(self, foreground_red=0, foreground_green=0, foreground_blue=0, led_overlapped_percent=0, period=0,
                 background_red=0, background_green=0, background_blue=0, brightness=0, random_value=False):
        """
        :param foreground_red: The light level of red for foreground - OPTIONAL
        :type foreground_red: ``int``
        :param foreground_green: The light level of green for foreground - OPTIONAL
        :type foreground_green: ``int``
        :param foreground_blue: The light level of blue for foreground - OPTIONAL
        :type foreground_blue: ``int``
        :param led_overlapped_percent: The percentage of led overlapped - OPTIONAL
        :type led_overlapped_percent: ``int``
        :param period: Period in ms - OPTIONAL
        :type period: ``int``
        :param background_red: The light level of red for background - OPTIONAL
        :type background_red: ``int``
        :param background_green: The light level of green for background - OPTIONAL
        :type background_green: ``int``
        :param background_blue: The light level of blue for background - OPTIONAL
        :type background_blue: ``int``
        :param brightness: Brightness - OPTIONAL
        :type brightness: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            foreground_red = random_number % (2 ** 8)
            foreground_green = 0xFF - foreground_red
            foreground_blue = abs(foreground_red - foreground_green)
            led_overlapped_percent = foreground_red
            period = random_number % (2 ** 16)
            background_red = foreground_blue
            background_green = foreground_red
            background_blue = foreground_green
            brightness = period & 0xFF
        # end if

        effect_params = [self.EFFECT_ID, foreground_red, foreground_green, foreground_blue,
                         led_overlapped_percent, period >> 8 & 0xFF, period & 0xFF,
                         background_red, background_green, background_blue, brightness]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class KittLighting


class ColorDecomposition(EffectClusterParams):
    """
    RGB effect ColorDecomposition data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.COLOR_DECOMPOSITION

    def __init__(self, period=0, brightness=0, random_value=False):
        """
        :param period: Period in ms - OPTIONAL
        :type period: ``int``
        :param brightness: Brightness - OPTIONAL
        :type brightness: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            period = random_number % (2 ** 16)
            brightness = period & 0xFF
        # end if

        effect_params = ([0] * 6) + [self.EFFECT_ID, period >> 8 & 0xFF, period & 0xFF, brightness]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class ColorDecomposition


class SnipePulseCyanPink(EffectClusterParams):
    """
    RGB effect SnipePulseCyanPink data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.SNIPE_PULSE_CYAN_PINK

    def __init__(self, frame_period=0, intensity=0, random_value=False):
        """
        :param frame_period: Period in ms/frame - OPTIONAL
        :type frame_period: ``int``
        :param intensity: Intensity - OPTIONAL
        :type intensity: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            frame_period = random_number % (2 ** 16)
            intensity = frame_period & 0xFF
        # end if

        effect_params = ([0] * 5) + [self.EFFECT_ID, frame_period >> 8 & 0xFF, frame_period & 0xFF, intensity]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class SnipePulseCyanPink


class NeuralWaveCyanPink(EffectClusterParams):
    """
    RGB effect NeuralWaveCyanPink data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.NEURAL_WAVE_CYAN_PINK

    def __init__(self, frame_period=0, intensity=0, random_value=0):
        """
        :param frame_period: Period in ms/frame - OPTIONAL
        :type frame_period: ``int``
        :param intensity: Intensity - OPTIONAL
        :type intensity: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            frame_period = random_number % (2 ** 16)
            intensity = frame_period & 0xFF
        # end if

        effect_params = ([0] * 5) + [self.EFFECT_ID, frame_period >> 8 & 0xFF, frame_period & 0xFF, intensity]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class NeuralWaveCyanPink


class FrameBasedSignatureEffectActive(EffectClusterParams):
    """
    RGB effect FrameBasedSignatureEffectActive data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.FRAME_BASED_SIGNATURE_EFFECT_ACTIVE

    def __init__(self, frame_period=0, intensity=0, random_value=False):
        """
        :param frame_period: Period in ms/frame - OPTIONAL
        :type frame_period: ``int``
        :param intensity: Intensity - OPTIONAL
        :type intensity: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            frame_period = random_number % (2 ** 16)
            intensity = frame_period & 0xFF
        # end if

        effect_params = ([0] * 5) + [self.EFFECT_ID, frame_period >> 8 & 0xFF, frame_period & 0xFF, intensity]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class FrameBasedSignatureEffectActive


class FrameBasedSignatureEffectPassive(EffectClusterParams):
    """
    RGB effect FrameBasedSignatureEffectPassive data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.FRAME_BASED_SIGNATURE_EFFECT_PASSIVE

    def __init__(self, frame_period=0, intensity=0, random_value=False):
        """
        :param frame_period: Period in ms/frame - OPTIONAL
        :type frame_period: ``int``
        :param intensity: Intensity - OPTIONAL
        :type intensity: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            frame_period = random_number % (2 ** 16)
            intensity = frame_period & 0xFF
        # end if

        effect_params = ([0] * 5) + [self.EFFECT_ID, frame_period >> 8 & 0xFF, frame_period & 0xFF, intensity]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class FrameBasedSignatureEffectPassive


class SnipePulseConfigurableColor(EffectClusterParams):
    """
    RGB effect SnipePulseConfigurableColor data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.SNIPE_PULSE_CONFIGURABLE_COLOR

    def __init__(self, background_red=0, background_green=0, background_blue=0,
                 foreground_red=0, foreground_green=0, foreground_blue=0, period=0, intensity=0, random_value=False):
        """
        :param background_red: The light level of red for background - OPTIONAL
        :type background_red: ``int``
        :param background_green: The light level of green for background - OPTIONAL
        :type background_green: ``int``
        :param background_blue: The light level of blue for background - OPTIONAL
        :type background_blue: ``int``
        :param foreground_red: The light level of red for foreground - OPTIONAL
        :type foreground_red: ``int``
        :param foreground_green: The light level of green for foreground - OPTIONAL
        :type foreground_green: ``int``
        :param foreground_blue: The light level of blue for foreground - OPTIONAL
        :type foreground_blue: ``int``
        :param period: Period in ms - OPTIONAL
        :type period: ``int``
        :param intensity: Intensity - OPTIONAL
        :type intensity: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            background_red = random_number % (2 ** 8)
            background_green = 0xFF - background_red
            background_blue = abs(background_red-background_blue)
            foreground_red = background_blue
            foreground_green = background_red
            foreground_blue = background_green
            period = random_number % (2 ** 16)
            intensity = background_red
        # end if

        effect_params = [self.EFFECT_ID, background_red, background_green, background_blue,
                         foreground_red, foreground_green, foreground_blue, period >> 8 & 0xFF, period & 0xFF,
                         intensity]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class SnipePulseConfigurableColor


class NeuralWaveConfigurableColor(EffectClusterParams):
    """
    RGB effect NeuralWaveConfigurableColor data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.NEURAL_WAVE_CONFIGURABLE_COLOR

    def __init__(self, background_red=0, background_green=0, background_blue=0,
                 foreground_red=0, foreground_green=0, foreground_blue=0, period=0, intensity=0, random_value=False):
        """
        :param background_red: The light level of red for background - OPTIONAL
        :type background_red: ``int``
        :param background_green: The light level of green for background - OPTIONAL
        :type background_green: ``int``
        :param background_blue: The light level of blue for background - OPTIONAL
        :type background_blue: ``int``
        :param foreground_red: The light level of red for foreground - OPTIONAL
        :type foreground_red: ``int``
        :param foreground_green: The light level of green for foreground - OPTIONAL
        :type foreground_green: ``int``
        :param foreground_blue: The light level of blue for foreground - OPTIONAL
        :type foreground_blue: ``int``
        :param period: Period in ms - OPTIONAL
        :type period: ``int``
        :param intensity: Intensity - OPTIONAL
        :type intensity: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            background_red = random_number % (2 ** 8)
            background_green = 0xFF - background_red
            background_blue = abs(background_red-background_blue)
            foreground_red = background_blue
            foreground_green = background_red
            foreground_blue = background_green
            period = random_number % (2 ** 16)
            intensity = background_red
        # end if

        effect_params = [self.EFFECT_ID, background_red, background_green, background_blue,
                         foreground_red, foreground_green, foreground_blue, period >> 8 & 0xFF, period & 0xFF,
                         intensity]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class NeuralWaveConfigurableColor


class HostSteaming(EffectClusterParams):
    """
    RGB effect HostSteaming data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.HOST_STREAMING

    # Next comment is for Pycharm to remove unused warning
    # noinspection PyUnusedLocal
    def __init__(self, random_value=False):
        """
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        effect_params = [self.EFFECT_ID]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class HostSteaming


class HsvPulsingBreathing(EffectClusterParams):
    """
    RGB effect HsvPulsingBreathing data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.HSV_PULSING_BREATHING

    def __init__(self, hue=0, saturation=0, value=0, period=0, random_value=False):
        """
        :param hue: Color property Hue - OPTIONAL
        :type hue: ``int``
        :param saturation: Color property Saturation - OPTIONAL
        :type saturation: ``int``
        :param value: Color property Value - OPTIONAL
        :type value: ``int``
        :param period: Pulsing/Breathing period in ms - OPTIONAL
        :type period: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            hue = random_number % (2 ** 8)
            saturation = 0xFF - hue
            value = abs(hue-saturation)
            period = random_number % (2 ** 16)
        # end if

        effect_params = [self.EFFECT_ID, hue, saturation, value, 0, 0, 0, period >> 8 & 0xFF, period & 0xFF]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class HsvPulsingBreathing


class ColorCyclingConfigurableS(EffectClusterParams):
    """
    RGB effect ColorCyclingConfigurableS data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.COLOR_CYCLING_CONFIGURABLE_S

    def __init__(self, saturation=0, period=0, intensity=0, random_value=False):
        """
        :param saturation: Color property Saturation - OPTIONAL
        :type saturation: ``int``
        :param period: Pulsing/Breathing period in ms - OPTIONAL
        :type period: ``int``
        :param intensity: Intensity - OPTIONAL
        :type intensity: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            saturation = random_number % (2 ** 8)
            period = random_number % (2 ** 16)
            intensity = 0xFF - saturation
        # end if

        effect_params = [self.EFFECT_ID, 0, saturation, 0, 0, 0, 0, period >> 8 & 0xFF, period & 0xFF, intensity]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class ColorCyclingConfigurableS


class ColorWaveConfigurableS(EffectClusterParams):
    """
    RGB effect ColorWaveConfigurableS data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.COLOR_WAVE_CONFIGURABLE_S

    @unique
    class Direction(IntEnum):
        DEFAULT = 0
        HORIZONTAL = 1
        VERTICAL = 2
        CENTER_OUT = 3
        INWARD = 4
        OUTWARD = 5
        REVERSE_HORIZONTAL = 6
        REVERSE_VERTICAL = 7
        CENTER_IN = 8
    # end class Direction

    def __init__(self, saturation=0, period=0, intensity=0, direction=Direction.DEFAULT, random_value=False):
        """
        :param saturation: Color property Saturation - OPTIONAL
        :type saturation: ``int``
        :param period: Pulsing/Breathing period in ms - OPTIONAL
        :type period: ``int``
        :param intensity: Intensity - OPTIONAL
        :type intensity: ``int``
        :param direction: The direction of wave - OPTIONAL
        :type direction: ``int | ColorWaveConfigurableS.Direction``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            saturation = random_number % (2 ** 8)
            period = random_number % (2 ** 16)
            intensity = 0xFF - saturation
            direction = random_number % (self.Direction.CENTER_IN + 1)
        # end if

        effect_params = [self.EFFECT_ID, 0, saturation, 0, 0, 0, 0, period >> 8 & 0xFF, period & 0xFF,
                         intensity, direction]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class ColorWaveConfigurableS


class RippleConfigurableS(EffectClusterParams):
    """
    RGB effect RippleConfigurableS data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.RIPPLE_CONFIGURATION_S

    @unique
    class Animation(IntEnum):
        DEFAULT = 0
        SKIP_START_UP_ANIMATION = 1
    # end class Animation

    def __init__(self, red=0, green=0, blue=0, saturation=0, animation=Animation.DEFAULT, period=0, random_value=False):
        """
        :param red: The light level of red - OPTIONAL
        :type red: ``int``
        :param green: The light level of green - OPTIONAL
        :type green: ``int``
        :param blue: The light level of blue - OPTIONAL
        :type blue: ``int``
        :param saturation: Color property Saturation - OPTIONAL
        :type saturation: ``int``
        :param animation: Animation - OPTIONAL
        :type animation: ``int``
        :param period: Ripple period in ms - OPTIONAL
        :type period: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            red = random_number % (2 ** 8)
            green = 0xFF - red
            blue = abs(red - green)
            saturation = red
            animation = random_number % (self.Animation.SKIP_START_UP_ANIMATION + 1)
            period = random_number % (2 ** 16)
        # end if

        effect_params = [self.EFFECT_ID, red, green, blue, saturation, animation, 0, period >> 8 & 0xFF, period & 0xFF]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class RippleConfigurableS


class SmoothStarBreathing(EffectClusterParams):
    """
    RGB effect SmoothStarBreathing data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.SMOOTH_STAR_BREATHING

    def __init__(self, first_red=0, first_green=0, first_blue=0, second_red=0, second_green=0, second_blue=0,
                 period=0, intensity=0, random_value=False):
        """
        :param first_red: The light level of red for the first choice - OPTIONAL
        :type first_red: ``int``
        :param first_green: The light level of green for the first choice - OPTIONAL
        :type first_green: ``int``
        :param first_blue: The light level of blue for the first choice - OPTIONAL
        :type first_blue: ``int``
        :param second_red: The light level of red for the second choice - OPTIONAL
        :type second_red: ``int``
        :param second_green: The light level of green for the second choice - OPTIONAL
        :type second_green: ``int``
        :param second_blue: The light level of blue for the second choice - OPTIONAL
        :type second_blue: ``int``
        :param period: Breathing period in ms - OPTIONAL
        :type period: ``int``
        :param intensity: Intensity - OPTIONAL
        :type intensity: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            first_red = random_number % (2 ** 8)
            first_green = 0xFF - first_red
            first_blue = abs(first_red - first_green)
            second_red = first_blue
            second_green = first_red
            second_blue = first_green
            period = random_number % (2 ** 16)
            intensity = first_red
        # end if

        effect_params = [self.EFFECT_ID, first_red, first_green, first_blue, second_red, second_green, second_blue,
                         period >> 8 & 0xFF, period & 0xFF, intensity]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class SmoothStarBreathing


class SmoothWave(EffectClusterParams):
    """
    RGB effect SmoothWave data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.SMOOTH_WAVE

    def __init__(self, first_red=0, first_green=0, first_blue=0, second_red=0, second_green=0, second_blue=0,
                 period=0, intensity=0, random_value=False):
        """
        :param first_red: The light level of red for the first choice - OPTIONAL
        :type first_red: ``int``
        :param first_green: The light level of green for the first choice - OPTIONAL
        :type first_green: ``int``
        :param first_blue: The light level of blue for the first choice - OPTIONAL
        :type first_blue: ``int``
        :param second_red: The light level of red for the second choice - OPTIONAL
        :type second_red: ``int``
        :param second_green: The light level of green for the second choice - OPTIONAL
        :type second_green: ``int``
        :param second_blue: The light level of blue for the second choice - OPTIONAL
        :type second_blue: ``int``
        :param period: Breathing period in ms - OPTIONAL
        :type period: ``int``
        :param intensity: Intensity - OPTIONAL
        :type intensity: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            first_red = random_number % (2 ** 8)
            first_green = 0xFF - first_red
            first_blue = abs(first_red - first_green)
            second_red = first_blue
            second_green = first_red
            second_blue = first_green
            period = random_number % (2 ** 16)
            intensity = first_red
        # end if

        effect_params = [self.EFFECT_ID, first_red, first_green, first_blue, second_red, second_green, second_blue,
                         period >> 8 & 0xFF, period & 0xFF, intensity]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class SmoothWave


class FormulaBasedSignatureEffectActive(EffectClusterParams):
    """
    RGB effect FormulaBasedSignatureEffectActive data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.FORMULA_BASED_SIGNATURE_EFFECT_ACTIVE

    def __init__(self, first_red=0, first_green=0, first_blue=0, second_red=0, second_green=0, second_blue=0,
                 period=0, intensity=0, random_value=False):
        """
        :param first_red: The light level of red for the first choice - OPTIONAL
        :type first_red: ``int``
        :param first_green: The light level of green for the first choice - OPTIONAL
        :type first_green: ``int``
        :param first_blue: The light level of blue for the first choice - OPTIONAL
        :type first_blue: ``int``
        :param second_red: The light level of red for the second choice - OPTIONAL
        :type second_red: ``int``
        :param second_green: The light level of green for the second choice - OPTIONAL
        :type second_green: ``int``
        :param second_blue: The light level of blue for the second choice - OPTIONAL
        :type second_blue: ``int``
        :param period: Breathing period in ms - OPTIONAL
        :type period: ``int``
        :param intensity: Intensity - OPTIONAL
        :type intensity: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            first_red = random_number % (2 ** 8)
            first_green = 0xFF - first_red
            first_blue = abs(first_red - first_green)
            second_red = first_blue
            second_green = first_red
            second_blue = first_green
            period = random_number % (2 ** 16)
            intensity = first_red
        # end if

        effect_params = [self.EFFECT_ID, first_red, first_green, first_blue, second_red, second_green, second_blue,
                         period >> 8 & 0xFF, period & 0xFF, intensity]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class FormulaBasedSignatureEffectActive


class FormulaBasedSignatureEffectPassive(EffectClusterParams):
    """
    RGB effect FormulaBasedSignatureEffectPassive data class definition
    """
    EFFECT_ID = RGBEffects.RGBEffectID.FORMULA_BASED_SIGNATURE_EFFECT_PASSIVE

    def __init__(self, first_red=0, first_green=0, first_blue=0, second_red=0, second_green=0, second_blue=0,
                 period=0, intensity=0, random_value=False):
        """
        :param first_red: The light level of red for the first choice - OPTIONAL
        :type first_red: ``int``
        :param first_green: The light level of green for the first choice - OPTIONAL
        :type first_green: ``int``
        :param first_blue: The light level of blue for the first choice - OPTIONAL
        :type first_blue: ``int``
        :param second_red: The light level of red for the second choice - OPTIONAL
        :type second_red: ``int``
        :param second_green: The light level of green for the second choice - OPTIONAL
        :type second_green: ``int``
        :param second_blue: The light level of blue for the second choice - OPTIONAL
        :type second_blue: ``int``
        :param period: Breathing period in ms - OPTIONAL
        :type period: ``int``
        :param intensity: Intensity - OPTIONAL
        :type intensity: ``int``
        :param random_value: Flag indicating the params are generated randomly - OPTIONAL
        :type random_value: ``bool``
        """
        if random_value:
            random_number = time.time_ns()
            first_red = random_number % (2 ** 8)
            first_green = 0xFF - first_red
            first_blue = abs(first_red - first_green)
            second_red = first_blue
            second_green = first_red
            second_blue = first_green
            period = random_number % (2 ** 16)
            intensity = first_red
        # end if

        effect_params = [self.EFFECT_ID, first_red, first_green, first_blue, second_red, second_green, second_blue,
                         period >> 8 & 0xFF, period & 0xFF, intensity]
        super().__init__(HexList(effect_params + ([0] * (self.PARAMS_COUNTS - len(effect_params)))))
    # end def __init__
# end class FormulaBasedSignatureEffectPassive


EFFECT_ID_TO_CLASS_MAP_V0_V1 = {
    RGBEffects.RGBEffectID.DISABLED: Disabled,
    RGBEffects.RGBEffectID.FIXED: Fixed,
    RGBEffects.RGBEffectID.PULSING_BREATHING: PulsingBreathing,
    RGBEffects.RGBEffectID.CYCLING: Cycling,
    RGBEffects.RGBEffectID.COLOR_WAVE: ColorWave,
    RGBEffects.RGBEffectID.STARLIGHT: Starlight,
    RGBEffects.RGBEffectID.LIGHT_ON_PRESS: LightOnPress,
    RGBEffects.RGBEffectID.AUDIO_VISUALIZER: AudioVisualizer,
    RGBEffects.RGBEffectID.BOOT_UP: BootUp,
    RGBEffects.RGBEffectID.DEMO_MODE: DemoMode,
    RGBEffects.RGBEffectID.PULSING_BREATHING_WAVEFORM: PulsingBreathingWaveform,
    RGBEffects.RGBEffectID.RIPPLE: Ripple,
    RGBEffects.RGBEffectID.CUSTOM_ONBOARD_STORED: CustomOnboardStored
}

EFFECT_ID_TO_CLASS_MAP_V2 = {
    **EFFECT_ID_TO_CLASS_MAP_V0_V1,
    RGBEffects.RGBEffectID.KITT_LIGHTING: KittLighting,
    RGBEffects.RGBEffectID.COLOR_DECOMPOSITION: ColorDecomposition,
    RGBEffects.RGBEffectID.SNIPE_PULSE_CYAN_PINK: SnipePulseCyanPink,
    RGBEffects.RGBEffectID.NEURAL_WAVE_CYAN_PINK: NeuralWaveCyanPink,
    RGBEffects.RGBEffectID.SNIPE_PULSE_CONFIGURABLE_COLOR: SnipePulseConfigurableColor,
    RGBEffects.RGBEffectID.NEURAL_WAVE_CONFIGURABLE_COLOR: NeuralWaveConfigurableColor,
    RGBEffects.RGBEffectID.HOST_STREAMING: HostSteaming,
    RGBEffects.RGBEffectID.HSV_PULSING_BREATHING: HsvPulsingBreathing,
    RGBEffects.RGBEffectID.COLOR_CYCLING_CONFIGURABLE_S: ColorCyclingConfigurableS
}

EFFECT_ID_TO_CLASS_MAP_V3 = {
    **EFFECT_ID_TO_CLASS_MAP_V2,
    RGBEffects.RGBEffectID.COLOR_WAVE_CONFIGURABLE_S: ColorWaveConfigurableS,
    RGBEffects.RGBEffectID.RIPPLE_CONFIGURATION_S: RippleConfigurableS,
    RGBEffects.RGBEffectID.SMOOTH_STAR_BREATHING: SmoothStarBreathing,
    RGBEffects.RGBEffectID.SMOOTH_WAVE: SmoothWave
}

EFFECT_ID_TO_CLASS_MAP_V4 = {
    **EFFECT_ID_TO_CLASS_MAP_V0_V1,
    RGBEffects.RGBEffectID.KITT_LIGHTING: KittLighting,
    RGBEffects.RGBEffectID.COLOR_DECOMPOSITION: ColorDecomposition,
    RGBEffects.RGBEffectID.FRAME_BASED_SIGNATURE_EFFECT_ACTIVE: FrameBasedSignatureEffectActive,
    RGBEffects.RGBEffectID.FRAME_BASED_SIGNATURE_EFFECT_PASSIVE: FrameBasedSignatureEffectPassive,
    RGBEffects.RGBEffectID.HOST_STREAMING: HostSteaming,
    RGBEffects.RGBEffectID.HSV_PULSING_BREATHING: HsvPulsingBreathing,
    RGBEffects.RGBEffectID.COLOR_CYCLING_CONFIGURABLE_S: ColorCyclingConfigurableS,
    RGBEffects.RGBEffectID.COLOR_WAVE_CONFIGURABLE_S: ColorWaveConfigurableS,
    RGBEffects.RGBEffectID.RIPPLE_CONFIGURATION_S: RippleConfigurableS,
    RGBEffects.RGBEffectID.FORMULA_BASED_SIGNATURE_EFFECT_ACTIVE: FormulaBasedSignatureEffectActive,
    RGBEffects.RGBEffectID.FORMULA_BASED_SIGNATURE_EFFECT_PASSIVE: FormulaBasedSignatureEffectPassive
}

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
