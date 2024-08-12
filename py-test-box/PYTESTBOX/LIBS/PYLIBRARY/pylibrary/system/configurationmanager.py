#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package:pylibrary.system.configurationmanager
:brief: Base definition of the interface classes of a configuration manager
:author: Christophe Roquebert
:date: 2021/04/13
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import abc
from enum import auto
from enum import IntEnum
from enum import unique


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ConfigurationManagerInterface(object, metaclass=abc.ABCMeta):
    """
    Interface for a configuration manager
    """
    @unique
    class ID(IntEnum):
        """
        Feature Identifiers
        """
        TARGET_SW = auto()
        FEATURE_COUNT = auto()
        VLP_FEATURE_COUNT = auto()
        ENTITY_COUNT = auto()
        TRANSPORT_USB = auto()
        TRANSPORT_EQUAD = auto()
        TRANSPORT_BTLE = auto()
        TRANSPORT_BT = auto()
        MODEL_ID = auto()
        EXTENDED_MODEL_ID = auto()
        FW_TYPE = auto()
        FW_PREFIX = auto()
        FW_NUMBER = auto()
        REVISION = auto()
        BUILD = auto()
        FW_RESERVED = auto()
        TRANSPORT_ID = auto()
        MARKETING_NAME = auto()
        BLE_PRO_PREPAIRING_CFG = auto()
        BLE_PRO_SRV_VERSION = auto()
        DEVICES_BLUETOOTH_PIDS = auto()
        IS_PLATFORM = auto()
        CID_TABLE = auto()
        CID_INFO_TABLE_FRIENDLY_NAME = auto()
        CID_INFO_TABLE_CID = auto()
        CID_INFO_TABLE_TASK = auto()
        CID_INFO_TABLE_FLAG_VIRTUAL = auto()
        CID_INFO_TABLE_FLAG_PERSIST = auto()
        CID_INFO_TABLE_FLAG_DIVERT = auto()
        CID_INFO_TABLE_FLAG_REPROG = auto()
        CID_INFO_TABLE_FLAG_FNTOG = auto()
        CID_INFO_TABLE_FLAG_HOTKEY = auto()
        CID_INFO_TABLE_FLAG_FKEY = auto()
        CID_INFO_TABLE_FLAG_MOUSE = auto()
        CID_INFO_TABLE_POS = auto()
        CID_INFO_TABLE_GROUP = auto()
        CID_INFO_TABLE_GMASK = auto()
        CID_INFO_TABLE_ADDITIONAL_FLAGS_RAW_WHEEL = auto()
        CID_INFO_TABLE_ADDITIONAL_FLAGS_ANALYTICS_KEY_EVENTS = auto()
        CID_INFO_TABLE_ADDITIONAL_FLAGS_FORCE_RAW_XY = auto()
        CID_INFO_TABLE_ADDITIONAL_FLAGS_RAW_XY = auto()
        DISPLAY_INFO_TABLE_INDEX = auto()
        DISPLAY_INFO_TABLE_DISPLAY_SHAPE = auto()
        DISPLAY_INFO_TABLE_DIMENSION = auto()
        DISPLAY_INFO_TABLE_H_RES = auto()
        DISPLAY_INFO_TABLE_V_RES = auto()
        DISPLAY_INFO_TABLE_BUTTON_COUNT = auto()
        DISPLAY_INFO_TABLE_VISIBLE_AREA_COUNT = auto()
        BUTTON_TABLE_INDEX = auto()
        BUTTON_TABLE_BUTTON_SHAPE = auto()
        BUTTON_TABLE_LOC_X = auto()
        BUTTON_TABLE_LOC_Y = auto()
        BUTTON_TABLE_LOC_WIDTH = auto()
        BUTTON_TABLE_LOC_HEIGHT = auto()
        VISIBLE_AREA_TABLE_INDEX = auto()
        VISIBLE_AREA_TABLE_AREA_SHAPE = auto()
        VISIBLE_AREA_TABLE_LOC_X = auto()
        VISIBLE_AREA_TABLE_LOC_Y = auto()
        VISIBLE_AREA_TABLE_LOC_WIDTH = auto()
        VISIBLE_AREA_TABLE_LOC_HEIGHT = auto()
        ROOT_VERSION = auto()
        CHUNK_ID_VARIANT = auto()
        CHUNK_ID_NAMES = auto()
        CHUNK_ID_VALUES = auto()
        BOOTLOADER_ADDRESS = auto()
        SUPPORTED_PROPERTIES = auto()
        SPECIFIC_PROPERTIES_SIZES = auto()
        SW_ACCESSIBLE_PROPERTIES = auto()
        SW_ACCESSIBLE_PROPERTIES_SIZES = auto()
        EFFECTS_INFO_TABLE = auto()
        OOB_PROFILE_DIRECTORY_SECTOR_ID = auto()
        OOB_PROFILE_DIRECTORY_STATUS = auto()
        OOB_PROFILE_DIRECTORY = auto()
        OOB_PROFILES_REPORT_RATE = auto()
        OOB_PROFILES_REPORT_RATE_WIRELESS = auto()
        OOB_PROFILES_REPORT_RATE_WIRED = auto()
        OOB_PROFILES_DEFAULT_DPI_INDEX = auto()
        OOB_PROFILES_SHIFT_DPI_INDEX = auto()
        OOB_PROFILES_DPI_LIST = auto()
        OOB_PROFILES_DPI_XY_LIST = auto()
        OOB_PROFILES_DPI_DELTA_X = auto()
        OOB_PROFILES_DPI_DELTA_Y = auto()
        OOB_PROFILES_LED_COLOR_RED = auto()
        OOB_PROFILES_LED_COLOR_GREEN = auto()
        OOB_PROFILES_LED_COLOR_BLUE = auto()
        OOB_PROFILES_POWER_MODE = auto()
        OOB_PROFILES_ANGLE_SNAPPING = auto()
        OOB_PROFILES_WRITE_COUNTER = auto()
        OOB_PROFILES_POWER_SAVE_TIMEOUT = auto()
        OOB_PROFILES_POWER_OFF_TIMEOUT = auto()
        OOB_PROFILES_BTN_16 = auto()
        OOB_PROFILES_BTN_12 = auto()
        OOB_PROFILES_G_SHIFT_BTN_16 = auto()
        OOB_PROFILES_G_SHIFT_BTN_12 = auto()
        OOB_PROFILES_NAME = auto()
        OOB_PROFILES_LOGO_EFFECT = auto()
        OOB_PROFILES_SIDE_EFFECT = auto()
        OOB_PROFILES_LOGO_ACTIVE_EFFECT = auto()
        OOB_PROFILES_SIDE_ACTIVE_EFFECT = auto()
        OOB_PROFILES_LOGO_PASSIVE_EFFECT = auto()
        OOB_PROFILES_SIDE_PASSIVE_EFFECT = auto()
        OOB_PROFILES_CLUSTER_0_ACTIVE_EFFECT = auto()
        OOB_PROFILES_CLUSTER_1_ACTIVE_EFFECT = auto()
        OOB_PROFILES_CLUSTER_0_PASSIVE_EFFECT = auto()
        OOB_PROFILES_CLUSTER_1_PASSIVE_EFFECT = auto()
        OOB_PROFILES_LIGHTNING_FLAG = auto()
        OOB_PROFILES_CRC = auto()
        OPTICAL_SWITCHES_KBD_MASK_TABLE = auto()
        STARTUP_TIME_COLD_BOOT = auto()
        DUAL_BANK_IMAGE_HEADERS = auto()
        LOGI_MCU_BOOT_GIT_HASH = auto()
    # end class ID

    @abc.abstractmethod
    def get_feature(self, feature_id):
        """
        Resolve dependencies to fetch an expected feature value

        :param feature_id: Feature unique identifier (defined in ConfigurationManager.ID class)
        :type feature_id: ``ConfigurationManager.ID``

        :return: Expected feature value from the test config based on the current context
        :rtype: ``any`` (type of the feature value)
        """
        raise NotImplementedError('users must define get_feature to use this base class')
    # end def get_feature

    @staticmethod
    @abc.abstractmethod
    def get_feature_version(feature_config):
        """
        Get the version of a feature from the test configuration and convert it to int format

        :param feature_config: Feature SubSystem
        :type feature_config: ``AbstractSubSystem``

        :return: feature version enabled in SubSystem
        :rtype: ``int``
        """
        raise NotImplementedError('users must define get_feature_version to use this base class')
    # end get_feature_version

# end class ConfigurationManagerInterface

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
