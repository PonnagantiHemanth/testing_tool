#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.base.registration
:brief: Feature registration module
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/12/13
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from warnings import warn

from math import log

from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.backlight import Backlight
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ExtendedAdjustableReportRate
from pyhid.hidpp.features.gaming.modestatus import ModeStatus
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.nvsparser import CHUNK_ID_TO_CLASS_MAP
from pyraspi.services.ina226 import INA226
from pyraspi.services.keyboardemulator import KeyboardMixin
from pyraspi.services.kosmos.config.buttonlayout import BUTTON_LAYOUT_BY_ID
from pyraspi.services.kosmos.config.keybaordlayout import GET_KEYBOARD_LAYOUT_BY_ID
from pyraspi.services.kosmos.config.ledlayout import GET_LED_LAYOUT_BY_ID
from pyraspi.services.kosmos.config.rgbconfiguration import GET_RGB_CONFIGURATION_BY_ID
from pyraspi.services.kosmos.kosmos import Kosmos
from pyraspi.services.kosmos.module.devicetree import DeviceFamilyName
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.mcp4725 import MCP4725
from pytestbox.base.cidutils import CidEmulation
from pytestbox.base.cidutils import CidInfoCoverage
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.emulatorsmanager import EmulatorsManager
from pytestbox.base.productdata import RECOVERY_KEYS_LIST_MAP
from pytransport.tools.agilent import Agilent
from pyusb.libusbdriver import LibusbDriver


# ------------------------------------------------------------------------------
# Features implementation
# ------------------------------------------------------------------------------
def check_feature(context, subsystem_name, feature):
    """
    Check if a feature has a specific value.

    :param context: Context
    :type context: ``Context``
    :param subsystem_name: Sub-system name
    :type subsystem_name: ``str``
    :param feature: Feature name
    :type feature: ``str``

    :return: True is the feature is enabled in the given sub-system, false otherwise
    :rtype: ``bool``
    """
    subsystem_list = subsystem_name.split('/')
    try:
        subsystem = context.getFeatures()
        for item in subsystem_list:
            subsystem = subsystem.getChild(item)
        # end for
        if feature in dir(subsystem):
            result = getattr(subsystem, feature)
        else:
            result = False
        # end if
    except Exception as e:
        warn(f"pytestbox.base.registration.check_feature exception: {e}")
        result = False
    # end try
    return result
# end def check_feature


def get_attribute(context, subsystem_name, feature):
    """
    Get the attribute value associated to a given name.

    :param context: Context
    :type context: ``Context``
    :param subsystem_name: Sub-system name
    :type subsystem_name: ``str``
    :param feature: Feature name
    :type feature: ``str``

    :return: Attribute value
    :rtype: ``bool`` or ``int`` or ``tuple`` or ``str``
    """
    try:
        subsystem_list = subsystem_name.split('/')
        subsystem = context.getFeatures()
        for item in subsystem_list:
            subsystem = subsystem.getChild(item)
        # end for
        if feature in dir(subsystem):
            attribute = getattr(subsystem, feature)
            return attribute
        # end if
    except Exception as e:
        warn(f"pytestbox.base.registration.get_attribute exception: {e}")
        pass
    # end try
    return None
# end def get_attribute


def get_non_0_byte_number_in_list(context, subsystem_name, feature):
    """
    Extract a list of non-zero bytes from a number.

    :param context: Context
    :type context: ``Context``
    :param subsystem_name: Sub-system Name
    :type subsystem_name: ``str``
    :param feature: Feature Name
    :type feature: ``str``

    :return: The list of non-zero bytes or 0
    :rtype: ``list`` or ``int``
    """
    attribute = get_attribute(context=context, subsystem_name=subsystem_name, feature=feature)

    if isinstance(attribute, int):
        if attribute == 0:
            return 0
        # end if

        attribute = list(attribute.to_bytes(int(log(attribute, 256)) + 1, "big"))
    # end if

    return len([x for x in attribute if x not in ('00', 0)])
# end def get_non_0_byte_number_in_list

def check_supported_keys(context, keys, physical_layout=KeyboardMixin.LAYOUT.ANSI, at_least_one=False):
    """
    Check whether the required keys are supported by the DUT.

    :param context: Context
    :type context: ``Context``
    :param keys: Key Names
    :type keys: ``tuple(KEY_ID)``
    :param physical_layout: Type of physical layout - OPTIONAL
    :type physical_layout: ``KeyboardMixin.LAYOUT``
    :param at_least_one: Flag indicating if all given keys have to be supported or if at least one is enough. - OPTIONAL
    :type at_least_one: ``bool``

    :return: ``True`` if requested keys are supported (at least one or all depending on the parameter),
             ``False`` otherwise.
    :rtype: ``bool``
    """
    result = True
    subsystem = context.getFeatures()
    if subsystem.PRODUCT.F_ProductReference in GET_KEYBOARD_LAYOUT_BY_ID:
        # Check keyboard supported keys
        keyboard = GET_KEYBOARD_LAYOUT_BY_ID[subsystem.PRODUCT.F_ProductReference][physical_layout]
        try:
            for key in keys:
                if key not in keyboard.KEYS and key not in keyboard.FN_KEYS:
                    # Set temporary result to False because this key does not belong to the target matrix.
                    result = False
                elif at_least_one:
                    # return True because at least one key belongs to the target matrix.
                    return True
                # end if
            # end for
        except Exception as e:
            warn(f"pytestbox.base.registration.check_supported_keys exception: {e}")
        # end try
    else:
        # Check mouse connected keys
        result = check_connected_keys(context, keys, at_least_one=at_least_one)
    # end if

    return result
# end def check_supported_keys


def check_supported_leds(context, leds, at_least_one=False):
    """
    Check whether the required leds are supported by the DUT.

    :param context: Context
    :type context: ``Context``
    :param leds: Led Names
    :type leds: ``tuple(LED_ID)``
    :param at_least_one: Flag indicating if we request that all given leds are supported or only one. - OPTIONAL
    :type at_least_one: ``bool``

    :return: ``True`` if requested leds are supported
             ``False`` otherwise.
    :rtype: ``bool``
    """
    result = True
    subsystem = context.getFeatures()
    if subsystem.PRODUCT.F_ProductReference in GET_LED_LAYOUT_BY_ID:
        # Check supported leds
        led_list = GET_LED_LAYOUT_BY_ID[subsystem.PRODUCT.F_ProductReference]
        try:
            for led in leds:
                if led not in led_list.LEDS:
                    # Set temporary result to False because this led does not belong to the target.
                    result = False
                elif at_least_one:
                    # return True because at least on led belongs to the target.
                    return True
                # end if
            # end for
        except Exception as e:
            warn(f"pytestbox.base.registration.check_supported_leds exception: {e}")
        # end try
    else:
        result = False
    # end if
    return result
# end def check_supported_leds


def check_supported_os_layout(context, keyboard_os_layouts):
    """
    Check the supported keys.

    :param context: Context
    :type context: ``Context``
    :param keyboard_os_layouts: The value of the corresponding OS. cf ``MultiPlatform.OSMask``
    :type keyboard_os_layouts: ``tuple[int]``

    :return: ``True`` if the keyboard os layout is supported, ``False`` otherwise.
    :rtype: ``bool``
    """
    subsystem = context.getFeatures()

    supported_os_layouts = []
    for os_mask in subsystem.PRODUCT.FEATURES.KEYBOARD.MULTI_PLATFORM.F_OsMask:
        try:
            for i in range(16):
                if int(os_mask) & (2 ** i):
                    supported_os_layouts.append(2 ** i)
                # end if
            # end for
        except Exception as e:
            warn(f"pytestbox.base.registration.check_supported_os_layout exception: {e}")
        # end try
    # end for

    for keyboard_os_layout in keyboard_os_layouts:
        if keyboard_os_layout not in supported_os_layouts:
            return False
        # end if
    # end for

    return True
# end def check_supported_os_layout


def check_supported_keyboard_layout(context, keyboard_layout):
    """
    Check the supported keyboard layout.

    :param context: Context
    :type context: ``Context``
    :param keyboard_layout: The value of keyboard layout
    :type keyboard_layout: ``int``

    :return: ``True`` if the keyboard layout in test settings matches the one given, ``False`` otherwise.
    :rtype: ``bool``
    """
    subsystem = context.getFeatures()

    return subsystem.PRODUCT.FEATURES.KEYBOARD.KEYBOARD_INTERNATIONAL_LAYOUTS.F_KeyboardLayout == keyboard_layout
# end def check_supported_keyboard_layout


def check_connected_keys(context, key_ids=None, keyword_keys=None, at_least_one=False):
    """
    Check if the requested keys are connected

    :param context: Context
    :type context: ``Context``
    :param key_ids: Tuple of key ids - OPTIONAL
    :type key_ids: ``tuple[KEY_ID]``
    :param keyword_keys: Tuple of keys named with keywords - OPTIONAL
    :type keyword_keys: ``tuple[str]``
    :param at_least_one: Flag indicating if we request that all given keys are supported or only one. - OPTIONAL
    :type at_least_one: ``bool``

    :return: ``True`` if requested keys are connected (at least one or all depending on the parameter),
             ``False`` if the condition is not met.
    :rtype: ``bool``
    """
    key_ids = [] if key_ids is None else list(key_ids)

    # Get configuration and init
    context_features = context.getFeatures()
    config_manager = ConfigurationManager(context_features)
    emulators_manager = EmulatorsManager.get_instance(context_features)
    emulators_manager.init(config_manager.current_device_type)
    if emulators_manager.button_stimuli_emulator is None:
        result = False
    else:
        emu_keyword_key_ids = emulators_manager.button_stimuli_emulator.keyword_key_ids
        if keyword_keys is not None:
            if not at_least_one and not all(elem in emu_keyword_key_ids for elem in keyword_keys):
                return False
            elif at_least_one and not any(elem in emu_keyword_key_ids for elem in keyword_keys):
                return False
            # end if
            key_ids.extend([emu_keyword_key_ids[keyword_key] for keyword_key in keyword_keys])
        # end if
        result = any(elem in emulators_manager.get_connected_key_ids() for elem in key_ids) if at_least_one else \
            all(elem in emulators_manager.get_connected_key_ids() for elem in key_ids)
    # end if
    return result
# end def check_connected_keys


def check_passive_hold_press_support(context):
    """
    Check if buttons stimuli emulator can hold a key press passively while other action can be performed

    :param context: Context
    :type context: ``Context``
    :return: Passive hold press support
    :rtype: ``bool``
    """
    context_features = context.getFeatures()
    config_manager = ConfigurationManager(context_features)
    emulators_manager = EmulatorsManager.get_instance(context_features)
    emulators_manager.init(config_manager.current_device_type)
    return emulators_manager.button_stimuli_emulator.passive_hold_press_support
# end def check_passive_hold_press_support


def check_rgb_configuration(context):
    """
    Check RGB configuration of the device is defined in the GET_RGB_CONFIGURATION_BY_ID

    :param context: Context
    :type context: ``Context``

    :return: True if the RGB configuration of the device is defined in the GET_RGB_CONFIGURATION_BY_ID
    :rtype: ``bool``
    """
    subsystem = context.getFeatures()

    product_reference = subsystem.PRODUCT.F_ProductReference

    return product_reference in GET_RGB_CONFIGURATION_BY_ID.keys()
# end def check_rgb_configuration


def is_recovery_action_supported(context, action, number=1):
    """
    Checker function used by the 'DeviceRecoveryActions' decorator
    Evaluate if the type of action and their number are supported by the DUT

    :param context: Context
    :type context: ``Context``
    :param action: Recovery Keys list name ("pre-reset_actions" or "post-reset_actions")
    :type action: ``str``
    :param number: number of action in the list - OPTIONAL
    :type number: ``int``

    :return: True if the recovery action and key count are supported by the device otherwise False
    :rtype: ``bool``
    """
    key_list = RECOVERY_KEYS_LIST_MAP[
                context.getFeatures().PRODUCT.DEVICE.CONNECTION_SCHEME.DEVICE_RECOVERY.F_RecoveryKeysVariant][action]
    # using filter() to remove None values in list
    key_list = list(filter(None, key_list))
    key_list = list(filter(lambda x: x[1] != BREAK, key_list))
    if key_list is None or len(key_list) == 0:
        return False
    elif len(key_list) < int(number):
        return False
    else:
        return True
    # end if
# end def is_recovery_action_supported


def is_an_empty_tuple(context, subsystem_name, feature):
    """
    Checks if a feature is an empty tuple or not

    :param context: Context
    :type context: ``Context``
    :param subsystem_name: Sub-system Name
    :type subsystem_name: ``str``
    :param feature: Feature Name
    :type feature: ``str``

    :return: True if the feature is an empty tuple, False otherwise
    :rtype: ``bool``
    """
    subsystem_list = subsystem_name.split('/')
    result = True
    try:
        subsystem = context.getFeatures()
        for item in subsystem_list:
            subsystem = subsystem.getChild(item)
        # end for
        if feature in dir(subsystem):
            input_list = getattr(subsystem, feature)
            if input_list != ('',):
                result = False
            # end if
        # end if
    except Exception as e:
        warn(f"pytestbox.base.registration.check_feature exception: {e}")
    # end try
    return result
# end def is_an_empty_tuple


def is_dpi_range_supported(context):
    """
    Check the DPI report type is by ranges or fixed DPI values

    :param context: Context
    :type context: ``Context``

    :return: True, if report by DPI ranges, otherwise report by fixed DPI value list
    :rtype: ``bool``
    """
    dpi_ranges = get_attribute(
        context=context, subsystem_name='PRODUCT/FEATURES/MOUSE/EXTENDED_ADJUSTABLE_DPI', feature='F_DpiRangesX')
    return True if any([(int(x, 16) & 0xFF00) == 0xE000 for x in dpi_ranges if x != '']) else False
# end def is_dpi_range_supported


def is_multiple_pairing_slots_supported(context):
    """
    Check the pairing slots supported on the device more than one.

    :param context: Context
    :type context: ``Context``

    :return: True, if the device supports multiple pairing slots
    :rtype: ``bool``
    """
    slots = ('Ls2Slot', 'LsSlot', 'CrushSlot')
    number_of_supported_slot = 0
    for slot in slots:
        if get_attribute(
            context=context, subsystem_name='PRODUCT/FEATURES/COMMON/LIGHTSPEED_PREPAIRING', feature=f'F_{slot}'):
            number_of_supported_slot += 1
        # end if

        if number_of_supported_slot > 1:
            return True
        # end if
    # end for

    return False
# end def is_multiple_pairing_slots_supported


def is_backlight_options_supported(context, options_mask):
    """
    Check whether the given backlight options are all supported or not

    :param context: Context
    :type context: ``Context``
    :param options_mask: Supported options mask
    :type options_mask: ``Backlight.SupportedOptionsMask``

    :return: Flag indicating if the required backlight options are all supported
    :rtype: ``bool``
    """
    support_options = get_attribute(
        context=context, subsystem_name='PRODUCT/FEATURES/COMMON/BACKLIGHT', feature='F_SupportedOptions')
    if support_options is None:
        return False
    else:
        return True if to_int(support_options) & options_mask == options_mask else False
    # end if
# end def is_backlight_options_supported


def is_backlight_effect_supported(context, effect_mask):
    """
    Check if the given backlight effect is supported or not

    :param context: Context
    :type context: ``Context``
    :param effect_mask: Supported options mask
    :type effect_mask: ``Backlight.SupportedBacklightEffectMask``

    :return: Flag indicating if the required backlight effect is supported
    :rtype: ``bool``
    """
    support_options = get_attribute(
        context=context, subsystem_name='PRODUCT/FEATURES/COMMON/BACKLIGHT', feature='F_BacklightEffectList')
    return support_options is not None and (to_int(support_options) & effect_mask) == effect_mask
# end def is_backlight_effect_supported


def is_brightness_capability_supported(context, capability_bit_index):
    """
    Check if the given brightness capability is supported or not

    :param context: Context
    :type context: ``Context``
    :param capability_bit_index: The bit index of brightness capabilities
    :type capability_bit_index: ``pyhid.hidpp.features.gaming.brightnesscontrol.CapabilitiesV1.POS``

    :return: Flag indicating if the required brightness capability is supported
    :rtype: ``bool``
    """
    capabilities = get_attribute(
        context=context, subsystem_name='PRODUCT/FEATURES/GAMING/BRIGHTNESS_CONTROL', feature='F_Capabilities')
    return HexList(capabilities).testBit(capability_bit_index)
# end def is_brightness_capability_supported


def is_rgb_effect_supported(context, cluster_index, effect_id):
    """
    Check if the given rgb effect is supported or not on the cluster

    :param context: Context
    :type context: ``Context``
    :param cluster_index: RGB cluster index
    :type cluster_index: ``int``
    :param effect_id: Effect ID
    :type effect_id: ``int``

    :return: Flag indicating if the required RGB effect is supported on the given cluster
    :rtype: ``bool``
    """
    status = False
    is_effect_id_empty_tuple = is_an_empty_tuple(context=context,
                                                 subsystem_name='PRODUCT/FEATURES/GAMING/RGB_EFFECTS/EFFECT_INFO_TABLE',
                                                 feature='F_EffectId')
    is_cluster_index_empty_tuple = is_an_empty_tuple(context=context,
                                                     subsystem_name='PRODUCT/FEATURES/GAMING/RGB_EFFECTS/EFFECT_INFO_TABLE',
                                                     feature='F_ClusterIndex')
    if is_effect_id_empty_tuple or is_cluster_index_empty_tuple:
        return False
    # end if

    effect_id_list = get_attribute(context=context,
                                   subsystem_name='PRODUCT/FEATURES/GAMING/RGB_EFFECTS/EFFECT_INFO_TABLE',
                                   feature='F_EffectId')
    cluster_index_list = get_attribute(context=context,
                                   subsystem_name='PRODUCT/FEATURES/GAMING/RGB_EFFECTS/EFFECT_INFO_TABLE',
                                   feature='F_ClusterIndex')
    for e_id, c_id in zip(effect_id_list, cluster_index_list):
        if effect_id == int(e_id, 16) and cluster_index == int(c_id, 16):
            status = True
            break
        # end if
    # end for
    return status
# end def is_rgb_effect_supported

def is_rgb_nv_capability_supported(context, capability):
    """
    Check if the given rgb non volatile capability is supported or not by the dut

    :param context: Context
    :type context: ``Context``
    :param capability: RGB non volatile capability
    :type capability: ``RGBEffectsTestUtils.NvCapabilities``

    :return: Flag indicating if the given rgb non volatile capability is supported or not by the dut
    :rtype: ``bool``
    """
    support_nv_capabilities = get_attribute(context=context,
                                            subsystem_name='PRODUCT/FEATURES/GAMING/RGB_EFFECTS',
                                            feature='F_NvCapabilities')
    return support_nv_capabilities is not None and (to_int(support_nv_capabilities) & capability) == capability
# end def is_rgb_nv_capability_supported

def is_persistence_supported(context):
    """
    Check if persistance is supported by atleast one cluster

    :param context: Context
    :type context: ``Context``

    :return: Flag indicating if persistence is supported by atleast one cluster
    :rtype: ``bool``
    """
    persistence_list = get_attribute(context=context,
                                     subsystem_name='PRODUCT/FEATURES/GAMING/RGB_EFFECTS/CLUSTER_INFO_TABLE',
                                     feature='F_EffectPersistencyCapabilities')
    return len([persist for persist in persistence_list if persist != '' and int(persist, 16) > 0])
# end def is_persistence_supported


def btldr_ble_support(context):
    """
    Check if bootloader supports BLE

    :param context: Context
    :type context: ``Context``

    :return: BLE support in Bootloader
    :rtype: ``bool``
    """
    config_manager = ConfigurationManager(context.getFeatures())
    return config_manager.feature_value_map[config_manager.ID.TRANSPORT_BTLE][config_manager.MODE.BOOTLOADER]
# end def btldr_ble_support


def check_nvs_chunk_class_available(context, chunk_name):
    """
    Check if a given NVS Chunk class is implemented

    :param context: Context
    :type context: ``Context``
    :param chunk_name: chunk name as defined in the chunk id map
    :type chunk_name: ``str``

    :return: Flag indicating if the given NVS Chunk class is implemented
    :rtype: ``bool``
    """

    if chunk_name in CHUNK_ID_TO_CLASS_MAP:
        return True
    else:
        return False
    # end if
# end def check_nvs_chunk_class_available


def is_hybrid_switch_power_mode_supported(context, power_mode):
    """
    Check if a given hybrid switch power mode is supported by the DUT

    :param context: Context
    :type context: ``Context``
    :param power_mode: Hybrid switch power mode
    :type power_mode: ``pyhid.hidpp.features.gaming.modestatus.ModeStatus.ModeStatus1.PowerMode``

    :return: Flag indicating if the given hybrid switch power mode is supported by the DUT
    :rtype: ``bool``
    """
    status = False
    mode_status_1 = get_attribute(context=context,
                                  subsystem_name='PRODUCT/FEATURES/GAMING/MODE_STATUS',
                                  feature='F_ModeStatus1')
    is_enabled = get_attribute(context=context,
                            subsystem_name='PRODUCT/FEATURES/GAMING/MODE_STATUS',
                            feature='F_Enabled')
    power_save_mode_supported = get_attribute(context=context,
                                              subsystem_name='PRODUCT/FEATURES/GAMING/MODE_STATUS',
                                              feature='F_PowerSaveModeSupported')
    if HexList(mode_status_1).testBit(ModeStatus.ModeStatus1.POS.POWER_MODE) == power_mode:
        # Check if power_mode is the default mode
        status = True
    elif is_enabled:
        # Check if feature 0x8090 (mode status) is enabled
        if power_mode == ModeStatus.ModeStatus1.PowerMode.POWER_SAVE_MODE and power_save_mode_supported:
            status = True
        elif power_mode == ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE:
            status = True
        # end if
    # end if
    return status
# end def is_hybrid_switch_power_mode_supported


def check_hybrid_switch_emulator(context):
    """
    Check if hybrid switch can be emulated (galvanic and optical part separately) with the DUT setup

    :param context: Context
    :type context: ``Context``

    :return: Flag indicating if hybrid switch can be emulated with the DUT setup
    :rtype: ``bool``
    """
    result = False
    subsystem = context.getFeatures()
    if subsystem.PRODUCT.F_ProductReference in BUTTON_LAYOUT_BY_ID:
        if (BUTTON_LAYOUT_BY_ID[subsystem.PRODUCT.F_ProductReference].HAS_HYBRID_SWITCH and
                Kosmos.discover_emulator(emulation_type=DeviceName.BAS)):
            result = True
        # end if
    # end if
    return result
# end def check_hybrid_switch_emulator


def is_report_rate_supported(context, connection_type, report_rate):
    """
    Check if the given report rate is supported or not on the connection type

    :param context: Context
    :type context: ``Context``
    :param connection_type: Connection type index
    :type connection_type: ``ExtendedAdjustableReportRate.ConnectionType``
    :param report_rate: Report rate
    :type report_rate: ``ExtendedAdjustableReportRate.RATE``

    :return: Flag indicating if the given report rate is supported or not on the connection type
    :rtype: ``bool``
    """
    status = False
    default_report_rate = None
    is_enabled = get_attribute(context=context,
                               subsystem_name='PRODUCT/FEATURES/GAMING/EXTENDED_ADJUSTABLE_REPORT_RATE',
                               feature='F_Enabled')
    supported_report_rate_list = get_attribute(context=context,
                                               subsystem_name='PRODUCT/FEATURES/GAMING/EXTENDED_ADJUSTABLE_REPORT_RATE',
                                               feature='F_SupportedReportRateList')
    if connection_type == ExtendedAdjustableReportRate.ConnectionType.WIRED:
        default_report_rate = get_attribute(context=context,
                                            subsystem_name='PRODUCT/FEATURES/GAMING/EXTENDED_ADJUSTABLE_REPORT_RATE',
                                            feature='F_DefaultReportRateWired')
    elif connection_type == ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS:
        default_report_rate = get_attribute(context=context,
                                            subsystem_name='PRODUCT/FEATURES/GAMING/EXTENDED_ADJUSTABLE_REPORT_RATE',
                                            feature='F_DefaultReportRateWireless')
    # end if

    if default_report_rate == report_rate:
        # Check if report_rate is the default report rate
        status = True
    elif is_enabled:
        # Check if feature 0x8061 (extend adjustable report rate) is enabled
        if HexList(supported_report_rate_list[connection_type]).testBit(report_rate):
            status = True
        else:
            status = False
        # end if
    # end if
    return status
# end def is_report_rate_supported


# -----------------
# Generic Features
# -----------------
function = lambda context: (check_feature(context, 'PRODUCT', 'F_IsMice')
                            and not check_feature(context, 'PRODUCT', 'F_IsKeyPad')
                            and not check_feature(context, 'PRODUCT', 'F_IsSimulation'))
features.registerFeature('Mice', function, featureHelp='Help for Mice')
function = lambda context: (not check_feature(context, 'PRODUCT', 'F_IsMice')
                            and not check_feature(context, 'PRODUCT', 'F_IsKeyPad')
                            and not check_feature(context, 'PRODUCT', 'F_IsSimulation'))
features.registerFeature('Keyboard', function, featureHelp='Help for Keyboard')
function = lambda context: (check_feature(context, 'PRODUCT', 'F_IsPlatform'))
features.registerFeature('IsPlatform', function, featureHelp='Help for Platform Dev Board detection')
# Ghost Key Tests
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/KEYBOARD', 'F_GhostKeys'))
features.registerFeature('GhostKeys', function, featureHelp='Help for Ghost Keys related tests')
# Key Code Tests
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/KEYBOARD', 'F_KeyCode'))
features.registerFeature('KeyCode', function, featureHelp='Help for Key Code related tests')
# Layout Tests
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/KEYBOARD', 'F_Layout'))
features.registerFeature('Layout', function, featureHelp='Help for Layout related tests')
# Sholo Tests
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/KEYBOARD', 'F_Sholo'))
features.registerFeature('Sholo', function, featureHelp='Help for Sholo related tests')
function = lambda context: (check_feature(context, 'PRODUCT/DEVICE', 'F_Is60PercentKeyboard'))
features.registerFeature('60PercentKeyboard', function, featureHelp='Help for 60 percent keyboard')
function = lambda context: (check_feature( # 25 is the device type value of Contextual Key
    context, 'PRODUCT/FEATURES/COMMON/DEVICE_TYPE_AND_NAME', 'F_DeviceType') == 25)
features.registerFeature('ContextualKeys', function, featureHelp='Help for ContextualKeys')
function = lambda context: (check_feature(context, 'PRODUCT', 'F_CompanionMCU'))
features.registerFeature('CompanionMCU', function, featureHelp='Help for Companion MCU')
function = lambda context: (check_feature(context, 'PRODUCT', 'F_IsGaming'))
features.registerFeature('GamingDevice', function, featureHelp='Help for Gaming Device')
function = lambda context: (get_attribute(context, 'PRODUCT/DEVICE', 'F_KeyboardType') == 'membrane')
features.registerFeature('MembraneKeyboard', function, featureHelp='Help for Membrane Keyboard')
function = lambda context: (check_feature(context, 'PRODUCT/TIMINGS', 'F_Enabled'))
features.registerFeature('Timings', function, featureHelp='Help for FW Timings')
function = lambda context: (check_feature(context, 'PRODUCT/TIMINGS', 'F_2kHzSupport'))
features.registerFeature('2kHzTimings', function, featureHelp='Help for FW Timings')
function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/DEVICE_RECOVERY', 'F_Enabled'))
features.registerFeature('DeviceRecovery', function, featureHelp='Help for Device Recovery')
function = lambda context, action, number=1: (check_feature(
                                              context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/DEVICE_RECOVERY', 'F_Enabled')
                                              and is_recovery_action_supported(context, action, number))
features.registerFeature('DeviceRecoveryActions', function, featureHelp='Help for Device Recovery Robustness')
# UICR and NVS features
function = lambda context: (check_feature(context, 'PRODUCT', 'F_FullBankErase'))
features.registerFeature('FullBankErase', function, featureHelp="Help for Full Bank Erase")
function = lambda context, chunk_name: (check_nvs_chunk_class_available(context, chunk_name))
features.registerFeature('NvsChunkID', function, featureHelp="Help for checking availability of NVS class")
function = lambda context: (check_feature(context, 'PRODUCT/NVS_UICR', 'F_Enabled'))
features.registerFeature('UICR', function, featureHelp='Help for UICR')
function = lambda context: (check_feature(context, 'PRODUCT/NVS_UICR', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/NVS_UICR', 'F_NVSEncryption'))
features.registerFeature('NVSEncryption', function, featureHelp='Help for NVS Encryption')
function = lambda context: (check_feature(context, 'PRODUCT/NVS_UICR', 'F_Enabled') and
                            get_attribute(context, 'PRODUCT/NVS_UICR', 'F_NFCPINS') is not None)
features.registerFeature('UicrNfcPins', function, featureHelp='Help for NFCPINS')
function = lambda context: (check_feature(context, 'PRODUCT/NVS_UICR', 'F_Enabled') and
                            get_attribute(context, 'PRODUCT/NVS_UICR', 'F_DEBUGCTRL') is not None)
features.registerFeature('UicrDebugCtrl', function, featureHelp='Help for DEBUGCTRL')
function = lambda context: (check_feature(context, 'PRODUCT/NVS_UICR', 'F_Enabled') and
                            get_attribute(context, 'PRODUCT/NVS_UICR', 'F_REGOUT0') is not None)
features.registerFeature('UicrRegout0', function, featureHelp='Help for REGOUT0')
function = lambda context: (check_feature(context, 'PRODUCT/NVS_UICR', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/NVS_UICR', 'F_MagicNumber'))
features.registerFeature('UicrMagicNumber', function, featureHelp='Help for UICR MagicNumber')
# Code CheckList
function = lambda context: (check_feature(context, 'PRODUCT/CODE_CHECKLIST', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/CODE_CHECKLIST', 'F_StackVerification'))
features.registerFeature('StackDepth', function, featureHelp='Help for Stack depth verification')
function = lambda context: (check_feature(context, 'PRODUCT/CODE_CHECKLIST', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/CODE_CHECKLIST', 'F_RamInitialization'))
features.registerFeature('RamInit', function, featureHelp='Help for Ram Initilization verification')
# Supported Protocol
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_TransportUsb') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_TransportEQuad') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_TransportBT') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_TransportBTLE'))
features.registerFeature('USBOnly', function, featureHelp='Help for USB Protocol Support only')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_TransportEQuad'))
features.registerFeature('Unifying', function, featureHelp='Help for Unifying Protocol Support')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_TransportBT') or
                            check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_TransportBTLE'))
features.registerFeature('Bluetooth', function, featureHelp='Help for Bluetooth Protocol Support')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_TransportEQuad') or
                            check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_TransportBT') or
                            check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_TransportBTLE'))
features.registerFeature('Wireless', function, featureHelp='Help for Wireless Protocol Support')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_TransportUsb'))
features.registerFeature('USB', function, featureHelp='Help for USB Protocol Support')
# -----------------
# Protocols Test suites
# -----------------
function = lambda context: (check_feature(context, 'PRODUCT/PROTOCOLS/USB', 'F_Enabled'))
features.registerFeature('USBProtocol', function, featureHelp='Help for USB Protocol Test Suite')
function = lambda context: (
        check_feature(context, 'PRODUCT/PROTOCOLS/USB', 'F_Enabled') and
        get_attribute(context, 'PRODUCT/PROTOCOLS/USB', 'F_DigitizerInterfaceDescriptor') is not None)
features.registerFeature('DigitizerInterface', function, featureHelp='Help for USB Protocol Test Suite')
function = lambda context: (check_feature(context, 'PRODUCT/PROTOCOLS/BLE', 'F_Enabled'))
features.registerFeature('BLEProtocol', function, featureHelp='Help for BLE Protocol Test Suite')
function = lambda context: (btldr_ble_support(context))
features.registerFeature('BootloaderBLESupport', function, featureHelp='Help for BLE Protocol Test Suite')
function = lambda context: (get_attribute(context, 'PRODUCT/PROTOCOLS/BLE', 'F_HidReportMap') is not None)
features.registerFeature('HidReportMap', function, featureHelp='Help for HID Report Map')
function = lambda context: (check_feature(context, 'PRODUCT/PROTOCOLS/BLE', 'F_BLEppCccdToggled'))
features.registerFeature('BLEppCccdToggled', function, featureHelp='Help for BLE++ service CCCD toggled')
function = lambda context: (check_feature(context, 'PRODUCT/PROTOCOLS/BLE_PRO', 'F_Enabled'))
features.registerFeature('BLEProProtocol', function, featureHelp='Help for BLE Pro Protocol Test Suite')
function = lambda context: (check_feature(context, 'PRODUCT/PROTOCOLS/BLE_PRO', 'F_Version_1'))
features.registerFeature('BLEProV1', function, featureHelp='Help for BLE Pro Protocol version 1 Test Suite')
function = lambda context: (check_feature(context, 'PRODUCT/PROTOCOLS/BLE_PRO', 'F_Version_2'))
features.registerFeature('BLEProV2', function, featureHelp='Help for BLE Pro Protocol version 2 Test Suite')
function = lambda context: (check_feature(context, 'PRODUCT/PROTOCOLS/BLE', 'F_ChromeSupport'))
features.registerFeature('ChromeSupport', function, featureHelp='Help for Chrome support Os Detection Test Suite')
function = lambda context: (check_feature(context, 'PRODUCT/PROTOCOLS/BLE', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/PROTOCOLS/BLE', 'F_OsDetection'))
features.registerFeature('OsDetection', function, featureHelp='Help for Os Detection Test Suite')
function = lambda context: (check_feature(context, 'PRODUCT/PROTOCOLS/BLE', 'F_Enabled')
                            and check_feature(context, 'PRODUCT/PROTOCOLS/BLE', 'F_Spaces_Specifications'))
features.registerFeature('BLESpacesSpecification', function, featureHelp='Help for Spaces specifications BLE Test Suite')
function = lambda context, keyboard_os_layout: (check_supported_os_layout(context, keyboard_os_layout))
services.registerFeature('RequiredOsLayout', function, featureHelp='Help for RequiredOsLayout service')
function = lambda context: get_attribute(context, "PRODUCT/PROTOCOLS/BLE", "F_BAS_Version") == "1.0"
features.registerFeature('BAS1.0', function, featureHelp="Help for BAS version 1.0 Test Suite")
function = lambda context: get_attribute(context, "PRODUCT/PROTOCOLS/BLE", "F_BAS_Version") == "1.1"
features.registerFeature('BAS1.1', function, featureHelp="Help for BAS version 1.1 Test Suite")
function = lambda context: get_attribute(context, "PRODUCT/PROTOCOLS/BLE", "F_BAS_Version") is not None
features.registerFeature('BAS1.0+', function, featureHelp="Help for BAS version 1.0+ Test Suite")
# -----------------
# HID++ Features
# -----------------
# Important Features
# -----------------
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/IMPORTANT/ROOT', 'F_Enabled'))
features.registerFeature('Feature0000', function, featureHelp='Help for Root')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/IMPORTANT/ROOT', 'F_Version_0'))
features.registerFeature('Feature0000v0', function, featureHelp='Help for Root v0')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/IMPORTANT/ROOT', 'F_Enabled') and
                            not check_feature(context, 'PRODUCT/FEATURES/IMPORTANT/ROOT', 'F_Version_0'))
features.registerFeature('Feature0000v1+', function, featureHelp='Help for Root v1 and higher')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/IMPORTANT/FEATURE_SET', 'F_Enabled'))
features.registerFeature('Feature0001', function, featureHelp='Help for Feature Set')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/IMPORTANT/FEATURE_SET', 'F_Version_0'))
features.registerFeature('Feature0001v0', function, featureHelp='Help for Feature Set v0')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/IMPORTANT/FEATURE_SET', 'F_Version_1'))
features.registerFeature('Feature0001v1', function, featureHelp='Help for Feature Set v1')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/IMPORTANT/FEATURE_SET', 'F_Enabled') and
                            not check_feature(context, 'PRODUCT/FEATURES/IMPORTANT/FEATURE_SET', 'F_Version_0'))
features.registerFeature('Feature0001v1+', function, featureHelp='Help for  Feature Set v1 and higher')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/IMPORTANT/FEATURE_SET', 'F_Enabled') and
                            not check_feature(context, 'PRODUCT/FEATURES/IMPORTANT/FEATURE_SET', 'F_Version_0') and
                            not check_feature(context, 'PRODUCT/FEATURES/IMPORTANT/FEATURE_SET', 'F_Version_1'))
features.registerFeature('Feature0001v2+', function, featureHelp='Help for  Feature Set v1 and higher')

# Common Features
# -----------------
# GetDeviceInfo
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_Enabled'))
features.registerFeature('Feature0003', function, featureHelp='Help for GetDeviceInfo')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_Version_0'))
features.registerFeature('Feature0003v0', function, featureHelp='Help for GetDeviceInfo v0')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_Enabled') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_Version_0'))
features.registerFeature('Feature0003v1+', function, featureHelp='Help for GetDeviceInfo v1 and higher')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_Version_2'))
features.registerFeature('Feature0003v2', function, featureHelp='Help for GetDeviceInfo v2')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_Version_4'))
features.registerFeature('Feature0003v4', function, featureHelp='Help for GetDeviceInfo v4')
function = lambda context: (
        check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_Enabled') and
        not check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_Version_0') and
        not check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_Version_1') and
        not check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_Version_2') and
        not check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_INFORMATION', 'F_Version_3'))
features.registerFeature('Feature0003v4+', function, featureHelp='Help for GetDeviceInfo v4 and higher')
# GetDeviceTypeAndName
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_TYPE_AND_NAME', 'F_Enabled'))
features.registerFeature('Feature0005', function, featureHelp='Help for Get Device Type And Name')
function = lambda context: (
    get_attribute(context, 'PRODUCT/FEATURES/COMMON/DEVICE_TYPE_AND_NAME', 'F_MarketingName').endswith('for Mac'))
features.registerFeature('ForMAC', function, featureHelp='Help for For MAC product identification')
# Property Access
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/PROPERTY_ACCESS', 'F_Enabled'))
features.registerFeature('Feature0011', function, featureHelp='Help for Property Access')
function = lambda context, property_id: (
        property_id.name in get_attribute(context,
                                          'PRODUCT/FEATURES/COMMON/PROPERTY_ACCESS', 'F_SwAccessibleProperties'))
features.registerFeature('Feature0011AccessiblePropertyId', function, featureHelp='Help for Configurable Properties')
# Configuration Change
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/CONFIG_CHANGE', 'F_Enabled'))
features.registerFeature('Feature0020', function, featureHelp='Help for Config Change')
# Device Friendly Name
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_FRIENDLY_NAME', 'F_Enabled'))
features.registerFeature('Feature0007', function, featureHelp='Help for Device Friendly Name')
# Keep Alive
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/COMMON/KEEP_ALIVE', 'F_Enabled'))
features.registerFeature('Feature0008', function, featureHelp='Help for Keep Alive')
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/COMMON/KEEP_ALIVE', 'F_Enabled') and
    check_feature(context, 'PRODUCT/FEATURES/COMMON/KEEP_ALIVE', 'F_Version_0'))
features.registerFeature('Feature0008v0', function, featureHelp='Help for Keep Alive v0')
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/COMMON/KEEP_ALIVE', 'F_Enabled') and
    check_feature(context, 'PRODUCT/FEATURES/COMMON/KEEP_ALIVE', 'F_Version_1'))
features.registerFeature('Feature0008v1', function, featureHelp='Help for Keep Alive v1')
# Force Pairing
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/FORCE_PAIRING', 'F_Enabled'))
features.registerFeature('Feature1500', function, featureHelp='Help for Force Pairing tests')

function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/LS2_CS', 'F_Enabled') and
                            (check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/LS2_CS', 'F_LS2_Support') or
                             check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/LS2_CS', 'F_UHS_Support')))
features.registerFeature('CSForcePairing', function, featureHelp='Help for CSForcePairingTestCases')

function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/FORCE_PAIRING', 'F_MaxWaitForLedOff'))
features.registerFeature('MaxWaitForLedOff', function, featureHelp='Help for Max Wait for Led Off')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/FORCE_PAIRING', 'F_HasImmersiveLighting'))
features.registerFeature('HasImmersiveLighting', function, featureHelp='Help for Immersive Lighting')
# Password Authentication
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/COMMON/PASSWORD_AUTHENTICATION', 'F_Enabled'))
features.registerFeature('PasswordAuthentication', function, featureHelp='Help for Password Authentication')
# Password Authentication Support Long Password
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/COMMON/PASSWORD_AUTHENTICATION', 'F_SupportLongPassword'))
features.registerFeature('PasswordAuthenticationLongPassword', function,
                         featureHelp='Help for Long Password Authentication')
# Password Authentication Support Smaller Password
function = lambda context: False  # TODO : Check for smaller password if implemented in a firmware
features.registerFeature('PasswordAuthenticationSmallerPassword', function,
                         featureHelp='Help for Smaller Password Authentication')
# Manufacturing Mode
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/COMMON/MANUFACTURING_MODE', 'F_Enabled'))
features.registerFeature('Feature1801', function, featureHelp='Help for Manufacturing Mode')
# Device Reset
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DEVICE_RESET', 'F_Enabled'))
features.registerFeature('Feature1802', function, featureHelp='Help for Device Reset')
# GPIO access
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/GPIO_ACCESS', 'F_Enabled'))
features.registerFeature('Feature1803', function, featureHelp='Help for GPIO access')
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/COMMON/GPIO_ACCESS', 'F_Enabled') and
    check_feature(context, 'PRODUCT/FEATURES/COMMON/GPIO_ACCESS', 'F_Version_1'))
features.registerFeature('Feature1803v1', function, featureHelp='Help for GPIO access v1')
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/COMMON/GPIO_ACCESS', 'F_Enabled') and
    sum(int(x) for x in HexList(get_attribute(
        context, 'PRODUCT/FEATURES/COMMON/GPIO_ACCESS', 'F_GpioForbiddenMask')) if x != '') > 0)
features.registerFeature('Feature1803HasForbiddenMask',
                         function, featureHelp='Help for GPIO access with GpioForbiddenMask not null')
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/COMMON/GPIO_ACCESS', 'F_Enabled') and
    sum(int(x) for x in HexList(get_attribute(
        context, 'PRODUCT/FEATURES/COMMON/GPIO_ACCESS', 'F_GpioUnusedMask')) if x != '') > 0)
features.registerFeature('Feature1803HasUnusedGPIO',
                         function, featureHelp='Help for GPIO access with GpioUnusedMask not null')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/GPIO_ACCESS', 'F_SupportReadGroupOut'))
features.registerFeature('Feature1803SupportReadGroupOut', function, featureHelp='Help for GPIO access with SupportReadGroupOut')
# OOB State
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/OOB_STATE', 'F_Enabled'))
features.registerFeature('Feature1805', function, featureHelp='Help for OOB state')
# Configurable Device Properties
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/CONFIGURABLE_DEVICE_PROPERTIES', 'F_Enabled'))
features.registerFeature('Feature1806', function, featureHelp='Help for Configurable Device Properties')
# Configurable Properties
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/CONFIGURABLE_PROPERTIES', 'F_Enabled'))
features.registerFeature('Feature1807', function, featureHelp='Help for Configurable Properties')
function = lambda context, property_id: (
        property_id.name in get_attribute(context, 'PRODUCT/FEATURES/COMMON/CONFIGURABLE_PROPERTIES', 'F_SupportedProperties'))
features.registerFeature('Feature1807SupportedPropertyId', function, featureHelp='Help for Configurable Properties')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/CONFIGURABLE_PROPERTIES', 'F_FilterUnstableTest'))
features.registerFeature('Feature1807FilterUnstableTest', function, featureHelp='Help for Filter Unstable Test')
# Configurable Device Registers
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/CONFIGURABLE_DEVICE_REGISTERS', 'F_Enabled'))
features.registerFeature('Feature180B', function, featureHelp='Help for Configurable Device Registers')
# BLE Pro Pre-pairing
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/BLE_PRO_PREPAIRING', 'F_Enabled'))
features.registerFeature('Feature1816', function, featureHelp='Help for BLE Pro pre-pairing')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/BLE_PRO_PREPAIRING', 'F_IrkOptional'))
features.registerFeature('Feature1816IrkOptional', function, featureHelp='Help for BLE Pro pre-pairing')
function = lambda context, key_mask: (check_feature(
            context, 'PRODUCT/FEATURES/COMMON/BLE_PRO_PREPAIRING', 'F_Enabled')
            and (key_mask & get_attribute(context, 'PRODUCT/FEATURES/COMMON/BLE_PRO_PREPAIRING', 'F_KeysSupported')))
features.registerFeature('Feature1816KeysSupported', function,
                         featureHelp='Help for BLE Pro pre-pairing supported keys')
# RF test
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/RF_TEST', 'F_Enabled'))
features.registerFeature('Feature1890', function, featureHelp='Help for RF test')
# LED Test
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/LED_TEST', 'F_Enabled'))
features.registerFeature('Feature18A1', function, featureHelp='Help for LED Test')
# Backlight
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/BACKLIGHT', 'F_Enabled'))
features.registerFeature('Feature1982', function, featureHelp='Help for Backlight')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/BACKLIGHT', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/FEATURES/COMMON/BACKLIGHT', 'F_Version_0') and
                            check_feature(context, 'PRODUCT/FEATURES/COMMON/BACKLIGHT', 'F_Version_1') and
                            check_feature(context, 'PRODUCT/FEATURES/COMMON/BACKLIGHT', 'F_Version_2'))
features.registerFeature('Feature1982v0tov2', function, featureHelp='Help for Backlight v0 to v2')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/BACKLIGHT', 'F_Enabled') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/BACKLIGHT', 'F_Version_0') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/BACKLIGHT', 'F_Version_1'))
features.registerFeature('Feature1982v2+', function, featureHelp='Help for Backlight v2 and higher')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/BACKLIGHT', 'F_Enabled') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/BACKLIGHT', 'F_Version_0') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/BACKLIGHT', 'F_Version_1') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/BACKLIGHT', 'F_Version_2'))
features.registerFeature('Feature1982v3+', function, featureHelp='Help for Backlight v3 and higher')
function = lambda context, effects_bitmap=Backlight.SupportedOptionsMask.NONE: (
    is_backlight_options_supported(context, effects_bitmap))
features.registerFeature('Feature1982RequiredOptions', function, featureHelp='Help for Backlight effect support')
function = lambda context: (
        Numeral(get_attribute(context, 'PRODUCT/FEATURES/COMMON/BACKLIGHT', 'F_SupportedOptions')) & 0x0038 > 0)
features.registerFeature('BacklightModeSupported', function, featureHelp='Help for Supported Options')
function = lambda context, effects_bitmap: (is_backlight_effect_supported(context, effects_bitmap))
features.registerFeature('Feature1982RequiredEffect', function, featureHelp='Help for Backlight effect support')
# Force Sensing Button
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/COMMON/FORCE_SENSING_BUTTON', 'F_Enabled'))
features.registerFeature('Feature19C0', function, featureHelp='Help for Force Sensing Button')
# Keyboard reprogrammable Keys and Mouse buttons
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Enabled'))
features.registerFeature('Feature1B04', function, featureHelp='Help for Keyboard reprogrammable Keys and Mouse buttons')
function = lambda context: (check_feature(
    context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Enabled') and
    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_0'))
features.registerFeature('Feature1B04V1+', function,
                         featureHelp='Help for Keyboard reprogrammable Keys and Mouse buttons version 1 and higher')
function = lambda context: (check_feature(
    context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Enabled') and
    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_0') and
    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_1'))
features.registerFeature('Feature1B04V2+', function,
                         featureHelp='Help for Keyboard reprogrammable Keys and Mouse buttons version 2 and higher')
function = lambda context: (
                    check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Enabled') and
                    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_0') and
                    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_1') and
                    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_2'))
features.registerFeature('Feature1B04V3+', function,
                         featureHelp='Help for Keyboard reprogrammable Keys and Mouse buttons version 3 and higher')
function = lambda context: (
                    check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Enabled') and
                    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_0') and
                    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_1') and
                    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_2') and
                    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_3'))
features.registerFeature('Feature1B04V4+', function,
                         featureHelp='Help for Keyboard reprogrammable Keys and Mouse buttons version 4 and higher')
function = lambda context: (
                    check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Enabled') and
                    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_0') and
                    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_1') and
                    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_2') and
                    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_3') and
                    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_4'))
features.registerFeature('Feature1B04V5+', function,
                         featureHelp='Help for Keyboard reprogrammable Keys and Mouse buttons version 5 and higher')
function = lambda context: (
                    check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Enabled') and
                    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_0') and
                    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_1') and
                    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_2') and
                    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_3') and
                    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_4') and
                    not check_feature(context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_Version_5'))
features.registerFeature('Feature1B04V6+', function,
                         featureHelp='Help for Keyboard reprogrammable Keys and Mouse buttons version 6 and higher')
# Keyboard reprogrammable Keys and Mouse buttons : Flags, Groups and Emulation
cid_info_coverage = CidInfoCoverage()
function = lambda context, flags, min_number=1: (
    cid_info_coverage.cid_flags_coverage(context, flags, True, CidEmulation.IGNORED, min_number))
features.registerFeature('Feature1B04WithFlags', function, featureHelp='Help for Keyboard reprogrammable Keys and ' +
                                                                       'Mouse buttons for button with the required ' +
                                                                       'capability')
function = lambda context, flags, min_number=1: (
    cid_info_coverage.cid_flags_coverage(context, flags, False, CidEmulation.IGNORED, min_number))
features.registerFeature('Feature1B04WithoutFlags', function, featureHelp='Help for Keyboard reprogrammable Keys and ' +
                                                                          'Mouse buttons for button with the ' +
                                                                          'required capability')
function = lambda context, flags, emulation=CidEmulation.FULL, min_number=1: (
    cid_info_coverage.cid_flags_coverage(context, flags, True, emulation, min_number))
features.registerFeature('Feature1B04WithFlagsEmulated', function,
                         featureHelp='Help for Keyboard reprogrammable Keys and Mouse buttons for button with the '
                                     'required capability')
function = lambda context, flags, emulation=CidEmulation.FULL, min_number=1: (
    cid_info_coverage.cid_flags_coverage(context, flags, False, emulation, min_number))
features.registerFeature('Feature1B04WithoutFlagsEmulated', function,
                         featureHelp='Help for Keyboard reprogrammable Keys and Mouse buttons for button with the '
                                     'required capability')
function = lambda context, emulation=CidEmulation.FULL, min_number=1: (
    cid_info_coverage.cid_groups_coverage(context, emulation, min_number))
features.registerFeature('Feature1B04WithRemappingEmulated', function,
                         featureHelp='Help for Keyboard reprogrammable Keys and Mouse buttons for button with the '
                                     'remapping capability')
function = lambda context, cid: (
    cid_info_coverage.is_remappable(context, cid, emulation=True))
features.registerFeature('CidRemappingEmulated', function,
                         featureHelp='Help for Keyboard reprogrammable Keys and Mouse buttons for button with the '
                                     'remapping capability')
function = lambda context, cid_target: (
    cid_info_coverage.is_remap_target(context, cid_target, emulation=True))
features.registerFeature('CidRemapTargetEmulated', function,
                         featureHelp='Help for Keyboard reprogrammable Keys and Mouse buttons for button with the '
                                     'remapping capability')
# Keyboard reprogrammable Keys and Mouse buttons: [5] resetAllCidReportSettings is supported or not
function = lambda context: (check_feature(
    context, 'PRODUCT/FEATURES/COMMON/SPECIAL_KEYS_MSE_BUTTONS', 'F_SupportResetAllCidReportSettings'))
features.registerFeature('Feature1B04resetAllCidReportSettings', function,
                         featureHelp='Help for Keyboard reprogrammable Keys and Mouse buttons: '
                                     '[5] resetAllCidReportSettings is supported or not for v6+')
# FullKeyCustomization
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/FULL_KEY_CUSTOMIZATION', 'F_Enabled'))
features.registerFeature('Feature1B05', function, featureHelp='Help for Full Key Customization HID++ feature')
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/COMMON/FULL_KEY_CUSTOMIZATION', 'F_Enabled') and
    check_feature(context, 'PRODUCT/FEATURES/COMMON/FULL_KEY_CUSTOMIZATION', 'F_Version_1'))
features.registerFeature('Feature1B05V1+', function, featureHelp='Help for Full Key Customization version 1 and higher')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/CONTROL_LIST', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/FEATURES/COMMON/FULL_KEY_CUSTOMIZATION', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/FEATURES/GAMING/PROFILE_MANAGEMENT', 'F_Enabled'))
features.registerFeature('FullKeyCustomization', function, featureHelp='Help for Full Key Customization System Feature')
function = lambda context: (Numeral(get_attribute(context, 'PRODUCT/FEATURES/COMMON/FULL_KEY_CUSTOMIZATION',
                                                  'F_FkcConfigFileMaxsize')) != 0)
features.registerFeature('Feature1B05FileMaxSize', function,
                         featureHelp='Help for Full Key Customization fkc_config_file_maxsize')
function = lambda context: (Numeral(get_attribute(context, 'PRODUCT/FEATURES/COMMON/FULL_KEY_CUSTOMIZATION',
                                                  'F_MacroDefFileMaxsize')) != 0)
features.registerFeature('Feature1B05MacroMaxSize', function,
                         featureHelp='Help for Full Key Customization macro_def_file_maxsize')
# Analog Keys
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/ANALOG_KEYS', 'F_Enabled'))
features.registerFeature('Feature1B08', function, featureHelp='Help for Analog Keys')
# Control List
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/CONTROL_LIST', 'F_Enabled'))
features.registerFeature('Feature1B10', function, featureHelp='Help for Control List')
# EquadDJDebugInfo
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/EQUAD_DJ_DEBUG_INFO', 'F_Enabled'))
features.registerFeature('Feature1DF3', function, featureHelp='Help for EquadDJDebugInfo')

# Debounce
function = lambda context: (check_feature(context, 'PRODUCT/DEBOUNCE', 'F_Enabled'))
features.registerFeature('Debounce', function, featureHelp='Help for Debounce tests')
# Battery Unified Level Status
function = lambda context: (check_feature(
    context, 'PRODUCT/FEATURES/COMMON/BATTERY_UNIFIED_LEVEL_STATUS', 'F_Enabled'))
features.registerFeature('Feature1000', function, featureHelp='Help for Battery tests')
function = lambda context: (check_feature(
    context, 'PRODUCT/FEATURES/COMMON/BATTERY_UNIFIED_LEVEL_STATUS', 'F_Version_0'))
features.registerFeature('Feature1000v0', function, featureHelp='Help for Feature 1000')
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/COMMON/BATTERY_UNIFIED_LEVEL_STATUS', 'F_Version_1'))
features.registerFeature('Feature1000v1', function, featureHelp='Help for Feature 1000')
# Todo: Shall add 0x1001 to the check function
function = lambda context: (
        check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Enabled') or
        check_feature(context, 'PRODUCT/FEATURES/COMMON/BATTERY_UNIFIED_LEVEL_STATUS', 'F_Enabled'))
features.registerFeature('EnabledBatteryFeature', function, featureHelp='Help for Battery tests')
# Change Host
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/CHANGE_HOST', 'F_Enabled'))
features.registerFeature('Feature1814', function, featureHelp='Help for Change Host')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/CHANGE_HOST', 'F_Version_0'))
features.registerFeature('Feature1814v0', function, featureHelp='Help for Change Host v0')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/CHANGE_HOST', 'F_Version_1'))
features.registerFeature('Feature1814v1', function, featureHelp='Help for Change Host v1')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/CHANGE_HOST', 'F_TypeC'))
features.registerFeature('Feature1814TypeC', function, featureHelp='Help for Change Host by USB TypeC')
# Hosts Info
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/HOSTS_INFO', 'F_Enabled'))
features.registerFeature('Feature1815', function, featureHelp='Help for HostsInfo')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/HOSTS_INFO', 'F_Enabled') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/HOSTS_INFO', 'F_Version_0') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/HOSTS_INFO', 'F_Version_1'))
features.registerFeature('Feature1815v2+', function, featureHelp='Help for HostsInfo v2 and higher')
# LightspeedPrepairing
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/LIGHTSPEED_PREPAIRING', 'F_Enabled'))
features.registerFeature('Feature1817', function, featureHelp='Help for LightspeedPrepairing')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/LIGHTSPEED_PREPAIRING', 'F_LsSlot'))
features.registerFeature('Feature1817LsSlotSupported', function, featureHelp='Help for LS Slot')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/LIGHTSPEED_PREPAIRING', 'F_CrushSlot'))
features.registerFeature('Feature1817CrushSlotSupported', function, featureHelp='Help for Crush Slot')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/LIGHTSPEED_PREPAIRING', 'F_Ls2Slot'))
features.registerFeature('Feature1817Ls2SlotSupported', function, featureHelp='Help for LS2 Slot')
function = lambda context: (is_multiple_pairing_slots_supported(context))
features.registerFeature('MultiplePairingSlots', function, featureHelp='Help for multiple slots')
# Power Modes
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/POWER_MODES', 'F_Enabled'))
features.registerFeature('Feature1830', function, featureHelp='Help for PowerModes')
function = lambda context, power_mode: (power_mode in [int(x) for x in
                                                       check_feature(context, 'PRODUCT/FEATURES/COMMON/POWER_MODES',
                                                                     'F_NumberList').split(" ") if x != ''])
features.registerFeature('Feature1830powerMode', function, featureHelp='Help for PowerModes mode 1')
# Battery levels calibration
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/BATTERY_LEVELS_CALIBRATION', 'F_Enabled'))
features.registerFeature('Feature1861', function, featureHelp='Help for battery levels calibration tests')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/BATTERY_LEVELS_CALIBRATION', 'F_Enabled')
                            and not check_feature(context,
                                                  'PRODUCT/FEATURES/COMMON/BATTERY_LEVELS_CALIBRATION',
                                                  'F_Version_0'))
features.registerFeature('Feature1861v1+', function, featureHelp='Help for battery levels calibration tests')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/BATTERY_LEVELS_CALIBRATION', 'F_Enabled')
                            and check_feature(context,
                                              'PRODUCT/FEATURES/COMMON/BATTERY_LEVELS_CALIBRATION',
                                              'F_Comparator'))
features.registerFeature('Feature1861Comparator', function, featureHelp='Help for battery levels calibration tests '
                                                                        'using comparator')
# Static Monitor Mode (0x18b0)
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/STATIC_MONITOR_MODE', 'F_Enabled'))
features.registerFeature('Feature18B0', function, featureHelp='Help for Static Monitor Mode')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/STATIC_MONITOR_MODE', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/FEATURES/COMMON/STATIC_MONITOR_MODE', 'F_Version_1'))
features.registerFeature('Feature18B0v1', function, featureHelp='Help for Static Monitor Mode')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/STATIC_MONITOR_MODE', 'F_KeyboardMode'))
features.registerFeature('KeyboardMode', function, featureHelp='Help for KeyboardMode')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/STATIC_MONITOR_MODE',
                                          'F_EnhancedKeyboardMode'))
features.registerFeature('EnhancedKeyboardMode', function, featureHelp='Help for EnhancedKeyboard')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/STATIC_MONITOR_MODE',
                                          'F_KeyboardWithLargerMatrixMode'))
features.registerFeature('KeyboardWithLargerMatrixMode', function, featureHelp='Help for KeyboardWithLargerMatrix')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/STATIC_MONITOR_MODE',
                                          'F_EnhancedKeyboardWithLargerMatrixMode'))
features.registerFeature('EnhancedKeyboardWithLargerMatrixMode', function,
                         featureHelp='Help for EnhancedKeyboardWithLargerMatrixMode')
# ALS Calibration
function = lambda context: False
features.registerFeature('Feature1A20', function, featureHelp='Help for ALS Calibration')
# Enable Hidden Features
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/ENABLE_HIDDEN', 'F_Enabled'))
features.registerFeature('Feature1E00', function, featureHelp='Help for Enable Hidden Features tests')
# Manage Deactivatable Features
function = lambda context: \
    (check_feature(context, 'PRODUCT/FEATURES/COMMON/MANAGE_DEACTIVATABLE_FEATURES', 'F_Enabled'))
features.registerFeature('Feature1E01', function, featureHelp='Help for Manage Deactivatable Features tests')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/MANAGE_DEACTIVATABLE_FEATURES',
                                          'F_SupportManufacturingCounter'))
features.registerFeature(
    'Feature1E01WithManufacturingCounter', function, featureHelp='Help for Manufacturing Counter support')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/MANAGE_DEACTIVATABLE_FEATURES',
                                          'F_SupportComplianceCounter'))
features.registerFeature(
    'Feature1E01WithComplianceCounter', function, featureHelp='Help for Compliance Counter support')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/MANAGE_DEACTIVATABLE_FEATURES',
                                          'F_SupportGothardCounter'))
features.registerFeature('Feature1E01WithGothardCounter', function, featureHelp='Help for Gothard Counter support')
# Manage Deactivatable Features based on authentication
function = lambda context: (check_feature(context,
                                          'PRODUCT/FEATURES/COMMON/MANAGE_DEACTIVATABLE_FEATURES_AUTH',
                                          'F_Enabled'))
features.registerFeature('ManageDeactivatableFeaturesAuth', function,
                         featureHelp='Help for Manage Deactivatable Features based on authentication tests')
function = lambda context: (check_feature(context,
                                          'PRODUCT/FEATURES/COMMON/MANAGE_DEACTIVATABLE_FEATURES_AUTH',
                                          'F_SupportManufacturing'))
features.registerFeature('ManageDeactivatableFeaturesSupportManufacturing', function,
                         featureHelp='Help for Manage Deactivatable Features Manufacturing session')
function = lambda context: (check_feature(context,
                                          'PRODUCT/FEATURES/COMMON/MANAGE_DEACTIVATABLE_FEATURES_AUTH',
                                          'F_SupportCompliance'))
features.registerFeature('ManageDeactivatableFeaturesSupportCompliance', function,
                         featureHelp='Help for Manage Deactivatable Features Compliance session')
function = lambda context: (check_feature(context,
                                          'PRODUCT/FEATURES/COMMON/MANAGE_DEACTIVATABLE_FEATURES_AUTH',
                                          'F_SupportGotthard'))
features.registerFeature('ManageDeactivatableFeaturesSupportGotthard', function,
                         featureHelp='Help for Manage Deactivatable Features Gotthard session')
# SPI Direct Access Features
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/SPI_DIRECT_ACCESS', 'F_Enabled'))
features.registerFeature('Feature1E22', function, featureHelp='Help for SPI Direct Access')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/SPI_DIRECT_ACCESS', 'F_Enabled') and
                            get_attribute(context,
                                          'PRODUCT/FEATURES/COMMON/SPI_DIRECT_ACCESS', 'F_NumberOfDevices') > 0)
features.registerFeature('Feature1E22WithSpiPeripheral', function, featureHelp='Help for number of SPI peripheral')
function = lambda context, names: (get_attribute(context, 'PRODUCT/FEATURES/MOUSE', 'F_OpticalSensorName') in names)
features.registerFeature('RequiredOpticalSensors', function,
                         featureHelp='Help for checking the support of optical sensors')
# I2C Direct Access Features
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/I2C_DIRECT_ACCESS', 'F_Enabled'))
features.registerFeature('Feature1E30', function, featureHelp='Help for I2C Direct Access')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/I2C_DIRECT_ACCESS', 'F_Enabled') and
                            get_attribute(context,
                                          'PRODUCT/FEATURES/COMMON/I2C_DIRECT_ACCESS', 'F_NumberOfDevices') > 0)
features.registerFeature('Feature1E30WithI2cPeripheral', function, featureHelp='Help for number of I2C peripheral')
# TdeAccessToNvm Features
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/TDE_ACCESS_TO_NVM', 'F_Enabled'))
features.registerFeature('Feature1EB0', function, featureHelp='Help for TDE access to non-volatile memory')
# TemperatureMeasurement Features
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/TEMPERATURE_MEASUREMENT', 'F_Enabled'))
features.registerFeature('Feature1F30', function, featureHelp='Help for Temperature Measurement')
# DFU Control Features
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU_CONTROL', 'F_Enabled'))
features.registerFeature('DfuControl', function, featureHelp='Help for DFU Control tests')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU_CONTROL', 'F_Enabled') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU_CONTROL', 'F_NotAvailable'))
features.registerFeature('DfuControlDfuAvailable', function, featureHelp='Help for DFU Control tests on device with ' +
                                                                         'DFU available')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU_CONTROL', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU_CONTROL', 'F_NotAvailable'))
features.registerFeature('DfuControlDfuNotAvailable', function, featureHelp='Help for DFU Control tests on device ' +
                                                                            'with DFU not available')
# Secure DFU Control Features
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL', 'F_Enabled') and
                            get_attribute(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL',
                                          'F_DfuControlActionType') != 0)
features.registerFeature('SecureDfuControlActionTypeNot0', function, featureHelp='Help for Secure DFU Control tests but not for '
                                                                   'action type = 0')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL', 'F_Enabled') and
                            get_attribute(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL',
                                          'F_DfuControlActionType') not in [0, 4])
features.registerFeature('SecureDfuControlUseNVS', function, featureHelp='Help for Secure DFU Control tests using NVS')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL', 'F_Enabled') and
                            get_attribute(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL',
                                          'F_DfuControlActionType') == 4)
features.registerFeature('SecureDfuControlActionType4', function, featureHelp='Help for Secure DFU Control tests with '
                                                                   'action type = 4')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL', 'F_Enabled'))
features.registerFeature('SecureDfuControlAllActionTypes', function, featureHelp='Help for Secure DFU Control tests '
                                                                                 'for all action types (including 0)')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL', 'F_Enabled') and
                            get_attribute(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL',
                                          'F_DfuControlActionType') == 0)
features.registerFeature('SecureDfuControlActionType0', function, featureHelp='Help for Secure DFU Control tests '
                                                                              'only for action type = 0')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL', 'F_Enabled') and
                            get_attribute(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL',
                                          'F_DfuControlActionType') > 1 and
                            get_non_0_byte_number_in_list(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL',
                                                          'F_DfuControlActionData') >= 1
                            )
features.registerFeature('SecureDfuControlAtLeast1ActionData', function,
                         featureHelp='Help for Secure DFU Control tests that has at least 1 action data != 0, '
                                     'but not for action type = 0')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL', 'F_Enabled') and
                            get_attribute(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL',
                                          'F_DfuControlActionType') > 1 and
                            get_non_0_byte_number_in_list(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL',
                                                          'F_DfuControlActionData') >= 2
                            )
features.registerFeature('SecureDfuControlAtLeast2ActionData', function,
                         featureHelp='Help for Secure DFU Control tests that has at least 2 action data != 0, '
                                     'but not for action type = 0')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL', 'F_Enabled') and
                            get_attribute(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL',
                                          'F_DfuControlActionType') > 1 and
                            get_non_0_byte_number_in_list(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL',
                                                          'F_DfuControlActionData') >= 3
                            )
features.registerFeature('SecureDfuControlAtLeast3ActionData', function,
                         featureHelp='Help for Secure DFU Control tests that has at least 3 action data != 0, '
                                     'but not for action type = 0')
function = lambda context, action_type: (
        check_feature(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL', 'F_Enabled') and
        action_type in [int(x) for x in get_attribute(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL',
                                                      'F_ReloadActionTypes') if x != ''])
features.registerFeature('SecureDfuControlReloadActionType', function,
                         featureHelp='Help for Secure DFU Control tests for reloading a specific action type')
function = lambda context: (
        check_feature(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL', 'F_Enabled') and
        len([int(x) for x in get_attribute(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL',
                                           'F_ReloadActionTypes') if x != '']) > 0)
features.registerFeature('SecureDfuControlAnyReloadActionType', function,
                         featureHelp='Help for Secure DFU Control tests for reloading any action type')
function = lambda context: (
        check_feature(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL', 'F_Enabled') and
        check_feature(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL', 'F_OtherActionType'))
features.registerFeature('SecureDfuControlOtherActionType', function,
                         featureHelp='Help for Secure DFU Control tests for other action type support')
function = lambda context: (
        check_feature(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL', 'F_Enabled') and
        check_feature(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL', 'F_ChangeActionTypeByDFU'))
features.registerFeature('SecureDfuControlChangeActionTypeByDFU', function,
                         featureHelp='Help for Secure DFU Control tests for change action type by DFU support')

function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU_CONTROL', 'F_Enabled')
                            or check_feature(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL', 'F_Enabled'))
features.registerFeature('BootloaderAvailable', function, featureHelp='Help for Bootloader available')

# DFU Features
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_Enabled'))
features.registerFeature('Feature00D0', function, featureHelp='Help for DFU tests')
function = lambda context, max_size: (
                                len(get_attribute(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_MagicString')) <= max_size)
features.registerFeature('Feature00D0MagicStrMaxSize', function, featureHelp='Help for DFU tests with maximum magic '
                                                                             'string size')
function = lambda context, max_program_quantum: (
        get_attribute(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_QuantumProgram') <= max_program_quantum)
features.registerFeature('Feature00D0MaxProgramQuantum', function,
                         featureHelp='Help for DFU tests with maximum program quantum')
function = lambda context, min_program_quantum: (
                    get_attribute(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_QuantumProgram') >= min_program_quantum)
features.registerFeature('Feature00D0MinProgramQuantum', function,
                         featureHelp='Help for DFU tests with maximum program quantum')
function = lambda context, min_check_quantum: (
        get_attribute(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_QuantumCheck') >= min_check_quantum)
features.registerFeature('Feature00D0MinCheckQuantum', function,
                         featureHelp='Help for DFU tests with maximum check quantum')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_Enabled') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_Version_0'))
features.registerFeature('Feature00D0V1+', function, featureHelp='Help for DFU tests version 1 and later')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_Enabled') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_Version_0') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_Version_1'))
features.registerFeature('Feature00D0V2+', function, featureHelp='Help for DFU tests version 2 and later')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_FlashWriteVerify'))
features.registerFeature('Feature00D0FlashWriteVerify', function, featureHelp='Help for DFU tests')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_VerifyFlag'))
features.registerFeature('Feature00D0VerifyFlag', function, featureHelp='Help for DFU tests')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_VerifyCmd3DoneAfterCmd1And2'))
features.registerFeature('Feature00D0VerifyCmd3DoneAfterCmd1And2', function, featureHelp='Help for DFU tests')
function = lambda context, encrypt_value: (
        check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_Enabled') and
        encrypt_value in [int(x) for x in get_attribute(
                                            context,'PRODUCT/FEATURES/COMMON/DFU', 'F_EncryptCapabilities') if x != ''])
features.registerFeature('Feature00D0EncryptCapabilities', function, featureHelp='Help for DFU tests')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_Enabled') and
                            len(get_attribute(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_SoftDeviceDfuFileName')) > 0)
features.registerFeature('Feature00D0SoftDevice', function, featureHelp='Help for SoftDevice DFU tests')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_DfuInPlace'))
features.registerFeature('Feature00D0DfuInPlace', function, featureHelp='Help for SoftDevice DFU In Place tests')
# DFU compatibility with previous versions
function = lambda context, index=0: (
        check_feature(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_Enabled') and
        len(get_attribute(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_CompatibleTags')) > index and
        len(get_attribute(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_CompatibleTags')[index]) > 0)
features.registerFeature('Feature00D0Tags', function, featureHelp='Help for DFU compatibility tests')
# Lexend Image DFU
function = lambda context: (len(get_attribute(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_ImagesDfuFileName')) > 0)
features.registerFeature('ImageDFU', function, featureHelp='Help for Image DFU tests')
# DFU signature algorithm
function = lambda context, algo: (get_attribute(context, 'PRODUCT/FEATURES/COMMON/DFU', 'F_SignatureAlgorithm') == algo)
features.registerFeature('DFUSignatureAlgorithm', function, featureHelp='Help for DFU signature algorithm')
# Wireless Device Status
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/WIRELESS_DEVICE_STATUS', 'F_Enabled'))
features.registerFeature('Feature1D4B', function, featureHelp='Help for Wireless Device Status Features tests')
# 32 Bytes Unique Identifier
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIQUE_IDENTIFIER_32_BYTES', 'F_Enabled'))
features.registerFeature('Feature0021', function, featureHelp='Help for 32 Bytes Unique Identifier Features tests')
# Unified Battery
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Enabled'))
features.registerFeature('Feature1004', function, featureHelp='Help for Unified Battery Features tests')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Enabled') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Version_0'))
features.registerFeature('Feature1004v1+', function, featureHelp='Help for Unified Battery Features tests')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Enabled') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Version_0') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Version_1') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Version_2'))
features.registerFeature('Feature1004v3+', function, featureHelp='Help for Unified Battery Features tests')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Enabled') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Version_0') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Version_1') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Version_2') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Version_3'))
features.registerFeature('Feature1004v4+', function, featureHelp='Help for Unified Battery Features tests')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Enabled') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Version_0') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Version_1') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Version_2') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Version_3') and
                            not check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Version_4'))
features.registerFeature('Feature1004v5+', function, featureHelp='Help for Unified Battery Features tests')
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Enabled') and
    check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_EnableChargingTests') and
    int(get_attribute(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_CapabilitiesFlags')[0])
    if len(get_attribute(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_CapabilitiesFlags')) > 0 else 0)
features.registerFeature('Rechargeable', function,
                         featureHelp='Help for Unified Battery RechargeableBatteryStatus tests')
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Enabled') and
    int(get_attribute(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_CapabilitiesFlags')[2])
    if len(get_attribute(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_CapabilitiesFlags')) > 2 else 0)
features.registerFeature('Feature1004ShowBatteryStatusCapability', function,
                         featureHelp='Help for Unified Battery ShowBatteryStatus tests')
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Enabled') and
    int(get_attribute(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_CapabilitiesFlags')[3])
    if len(get_attribute(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_CapabilitiesFlags')) > 3 else 0)
features.registerFeature('Feature1004BatteryMultiSourcing', function,
                         featureHelp='Help for Unified Battery Multi Sourcing tests')
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Enabled') and
    int(get_attribute(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_CapabilitiesFlags')[4])
    if len(get_attribute(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_CapabilitiesFlags')) > 4 else 0)
features.registerFeature('Feature1004FastCharging', function,
                         featureHelp='Help for Unified Battery FastCharging tests')
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_Enabled') and
    int(get_attribute(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_CapabilitiesFlags')[5])
    if len(get_attribute(context, 'PRODUCT/FEATURES/COMMON/UNIFIED_BATTERY', 'F_CapabilitiesFlags')) > 5 else 0)
features.registerFeature('Feature1004RemovableBattery', function,
                         featureHelp='Help for Unified Removable Battery tests')

# Mouse Features
# -----------------
# VerticalScrolling
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/VERTICAL_SCROLLING', 'F_Enabled'))
features.registerFeature('Feature2100', function, featureHelp='Help for Feature 2100')
# SmartShift
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/SMART_SHIFT', 'F_Enabled'))
features.registerFeature('Feature2110', function, featureHelp='Help for Feature 2110')
# SmartShift Tunable
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/SMART_SHIFT_TUNABLE', 'F_Enabled'))
features.registerFeature('Feature2111', function, featureHelp='Help for Feature 2111')
# Ratchet Wheel
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/RATCHET_WHEEL', 'F_Enabled'))
features.registerFeature('Feature2130', function, featureHelp='Help for Feature 2130')
# Thumbwheel
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/THUMBWHEEL', 'F_Enabled'))
features.registerFeature('Feature2150', function, featureHelp='Help for Feature 2150')
# Adjustable DPI
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/ADJUSTABLE_DPI', 'F_Enabled'))
features.registerFeature('Feature2201', function, featureHelp='Help for Feature 2201')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/ADJUSTABLE_DPI', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/FEATURES/MOUSE/ADJUSTABLE_DPI', 'F_Version_2'))
features.registerFeature('Feature2201v2+', function, featureHelp='Help for Feature 2201')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/ADJUSTABLE_DPI', 'F_MaxSupportedDpiLevels'))
features.registerFeature('SupportDPILevels', function, featureHelp='Help for max supported DPI levels')
function = lambda context: (
                    not is_an_empty_tuple(context, 'PRODUCT/FEATURES/MOUSE/ADJUSTABLE_DPI', 'F_PredefinedDpiValueList'))
features.registerFeature('PredefinedDPI', function, featureHelp='Help for Predefined DPI')
# ExtendedAdjustableDPI
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/EXTENDED_ADJUSTABLE_DPI', 'F_Enabled'))
features.registerFeature('Feature2202', function, featureHelp='Help for ExtendedAdjustableDPI')
function = lambda context: (check_feature(
    context, 'PRODUCT/FEATURES/MOUSE/EXTENDED_ADJUSTABLE_DPI', 'F_ProfileSupported'))
features.registerFeature('ProfileSupported', function, featureHelp='Help for ExtendedAdjustableDPI')
function = lambda context: (check_feature(
    context, 'PRODUCT/FEATURES/MOUSE/EXTENDED_ADJUSTABLE_DPI', 'F_CalibrationSupported'))
features.registerFeature('DpiCalibrationSupported', function, featureHelp='Help for ExtendedAdjustableDPI')
function = lambda context: (is_dpi_range_supported(context))
features.registerFeature('ReportDpiByRanges', function, featureHelp='Help for 0x2202 report DPI ranges')
# AnalysisMode
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/ANALYSIS_MODE', 'F_Enabled'))
features.registerFeature('Feature2250', function, featureHelp='Help for Feature 2250')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/ANALYSIS_MODE', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/FEATURES/MOUSE/ANALYSIS_MODE', 'F_Version_1'))
features.registerFeature('Feature2250v1', function, featureHelp='Help for Feature 2250')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/ANALYSIS_MODE', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/FEATURES/MOUSE/ANALYSIS_MODE', 'F_OverflowCapability') and
                            check_feature(context, 'PRODUCT/FEATURES/MOUSE/ANALYSIS_MODE', 'F_Version_1'))
features.registerFeature('SaturatedData', function,
                         featureHelp='Help for wrap around / saturated data capability in AnalysisMode v1')
# Mouse Wheel Analytics
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/MOUSE_WHEEL_ANALYTICS', 'F_Enabled'))
features.registerFeature('Feature2251', function, featureHelp='Help for Mouse Wheel Analytics')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/MOUSE_WHEEL_ANALYTICS',
                                          'F_SmartShiftCapability'))
features.registerFeature('SmartShiftCapability', function, featureHelp='Help for Mouse Wheel Analytics Smart Shift '
                                                                       'capability')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/MOUSE_WHEEL_ANALYTICS',
                                          'F_ThumbwheelCapability'))
features.registerFeature('ThumbwheelCapability', function, featureHelp='Help for Mouse Wheel Analytics Thumbwheel '
                                                                       'capability')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/MOUSE_WHEEL_ANALYTICS',
                                          'F_RatchetFreeCapability'))
features.registerFeature('RatchetFreeCapability', function, featureHelp='Help for Mouse Wheel Analytics Ratchet Free '
                                                                       'capability')
function = lambda context: (check_feature(
    context, 'PRODUCT/FEATURES/MOUSE/MOUSE_WHEEL_ANALYTICS', 'F_RatchetFreeCapability') or
    check_feature(context, 'PRODUCT/FEATURES/MOUSE/MOUSE_WHEEL_ANALYTICS', 'F_SmartShiftCapability'))
features.registerFeature('SupportWheelModes', function, featureHelp='Help for Mouse Wheel Analytics Wheel modes '
                                                                       'support')
# HiRes Wheel
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/HI_RES_WHEEL', 'F_Enabled'))
features.registerFeature('Feature2121', function, featureHelp='Help for Feature 2121')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/HI_RES_WHEEL', 'F_Version_0'))
features.registerFeature('Feature2121v0', function, featureHelp='Help for Feature 2121 v0')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/MOUSE/HI_RES_WHEEL', 'F_Enabled') and
                            not check_feature(context, 'PRODUCT/FEATURES/MOUSE/HI_RES_WHEEL', 'F_Version_0'))
features.registerFeature('Feature2121v1+', function, featureHelp='Help for Feature 2121 v1 and higher')
# Motion latency
function = lambda context: (check_feature(context, 'PRODUCT/LATENCY/MOTION_LATENCY', 'F_Enabled'))
features.registerFeature('MotionLatency', function, featureHelp='Help for Motion Latency')

# Touchpad Features
# -----------------
# Touchpad Raw XY
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/TOUCHPAD/TOUCHPAD_RAW_XY', 'F_Enabled'))
features.registerFeature('Feature6100', function, featureHelp='Help for Touchpad Raw XY tests')

# Gaming Features
# -----------------
# Gaming G-Keys
function = lambda context: False
features.registerFeature('Feature8010', function, featureHelp='Help for Gaming G-Keys')
# Gaming M-Keys
function = lambda context: False
features.registerFeature('Feature8020', function, featureHelp='Help for Gaming M-Keys')
# MacroRecord key
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/GAMING/MACRORECORD_KEY', 'F_Enabled'))
features.registerFeature('Feature8030', function, featureHelp='Help for MacroRecord key')
# Brightness Control
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/GAMING/BRIGHTNESS_CONTROL', 'F_Enabled'))
features.registerFeature('Feature8040', function, featureHelp='Help for Brightness Control')
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/GAMING/BRIGHTNESS_CONTROL', 'F_Enabled') and
    check_feature(context, 'PRODUCT/FEATURES/GAMING/BRIGHTNESS_CONTROL', 'F_Version_0'))
features.registerFeature('Feature8040v0', function, featureHelp='Help for Brightness Control v0')
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/GAMING/BRIGHTNESS_CONTROL', 'F_Enabled') and
    check_feature(context, 'PRODUCT/FEATURES/GAMING/BRIGHTNESS_CONTROL', 'F_Version_1'))
features.registerFeature('Feature8040v1', function, featureHelp='Help for Brightness Control v1')
function = lambda context, capability_index: (is_brightness_capability_supported(context, capability_index))
features.registerFeature('RequiredBrightnessCapability', function, featureHelp='Help for Brightness Control Capability')
# Logi Modifiers
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/GAMING/LOGI_MODIFIERS', 'F_Enabled'))
features.registerFeature('Feature8051', function, featureHelp='Help for Logi Modifiers')

function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/LOGI_MODIFIERS', 'F_FM_Fn'))
features.registerFeature('Feature8051FnForceable', function,
                         featureHelp='Help for Fn state forced by SW capability')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/LOGI_MODIFIERS', 'F_FM_GShift'))
features.registerFeature('Feature8051GShiftForceable', function,
                         featureHelp='Help for GShift state forced by SW capability')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/LOGI_MODIFIERS', 'F_GM_Fn'))
features.registerFeature('Feature8051FnGettable', function,
                         featureHelp='Help for Fn state gettable by SW capability')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/LOGI_MODIFIERS', 'F_GM_GShift'))
features.registerFeature('Feature8051GShiftGettable', function,
                         featureHelp='Help for GShift state gettable by SW capability')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/LOGI_MODIFIERS', 'F_GM_LeftCtrl'))
features.registerFeature('Feature8051LeftCtrlGettable', function,
                         featureHelp='Help for LeftCtrl state gettable by SW capability')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/LOGI_MODIFIERS', 'F_GM_LeftShift'))
features.registerFeature('Feature8051LeftShiftGettable', function,
                         featureHelp='Help for LeftShift state gettable by SW capability')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/LOGI_MODIFIERS', 'F_GM_LeftAlt'))
features.registerFeature('Feature8051LeftAltGettable', function,
                         featureHelp='Help for LeftAlt state gettable by SW capability')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/LOGI_MODIFIERS', 'F_GM_LeftGui'))
features.registerFeature('Feature8051LeftGuiGettable', function,
                         featureHelp='Help for LeftGui state gettable by SW capability')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/LOGI_MODIFIERS', 'F_GM_RightCtrl'))
features.registerFeature('Feature8051RightCtrlGettable', function,
                         featureHelp='Help for RightCtrl state gettable by SW capability')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/LOGI_MODIFIERS', 'F_GM_RightShift'))
features.registerFeature('Feature8051RightShiftGettable', function,
                         featureHelp='Help for RightShift state gettable by SW capability')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/LOGI_MODIFIERS', 'F_GM_RightAlt'))
features.registerFeature('Feature8051RightAltGettable', function,
                         featureHelp='Help for RightAlt state gettable by SW capability')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/LOGI_MODIFIERS', 'F_GM_RightGui'))
features.registerFeature('Feature8051RightGuiGettable', function,
                         featureHelp='Help for RightGui state gettable by SW capability')
# ReportRate
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/REPORT_RATE', 'F_Enabled'))
features.registerFeature('Feature8060', function, featureHelp='Help for ReportRate')
# AdjustableReportRate
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/EXTENDED_ADJUSTABLE_REPORT_RATE',
                                          'F_Enabled'))
features.registerFeature('Feature8061', function, featureHelp='Help for AdjustableReportRate')
function = lambda context, connection_type, report_rate: (is_report_rate_supported(context, connection_type, report_rate))
features.registerFeature('Feature8061SupportedReportRate', function, featureHelp='Help for checking if report rate is '
                                                                                 'supported for the connectionType')
# RgbEffect
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/RGB_EFFECTS', 'F_Enabled'))
features.registerFeature('Feature8071', function, featureHelp='Help for RgbEffect')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/RGB_EFFECTS', 'F_Enabled') and
                            not check_feature(context, 'PRODUCT/FEATURES/GAMING/RGB_EFFECTS', 'F_Version_0') and
                            not check_feature(context, 'PRODUCT/FEATURES/GAMING/RGB_EFFECTS', 'F_Version_1') and
                            not check_feature(context, 'PRODUCT/FEATURES/GAMING/RGB_EFFECTS', 'F_Version_2') and
                            not check_feature(context, 'PRODUCT/FEATURES/GAMING/RGB_EFFECTS', 'F_Version_3'))
features.registerFeature('Feature8071v4+', function, featureHelp='Help for rgb effect v4 and higher')
function = lambda context, cluster_index, effect_id: (is_rgb_effect_supported(context, cluster_index, effect_id))
features.registerFeature('Feature8071RequiredEffect', function, featureHelp='Help for RgbEffect support on cluster')
function = lambda context, nv_capability: (is_rgb_nv_capability_supported(context, nv_capability))
features.registerFeature('Feature8071RequiredNvCapability', function, featureHelp='Help for RgbEffect Non Volatile '
                                                                                  'capability')
function = lambda context: (check_rgb_configuration(context))
features.registerFeature('HasRGBConfiguration', function, featureHelp='Help for RGB configuration')
function = lambda context: (is_persistence_supported(context))
features.registerFeature('PersistenceSupport', function, featureHelp='Help for checking if persistance is supported '
                                                                     'for atleast one cluster index')
# PerKeyLighting
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/PER_KEY_LIGHTING', 'F_Enabled'))
features.registerFeature('Feature8081', function, featureHelp='Help for PerKeyLighting')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/PER_KEY_LIGHTING', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/FEATURES/GAMING/PER_KEY_LIGHTING', 'F_Version_1'))
features.registerFeature('Feature8081v1', function, featureHelp='Help for PerKeyLighting')
# ModeStatus
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/MODE_STATUS', 'F_Enabled'))
features.registerFeature('Feature8090', function, featureHelp='Help for ModeStatus')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/MODE_STATUS', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/FEATURES/GAMING/MODE_STATUS', 'F_ModeStatus0ChangedByHw'))
features.registerFeature('Feature8090HwSwitch', function, featureHelp='Help for ModeStatus HwSwitch presence')
function = lambda context, power_mode: (is_hybrid_switch_power_mode_supported(context, power_mode))
features.registerFeature('Feature8090HybridSwitchMode', function, featureHelp='Help for ModeStatus Hybrid switch power mode presence')
# AxisResponseCurve
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/AXIS_RESPONSE_CURVE', 'F_Enabled'))
features.registerFeature('Feature80A4', function, featureHelp='Help for AxisResponseCurve')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/AXIS_RESPONSE_CURVE', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/FEATURES/GAMING/AXIS_RESPONSE_CURVE', 'F_Version_0'))
features.registerFeature('Feature80A4v0', function, featureHelp='Help for AxisResponseCurve')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/AXIS_RESPONSE_CURVE', 'F_Enabled') and
                            not check_feature(context, 'PRODUCT/FEATURES/GAMING/AXIS_RESPONSE_CURVE', 'F_Version_0'))
features.registerFeature('Feature80A4v1+', function, featureHelp='Help for AxisResponseCurve')
# CombinedPedals
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/COMBINED_PEDALS', 'F_Enabled'))
features.registerFeature('Feature80D0', function, featureHelp='Help for CombinedPedals')
# OnboardProfiles
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/ONBOARD_PROFILES', 'F_Enabled'))
features.registerFeature('Feature8100', function, featureHelp='Help for OnboardProfiles')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/ONBOARD_PROFILES', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/FEATURES/GAMING/ONBOARD_PROFILES', 'F_Version_1'))
features.registerFeature('Feature8100v1', function, featureHelp='Help for OnboardProfiles')
function = lambda context: (get_attribute(context, 'PRODUCT/FEATURES/GAMING/ONBOARD_PROFILES', 'F_ProfileFormatID') > 1)
features.registerFeature('ProfileFormatV2+', function, featureHelp='Help for ProfileFormat')
function = lambda context: (get_attribute(context, 'PRODUCT/FEATURES/GAMING/ONBOARD_PROFILES', 'F_ProfileFormatID') > 3)
features.registerFeature('ProfileFormatV4+', function, featureHelp='Help for ProfileFormat')
function = lambda context: (get_attribute(context, 'PRODUCT/FEATURES/GAMING/ONBOARD_PROFILES', 'F_ProfileFormatID')
                            <= 5)
features.registerFeature('ProfileFormatV1ToV5', function, featureHelp='Help for ProfileFormat')
function = lambda context: \
    (get_attribute(context, 'PRODUCT/FEATURES/GAMING/ONBOARD_PROFILES', 'F_ProfileFormatID') == 6)
features.registerFeature('ProfileFormatV6', function, featureHelp='Help for ProfileFormat')
function = lambda context: (get_attribute(context, 'PRODUCT/FEATURES/GAMING/ONBOARD_PROFILES', 'F_ProfileCount') > 1)
features.registerFeature('PluralProfiles', function, featureHelp='Help for ProfileFormat')
# ProfileManagement
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/PROFILE_MANAGEMENT', 'F_Enabled'))
features.registerFeature('Feature8101', function, featureHelp='Help for ProfileManagement')
function = lambda context: (get_attribute(
    context, 'PRODUCT/FEATURES/GAMING/PROFILE_MANAGEMENT', 'F_NumOnboardProfiles') > 1)
features.registerFeature('Feature8101MultipleProfiles', function, featureHelp='Help for Multiple Onboard Profiles')
function = lambda context: (get_attribute(
    context, 'PRODUCT/FEATURES/GAMING/PROFILE_MANAGEMENT', 'F_FlashEraseCounter') not in [0xFFFFFF, None])
features.registerFeature('Feature8101FlashEraseCounter', function, featureHelp='Help for FlashEraseCounter')
# MouseButtonSpy
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/MOUSE_BUTTON_SPY', 'F_Enabled'))
features.registerFeature('Feature8110', function, featureHelp='Help for MouseButtonSpy')
# BrakeForce
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/BRAKE_FORCE', 'F_Enabled'))
features.registerFeature('Feature8134', function, featureHelp='Help for BrakeForce')
# PedalStatus
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/GAMING/PEDAL_STATUS', 'F_Enabled'))
features.registerFeature('Feature8135', function, featureHelp='Help for PedalStatus')
# Peripheral Features
# -----------------
# PMW3819_and_PMW3826
function = lambda context: (
                    check_feature(context, 'PRODUCT/FEATURES/PERIPHERAL/PMW3816_AND_PMW3826', 'F_Enabled'))
features.registerFeature('Feature9001', function, featureHelp='Help for PMW3816 and PMW3826')
function = lambda context: (
                    check_feature(context, 'PRODUCT/FEATURES/PERIPHERAL/PMW3816_AND_PMW3826', 'F_Enabled') and
                    check_feature(context, 'PRODUCT/FEATURES/PERIPHERAL/PMW3816_AND_PMW3826', 'F_Version_0'))
features.registerFeature('Feature9001v0', function, featureHelp='Help for PMW3816 and PMW3826')
function = lambda context: (
                    check_feature(context, 'PRODUCT/FEATURES/PERIPHERAL/PMW3816_AND_PMW3826', 'F_Enabled') and
                    check_feature(context, 'PRODUCT/FEATURES/PERIPHERAL/PMW3816_AND_PMW3826', 'F_Version_1'))
features.registerFeature('Feature9001v1', function, featureHelp='Help for PMW3816 and PMW3826')
# IQS624
function = lambda context: False
features.registerFeature('Feature9203', function, featureHelp='Help for IQS624')
# MLX903xx
function = lambda context: (
                    check_feature(context, 'PRODUCT/FEATURES/PERIPHERAL/MLX903XX', 'F_Enabled'))
features.registerFeature('Feature9205', function, featureHelp='Help for MLX903xx')
# MLX_90393_MULTI_SENSOR
function = lambda context: (
                    check_feature(context, 'PRODUCT/FEATURES/PERIPHERAL/MLX_90393_MULTI_SENSOR', 'F_Enabled'))
features.registerFeature('Feature9209', function, featureHelp='Help for MLX 90393 Multi Sensor')
# Ads1231
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/PERIPHERAL/ADS_1231', 'F_Enabled'))
features.registerFeature('Feature9215', function, featureHelp='Help for Ads1231')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/PERIPHERAL/ADS_1231', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/FEATURES/PERIPHERAL/ADS_1231',
                                          'F_Support_Manage_Dynamic_Calibration_Parameters'))
features.registerFeature('Feature9215WithManDynCal', function, featureHelp='Help for Ads1231')
# Test Keys Display
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/PERIPHERAL/TEST_KEYS_DISPLAY', 'F_Enabled'))
features.registerFeature('Feature92E2', function, featureHelp='Help for Test Keys Display')
# set key icon api may not be supported in future versions
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/PERIPHERAL/TEST_KEYS_DISPLAY', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/FEATURES/PERIPHERAL/TEST_KEYS_DISPLAY', 'F_Version_0'))
features.registerFeature('SupportSetKeyIcon', function, featureHelp='Help for Support Set Key Icon Api')
# Mouse Features
# -----------------
# Keyboard Features
# -----------------
# Double press PP/NT support
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/KEYBOARD', 'F_PlayPauseDoublePress'))
features.registerFeature('PlayPauseDoublePress', function, featureHelp='Help for Keyboard Double press PP/NT')
# Switch latency
function = lambda context: (check_feature(context, 'PRODUCT/LATENCY/SWITCH_LATENCY', 'F_Enabled'))
features.registerFeature('SwitchLatency', function, featureHelp='Help for Switch Latency')
# Fn Inversion for multi-host devices
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/FN_INVERSION_FOR_MULTI_HOST_DEVICES',
                                          'F_Enabled'))
features.registerFeature('Feature40A3', function, featureHelp='Help for Keyboard fn inversion')
# Lock Key State
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/LOCK_KEY_STATE', 'F_Enabled'))
features.registerFeature('Feature4220', function, featureHelp='Help for Keyboard Lock Key State')
# disable keys
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/DISABLE_KEYS', 'F_Enabled'))
features.registerFeature('Feature4521', function, featureHelp='Help for disable keys')
function = lambda context: (not check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/DISABLE_KEYS', 'F_CapsLock') or
                            not check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/DISABLE_KEYS', 'F_NumLock') or
                            not check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/DISABLE_KEYS', 'F_ScrollLock') or
                            not check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/DISABLE_KEYS', 'F_Insert') or
                            not check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/DISABLE_KEYS', 'F_Windows'))
features.registerFeature('Feature4521UnsupportedKeys', function, featureHelp='Help for disabling unsupported keys')
# disable keys by usage
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/DISABLE_KEYS_BY_USAGE', 'F_Enabled'))
features.registerFeature('Feature4522', function, featureHelp='Help for disable keys by usage')
# Disable Controls By CIDX
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/DISABLE_CONTROLS_BY_CIDX', 'F_Enabled'))
features.registerFeature('Feature4523', function, featureHelp='Help for Disable Controls By CIDX')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/DISABLE_CONTROLS_BY_CIDX', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/DISABLE_CONTROLS_BY_CIDX', 'F_Version_1'))
features.registerFeature('Feature4523v1', function, featureHelp='Help for Disable Controls by CIDX v1')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/DISABLE_CONTROLS_BY_CIDX', 'F_GameModeSupported'))
features.registerFeature('Feature4523GameModeSupported', function, featureHelp='Help for Disable Controls By CIDX')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/DISABLE_CONTROLS_BY_CIDX', 'F_GameModeLockSupported'))
features.registerFeature('Feature4523GameModeLockSupported', function, featureHelp='Help for Disable Controls By CIDX')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/DISABLE_CONTROLS_BY_CIDX', 'F_PowerOnGameModeSupported'))
features.registerFeature('Feature4523PowerOnGameModeSupported', function, featureHelp='Help for Disable Controls By CIDX')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/DISABLE_CONTROLS_BY_CIDX', 'F_PowerOnGameModeLockSupported'))
features.registerFeature('Feature4523PowerOnGameModeLockSupported', function, featureHelp='Help for Disable Controls By CIDX')
# Multi platform
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/MULTI_PLATFORM', 'F_Enabled'))
features.registerFeature('Feature4531', function, featureHelp='Help for multi platform')
# Multi platform - Set Host Platform
function = lambda context: (
        get_attribute(context, 'PRODUCT/FEATURES/KEYBOARD/MULTI_PLATFORM', 'F_SetHostPlatform') == 1)
features.registerFeature('SetHostPlatform', function, featureHelp='Help for set host platform')
# Keyboard international layouts
function = lambda context: (
                    check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/KEYBOARD_INTERNATIONAL_LAYOUTS', 'F_Enabled'))
features.registerFeature('Feature4540', function, featureHelp='Help for Keyboard international layouts')
# Multi Roller
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/KEYBOARD/MULTI_ROLLER', 'F_Enabled'))
features.registerFeature('Feature4610', function, featureHelp='Help for Multi Roller')

# -----------------
# VLP Features
# -----------------
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/VLP', 'F_Enabled'))
features.registerFeature('VLP', function, featureHelp='Help for VLP Protocol')
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/VLP', 'F_Extended'))
features.registerFeature('VLPExtended', function, featureHelp='Help for VLP Extended support')
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/VLP', 'F_MultiPacket'))
features.registerFeature('MultiPacket', function, featureHelp='Help for VLP Protocol Multi Packet')
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/VLP', 'F_MultiPacketMultiReportTypes'))
features.registerFeature(
    'MultiPacketMultiReportTypes', function,
    featureHelp='Help for VLP Protocol Multi Packet if multi report types within a transfer is supported')
# -----------------
# Important Features
# -----------------
# VLP Root
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/VLP/IMPORTANT/ROOT', 'F_Enabled'))
features.registerFeature('Feature0102', function, featureHelp='Help for VLP Root')
# VLP Feature Set
function = lambda context: check_feature(context, 'PRODUCT/FEATURES/VLP/IMPORTANT/FEATURE_SET', 'F_Enabled')
features.registerFeature('Feature0103', function, featureHelp='Help for VLP Feature Set')
# -----------------
# Common Features
# -----------------
# Contextual Display
function = lambda context: (
    check_feature(context, 'PRODUCT/FEATURES/VLP/COMMON/CONTEXTUAL_DISPLAY', 'F_Enabled'))
features.registerFeature('Feature19A1', function, featureHelp='Help for Contextual Display')
function = lambda context, capabilities, min_number=1: (
    sum(int(get_attribute(context, 'PRODUCT/FEATURES/VLP/COMMON/CONTEXTUAL_DISPLAY',
                          'F_CapabilitiesFlags')[i]=="1")
        for i in capabilities
    ) >= min_number)
features.registerFeature('Feature19A1Capability', function, featureHelp='Help for Supported Capabilities of 0x19A1')

# -----------------
# Connection scheme
# -----------------
# Connection Scheme Single Host Supported
function = lambda context: (not check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME', 'F_MultipleChannels'))
features.registerFeature('SingleHost', function, featureHelp='Help for Connection scheme Single Host')
# Connection Scheme Multiple Channels (i.e Multiple Host Supported)
function = lambda context, min_host_count=1: (
        check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME', 'F_MultipleChannels') and
        min_host_count <= get_attribute(context, 'PRODUCT/DEVICE', 'F_NbHosts'))
features.registerFeature('MultipleChannels', function, featureHelp='Help for Connection scheme Multiple Channels')
# Connection Scheme Connect Button (i.e Single Button Product)
function = lambda context: (not check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME',
                                              'F_MultipleEasySwitchButtons'))
features.registerFeature('ConnectButton', function, featureHelp='Help for Connection scheme Connect Button')
# Connection Scheme Multiple EasySwitch Buttons (i.e Multiple Button Product)
function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME', 'F_MultipleEasySwitchButtons'))
features.registerFeature('MultipleEasySwitchButtons', function, featureHelp='Help for Connection scheme Multiple '
                                                                            'EasySwitch Buttons')
# BLE Pro Connection scheme
function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/BLE_PRO_CS', 'F_Enabled'))
features.registerFeature('BLEProConnectionScheme', function, featureHelp='Help for BLE Pro Connection scheme')
# SafePrePairedReceiver
function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/BLE_PRO_CS',
                                          'F_SafePrePairedReceiver'))
features.registerFeature('SafePrePairedReceiver', function, featureHelp='Help for Safe Pre-Paired Receiver')
# BLE Service Change Support
function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/BLE_PRO_CS',
                                          'F_BLEServiceChangeSupport'))
features.registerFeature('BLEServiceChangeSupport', function, featureHelp='Help for BLE Service Change Support')

# LS2 Connection scheme
function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/LS2_CS', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/LS2_CS', 'F_LS2_Support'))
features.registerFeature('Ls2ConnectionScheme', function, featureHelp='Help for LS2 Connection scheme')
function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/LS2_CS', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/LS2_CS', 'F_UHS_Support'))
features.registerFeature('UhsConnectionScheme', function, featureHelp='Help for UHS Connection scheme')
function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/LS2_CS', 'F_USB_Cable_Support'))
features.registerFeature('USBCableSupport', function, featureHelp='Help for Connection scheme')

function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/LS2_CS',
                                          'F_DeepSleepCurrentThreshold'))
features.registerFeature('DeepSleepCurrentThreshold', function, featureHelp='Help for Deep Sleep Current Threshold')
function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/LS2_CS',
                                          'F_MaxWaitSleep'))
features.registerFeature('MaxWaitSleep', function, featureHelp='Help for Max Wait Sleep')
function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/LS2_CS', 'F_ThreePairingSlots'))
features.registerFeature('ThreePairingSlots', function, featureHelp='Help for 3-pairing-slots devices')
function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/LS2_CS', 'F_ConnectButton'))
features.registerFeature('LS2Pairing', function, featureHelp='Help for devices with a connect button')
function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/LS2_CS', 'F_ProtocolSwitch'))
features.registerFeature('LS2ProtocolSwitch', function, featureHelp='Help for the protocol switch')
function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/LS2_CS', 'F_WakeUpByConnectButton'))
features.registerFeature('LS2WakeUpByConnectButton', function,
                         featureHelp='Help for the devices which can be woken by the connect button')
function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/LS2_CS', 'F_Enabled') and
                            check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/LS2_CS', 'F_ConnectButton') and
                            check_feature(context, 'PRODUCT/DEVICE/CONNECTION_SCHEME/LS2_CS', 'F_BleSupport'))
features.registerFeature('LS2BleTest', function, featureHelp='Help for LS2 BLE Test')

# --------------------
# EVT Tests
# --------------------
# Typing Test
function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/EVT_AUTOMATION/TYPING_TEST', 'F_Enabled'))
features.registerFeature('EvtTyping', function, featureHelp='Help for EVT Typing Test')

# Battery Notification Test
function = lambda context: (check_feature(
    context, 'PRODUCT/DEVICE/EVT_AUTOMATION/BATTERY_NOTIFICATION_TEST', 'F_Enabled'))
features.registerFeature('EvtBatteryNotification', function, featureHelp='Help for EVT Battery Notification Test')

# --------------------
# Latency Test
# --------------------
function = lambda context: (check_feature(context, 'PRODUCT/LATENCY', 'F_EnableLSXLatencyTestsWithUsbAnalyser'))
features.registerFeature('LSXLatencyTestsWithUsbAnalyser', function, featureHelp='Help LSX Latency Test with USB analyser')
function = lambda context: (check_feature(context, 'PRODUCT/LATENCY', 'F_EnableUSBLatencyTestsWithUsbAnalyser'))
features.registerFeature('USBLatencyTestsWithUsbAnalyser', function, featureHelp='Help USB Latency Test with USB analyser')

# --------------------
# Dual Bank
# --------------------
function = lambda context: (check_feature(context, 'PRODUCT/DUAL_BANK', 'F_Enabled'))
features.registerFeature('DualBank', function, featureHelp='Help for Dual Bank')
function = lambda context: (check_feature(context, 'PRODUCT/DUAL_BANK/ROOT_OF_TRUST_TABLE', 'F_Enabled'))
features.registerFeature('RootOfTrustTable', function, featureHelp='Help for Root Of Trust Table')

# Emulator Validation
# -----------------
function = lambda context: (check_feature(context, 'EMULATOR', 'F_Enabled'))
features.registerFeature('PeripheralEmulation', function, featureHelp='Help for PeripheralEmulation')
# USB charging service
function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/BATTERY', 'F_USBCharging'))
features.registerFeature('USBCharging', function, featureHelp='Help for USB charging service')
# Wireless charging service
function = lambda context: (check_feature(context, 'PRODUCT/DEVICE/BATTERY', 'F_WirelessCharging'))
features.registerFeature('WirelessCharging', function, featureHelp='Help for wireless charging service')

# -----------------
# Tools services
# -----------------
# Multi Host service
function = lambda context: (LibusbDriver.discover_usb_hub() != [])
services.registerFeature('MultiHost', function, featureHelp='Help for Multi Host Management service')
# Charging at slow rate service
function = lambda context: False  # TODO
services.registerFeature('ChargingAtSlowRate', function, featureHelp='Help for charging at slow rate service')
# Charging without connection service
function = lambda context: (not check_feature(context, 'PRODUCT', 'F_IsGaming'))  # TODO
services.registerFeature('ChargingWithoutConnection', function,
                         featureHelp='Help for charging without connection service')
# Key Pressed service
function = lambda context: (Kosmos.discover_emulator(emulation_type=DeviceFamilyName.KBD) or
                            Kosmos.discover_emulator(emulation_type=DeviceName.BAS))
services.registerFeature('ButtonPressed', function, featureHelp='Help for Button Pressed Generator service')
function = lambda context: False
services.registerFeature('ExtensiveButtonPresses', function,
                         featureHelp='Help for Button Pressed Generator service that involves buttons to be press a '
                                     'very large number of times')
# KeyMatrix (Legacy)
function = lambda context: (Kosmos.discover_emulator(emulation_type=DeviceName.KBD_MATRIX) or
                            Kosmos.discover_emulator(emulation_type=DeviceName.KBD_GTECH))
services.registerFeature('KeyMatrix', function, featureHelp='Help for Key Matrix service')
# Dual KeyMatrix (Analog: Gtech + Galvanic: Matrix)
function = lambda context: (Kosmos.discover_emulator(emulation_type=DeviceName.KBD_MATRIX) and
                            Kosmos.discover_emulator(emulation_type=DeviceName.KBD_GTECH))
services.registerFeature('DualKeyMatrix', function, featureHelp='Help for Dual Key Matrix service')
# Single Keystroke
function = lambda context: (Kosmos.discover_emulator(emulation_type=DeviceFamilyName.KBD) or
                            get_attribute(context, 'PRODUCT/DEVICE', 'F_KeyboardType') is not None)
services.registerFeature('SingleKeystroke', function, featureHelp='Help for Single Keystroke service')
# Simultaneous Keystrokes
function = lambda context: (Kosmos.discover_emulator(emulation_type=DeviceName.KBD_MATRIX) or
                            Kosmos.discover_emulator(emulation_type=DeviceName.KBD_GTECH) or
                            get_attribute(context, 'PRODUCT/DEVICE', 'F_KeyboardType') == 'membrane' or
                            get_attribute(context, 'PRODUCT/DEVICE', 'F_KeyboardType') == 'optical_switch_array')
services.registerFeature('SimultaneousKeystrokes', function, featureHelp='Help for Simultaneous Keystrokes service')
# Optical Sensor service
function = lambda context: (Kosmos.discover_emulator(emulation_type=DeviceFamilyName.OPTICAL_SENSOR))
services.registerFeature('OpticalSensor', function, featureHelp='Help for Optical Sensor Emulator service')
function = lambda context: (Kosmos.discover_emulator(emulation_type=DeviceFamilyName.OPTICAL_SENSOR_16BITS))
services.registerFeature('OpticalSensor16bits', function,
                         featureHelp='Help for Optical Sensor Emulator (16-bit resolution) service')
# Touch Module service
function = lambda context: False
services.registerFeature('TouchModule', function, featureHelp='Help for Touch Module Emulator service')
# Main Wheel service
function = lambda context: Kosmos.discover_emulator(emulation_type=DeviceFamilyName.WHEEL_SENSOR)
services.registerFeature('MainWheel', function, featureHelp='Help for Main Wheel Emulator service')
function = lambda context: False
services.registerFeature('MainWheelContinuousMotion', function,
                         featureHelp='Help for Main Wheel Emulator service where main wheel rotations are to be done '
                                     'for a very large number of times')
# Thumbwheel service
function = lambda context: False
services.registerFeature('Thumbwheel', function, featureHelp='Help for Thumbheel Emulator service')
function = lambda context: False
services.registerFeature('ThumbwheelContinuousMotion', function,
                         featureHelp='Help for Thumbheel Emulator service where thumbwheel roatations are to be done '
                                     'for a very large number of times')
# LED Indicator service
function = lambda context: (Kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY))
services.registerFeature('LedIndicator', function, featureHelp='Help for Led Indicator Analyzer service')
# LED spy over I2C monitoring service
function = lambda context: (Kosmos.discover_emulator(emulation_type=DeviceName.I2C_SPY))
services.registerFeature('LedSpyOverI2cMonitoring', function,
                         featureHelp='Help for LED spy over I2C monitoring service')
# Backlight monitoring service
function = lambda context: (Kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY))
services.registerFeature('BacklightMonitoring', function,
                         featureHelp='Help for Backlight monitoring service')
# RGB monitoring service
function = lambda context: (Kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY))
services.registerFeature('RGBMonitoring', function,
                         featureHelp='Help for RGB effect monitoring service')
# Ambient Light Sensor service
function = lambda context: Kosmos.discover_emulator(emulation_type=DeviceFamilyName.AMBIENT_LIGHT_SENSOR)
services.registerFeature('AmbientLightSensor', function, featureHelp='Help for Ambient Light Sensor Emulator service')
# Proximity Sensor service
function = lambda context: Kosmos.discover_emulator(emulation_type=DeviceFamilyName.PROXIMITY_SENSOR)
services.registerFeature('ProximitySensor', function, featureHelp='Help for Proximity Sensor Emulator service')
# Power Supply service
#  - Agilent unit or Power supply board
function_power_supply = lambda context: (Agilent.discover_agilent() or MCP4725.discover())
services.registerFeature('PowerSupply', function_power_supply, featureHelp='Help for Programmable Power Supply service')
# JLink IO Switch service
function = lambda context: (EmulatorsManager.is_jlink_io_switch_present(context.getFeatures()))
services.registerFeature('JLinkIOSwitch', function, featureHelp='Help for JLink IO Switch service')
# Power Switch service
function = lambda context: (Kosmos.discover_emulator(emulation_type=DeviceName.BAS))
services.registerFeature('PowerSwitch', function, featureHelp='Help for Configurable Power Switch service')
# Power Board service
function = lambda context: False
services.registerFeature('PowerBoard', function, featureHelp='Help for Power Board service')
# Rechargeable tool service
function = lambda context: (MCP4725.discover())
services.registerFeature('Rechargeable', function, featureHelp='Help for Rechargeable tool service')
# Current Meter service
function = lambda context: (INA226.discover())
services.registerFeature('CurrentMeter', function, featureHelp='Help for Current Measurement Instrument service')
# Debugger service
function_debugger = lambda context: (LibusbDriver.discover_debug_probe() > 0)
services.registerFeature('Debugger', function_debugger, featureHelp='Help for Debugger service')
function = lambda context: ((LibusbDriver.discover_debug_probe() > 0) and (
                            len([debugger for debugger in check_feature(context, 'RUNTIME/DEBUGGERS', 'F_Targets')
                                 if "companion" in debugger.lower()]) > 0))
services.registerFeature('CompanionDebugger', function, featureHelp='Help for Companion Debugger service')
function = lambda context: (LibusbDriver.discover_gotthard())
services.registerFeature('Gotthard', function, featureHelp='Help for Gothard service')
function = lambda context: (LibusbDriver.discover_crush_receiver())
services.registerFeature('Crush', function, featureHelp='Help for Crush service')
# USB Analyzer service
function = lambda context: (LibusbDriver.discover_beagle_480())
services.registerFeature('USBAnalyser', function, featureHelp='Help for USB Protocol Analyzer service')
# Keyboard service
function = lambda context, keys, layout=KeyboardMixin.LAYOUT.ANSI: (check_supported_keys(context, keys, layout))
services.registerFeature('RequiredKeys', function, featureHelp='Help for Keyboard service when all keys are required')
function = lambda context, keys, layout=KeyboardMixin.LAYOUT.ANSI: (
    check_supported_keys(context, keys, layout, at_least_one=True))
services.registerFeature('AtLeastOneKey', function, featureHelp='Help for Keyboard service when one key is required')
function = lambda context: (check_passive_hold_press_support(context))
services.registerFeature('PassiveHoldPress', function, featureHelp='Help for PassiveHoldPress service')
function = lambda context, keys=None, keyword_keys=None: (check_connected_keys(context, keys, keyword_keys))
services.registerFeature('EmulatedKeys', function, featureHelp='Help for Emulated keys service')
function = lambda context: (check_connected_keys(context, keyword_keys=("user_action",)))
services.registerFeature('EmulatedUserAction', function, featureHelp='Help for Emulated keys service')
# Mouse service
function = lambda context: (check_hybrid_switch_emulator(context))
services.registerFeature('HybridSwitchPressed', function, featureHelp='Help for Hybrid switch emulator service')
# Signals capture service
function = lambda context, leds: (check_supported_leds(context, leds, at_least_one=False))
services.registerFeature('RequiredLeds', function, featureHelp='Help for Leds service when all leds are required')
# Hardware reset service, i.e. Power Supply or Debugger
function = lambda context: (Kosmos.discover_emulator(emulation_type=DeviceName.BAS)
                            or MCP4725.discover()
                            or LibusbDriver.discover_debug_probe() > 0)
services.registerFeature('HardwareReset', function, featureHelp='Help for Hardware reset service')
function = lambda context: (check_feature(context, 'PRODUCT/FEATURES/COMMON/SECURE_DFU_CONTROL', 'F_CancelDfuSupported'))
services.registerFeature('CancelSecureDfu', function, featureHelp='Help for DFU tests')
# Ratchet Spy service
function = lambda context: False
services.registerFeature('RatchetSpy', function, featureHelp='Help for Wheel Ratchet monitoring service')
# Ratchet Emulation service
function = lambda context: False
services.registerFeature('Ratchet', function, featureHelp='Help for Wheel Ratchet emulation service')
# Game Mode Button Emulation service
function = lambda context: (get_attribute(context, 'PRODUCT/DEVICE', 'F_GameModeButtonType') == 'game_mode_slider' or
                            get_attribute(context, 'PRODUCT/DEVICE', 'F_GameModeButtonType') == 'game_mode_button')
services.registerFeature('GameModeButton', function, featureHelp='Help for Game Mode button emulator service')
# Hardware for a BLE context service
function = lambda context: LibusbDriver.is_ble_context_present()
services.registerFeature('BleContext', function, featureHelp='Help for Hardware for a BLE context service')
# BLE Pro Receiver
function = lambda context: (LibusbDriver.discover_ble_pro_receiver())
services.registerFeature('BLEProReceiver', function, featureHelp='Help for BLE Pro Receiver service')
# ------------------------------------------------------------------------------
# End of file
# ------------------------------------------------------------------------------
