#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.base.configurationmanager
:brief: Manage data from configuration file
:author: Martin Cryonnet
:date: 2020/04/01
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import IntEnum
from enum import unique
from os.path import exists
from os.path import join
from re import match
from re import search
from warnings import warn

import pysetup
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.common.propertyaccess import PropertyAccess
from pyhid.hidpp.features.common.specialkeysmsebuttons import CidInfoPayload
from pylibrary.mcu.mcuboot.imageformat import ImageHeader
from pylibrary.mcu.mcuboot.imageformat import ImageVersion
from pylibrary.system.configurationmanager import ConfigurationManagerInterface
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ConfigurationManager(ConfigurationManagerInterface):
    """
    Manage data from configuration file depending on context
    """
    @unique
    class MODE(IntEnum):
        """
        Modes values
        """
        APPLICATION = 0
        BOOTLOADER = 1
    # end class MODE

    @unique
    class TARGET(IntEnum):
        """
        Types values
        """
        RECEIVER = 0
        DEVICE = 1
    # end class TARGET

    @unique
    class DEVICE_TYPE(IntEnum):
        """
        Device type values
        """
        MOUSE = 0
        KEYBOARD = 1
        KEYPAD = 2
    # end class MODE

    class DEFAULT:
        """
        Field default values
        """
        RESERVED = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,)
    # end class DEFAULT

    def __init__(self, features):
        """
        Constructor

        :param features: Context features
        :type features: ``context.features``
        """
        # Features available in the configuration
        self.features = features
        self._current_mode = self.MODE.APPLICATION
        self._current_protocol = LogitechProtocol.UNKNOWN
        if features.PRODUCT.F_IsMice:
            self._current_device_type = self.DEVICE_TYPE.MOUSE
        elif features.PRODUCT.F_IsKeyPad:
            self._current_device_type = self.DEVICE_TYPE.KEYPAD
        else:
            self._current_device_type = self.DEVICE_TYPE.KEYBOARD
        self._current_target = None
        self._cache = self.Cache(features)
        self._gaming_cache = self.GamingCache(features)
    # end class features

    @property
    def current_mode(self):
        """
        Current expected mode of the device under test
        """
        return self._current_mode
    # end def current_mode

    @current_mode.setter
    def current_mode(self, mode):
        """
        Set the current expected mode of the device under test
        """
        if mode in self.MODE:
            self._current_mode = mode
        else:
            raise ValueError("Unknown mode")
        # end if
    # end def current_mode

    @property
    def current_protocol(self):
        """
        Current expected protocol of the device under test
        """
        return self._current_protocol
    # end def protocol

    @current_protocol.setter
    def current_protocol(self, protocol):
        """
        Set the current expected protocol of the device under test
        """
        if isinstance(protocol, LogitechProtocol):
            self._current_protocol = protocol
        else:
            raise ValueError("Unknown communication protocol")
    # end def _current_protocol$

    @property
    def current_device_type(self):
        """
        Current expected mode of the device under test
        """
        return self._current_device_type
    # end def current_mode

    @current_device_type.setter
    def current_device_type(self, device_type):
        """
        Set the current expected device type of the device under test
        """
        if device_type in self.DEVICE_TYPE:
            self._current_device_type = device_type
        else:
            raise ValueError("Unknown device type")
    # end def current_mode

    @property
    def current_target(self):
        """
        Current expected target of the device under test
        """
        return self._current_target
    # end def current_target

    @current_target.setter
    def current_target(self, target):
        """
        Set the current expected target of the device under test
        """
        if target in self.TARGET:
            self._current_target = target
        else:
            raise ValueError("Unknown target")
        # end if
    # end def current_target

    @property
    def feature_value_map(self):
        """
        Get the mapping of expected feature value
        This map is readonly
        """
        root_features = self.features.PRODUCT.FEATURES.IMPORTANT.ROOT
        feature_set_features = self.features.PRODUCT.FEATURES.IMPORTANT.FEATURE_SET
        fw_info_features = self.features.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION
        device_name_features = self.features.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME
        ble_pro_prepairing_features = self.features.PRODUCT.FEATURES.COMMON.BLE_PRO_PREPAIRING
        bootloader_transport_id = \
            (fw_info_features.F_BootLoaderTransportId if fw_info_features.F_BootLoaderTransportId is not None else
             fw_info_features.F_TransportId)

        return {
            self.ID.TARGET_SW: {
                "dependency": "mode",
                self.MODE.APPLICATION: root_features.F_TargetSW,
                self.MODE.BOOTLOADER: (
                    root_features.F_BootLoaderTargetSW if root_features.F_BootLoaderTargetSW is not None else
                    root_features.F_TargetSW),
            },
            self.ID.FEATURE_COUNT: {
                "dependency": "mode",
                self.MODE.APPLICATION: {
                    **{"dependency": "protocol",
                       LogitechProtocol.USB: feature_set_features.F_FeatureCountInUSB,
                       LogitechProtocol.BLE: feature_set_features.F_FeatureCountInBLE,
                       LogitechProtocol.BLE_PRO: feature_set_features.F_FeatureCountInBLE,
                       },
                    **{x: feature_set_features.F_FeatureCountInUFY for x in LogitechProtocol
                       if x > LogitechProtocol.UNKNOWN and x != LogitechProtocol.BLE_PRO}
                },
                self.MODE.BOOTLOADER: {
                    **{"dependency": "protocol",
                       LogitechProtocol.USB: feature_set_features.F_BootloaderFeatureCountInUSB,
                       LogitechProtocol.BLE: feature_set_features.F_BootloaderFeatureCountInBLE,
                       LogitechProtocol.BLE_PRO: feature_set_features.F_BootloaderFeatureCountInBLE,
                       },
                    **{x: feature_set_features.F_BootloaderFeatureCountInUFY for x in LogitechProtocol
                       if x > LogitechProtocol.UNKNOWN and x != LogitechProtocol.BLE_PRO}
                }
            },
            self.ID.VLP_FEATURE_COUNT: {
                "dependency": "mode",
                self.MODE.APPLICATION: {
                    **{"dependency": "protocol",
                       LogitechProtocol.USB: 2, #vlp_feature_set_features.F_FeatureCountInUSB,
                       },
                },
                self.MODE.BOOTLOADER: {
                    **{"dependency": "protocol",
                       LogitechProtocol.USB: 0, # vlp_feature_set_features.F_BootloaderFeatureCountInUSB,
                       },
                }
            },
            self.ID.ENTITY_COUNT: {
                "dependency": "mode",
                self.MODE.APPLICATION: fw_info_features.F_EntityCount,
                self.MODE.BOOTLOADER: fw_info_features.F_BootLoaderEntityCount if
                fw_info_features.F_BootLoaderEntityCount is not None else fw_info_features.F_EntityCount,
            },
            self.ID.TRANSPORT_USB: {
                "dependency": "mode",
                self.MODE.APPLICATION: fw_info_features.F_TransportUsb,
                self.MODE.BOOTLOADER: fw_info_features.F_BootLoaderTransportUsb if
                fw_info_features.F_BootLoaderTransportUsb is not None else fw_info_features.F_TransportUsb,
            },
            self.ID.TRANSPORT_EQUAD: {
                "dependency": "mode",
                self.MODE.APPLICATION: fw_info_features.F_TransportEQuad,
                self.MODE.BOOTLOADER: fw_info_features.F_BootLoaderTransportEQuad if
                fw_info_features.F_BootLoaderTransportEQuad is not None else fw_info_features.F_TransportEQuad,
            },
            self.ID.TRANSPORT_BTLE: {
                "dependency": "mode",
                self.MODE.APPLICATION: fw_info_features.F_TransportBTLE,
                self.MODE.BOOTLOADER: fw_info_features.F_BootLoaderTransportBTLE if
                fw_info_features.F_BootLoaderTransportBTLE is not None else fw_info_features.F_TransportBTLE,
            },
            self.ID.TRANSPORT_BT: {
                "dependency": "mode",
                self.MODE.APPLICATION: fw_info_features.F_TransportBT,
                self.MODE.BOOTLOADER: fw_info_features.F_BootLoaderTransportBT if
                fw_info_features.F_BootLoaderTransportBT is not None else fw_info_features.F_TransportBT,
            },
            self.ID.MODEL_ID: {
                "dependency": "mode",
                self.MODE.APPLICATION: fw_info_features.F_ModelId,
                self.MODE.BOOTLOADER: (
                    fw_info_features.F_BootLoaderModelId if fw_info_features.F_BootLoaderModelId is not None else
                    fw_info_features.F_ModelId),
            },
            self.ID.EXTENDED_MODEL_ID: {
                "dependency": "mode",
                self.MODE.APPLICATION: fw_info_features.F_ExtendedModelId,
                self.MODE.BOOTLOADER: fw_info_features.F_BootLoaderExtendedModelId if
                fw_info_features.F_BootLoaderExtendedModelId is not None else fw_info_features.F_ExtendedModelId,
            },
            self.ID.FW_TYPE: {
                "dependency": "mode",
                self.MODE.APPLICATION: fw_info_features.F_FwType,
                self.MODE.BOOTLOADER: (
                    fw_info_features.F_BootLoaderFwType if fw_info_features.F_BootLoaderFwType is not None else
                    fw_info_features.F_FwType),
            },
            self.ID.FW_PREFIX: {
                "dependency": "mode",
                self.MODE.APPLICATION: fw_info_features.F_FwPrefix,
                self.MODE.BOOTLOADER: (
                    fw_info_features.F_BootLoaderFwPrefix if fw_info_features.F_BootLoaderFwPrefix is not None else
                    fw_info_features.F_FwPrefix),
            },
            self.ID.FW_NUMBER: {
                "dependency": "mode",
                self.MODE.APPLICATION: fw_info_features.F_FwNumber,
                self.MODE.BOOTLOADER: (
                    fw_info_features.F_BootLoaderFwNumber if fw_info_features.F_BootLoaderFwNumber is not None else
                    fw_info_features.F_FwNumber),
            },
            self.ID.REVISION: {
                "dependency": "mode",
                self.MODE.APPLICATION: fw_info_features.F_Revision,
                self.MODE.BOOTLOADER: (
                    fw_info_features.F_BootLoaderRevision if fw_info_features.F_BootLoaderRevision is not None else
                    fw_info_features.F_Revision),
            },
            self.ID.BUILD: {
                "dependency": "mode",
                self.MODE.APPLICATION: fw_info_features.F_Build,
                self.MODE.BOOTLOADER: (
                    fw_info_features.F_BootLoaderBuild if fw_info_features.F_BootLoaderBuild is not None else
                    fw_info_features.F_Build),
            },
            self.ID.FW_RESERVED: {
                "dependency": "mode",
                self.MODE.APPLICATION: (
                    fw_info_features.F_FwReserved if fw_info_features.F_FwReserved is not None else
                    ConfigurationManager.DEFAULT.RESERVED),
                self.MODE.BOOTLOADER: ConfigurationManager.DEFAULT.RESERVED,
            },
            self.ID.TRANSPORT_ID: {
                "dependency": "mode",
                self.MODE.APPLICATION: {
                    **{"dependency": "protocol",
                       LogitechProtocol.USB: fw_info_features.F_TransportIdInUSB,
                       },
                    **{x: fw_info_features.F_TransportId for x in [LogitechProtocol.BLE, LogitechProtocol.BLE_PRO]},
                    **{x: fw_info_features.F_TransportId for x in LogitechProtocol.unifying_protocols()}
                },
                self.MODE.BOOTLOADER: {
                    **{"dependency": "protocol",
                       LogitechProtocol.USB: fw_info_features.F_BootLoaderTransportIdInUSB,
                       },
                    **{x: bootloader_transport_id for x in [LogitechProtocol.BLE, LogitechProtocol.BLE_PRO]},
                    **{x: bootloader_transport_id for x in LogitechProtocol.unifying_protocols()}
                },
            },
            self.ID.MARKETING_NAME: {
                "dependency": "mode",
                self.MODE.APPLICATION: device_name_features.F_MarketingName,
                self.MODE.BOOTLOADER: device_name_features.F_BootLoaderMarketingName if
                device_name_features.F_BootLoaderMarketingName is not None else device_name_features.F_MarketingName,
            },
            self.ID.BLE_PRO_PREPAIRING_CFG: {
                "dependency": "mode",
                self.MODE.APPLICATION: ble_pro_prepairing_features.F_KeysSupported,
            },
            self.ID.BLE_PRO_SRV_VERSION: {
                "dependency": "target",
                # Note that rtype is list[int] if self.TARGET.DEVICE and tuple[str] if self.TARGET.RECEIVER
                self.TARGET.RECEIVER: self.features.SHARED.DEVICES.F_BLEProServiceVersion,
                self.TARGET.DEVICE: [self.get_feature_version(self.features.PRODUCT.PROTOCOLS.BLE_PRO)]
            },
            self.ID.DEVICES_BLUETOOTH_PIDS: {
                "dependency": "target",
                self.TARGET.RECEIVER: self.features.SHARED.DEVICES.F_BluetoothPID,
                self.TARGET.DEVICE: [self.features.PRODUCT.F_BluetoothPID]
            },
            self.ID.IS_PLATFORM: {
                "dependency": "target",
                self.TARGET.RECEIVER: self.features.SHARED.DEVICES.F_IsPlatform,
                self.TARGET.DEVICE: self.features.PRODUCT.F_IsPlatform
            },
            self.ID.CID_TABLE: self._cache.raw_cid_table,
            self.ID.CID_INFO_TABLE_FRIENDLY_NAME: self._cache.cid_info_table_friendly_name,
            self.ID.CID_INFO_TABLE_CID: self._cache.cid_info_table_cid,
            self.ID.CID_INFO_TABLE_TASK: self._cache.cid_info_table_task,
            self.ID.CID_INFO_TABLE_FLAG_VIRTUAL: self._cache.cid_info_table_flag_virtual,
            self.ID.CID_INFO_TABLE_FLAG_PERSIST: self._cache.cid_info_table_flag_persist,
            self.ID.CID_INFO_TABLE_FLAG_DIVERT: self._cache.cid_info_table_flag_divert,
            self.ID.CID_INFO_TABLE_FLAG_REPROG: self._cache.cid_info_table_flag_reprog,
            self.ID.CID_INFO_TABLE_FLAG_FNTOG: self._cache.cid_info_table_flag_fntog,
            self.ID.CID_INFO_TABLE_FLAG_HOTKEY: self._cache.cid_info_table_flag_hotkey,
            self.ID.CID_INFO_TABLE_FLAG_FKEY: self._cache.cid_info_table_flag_fkey,
            self.ID.CID_INFO_TABLE_FLAG_MOUSE: self._cache.cid_info_table_flag_mouse,
            self.ID.CID_INFO_TABLE_POS: self._cache.cid_info_table_pos,
            self.ID.CID_INFO_TABLE_GROUP: self._cache.cid_info_table_group,
            self.ID.CID_INFO_TABLE_GMASK: self._cache.cid_info_table_gmask,
            self.ID.CID_INFO_TABLE_ADDITIONAL_FLAGS_RAW_WHEEL: self._cache.cid_info_table_additional_flags_raw_wheel,
            self.ID.CID_INFO_TABLE_ADDITIONAL_FLAGS_ANALYTICS_KEY_EVENTS:
                self._cache.cid_info_table_additional_flags_analytics_key_events,
            self.ID.CID_INFO_TABLE_ADDITIONAL_FLAGS_FORCE_RAW_XY:
                self._cache.cid_info_table_additional_flags_force_raw_xy,
            self.ID.CID_INFO_TABLE_ADDITIONAL_FLAGS_RAW_XY: self._cache.cid_info_table_additional_flags_raw_xy,
            self.ID.DISPLAY_INFO_TABLE_INDEX: self._cache.display_index,
            self.ID.DISPLAY_INFO_TABLE_DISPLAY_SHAPE: self._cache.display_shape,
            self.ID.DISPLAY_INFO_TABLE_DIMENSION: self._cache.display_dimension,
            self.ID.DISPLAY_INFO_TABLE_H_RES: self._cache.horizontal_res,
            self.ID.DISPLAY_INFO_TABLE_V_RES: self._cache.vertical_res,
            self.ID.DISPLAY_INFO_TABLE_BUTTON_COUNT: self._cache.button_count,
            self.ID.DISPLAY_INFO_TABLE_VISIBLE_AREA_COUNT: self._cache.visible_area_count,
            self.ID.BUTTON_TABLE_INDEX: self._cache.button_index,
            self.ID.BUTTON_TABLE_BUTTON_SHAPE: self._cache.button_shape,
            self.ID.BUTTON_TABLE_LOC_X: self._cache.button_loc_x,
            self.ID.BUTTON_TABLE_LOC_Y: self._cache.button_loc_y,
            self.ID.BUTTON_TABLE_LOC_WIDTH: self._cache.button_loc_width,
            self.ID.BUTTON_TABLE_LOC_HEIGHT: self._cache.button_loc_height,
            self.ID.VISIBLE_AREA_TABLE_INDEX: self._cache.visible_area_index,
            self.ID.VISIBLE_AREA_TABLE_AREA_SHAPE: self._cache.visible_area_shape,
            self.ID.VISIBLE_AREA_TABLE_LOC_X: self._cache.visible_area_loc_x,
            self.ID.VISIBLE_AREA_TABLE_LOC_Y: self._cache.visible_area_loc_y,
            self.ID.VISIBLE_AREA_TABLE_LOC_WIDTH: self._cache.visible_area_loc_width,
            self.ID.VISIBLE_AREA_TABLE_LOC_HEIGHT: self._cache.visible_area_loc_height,
            self.ID.ROOT_VERSION: {
                "dependency": "target",
                self.TARGET.RECEIVER: self.features.SHARED.DEVICES.F_RootFeatureVersion[0] if
                self.features.SHARED.DEVICES.F_RootFeatureVersion is not None else None,
                self.TARGET.DEVICE: self.get_feature_version(self.features.PRODUCT.FEATURES.IMPORTANT.ROOT)
            },
            self.ID.CHUNK_ID_VARIANT: self._cache.is_gaming_chunk_id_map,
            self.ID.CHUNK_ID_NAMES: self._cache.chunk_id_names,
            self.ID.CHUNK_ID_VALUES: self._cache.chunk_id_values,
            self.ID.BOOTLOADER_ADDRESS: self.features.PRODUCT.NVS_UICR.F_BootloaderAddress if
                self.features.PRODUCT.NVS_UICR.F_BootloaderAddress is not None else
                self.features.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress,
            self.ID.SUPPORTED_PROPERTIES: self._cache.supported_properties,
            self.ID.SPECIFIC_PROPERTIES_SIZES: self._cache.specific_properties_sizes,
            self.ID.SW_ACCESSIBLE_PROPERTIES: self._cache.accessible_properties,
            self.ID.SW_ACCESSIBLE_PROPERTIES_SIZES: self._cache.accessible_properties_sizes,
            self.ID.EFFECTS_INFO_TABLE: self._gaming_cache.effect_info_table,
            self.ID.OOB_PROFILE_DIRECTORY_SECTOR_ID: self._gaming_cache.oob_profile_directory_sector_id,
            self.ID.OOB_PROFILE_DIRECTORY_STATUS: self._gaming_cache.oob_profile_directory_status,
            self.ID.OOB_PROFILE_DIRECTORY: self._gaming_cache.oob_profile_directory,
            self.ID.OOB_PROFILES_REPORT_RATE: self._gaming_cache.oob_profiles_report_rate,
            self.ID.OOB_PROFILES_REPORT_RATE_WIRELESS: self._gaming_cache.oob_profiles_report_rate_wireless,
            self.ID.OOB_PROFILES_REPORT_RATE_WIRED: self._gaming_cache.oob_profiles_report_rate_wired,
            self.ID.OOB_PROFILES_DEFAULT_DPI_INDEX: self._gaming_cache.oob_profiles_default_dpi_index,
            self.ID.OOB_PROFILES_SHIFT_DPI_INDEX: self._gaming_cache.oob_profiles_shift_dpi_index,
            self.ID.OOB_PROFILES_DPI_LIST: self._gaming_cache.oob_profiles_dpi_list,
            self.ID.OOB_PROFILES_DPI_XY_LIST: self._gaming_cache.oob_profiles_dpi_xy_list,
            self.ID.OOB_PROFILES_DPI_DELTA_X: self._gaming_cache.oob_profiles_dpi_delta_x,
            self.ID.OOB_PROFILES_DPI_DELTA_Y: self._gaming_cache.oob_profiles_dpi_delta_y,
            self.ID.OOB_PROFILES_LED_COLOR_RED: self._gaming_cache.oob_profiles_led_color_red,
            self.ID.OOB_PROFILES_LED_COLOR_GREEN: self._gaming_cache.oob_profiles_led_color_green,
            self.ID.OOB_PROFILES_LED_COLOR_BLUE: self._gaming_cache.oob_profiles_led_color_blue,
            self.ID.OOB_PROFILES_POWER_MODE: self._gaming_cache.oob_profiles_power_mode,
            self.ID.OOB_PROFILES_ANGLE_SNAPPING: self._gaming_cache.oob_profiles_angle_snapping,
            self.ID.OOB_PROFILES_WRITE_COUNTER: self._gaming_cache.oob_profiles_write_counter,
            self.ID.OOB_PROFILES_POWER_SAVE_TIMEOUT: self._gaming_cache.oob_profiles_power_save_timeout,
            self.ID.OOB_PROFILES_POWER_OFF_TIMEOUT: self._gaming_cache.oob_profiles_power_off_timeout,
            self.ID.OOB_PROFILES_BTN_16: self._gaming_cache.oob_profiles_btn_16,
            self.ID.OOB_PROFILES_BTN_12: self._gaming_cache.oob_profiles_btn_12,
            self.ID.OOB_PROFILES_G_SHIFT_BTN_16: self._gaming_cache.oob_profiles_g_shift_btn_16,
            self.ID.OOB_PROFILES_G_SHIFT_BTN_12: self._gaming_cache.oob_profiles_g_shift_btn_12,
            self.ID.OOB_PROFILES_NAME: self._gaming_cache.oob_profiles_name,
            self.ID.OOB_PROFILES_LOGO_EFFECT: self._gaming_cache.oob_profiles_logo_effect,
            self.ID.OOB_PROFILES_SIDE_EFFECT: self._gaming_cache.oob_profiles_side_effect,
            self.ID.OOB_PROFILES_LOGO_ACTIVE_EFFECT: self._gaming_cache.oob_profiles_logo_active_effect,
            self.ID.OOB_PROFILES_SIDE_ACTIVE_EFFECT: self._gaming_cache.oob_profiles_side_active_effect,
            self.ID.OOB_PROFILES_LOGO_PASSIVE_EFFECT: self._gaming_cache.oob_profiles_logo_passive_effect,
            self.ID.OOB_PROFILES_SIDE_PASSIVE_EFFECT: self._gaming_cache.oob_profiles_side_passive_effect,
            self.ID.OOB_PROFILES_CLUSTER_0_ACTIVE_EFFECT: self._gaming_cache.oob_profiles_cluster_0_active_effect,
            self.ID.OOB_PROFILES_CLUSTER_1_ACTIVE_EFFECT: self._gaming_cache.oob_profiles_cluster_1_active_effect,
            self.ID.OOB_PROFILES_CLUSTER_0_PASSIVE_EFFECT: self._gaming_cache.oob_profiles_cluster_0_passive_effect,
            self.ID.OOB_PROFILES_CLUSTER_1_PASSIVE_EFFECT: self._gaming_cache.oob_profiles_cluster_1_passive_effect,
            self.ID.OOB_PROFILES_LIGHTNING_FLAG: self._gaming_cache.oob_profiles_lightning_flag,
            self.ID.OOB_PROFILES_CRC: self._gaming_cache.oob_profiles_crc,
            self.ID.OPTICAL_SWITCHES_KBD_MASK_TABLE: self._cache.optical_switches_kbd_mask_table,
            self.ID.STARTUP_TIME_COLD_BOOT: self.features.PRODUCT.TIMINGS.F_StartupTimeColdBoot
                if self.features.PRODUCT.TIMINGS.F_StartupTimeColdBoot is not None
                else self.features.PRODUCT.TIMINGS.F_StartupTime,
            self.ID.DUAL_BANK_IMAGE_HEADERS: self._cache.dual_bank_image_headers,
            self.ID.LOGI_MCU_BOOT_GIT_HASH: self._cache.logi_mcu_boot_git_hash,
        }
    # end def feature_value_map

    def get_feature(self, feature_id):
        # See ``ConfigurationManagerInterface.get_feature``
        return self._resolve_dependency(feature_id, self.feature_value_map)
    # end def get_feature

    @staticmethod
    def get_feature_version(feature_config):
        # See ``ConfigurationManagerInterface.get_feature_version``
        try:
            return int(match(r"F_Version_(.*)", [version for version in dir(feature_config) if match(
                r"F_Version_.*", version) and getattr(feature_config, version)][0]).group(1))
        except IndexError:
            return None
        # end try
    # end get_feature_version

    @staticmethod
    def str_to_bool(keyword):
        """
        Method to convert a ``str`` to a ``bool``. Values returning True are defined in a list. All other values
        return False

        :param keyword: Keyword to convert (must be part of the list to return True)
        :type keyword: ``str``

        :return: Boolean conversion
        :rtype: ``bool``
        """
        return keyword.lower() in ['true', '1', 'set', 'yes']
    # end def str_to_bool

    def _resolve_dependency(self, dependency_value, feature_map):
        """
        Resolve dependency in a map
        """
        dependency_map = {
            "mode": self.current_mode,
            "protocol": self.current_protocol,
            "target": self.current_target,
        }
        value = None
        if dependency_value in feature_map:
            value = feature_map[dependency_value]
            if isinstance(value, dict) and "dependency" in value:
                dependency_value = dependency_map[value["dependency"]]
                value = self._resolve_dependency(dependency_value, value)
            # end if
        # end if
        return value
    # end def _resolve_dependency

    class Cache:
        """
        Cache values which can be computed only once
        """
        def __init__(self, features):
            """
            :param features: Context features
            :type features: ``context.features``
            """
            self.features = features
            cid_info_table = self.features.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.CID_INFO_TABLE

            if cid_info_table.F_Enabled:
                self.cid_info_table_friendly_name = cid_info_table.F_FriendlyName[:-1]
                self.cid_info_table_cid = [int(raw_cid, 16) for raw_cid in cid_info_table.F_Cid[:-1]]
                self.cid_info_table_task = [int(raw_tid, 16) for raw_tid in cid_info_table.F_Task[:-1]]
                self.cid_info_table_flag_virtual = [ConfigurationManager.str_to_bool(raw_flag) for raw_flag in
                                                    cid_info_table.F_FlagVirtual[:-1]]
                self.cid_info_table_flag_persist = [ConfigurationManager.str_to_bool(raw_flag) for raw_flag in
                                                    cid_info_table.F_FlagPersist[:-1]]
                self.cid_info_table_flag_divert = [ConfigurationManager.str_to_bool(raw_flag) for raw_flag in
                                                   cid_info_table.F_FlagDivert[:-1]]
                self.cid_info_table_flag_reprog = [ConfigurationManager.str_to_bool(raw_flag) for raw_flag in
                                                   cid_info_table.F_FlagReprog[:-1]]
                self.cid_info_table_flag_fntog = [ConfigurationManager.str_to_bool(raw_flag) for raw_flag in
                                                  cid_info_table.F_FlagFnTog[:-1]]
                self.cid_info_table_flag_hotkey = [ConfigurationManager.str_to_bool(raw_flag) for raw_flag in
                                                   cid_info_table.F_FlagHotKey[:-1]]
                self.cid_info_table_flag_fkey = [ConfigurationManager.str_to_bool(raw_flag) for raw_flag in
                                                 cid_info_table.F_FlagFKey[:-1]]
                self.cid_info_table_flag_mouse = [ConfigurationManager.str_to_bool(raw_flag) for raw_flag in
                                                  cid_info_table.F_FlagMouse[:-1]]
                self.cid_info_table_pos = [int(raw_pos, 16) for raw_pos in cid_info_table.F_Pos[:-1]]
                self.cid_info_table_group = [int(raw_group, 16) for raw_group in cid_info_table.F_Group[:-1]]
                self.cid_info_table_gmask = [int(raw_gmask, 16) for raw_gmask in cid_info_table.F_GMask[:-1]]
                self.cid_info_table_additional_flags_raw_wheel = [
                    ConfigurationManager.str_to_bool(raw_flag) for raw_flag in
                    cid_info_table.F_AdditionalFlagsRawWheel[:-1]]
                self.cid_info_table_additional_flags_analytics_key_events = [
                    ConfigurationManager.str_to_bool(raw_flag) for raw_flag in
                    cid_info_table.F_AdditionalFlagsAnalyticsKeyEvents[:-1]]
                self.cid_info_table_additional_flags_force_raw_xy = [
                    ConfigurationManager.str_to_bool(raw_flag) for raw_flag in
                    cid_info_table.F_AdditionalFlagsForceRawXY[:-1]]
                self.cid_info_table_additional_flags_raw_xy = [ConfigurationManager.str_to_bool(raw_flag) for raw_flag
                                                               in cid_info_table.F_AdditionalFlagsRawXY[:-1]]

                self.raw_cid_table = [
                    str(HexList(CidInfoPayload.from_detailed_fields(
                        cid=self.cid_info_table_cid[index],
                        task=self.cid_info_table_task[index],
                        flag_virtual=self.cid_info_table_flag_virtual[index],
                        flag_persist=self.cid_info_table_flag_persist[index],
                        flag_divert=self.cid_info_table_flag_divert[index],
                        flag_reprog=self.cid_info_table_flag_reprog[index],
                        flag_fn_tog=self.cid_info_table_flag_fntog[index],
                        flag_hot_key=self.cid_info_table_flag_hotkey[index],
                        flag_f_key=self.cid_info_table_flag_fkey[index],
                        flag_mouse=self.cid_info_table_flag_mouse[index],
                        pos=self.cid_info_table_pos[index],
                        group=self.cid_info_table_group[index],
                        gmask=self.cid_info_table_gmask[index],
                        additional_flags_raw_wheel=self.cid_info_table_additional_flags_raw_wheel[index],
                        additional_flags_analytics_key_event=(
                            self.cid_info_table_additional_flags_analytics_key_events[index]),
                        additional_flags_force_raw_xy=self.cid_info_table_additional_flags_force_raw_xy[index],
                        additional_flags_raw_xy=self.cid_info_table_additional_flags_raw_xy[index])))
                    for index in range(len(self.cid_info_table_cid))]
            else:
                self.raw_cid_table = self.features.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_CidInfoTable if \
                    self.features.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_CidInfoTable is not None else []
                self.cid_info_table_friendly_name = [f"Undefined ({cid_info})" for cid_info in self.raw_cid_table]
                self.cid_info_table_cid = [int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).cid)) for cid_info
                                           in self.raw_cid_table]
                self.cid_info_table_task = [int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).task)) for
                                            cid_info in self.raw_cid_table]
                self.cid_info_table_flag_virtual = [
                    int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).flags.virtual)) for cid_info in
                    self.raw_cid_table]
                self.cid_info_table_flag_persist = [
                    int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).flags.persist)) for cid_info in
                    self.raw_cid_table]
                self.cid_info_table_flag_divert = [
                    int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).flags.divert)) for cid_info in
                    self.raw_cid_table]
                self.cid_info_table_flag_reprog = [
                    int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).flags.reprog)) for cid_info in
                    self.raw_cid_table]
                self.cid_info_table_flag_fntog = [
                    int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).flags.fn_tog)) for cid_info in
                    self.raw_cid_table]
                self.cid_info_table_flag_hotkey = [
                    int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).flags.hot_key)) for cid_info in
                    self.raw_cid_table]
                self.cid_info_table_flag_fkey = [
                    int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).flags.fkey)) for cid_info in
                    self.raw_cid_table]
                self.cid_info_table_flag_mouse = [
                    int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).flags.mouse)) for cid_info in
                    self.raw_cid_table]
                self.cid_info_table_pos = [
                    int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).pos)) for cid_info in
                    self.raw_cid_table]
                self.cid_info_table_group = [
                    int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).group)) for cid_info in
                    self.raw_cid_table]
                self.cid_info_table_gmask = [
                    int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).gmask)) for cid_info in
                    self.raw_cid_table]
                self.cid_info_table_additional_flags_raw_wheel = [
                    int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).additional_flags.raw_wheel))
                    for cid_info in self.raw_cid_table]
                self.cid_info_table_additional_flags_analytics_key_events = [
                    int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).additional_flags.analytics_key_events))
                    for cid_info in self.raw_cid_table]
                self.cid_info_table_additional_flags_force_raw_xy = [
                    int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).additional_flags.force_raw_xy))
                    for cid_info in self.raw_cid_table]
                self.cid_info_table_additional_flags_raw_xy = [
                    int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).additional_flags.raw_xy))
                    for cid_info in self.raw_cid_table]
            # end if

            # Initialize 0x19A1 Contextual keys
            self._init_contextual_keys()

            nvs_chunk_ids = self.features.PRODUCT.NVS_CHUNK_IDS
            self.is_gaming_chunk_id_map = nvs_chunk_ids.F_IsGamingVariant
            if nvs_chunk_ids.F_Enabled:
                self.chunk_id_names = nvs_chunk_ids.F_ChunkIdNames[:-1]
                self.chunk_id_values = [int(nvs_id, 16) for nvs_id in nvs_chunk_ids.F_ChunkIdValues[:-1]]
            else:
                self.chunk_id_names = ()
                self.chunk_id_values = ()
            # end if

            self.supported_properties, self.specific_properties_sizes = self.get_x1807_properties()
            self.accessible_properties, self.accessible_properties_sizes = self.get_x0011_properties()

            # 0x1876 Optical Switches
            optical_switches = self.features.PRODUCT.FEATURES.COMMON.OPTICAL_SWITCHES
            self.optical_switches_kbd_mask_table = []
            if optical_switches.F_Enabled:
                col_num = optical_switches.F_NbColumns
                for lang_idx in range(len(optical_switches.F_SupportedKeyLayout)):
                    # The lang_index is the index of the supported language key matrix layout.
                    # Please refer the OpticalSwitches settings in features.py for more information.
                    if not getattr(optical_switches, 'F_SupportedKeyLayout')[lang_idx]:
                        continue
                    # end if
                    port_0 = HexList()
                    port_1 = HexList()
                    for col in range(col_num):
                        col_kbd_mask = HexList(getattr(optical_switches, f'F_ColumnMaskTable_{col}')[lang_idx])[::-1]
                        port_1 += Numeral(col_kbd_mask[0:4], byteCount=4)
                        port_0 += Numeral(col_kbd_mask[4:8], byteCount=4)
                    # end for
                    self.optical_switches_kbd_mask_table.append(port_0 + port_1)
                # end for
            # end if

            self.dual_bank_image_headers = self.get_dual_bank_image_headers()
            self.logi_mcu_boot_git_hash = self.get_logi_mcu_boot_git_hash()
        # end def __init__

        def _init_contextual_keys(self):
            """
            Initialize Product specific settings for 0x19A1 Contextual Keys
            """
            display_info_table = self.features.PRODUCT.FEATURES.VLP.COMMON.CONTEXTUAL_DISPLAY.DISPLAY_INFO_TABLE
            button_table = self.features.PRODUCT.FEATURES.VLP.COMMON.CONTEXTUAL_DISPLAY.BUTTON_TABLE
            visible_area_table = self.features.PRODUCT.FEATURES.VLP.COMMON.CONTEXTUAL_DISPLAY.VISIBLE_AREA_TABLE

            # display_info_table
            self.display_index = [int(dis_index, 8) for dis_index in display_info_table.F_DisplayIndex[:-1]]
            self.display_shape = [int(dis_shape, 8) for dis_shape in display_info_table.F_DisplayShape[:-1]]
            self.display_dimension = [int(raw_dimension, 16) for raw_dimension in
                                      display_info_table.F_DisplayDimension[:-1]]
            self.horizontal_res = [int(raw_h_res, 16) for raw_h_res in display_info_table.F_HorizontalRes[:-1]]
            self.vertical_res = [int(raw_v_res, 16) for raw_v_res in display_info_table.F_VerticalRes[:-1]]
            self.button_count = [int(button_count) for button_count in display_info_table.F_ButtonCount[:-1]]
            self.visible_area_count = [int(visible_area_count) for visible_area_count in
                                       display_info_table.F_VisibleAreaCount[:-1]]

            # button_table
            self.button_index = [int(b_index) for b_index in button_table.F_ButtonIndex[:-1]]
            self.button_shape = [int(b_shape, 8) for b_shape in button_table.F_ButtonShape[:-1]]
            self.button_loc_x = [int(button_x, 16) for button_x in button_table.F_ButtonLocationX[:-1]]
            self.button_loc_y = [int(button_y, 16) for button_y in button_table.F_ButtonLocationY[:-1]]
            self.button_loc_width = [int(button_w, 16) for button_w in button_table.F_ButtonLocationWidth[:-1]]
            self.button_loc_height = [int(button_h, 16) for button_h in button_table.F_ButtonLocationHeight[:-1]]

            # visible_area_table
            self.visible_area_index = [int(v_index) for v_index in visible_area_table.F_VisibleAreaIndex[:-1]]
            self.visible_area_shape = [int(v_area_shape) for v_area_shape in visible_area_table.F_VisibleAreaShape[:-1]]
            self.visible_area_loc_x = [int(v_area_loc_x, 16) for v_area_loc_x in
                                       visible_area_table.F_VisibleAreaLocationX[:-1]]
            self.visible_area_loc_y = [int(v_area_loc_y, 16) for v_area_loc_y in
                                       visible_area_table.F_VisibleAreaLocationY[:-1]]
            self.visible_area_loc_width = [int(v_area_loc_width, 16) for v_area_loc_width in
                                           visible_area_table.F_VisibleAreaLocationWidth[:-1]]
            self.visible_area_loc_height = [int(v_area_loc_height, 16) for v_area_loc_height in
                                            visible_area_table.F_VisibleAreaLocationHeight[:-1]]
        # end def _init_contextual_keys

        def get_x1807_properties(self):
            """
            Configure the properties associated to the 0x1807 HID++ feature

            :return: Supported properties and specific properties sizes
            :rtype: ``tuple[list, list]``
            """
            supported_properties = [
                getattr(ConfigurableProperties.PropertyId, supported_property)
                if (isinstance(supported_property, str)
                    and hasattr(ConfigurableProperties.PropertyId, supported_property))
                else [prop_id for prop_id in ConfigurableProperties.PropertyId
                      if prop_id.value == int(supported_property)][0]
                for supported_property in self.features.PRODUCT.FEATURES.COMMON.CONFIGURABLE_PROPERTIES.F_SupportedProperties
                if supported_property != '']

            if len(supported_properties) != len(set(supported_properties)):
                warn(f'Duplicated property id(s) in supported properties configuration. Check settings.ini file.')
                supported_properties = list(set(supported_properties))
            # end if

            # Pattern definition ('str : int',)
            pattern = r'(\S*)\s*:\s*(\d+)'
            specific_properties_sizes = {
                getattr(ConfigurableProperties.PropertyId, match(pattern, specific_prop_size)[1]):
                    int(match(pattern, specific_prop_size)[2])
                for specific_prop_size in self.features.PRODUCT.FEATURES.COMMON.CONFIGURABLE_PROPERTIES.F_SpecificPropertiesSizes
                if specific_prop_size != ''
            }

            return supported_properties, specific_properties_sizes
        # end def get_x1807_properties

        def get_x0011_properties(self):
            """
            Configure the properties associated to the 0x0011 HID++ feature

            :return: Supported properties and specific properties sizes
            :rtype: ``tuple[list, list]``
            """
            accessible_properties = [
                getattr(PropertyAccess.PropertyId, accessible_property)
                if (isinstance(accessible_property, str)
                    and hasattr(PropertyAccess.PropertyId, accessible_property))
                else [prop_id for prop_id in PropertyAccess.PropertyId
                      if prop_id.value == int(accessible_property)][0]
                for accessible_property in self.features.PRODUCT.FEATURES.COMMON.PROPERTY_ACCESS.F_SwAccessibleProperties
                if accessible_property != '']

            if len(accessible_properties) != len(set(accessible_properties)):
                warn(f'Duplicated property id(s) in supported properties configuration. Check settings.ini file.')
                accessible_properties = list(set(accessible_properties))
            # end if

            # Pattern definition ('str : int',)
            pattern = r'(\S*)\s*:\s*(\d+)'
            accessible_properties_sizes = {
                getattr(PropertyAccess.PropertyId, match(pattern, accessible_prop_size)[1]):
                    int(match(pattern, accessible_prop_size)[2])
                for accessible_prop_size in self.features.PRODUCT.FEATURES.COMMON.PROPERTY_ACCESS.F_SwAccessiblePropertiesSizes
                if accessible_prop_size != ''
            }

            return accessible_properties, accessible_properties_sizes
        # end def get_x0011_properties

        def get_dual_bank_image_headers(self):
            """
            Get the dual bank image headers configuration

            :return: List of image headers
            :rtype: ``list[ImageHeader]``
            """
            headers = []
            for index, slot_base in enumerate(self.features.PRODUCT.DUAL_BANK.SLOTS.F_Base):
                if slot_base == '':
                    break
                # end if
                headers.append(
                    ImageHeader(
                        load_addr=HexList(self.features.PRODUCT.DUAL_BANK.SLOTS.F_LoadAddr[index]),
                        header_size=HexList(self.features.PRODUCT.DUAL_BANK.SLOTS.F_HeaderSize[index]),
                        protect_tlv_size=HexList(self.features.PRODUCT.DUAL_BANK.SLOTS.F_ProtectTLVSize[index]),
                        image_size=HexList(self.features.PRODUCT.DUAL_BANK.SLOTS.F_ImageSize[index]),
                        flags=HexList(self.features.PRODUCT.DUAL_BANK.SLOTS.F_Flags[index]),
                        image_version=ImageVersion(
                            major=HexList(self.features.PRODUCT.DUAL_BANK.SLOTS.F_VersionMajor[index]),
                            minor=HexList(self.features.PRODUCT.DUAL_BANK.SLOTS.F_VersionMinor[index]),
                            revision=HexList(self.features.PRODUCT.DUAL_BANK.SLOTS.F_VersionRevision[index]),
                            build_number=HexList(self.features.PRODUCT.DUAL_BANK.SLOTS.F_VersionBuildNumber[index])
                        )
                    )
                )
            # end for
            return headers
        # end def get_dual_bank_image_headers

        def get_logi_mcu_boot_git_hash(self):
            """
            Get LogiMCUboot Git Hash

            :return: LogiMCUBoot submodule git hash
            :rtype: ``HexList``
            """
            git_hash = self.features.PRODUCT.DUAL_BANK.BOOTLOADER_IMAGE_COMMUNICATION.F_GitHash
            if git_hash is None:
                # noinspection PyUnresolvedReferences
                submodules_status_path = join(pysetup.TESTS_PATH, 'LOCAL', 'submodules_status')
                pattern = r'[0-9a-fA-F]{40}'
                if exists(submodules_status_path):
                    with open(submodules_status_path, 'r') as submodules_status_file:
                        lines = submodules_status_file.readlines()
                        for line in lines:
                            if 'bootloader/logi_mcuboot' in line:
                                git_hash = HexList(search(pattern, line).group()[:8])
                                break
                            # end if
                        # end for
                    # end with
                # end if
            # end if
            return git_hash
        # end def get_logi_mcu_boot_git_hash
    # end class Cache

    class GamingCache:
        """
        Cache values which can be computed only once for gaming configurations
        """
        def __init__(self, features):
            """
            Constructor

            :param features: Context features
            :type features: ``context.features``
            """
            self.features = features

            rgb_effect = self.features.PRODUCT.FEATURES.GAMING.RGB_EFFECTS
            if rgb_effect.F_Enabled:
                effect_info_table = rgb_effect.EFFECT_INFO_TABLE
                cluster_index = [int(x, 16) for x in effect_info_table.F_ClusterIndex if x != '']
                effect_index = [int(x, 16) for x in effect_info_table.F_EffectIndex if x != '']
                effect_id = [int(x, 16) for x in effect_info_table.F_EffectId if x != '']
                effect_capabilities = [int(x, 16) for x in effect_info_table.F_EffectCapabilities if x != '']
                effect_period = [int(x, 16) for x in effect_info_table.F_EffectPeriod if x != '']

                cluster = None
                self.effect_info_table = {}
                for idx in range(len(cluster_index)):
                    if cluster is None or cluster != cluster_index[idx]:
                        cluster = cluster_index[idx]
                        self.effect_info_table[cluster] = [[effect_index[idx], effect_id[idx],
                                                           effect_capabilities[idx], effect_period[idx]]]
                    else:
                        self.effect_info_table[cluster].append([effect_index[idx], effect_id[idx],
                                                                effect_capabilities[idx], effect_period[idx]])
                    # end if
                # end for
            else:
                self.effect_info_table = {}
            # end if

            onboard_profiles = self.features.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES
            if onboard_profiles.F_Enabled:
                oob_profile_directory = onboard_profiles.OOB_PROFILE_DIRECTORY
                oob_profiles = onboard_profiles.OOB_PROFILES
                # OOB Directory
                self.oob_profile_directory_sector_id = [int(x, 16) for x in oob_profile_directory.F_SectorId if x != '']
                self.oob_profile_directory_status = [int(x, 16) for x in oob_profile_directory.F_Status if x != '']
                self.oob_profile_directory = dict(zip(self.oob_profile_directory_sector_id,
                                                      self.oob_profile_directory_status))
                # OOB Profile
                self.oob_profiles_report_rate = [int(x) for x in oob_profiles.F_ReportRate if x != '']
                self.oob_profiles_report_rate_wireless = [int(x) for x in oob_profiles.F_ReportRateWireless if x != '']
                self.oob_profiles_report_rate_wired = [int(x) for x in oob_profiles.F_ReportRateWired if x != '']
                self.oob_profiles_default_dpi_index = [int(x) for x in oob_profiles.F_DefaultDpiIndex if x != '']
                self.oob_profiles_shift_dpi_index = [int(x) for x in oob_profiles.F_ShiftDpiIndex if x != '']
                oob_profiles_dpi_0 = [int(x) for x in oob_profiles.F_DPI_0 if x != '']
                oob_profiles_dpi_1 = [int(x) for x in oob_profiles.F_DPI_1 if x != '']
                oob_profiles_dpi_2 = [int(x) for x in oob_profiles.F_DPI_2 if x != '']
                oob_profiles_dpi_3 = [int(x) for x in oob_profiles.F_DPI_3 if x != '']
                oob_profiles_dpi_4 = [int(x) for x in oob_profiles.F_DPI_4 if x != '']
                self.oob_profiles_dpi_list = [
                    [oob_profiles_dpi_0[idx], oob_profiles_dpi_1[idx],
                     oob_profiles_dpi_2[idx], oob_profiles_dpi_3[idx],
                     oob_profiles_dpi_4[idx]]
                    for idx in range(len(oob_profiles_dpi_0))
                ]
                oob_profiles_dpi_x_0 = [int(x) for x in oob_profiles.F_DPI_X_0 if x != '']
                oob_profiles_dpi_y_0 = [int(x) for x in oob_profiles.F_DPI_Y_0 if x != '']
                oob_profiles_dpi_lod_0 = [int(x) for x in oob_profiles.F_DPI_LOD_0 if x != '']
                oob_profiles_dpi_x_1 = [int(x) for x in oob_profiles.F_DPI_X_1 if x != '']
                oob_profiles_dpi_y_1 = [int(x) for x in oob_profiles.F_DPI_Y_1 if x != '']
                oob_profiles_dpi_lod_1 = [int(x) for x in oob_profiles.F_DPI_LOD_1 if x != '']
                oob_profiles_dpi_x_2 = [int(x) for x in oob_profiles.F_DPI_X_2 if x != '']
                oob_profiles_dpi_y_2 = [int(x) for x in oob_profiles.F_DPI_Y_2 if x != '']
                oob_profiles_dpi_lod_2 = [int(x) for x in oob_profiles.F_DPI_LOD_2 if x != '']
                oob_profiles_dpi_x_3 = [int(x) for x in oob_profiles.F_DPI_X_3 if x != '']
                oob_profiles_dpi_y_3 = [int(x) for x in oob_profiles.F_DPI_Y_3 if x != '']
                oob_profiles_dpi_lod_3 = [int(x) for x in oob_profiles.F_DPI_LOD_3 if x != '']
                oob_profiles_dpi_x_4 = [int(x) for x in oob_profiles.F_DPI_X_4 if x != '']
                oob_profiles_dpi_y_4 = [int(x) for x in oob_profiles.F_DPI_Y_4 if x != '']
                oob_profiles_dpi_lod_4 = [int(x) for x in oob_profiles.F_DPI_LOD_4 if x != '']
                self.oob_profiles_dpi_xy_list = [
                    [[oob_profiles_dpi_x_0[idx], oob_profiles_dpi_y_0[idx],
                      oob_profiles_dpi_lod_0[idx]],
                     [oob_profiles_dpi_x_1[idx], oob_profiles_dpi_y_1[idx],
                      oob_profiles_dpi_lod_1[idx]],
                     [oob_profiles_dpi_x_2[idx], oob_profiles_dpi_y_2[idx],
                      oob_profiles_dpi_lod_2[idx]],
                     [oob_profiles_dpi_x_3[idx], oob_profiles_dpi_y_3[idx],
                      oob_profiles_dpi_lod_3[idx]],
                     [oob_profiles_dpi_x_4[idx], oob_profiles_dpi_y_4[idx],
                      oob_profiles_dpi_lod_4[idx]]]
                    for idx in range(len(oob_profiles_dpi_x_0))
                ]
                self.oob_profiles_dpi_delta_x = [int(x) for x in oob_profiles.F_DpiDeltaX if x != '']
                self.oob_profiles_dpi_delta_y = [int(x) for x in oob_profiles.F_DpiDeltaY if x != '']
                self.oob_profiles_led_color_red = [int(x, 16) for x in oob_profiles.F_LedColorRed if x != '']
                self.oob_profiles_led_color_green = [int(x, 16) for x in oob_profiles.F_LedColorGreen if x != '']
                self.oob_profiles_led_color_blue = [int(x, 16) for x in oob_profiles.F_LedColorBlue if x != '']
                self.oob_profiles_power_mode = [int(x, 16) for x in oob_profiles.F_PowerMode if x != '']
                self.oob_profiles_angle_snapping = [int(x) for x in oob_profiles.F_AngleSnapping if x != '']
                self.oob_profiles_write_counter = [int(x, 16) for x in oob_profiles.F_WriteCounter if x != '']
                self.oob_profiles_power_save_timeout = [int(x) for x in oob_profiles.F_PowerSaveTimeout_S if x != '']
                self.oob_profiles_power_off_timeout = [int(x) for x in oob_profiles.F_PowerOffTimeout_S if x != '']
                oob_profiles_btn_0 = [[int(value, 16) for value in settings.split(' ')]
                                      for settings in oob_profiles.F_Button_0 if settings != '']
                oob_profiles_btn_1 = [[int(value, 16) for value in settings.split(' ')]
                                      for settings in oob_profiles.F_Button_1 if settings != '']
                oob_profiles_btn_2 = [[int(value, 16) for value in settings.split(' ')]
                                      for settings in oob_profiles.F_Button_2 if settings != '']
                oob_profiles_btn_3 = [[int(value, 16) for value in settings.split(' ')]
                                      for settings in oob_profiles.F_Button_3 if settings != '']
                oob_profiles_btn_4 = [[int(value, 16) for value in settings.split(' ')]
                                      for settings in oob_profiles.F_Button_4 if settings != '']
                oob_profiles_btn_5 = [[int(value, 16) for value in settings.split(' ')]
                                      for settings in oob_profiles.F_Button_5 if settings != '']
                oob_profiles_btn_6 = [[int(value, 16) for value in settings.split(' ')]
                                      for settings in oob_profiles.F_Button_6 if settings != '']
                oob_profiles_btn_7 = [[int(value, 16) for value in settings.split(' ')]
                                      for settings in oob_profiles.F_Button_7 if settings != '']
                oob_profiles_btn_8 = [[int(value, 16) for value in settings.split(' ')]
                                      for settings in oob_profiles.F_Button_8 if settings != '']
                oob_profiles_btn_9 = [[int(value, 16) for value in settings.split(' ')]
                                      for settings in oob_profiles.F_Button_9 if settings != '']
                oob_profiles_btn_10 = [[int(value, 16) for value in settings.split(' ')]
                                       for settings in oob_profiles.F_Button_10 if settings != '']
                oob_profiles_btn_11 = [[int(value, 16) for value in settings.split(' ')]
                                       for settings in oob_profiles.F_Button_11 if settings != '']
                oob_profiles_btn_12 = [[int(value, 16) for value in settings.split(' ')]
                                       for settings in oob_profiles.F_Button_12 if settings != '']
                oob_profiles_btn_13 = [[int(value, 16) for value in settings.split(' ')]
                                       for settings in oob_profiles.F_Button_13 if settings != '']
                oob_profiles_btn_14 = [[int(value, 16) for value in settings.split(' ')]
                                       for settings in oob_profiles.F_Button_14 if settings != '']
                oob_profiles_btn_15 = [[int(value, 16) for value in settings.split(' ')]
                                       for settings in oob_profiles.F_Button_15 if settings != '']
                self.oob_profiles_btn_16 = [
                    oob_profiles_btn_0[idx] + oob_profiles_btn_1[idx] + oob_profiles_btn_2[idx] +
                    oob_profiles_btn_3[idx] + oob_profiles_btn_4[idx] + oob_profiles_btn_5[idx] +
                    oob_profiles_btn_6[idx] + oob_profiles_btn_7[idx] + oob_profiles_btn_8[idx] +
                    oob_profiles_btn_9[idx] + oob_profiles_btn_10[idx] + oob_profiles_btn_11[idx] +
                    oob_profiles_btn_12[idx] + oob_profiles_btn_13[idx] + oob_profiles_btn_14[idx] +
                    oob_profiles_btn_15[idx]
                    for idx in range(len(oob_profiles_btn_0))]
                self.oob_profiles_btn_12 = [
                    oob_profiles_btn_0[idx] + oob_profiles_btn_1[idx] + oob_profiles_btn_2[idx] +
                    oob_profiles_btn_3[idx] + oob_profiles_btn_4[idx] + oob_profiles_btn_5[idx] +
                    oob_profiles_btn_6[idx] + oob_profiles_btn_7[idx] + oob_profiles_btn_8[idx] +
                    oob_profiles_btn_9[idx] + oob_profiles_btn_10[idx] + oob_profiles_btn_11[idx]
                    for idx in range(len(oob_profiles_btn_0))]
                oob_profiles_g_shift_btn_0 = [
                    [int(value, 16) for value in settings.split(' ')]
                    for settings in oob_profiles.F_GShiftButton_0 if settings != '']
                oob_profiles_g_shift_btn_1 = [
                    [int(value, 16) for value in settings.split(' ')]
                    for settings in oob_profiles.F_GShiftButton_1 if settings != '']
                oob_profiles_g_shift_btn_2 = [
                    [int(value, 16) for value in settings.split(' ')]
                    for settings in oob_profiles.F_GShiftButton_2 if settings != '']
                oob_profiles_g_shift_btn_3 = [
                    [int(value, 16) for value in settings.split(' ')]
                    for settings in oob_profiles.F_GShiftButton_3 if settings != '']
                oob_profiles_g_shift_btn_4 = [
                    [int(value, 16) for value in settings.split(' ')]
                    for settings in oob_profiles.F_GShiftButton_4 if settings != '']
                oob_profiles_g_shift_btn_5 = [
                    [int(value, 16) for value in settings.split(' ')]
                    for settings in oob_profiles.F_GShiftButton_5 if settings != '']
                oob_profiles_g_shift_btn_6 = [
                    [int(value, 16) for value in settings.split(' ')]
                    for settings in oob_profiles.F_GShiftButton_6 if settings != '']
                oob_profiles_g_shift_btn_7 = [
                    [int(value, 16) for value in settings.split(' ')]
                    for settings in oob_profiles.F_GShiftButton_7 if settings != '']
                oob_profiles_g_shift_btn_8 = [
                    [int(value, 16) for value in settings.split(' ')]
                    for settings in oob_profiles.F_GShiftButton_8 if settings != '']
                oob_profiles_g_shift_btn_9 = [
                    [int(value, 16) for value in settings.split(' ')]
                    for settings in oob_profiles.F_GShiftButton_9 if settings != '']
                oob_profiles_g_shift_btn_10 = [
                    [int(value, 16) for value in settings.split(' ')]
                    for settings in oob_profiles.F_GShiftButton_10 if settings != '']
                oob_profiles_g_shift_btn_11 = [
                    [int(value, 16) for value in settings.split(' ')]
                    for settings in oob_profiles.F_GShiftButton_11 if settings != '']
                oob_profiles_g_shift_btn_12 = [
                    [int(value, 16) for value in settings.split(' ')]
                    for settings in oob_profiles.F_GShiftButton_12 if settings != '']
                oob_profiles_g_shift_btn_13 = [
                    [int(value, 16) for value in settings.split(' ')]
                    for settings in oob_profiles.F_GShiftButton_13 if settings != '']
                oob_profiles_g_shift_btn_14 = [
                    [int(value, 16) for value in settings.split(' ')]
                    for settings in oob_profiles.F_GShiftButton_14 if settings != '']
                oob_profiles_g_shift_btn_15 = [
                    [int(value, 16) for value in settings.split(' ')]
                    for settings in oob_profiles.F_GShiftButton_15 if settings != '']
                self.oob_profiles_g_shift_btn_16 = [
                    oob_profiles_g_shift_btn_0[idx] + oob_profiles_g_shift_btn_1[idx] +
                    oob_profiles_g_shift_btn_2[idx] + oob_profiles_g_shift_btn_3[idx] +
                    oob_profiles_g_shift_btn_4[idx] + oob_profiles_g_shift_btn_5[idx] +
                    oob_profiles_g_shift_btn_6[idx] + oob_profiles_g_shift_btn_7[idx] +
                    oob_profiles_g_shift_btn_8[idx] + oob_profiles_g_shift_btn_9[idx] +
                    oob_profiles_g_shift_btn_10[idx] + oob_profiles_g_shift_btn_11[idx] +
                    oob_profiles_g_shift_btn_12[idx] + oob_profiles_g_shift_btn_13[idx] +
                    oob_profiles_g_shift_btn_14[idx] + oob_profiles_g_shift_btn_15[idx]
                    for idx in range(len(oob_profiles_g_shift_btn_0))]
                self.oob_profiles_g_shift_btn_12 = [
                    oob_profiles_g_shift_btn_0[idx] + oob_profiles_g_shift_btn_1[idx] +
                    oob_profiles_g_shift_btn_2[idx] + oob_profiles_g_shift_btn_3[idx] +
                    oob_profiles_g_shift_btn_4[idx] + oob_profiles_g_shift_btn_5[idx] +
                    oob_profiles_g_shift_btn_6[idx] + oob_profiles_g_shift_btn_7[idx] +
                    oob_profiles_g_shift_btn_8[idx] + oob_profiles_g_shift_btn_9[idx] +
                    oob_profiles_g_shift_btn_10[idx] + oob_profiles_g_shift_btn_11[idx]
                    for idx in range(len(oob_profiles_g_shift_btn_0))]
                self.oob_profiles_name = [[int(value, 16) for value in settings.split(' ')]
                                          for settings in oob_profiles.F_ProfileName if settings != '']
                self.oob_profiles_logo_effect = [[int(value, 16) for value in settings.split(' ')]
                                                 for settings in oob_profiles.F_LogoEffect if settings != '']
                self.oob_profiles_side_effect = [[int(value, 16) for value in settings.split(' ')]
                                                 for settings in oob_profiles.F_SideEffect if settings != '']
                self.oob_profiles_logo_active_effect = [[int(value, 16) for value in settings.split(' ')]
                                                        for settings in oob_profiles.F_LogoActiveEffect
                                                        if settings != '']
                self.oob_profiles_side_active_effect = [[int(value, 16) for value in settings.split(' ')]
                                                        for settings in oob_profiles.F_SideActiveEffect
                                                        if settings != '']
                self.oob_profiles_logo_passive_effect = [[int(value, 16) for value in settings.split(' ')]
                                                         for settings in oob_profiles.F_LogoPassiveEffect
                                                         if settings != '']
                self.oob_profiles_side_passive_effect = [[int(value, 16) for value in settings.split(' ')]
                                                         for settings in oob_profiles.F_SidePassiveEffect
                                                         if settings != '']
                self.oob_profiles_cluster_0_active_effect = [[int(value, 16) for value in settings.split(' ')]
                                                             for settings in oob_profiles.F_Cluster_0_ActiveEffect
                                                             if settings != '']
                self.oob_profiles_cluster_1_active_effect = [[int(value, 16) for value in settings.split(' ')]
                                                             for settings in oob_profiles.F_Cluster_1_ActiveEffect
                                                             if settings != '']
                self.oob_profiles_cluster_0_passive_effect = \
                    [[int(value, 16) for value in settings.split(' ')]
                     for settings in oob_profiles.F_Cluster_0_PassiveEffect if settings != '']
                self.oob_profiles_cluster_1_passive_effect = \
                    [[int(value, 16) for value in settings.split(' ')]
                     for settings in oob_profiles.F_Cluster_1_PassiveEffect if settings != '']
                self.oob_profiles_lightning_flag = [int(x, 16) for x in oob_profiles.F_LightningFlag if x != '']
                self.oob_profiles_crc = [int(x, 16) for x in oob_profiles.F_CRC if x != '']
            else:
                self.oob_profile_directory_sector_id = []
                self.oob_profile_directory_status = []
                self.oob_profile_directory = []

                self.oob_profiles_report_rate = []
                self.oob_profiles_report_rate_wireless = []
                self.oob_profiles_report_rate_wired = []
                self.oob_profiles_default_dpi_index = []
                self.oob_profiles_shift_dpi_index = []
                self.oob_profiles_dpi_list = []
                self.oob_profiles_dpi_xy_list = []
                self.oob_profiles_dpi_delta_x = []
                self.oob_profiles_dpi_delta_y = []
                self.oob_profiles_led_color_red = []
                self.oob_profiles_led_color_green = []
                self.oob_profiles_led_color_blue = []
                self.oob_profiles_power_mode = []
                self.oob_profiles_angle_snapping = []
                self.oob_profiles_write_counter = []
                self.oob_profiles_power_save_timeout = []
                self.oob_profiles_power_off_timeout = []
                self.oob_profiles_btn_16 = []
                self.oob_profiles_btn_12 = []
                self.oob_profiles_g_shift_btn_16 = []
                self.oob_profiles_g_shift_btn_12 = []
                self.oob_profiles_name = []
                self.oob_profiles_logo_effect = []
                self.oob_profiles_side_effect = []
                self.oob_profiles_logo_active_effect = []
                self.oob_profiles_side_active_effect = []
                self.oob_profiles_logo_passive_effect = []
                self.oob_profiles_side_passive_effect = []
                self.oob_profiles_cluster_0_active_effect = []
                self.oob_profiles_cluster_1_active_effect = []
                self.oob_profiles_cluster_0_passive_effect = []
                self.oob_profiles_cluster_1_passive_effect = []
                self.oob_profiles_lightning_flag = []
                self.oob_profiles_crc = []
            # end if
        # end def __init__
    # end class GamingCache
# end class ConfigurationManager

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
