#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.test.fullkeycustomization_test
:brief: HID++ 2.0 ``FullKeyCustomization`` test module
:author: Masan Xu <mxu11@logitech.com>
:date: 2023/05/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.fullkeycustomization import BaseLayerTriggerAsBitmapEvent
from pyhid.hidpp.features.common.fullkeycustomization import BaseLayerTriggerAsListEvent
from pyhid.hidpp.features.common.fullkeycustomization import EnableDisableEvent
from pyhid.hidpp.features.common.fullkeycustomization import FNLayerTriggerAsBitmapEvent
from pyhid.hidpp.features.common.fullkeycustomization import FNLayerTriggerAsListEvent
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomization
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomizationFactory
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomizationV0
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomizationV1
from pyhid.hidpp.features.common.fullkeycustomization import GShiftLayerTriggerAsBitmapEvent
from pyhid.hidpp.features.common.fullkeycustomization import GShiftLayerTriggerAsListEvent
from pyhid.hidpp.features.common.fullkeycustomization import GetCapabilitiesV0ToV1
from pyhid.hidpp.features.common.fullkeycustomization import GetCapabilitiesResponseV0
from pyhid.hidpp.features.common.fullkeycustomization import GetCapabilitiesResponseV1
from pyhid.hidpp.features.common.fullkeycustomization import GetSetEnabled
from pyhid.hidpp.features.common.fullkeycustomization import GetSetEnabledResponse
from pyhid.hidpp.features.common.fullkeycustomization import GetSetPowerOnParams
from pyhid.hidpp.features.common.fullkeycustomization import GetSetPowerOnParamsResponse
from pyhid.hidpp.features.common.fullkeycustomization import GetSetSWConfigurationCookieResponseV1
from pyhid.hidpp.features.common.fullkeycustomization import GetSetSWConfigurationCookieV1
from pyhid.hidpp.features.common.fullkeycustomization import GetToggleKeyList
from pyhid.hidpp.features.common.fullkeycustomization import GetToggleKeyListResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FullKeyCustomizationInstantiationTestCase(TestCase):
    """
    Test ``FullKeyCustomization`` testing classes instantiations
    """

    @staticmethod
    def test_full_key_customization():
        """
        Test ``FullKeyCustomization`` class instantiation
        """
        my_class = FullKeyCustomization(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = FullKeyCustomization(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_full_key_customization

    @staticmethod
    def test_get_capabilities_v0_to_v1():
        """
        Test ``GetCapabilities`` class instantiation
        """
        my_class = GetCapabilitiesV0ToV1(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetCapabilitiesV0ToV1(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_capabilities

    @staticmethod
    def test_get_set_power_on_params():
        """
        Test ``GetSetPowerOnParams`` class instantiation
        """
        my_class = GetSetPowerOnParams(device_index=0, feature_index=0,
                                       set_power_on_fkc_enable=0, power_on_fkc_enable=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetSetPowerOnParams(device_index=0xFF, feature_index=0xFF,
                                       set_power_on_fkc_enable=0x1, power_on_fkc_enable=0x1)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_set_power_on_params

    @staticmethod
    def test_get_toggle_key_list():
        """
        Test ``GetToggleKeyList`` class instantiation
        """
        my_class = GetToggleKeyList(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetToggleKeyList(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_toggle_key_list

    @staticmethod
    def test_get_set_enabled():
        """
        Test ``GetSetEnabled`` class instantiation
        """
        my_class = GetSetEnabled(device_index=0, feature_index=0,
                                 set_toggle_keys_enabled=0, set_fkc_enabled=0, fkc_enabled=0,
                                 toggle_key_7_enabled=0, toggle_key_6_enabled=0, toggle_key_5_enabled=0,
                                 toggle_key_4_enabled=0, toggle_key_3_enabled=0, toggle_key_2_enabled=0,
                                 toggle_key_1_enabled=0, toggle_key_0_enabled=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetSetEnabled(device_index=0xFF, feature_index=0xFF,
                                 set_toggle_keys_enabled=0x1, set_fkc_enabled=0x1, fkc_enabled=0x1,
                                 toggle_key_7_enabled=0x1, toggle_key_6_enabled=0x1, toggle_key_5_enabled=0x1,
                                 toggle_key_4_enabled=0x1, toggle_key_3_enabled=0x1, toggle_key_2_enabled=0x1,
                                 toggle_key_1_enabled=0x1, toggle_key_0_enabled=0x1)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_set_enabled

    @staticmethod
    def test_get_set_sw_configuration_cookie_v1():
        """
        Test ``GetSetSWConfigurationCookieV1`` class instantiation
        """
        my_class = GetSetSWConfigurationCookieV1(device_index=0, feature_index=0,
                                                 set_sw_configuration_cookie=0,
                                                 sw_configuration_cookie=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetSetSWConfigurationCookieV1(device_index=0xFF, feature_index=0xFF,
                                                 set_sw_configuration_cookie=0x1,
                                                 sw_configuration_cookie=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_set_sw_configuration_cookie_v1

    @staticmethod
    def test_get_capabilities_response_v0():
        """
        Test ``GetCapabilitiesResponseV0`` class instantiation
        """
        my_class = GetCapabilitiesResponseV0(device_index=0, feature_index=0,
                                             fkc_config_file_ver=0,
                                             macro_def_file_ver=0,
                                             fkc_config_file_maxsize=0,
                                             macro_def_file_maxsize=0,
                                             fkc_config_max_triggers=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponseV0(device_index=0xFF, feature_index=0xFF,
                                             fkc_config_file_ver=0xFF,
                                             macro_def_file_ver=0xFF,
                                             fkc_config_file_maxsize=0xFFFF,
                                             macro_def_file_maxsize=0xFFFF,
                                             fkc_config_max_triggers=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response_v0

    @staticmethod
    def test_get_capabilities_response_v1():
        """
        Test ``GetCapabilitiesResponseV1`` class instantiation
        """
        my_class = GetCapabilitiesResponseV1(device_index=0, feature_index=0,
                                             fkc_config_file_ver=0,
                                             macro_def_file_ver=0,
                                             fkc_config_file_maxsize=0,
                                             macro_def_file_maxsize=0,
                                             fkc_config_max_triggers=0,
                                             sw_config_capabilities=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponseV1(device_index=0xFF, feature_index=0xFF,
                                             fkc_config_file_ver=0xFF,
                                             macro_def_file_ver=0xFF,
                                             fkc_config_file_maxsize=0xFFFF,
                                             macro_def_file_maxsize=0xFFFF,
                                             fkc_config_max_triggers=0xFF,
                                             sw_config_capabilities=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response_v1

    @staticmethod
    def test_get_set_power_on_params_response():
        """
        Test ``GetSetPowerOnParamsResponse`` class instantiation
        """
        my_class = GetSetPowerOnParamsResponse(device_index=0, feature_index=0, power_on_fkc_enable=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetSetPowerOnParamsResponse(device_index=0xFF, feature_index=0xFF, power_on_fkc_enable=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_set_power_on_params_response

    @staticmethod
    def test_get_toggle_key_list_response():
        """
        Test ``GetToggleKeyListResponse`` class instantiation
        """
        my_class = GetToggleKeyListResponse(device_index=0, feature_index=0,
                                            toggle_key_0_cidx=HexList(0), toggle_key_1_cidx=HexList(0),
                                            toggle_key_2_cidx=HexList(0), toggle_key_3_cidx=HexList(0),
                                            toggle_key_4_cidx=HexList(0), toggle_key_5_cidx=HexList(0),
                                            toggle_key_6_cidx=HexList(0), toggle_key_7_cidx=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetToggleKeyListResponse(device_index=0xFF, feature_index=0xFF,
                                            toggle_key_0_cidx=HexList("FF" * (GetToggleKeyListResponse.LEN.
                                                                              TOGGLE_KEY_0_CIDX // 8)),
                                            toggle_key_1_cidx=HexList("FF" * (GetToggleKeyListResponse.LEN.
                                                                              TOGGLE_KEY_1_CIDX // 8)),
                                            toggle_key_2_cidx=HexList("FF" * (GetToggleKeyListResponse.LEN.
                                                                              TOGGLE_KEY_2_CIDX // 8)),
                                            toggle_key_3_cidx=HexList("FF" * (GetToggleKeyListResponse.LEN.
                                                                              TOGGLE_KEY_3_CIDX // 8)),
                                            toggle_key_4_cidx=HexList("FF" * (GetToggleKeyListResponse.LEN.
                                                                              TOGGLE_KEY_4_CIDX // 8)),
                                            toggle_key_5_cidx=HexList("FF" * (GetToggleKeyListResponse.LEN.
                                                                              TOGGLE_KEY_5_CIDX // 8)),
                                            toggle_key_6_cidx=HexList("FF" * (GetToggleKeyListResponse.LEN.
                                                                              TOGGLE_KEY_6_CIDX // 8)),
                                            toggle_key_7_cidx=HexList("FF" * (GetToggleKeyListResponse.LEN.
                                                                              TOGGLE_KEY_7_CIDX // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_toggle_key_list_response

    @staticmethod
    def test_get_set_enabled_response():
        """
        Test ``GetSetEnabledResponse`` class instantiation
        """
        my_class = GetSetEnabledResponse(device_index=0, feature_index=0, fkc_enabled=0,
                                         toggle_key_7_enabled=0, toggle_key_6_enabled=0, toggle_key_5_enabled=0,
                                         toggle_key_4_enabled=0, toggle_key_3_enabled=0, toggle_key_2_enabled=0,
                                         toggle_key_1_enabled=0, toggle_key_0_enabled=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetSetEnabledResponse(device_index=0xFF, feature_index=0xFF, fkc_enabled=0x1,
                                         toggle_key_7_enabled=0x1, toggle_key_6_enabled=0x1, toggle_key_5_enabled=0x1,
                                         toggle_key_4_enabled=0x1, toggle_key_3_enabled=0x1, toggle_key_2_enabled=0x1,
                                         toggle_key_1_enabled=0x1, toggle_key_0_enabled=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_set_enabled_response

    @staticmethod
    def test_base_layer_trigger_as_list_event():
        """
        Test ``BaseLayerTriggerAsListEvent`` class instantiation
        """
        my_class = BaseLayerTriggerAsListEvent(device_index=0, feature_index=0,
                                               key_trigger_0=0, key_trigger_1=0, key_trigger_2=0, key_trigger_3=0,
                                               key_trigger_4=0, key_trigger_5=0, key_trigger_6=0, key_trigger_7=0,
                                               key_trigger_8=0, key_trigger_9=0, key_trigger_10=0, key_trigger_11=0,
                                               key_trigger_12=0, key_trigger_13=0, key_trigger_14=0, key_trigger_15=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = BaseLayerTriggerAsListEvent(device_index=0xFF, feature_index=0xFF,
                                               key_trigger_0=0xFF, key_trigger_1=0xFF, key_trigger_2=0xFF,
                                               key_trigger_3=0xFF, key_trigger_4=0xFF, key_trigger_5=0xFF,
                                               key_trigger_6=0xFF, key_trigger_7=0xFF, key_trigger_8=0xFF,
                                               key_trigger_9=0xFF, key_trigger_10=0xFF, key_trigger_11=0xFF,
                                               key_trigger_12=0xFF, key_trigger_13=0xFF, key_trigger_14=0xFF,
                                               key_trigger_15=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_base_layer_trigger_as_list_event

    @staticmethod
    def test_base_layer_trigger_as_bitmap_event():
        """
        Test ``BaseLayerTriggerAsBitmapEvent`` class instantiation
        """
        my_class = BaseLayerTriggerAsBitmapEvent(device_index=0, feature_index=0,
                                                 fkc_idx_7=0, fkc_idx_6=0, fkc_idx_5=0, fkc_idx_4=0,
                                                 fkc_idx_3=0, fkc_idx_2=0, fkc_idx_1=0, fkc_idx_0=0,
                                                 fkc_idx_15=0, fkc_idx_14=0, fkc_idx_13=0, fkc_idx_12=0,
                                                 fkc_idx_11=0, fkc_idx_10=0, fkc_idx_9=0, fkc_idx_8=0,
                                                 fkc_idx_23=0, fkc_idx_22=0, fkc_idx_21=0, fkc_idx_20=0,
                                                 fkc_idx_19=0, fkc_idx_18=0, fkc_idx_17=0, fkc_idx_16=0,
                                                 fkc_idx_31=0, fkc_idx_30=0, fkc_idx_29=0, fkc_idx_28=0,
                                                 fkc_idx_27=0, fkc_idx_26=0, fkc_idx_25=0, fkc_idx_24=0,
                                                 fkc_idx_39=0, fkc_idx_38=0, fkc_idx_37=0, fkc_idx_36=0,
                                                 fkc_idx_35=0, fkc_idx_34=0, fkc_idx_33=0, fkc_idx_32=0,
                                                 fkc_idx_47=0, fkc_idx_46=0, fkc_idx_45=0, fkc_idx_44=0,
                                                 fkc_idx_43=0, fkc_idx_42=0, fkc_idx_41=0, fkc_idx_40=0,
                                                 fkc_idx_55=0, fkc_idx_54=0, fkc_idx_53=0, fkc_idx_52=0,
                                                 fkc_idx_51=0, fkc_idx_50=0, fkc_idx_49=0, fkc_idx_48=0,
                                                 fkc_idx_63=0, fkc_idx_62=0, fkc_idx_61=0, fkc_idx_60=0,
                                                 fkc_idx_59=0, fkc_idx_58=0, fkc_idx_57=0, fkc_idx_56=0,
                                                 fkc_idx_71=0, fkc_idx_70=0, fkc_idx_69=0, fkc_idx_68=0,
                                                 fkc_idx_67=0, fkc_idx_66=0, fkc_idx_65=0, fkc_idx_64=0,
                                                 fkc_idx_79=0, fkc_idx_78=0, fkc_idx_77=0, fkc_idx_76=0,
                                                 fkc_idx_75=0, fkc_idx_74=0, fkc_idx_73=0, fkc_idx_72=0,
                                                 fkc_idx_87=0, fkc_idx_86=0, fkc_idx_85=0, fkc_idx_84=0,
                                                 fkc_idx_83=0, fkc_idx_82=0, fkc_idx_81=0, fkc_idx_80=0,
                                                 fkc_idx_95=0, fkc_idx_94=0, fkc_idx_93=0, fkc_idx_92=0,
                                                 fkc_idx_91=0, fkc_idx_90=0, fkc_idx_89=0, fkc_idx_88=0,
                                                 fkc_idx_103=0, fkc_idx_102=0, fkc_idx_101=0, fkc_idx_100=0,
                                                 fkc_idx_99=0, fkc_idx_98=0, fkc_idx_97=0, fkc_idx_96=0,
                                                 fkc_idx_111=0, fkc_idx_110=0, fkc_idx_109=0, fkc_idx_108=0,
                                                 fkc_idx_107=0, fkc_idx_106=0, fkc_idx_105=0, fkc_idx_104=0,
                                                 fkc_idx_119=0, fkc_idx_118=0, fkc_idx_117=0, fkc_idx_116=0,
                                                 fkc_idx_115=0, fkc_idx_114=0, fkc_idx_113=0, fkc_idx_112=0,
                                                 fkc_idx_127=0, fkc_idx_126=0, fkc_idx_125=0, fkc_idx_124=0,
                                                 fkc_idx_123=0, fkc_idx_122=0, fkc_idx_121=0, fkc_idx_120=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = BaseLayerTriggerAsBitmapEvent(device_index=0xFF, feature_index=0xFF,
                                                 fkc_idx_7=0x1, fkc_idx_6=0x1, fkc_idx_5=0x1, fkc_idx_4=0x1,
                                                 fkc_idx_3=0x1, fkc_idx_2=0x1, fkc_idx_1=0x1, fkc_idx_0=0x1,
                                                 fkc_idx_15=0x1, fkc_idx_14=0x1, fkc_idx_13=0x1, fkc_idx_12=0x1,
                                                 fkc_idx_11=0x1, fkc_idx_10=0x1, fkc_idx_9=0x1, fkc_idx_8=0x1,
                                                 fkc_idx_23=0x1, fkc_idx_22=0x1, fkc_idx_21=0x1, fkc_idx_20=0x1,
                                                 fkc_idx_19=0x1, fkc_idx_18=0x1, fkc_idx_17=0x1, fkc_idx_16=0x1,
                                                 fkc_idx_31=0x1, fkc_idx_30=0x1, fkc_idx_29=0x1, fkc_idx_28=0x1,
                                                 fkc_idx_27=0x1, fkc_idx_26=0x1, fkc_idx_25=0x1, fkc_idx_24=0x1,
                                                 fkc_idx_39=0x1, fkc_idx_38=0x1, fkc_idx_37=0x1, fkc_idx_36=0x1,
                                                 fkc_idx_35=0x1, fkc_idx_34=0x1, fkc_idx_33=0x1, fkc_idx_32=0x1,
                                                 fkc_idx_47=0x1, fkc_idx_46=0x1, fkc_idx_45=0x1, fkc_idx_44=0x1,
                                                 fkc_idx_43=0x1, fkc_idx_42=0x1, fkc_idx_41=0x1, fkc_idx_40=0x1,
                                                 fkc_idx_55=0x1, fkc_idx_54=0x1, fkc_idx_53=0x1, fkc_idx_52=0x1,
                                                 fkc_idx_51=0x1, fkc_idx_50=0x1, fkc_idx_49=0x1, fkc_idx_48=0x1,
                                                 fkc_idx_63=0x1, fkc_idx_62=0x1, fkc_idx_61=0x1, fkc_idx_60=0x1,
                                                 fkc_idx_59=0x1, fkc_idx_58=0x1, fkc_idx_57=0x1, fkc_idx_56=0x1,
                                                 fkc_idx_71=0x1, fkc_idx_70=0x1, fkc_idx_69=0x1, fkc_idx_68=0x1,
                                                 fkc_idx_67=0x1, fkc_idx_66=0x1, fkc_idx_65=0x1, fkc_idx_64=0x1,
                                                 fkc_idx_79=0x1, fkc_idx_78=0x1, fkc_idx_77=0x1, fkc_idx_76=0x1,
                                                 fkc_idx_75=0x1, fkc_idx_74=0x1, fkc_idx_73=0x1, fkc_idx_72=0x1,
                                                 fkc_idx_87=0x1, fkc_idx_86=0x1, fkc_idx_85=0x1, fkc_idx_84=0x1,
                                                 fkc_idx_83=0x1, fkc_idx_82=0x1, fkc_idx_81=0x1, fkc_idx_80=0x1,
                                                 fkc_idx_95=0x1, fkc_idx_94=0x1, fkc_idx_93=0x1, fkc_idx_92=0x1,
                                                 fkc_idx_91=0x1, fkc_idx_90=0x1, fkc_idx_89=0x1, fkc_idx_88=0x1,
                                                 fkc_idx_103=0x1, fkc_idx_102=0x1, fkc_idx_101=0x1, fkc_idx_100=0x1,
                                                 fkc_idx_99=0x1, fkc_idx_98=0x1, fkc_idx_97=0x1, fkc_idx_96=0x1,
                                                 fkc_idx_111=0x1, fkc_idx_110=0x1, fkc_idx_109=0x1, fkc_idx_108=0x1,
                                                 fkc_idx_107=0x1, fkc_idx_106=0x1, fkc_idx_105=0x1, fkc_idx_104=0x1,
                                                 fkc_idx_119=0x1, fkc_idx_118=0x1, fkc_idx_117=0x1, fkc_idx_116=0x1,
                                                 fkc_idx_115=0x1, fkc_idx_114=0x1, fkc_idx_113=0x1, fkc_idx_112=0x1,
                                                 fkc_idx_127=0x1, fkc_idx_126=0x1, fkc_idx_125=0x1, fkc_idx_124=0x1,
                                                 fkc_idx_123=0x1, fkc_idx_122=0x1, fkc_idx_121=0x1, fkc_idx_120=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_base_layer_trigger_as_bitmap_event

    @staticmethod
    def test_fn_layer_trigger_as_list_event():
        """
        Test ``FNLayerTriggerAsListEvent`` class instantiation
        """
        my_class = FNLayerTriggerAsListEvent(device_index=0, feature_index=0,
                                             key_trigger_0=0, key_trigger_1=0, key_trigger_2=0, key_trigger_3=0,
                                             key_trigger_4=0, key_trigger_5=0, key_trigger_6=0, key_trigger_7=0,
                                             key_trigger_8=0, key_trigger_9=0, key_trigger_10=0, key_trigger_11=0,
                                             key_trigger_12=0, key_trigger_13=0, key_trigger_14=0, key_trigger_15=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = FNLayerTriggerAsListEvent(device_index=0xFF, feature_index=0xFF,
                                             key_trigger_0=0xFF, key_trigger_1=0xFF, key_trigger_2=0xFF,
                                             key_trigger_3=0xFF, key_trigger_4=0xFF, key_trigger_5=0xFF,
                                             key_trigger_6=0xFF, key_trigger_7=0xFF, key_trigger_8=0xFF,
                                             key_trigger_9=0xFF, key_trigger_10=0xFF, key_trigger_11=0xFF,
                                             key_trigger_12=0xFF, key_trigger_13=0xFF, key_trigger_14=0xFF,
                                             key_trigger_15=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_fn_layer_trigger_as_list_event

    @staticmethod
    def test_fn_layer_trigger_as_bitmap_event():
        """
        Test ``FNLayerTriggerAsBitmapEvent`` class instantiation
        """
        my_class = FNLayerTriggerAsBitmapEvent(device_index=0, feature_index=0,
                                               fkc_idx_7=0, fkc_idx_6=0, fkc_idx_5=0, fkc_idx_4=0,
                                               fkc_idx_3=0, fkc_idx_2=0, fkc_idx_1=0, fkc_idx_0=0,
                                               fkc_idx_15=0, fkc_idx_14=0, fkc_idx_13=0, fkc_idx_12=0,
                                               fkc_idx_11=0, fkc_idx_10=0, fkc_idx_9=0, fkc_idx_8=0,
                                               fkc_idx_23=0, fkc_idx_22=0, fkc_idx_21=0, fkc_idx_20=0,
                                               fkc_idx_19=0, fkc_idx_18=0, fkc_idx_17=0, fkc_idx_16=0,
                                               fkc_idx_31=0, fkc_idx_30=0, fkc_idx_29=0, fkc_idx_28=0,
                                               fkc_idx_27=0, fkc_idx_26=0, fkc_idx_25=0, fkc_idx_24=0,
                                               fkc_idx_39=0, fkc_idx_38=0, fkc_idx_37=0, fkc_idx_36=0,
                                               fkc_idx_35=0, fkc_idx_34=0, fkc_idx_33=0, fkc_idx_32=0,
                                               fkc_idx_47=0, fkc_idx_46=0, fkc_idx_45=0, fkc_idx_44=0,
                                               fkc_idx_43=0, fkc_idx_42=0, fkc_idx_41=0, fkc_idx_40=0,
                                               fkc_idx_55=0, fkc_idx_54=0, fkc_idx_53=0, fkc_idx_52=0,
                                               fkc_idx_51=0, fkc_idx_50=0, fkc_idx_49=0, fkc_idx_48=0,
                                               fkc_idx_63=0, fkc_idx_62=0, fkc_idx_61=0, fkc_idx_60=0,
                                               fkc_idx_59=0, fkc_idx_58=0, fkc_idx_57=0, fkc_idx_56=0,
                                               fkc_idx_71=0, fkc_idx_70=0, fkc_idx_69=0, fkc_idx_68=0,
                                               fkc_idx_67=0, fkc_idx_66=0, fkc_idx_65=0, fkc_idx_64=0,
                                               fkc_idx_79=0, fkc_idx_78=0, fkc_idx_77=0, fkc_idx_76=0,
                                               fkc_idx_75=0, fkc_idx_74=0, fkc_idx_73=0, fkc_idx_72=0,
                                               fkc_idx_87=0, fkc_idx_86=0, fkc_idx_85=0, fkc_idx_84=0,
                                               fkc_idx_83=0, fkc_idx_82=0, fkc_idx_81=0, fkc_idx_80=0,
                                               fkc_idx_95=0, fkc_idx_94=0, fkc_idx_93=0, fkc_idx_92=0,
                                               fkc_idx_91=0, fkc_idx_90=0, fkc_idx_89=0, fkc_idx_88=0,
                                               fkc_idx_103=0, fkc_idx_102=0, fkc_idx_101=0, fkc_idx_100=0,
                                               fkc_idx_99=0, fkc_idx_98=0, fkc_idx_97=0, fkc_idx_96=0,
                                               fkc_idx_111=0, fkc_idx_110=0, fkc_idx_109=0, fkc_idx_108=0,
                                               fkc_idx_107=0, fkc_idx_106=0, fkc_idx_105=0, fkc_idx_104=0,
                                               fkc_idx_119=0, fkc_idx_118=0, fkc_idx_117=0, fkc_idx_116=0,
                                               fkc_idx_115=0, fkc_idx_114=0, fkc_idx_113=0, fkc_idx_112=0,
                                               fkc_idx_127=0, fkc_idx_126=0, fkc_idx_125=0, fkc_idx_124=0,
                                               fkc_idx_123=0, fkc_idx_122=0, fkc_idx_121=0, fkc_idx_120=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = FNLayerTriggerAsBitmapEvent(device_index=0xFF, feature_index=0xFF,
                                               fkc_idx_7=0x1, fkc_idx_6=0x1, fkc_idx_5=0x1, fkc_idx_4=0x1,
                                               fkc_idx_3=0x1, fkc_idx_2=0x1, fkc_idx_1=0x1, fkc_idx_0=0x1,
                                               fkc_idx_15=0x1, fkc_idx_14=0x1, fkc_idx_13=0x1, fkc_idx_12=0x1,
                                               fkc_idx_11=0x1, fkc_idx_10=0x1, fkc_idx_9=0x1, fkc_idx_8=0x1,
                                               fkc_idx_23=0x1, fkc_idx_22=0x1, fkc_idx_21=0x1, fkc_idx_20=0x1,
                                               fkc_idx_19=0x1, fkc_idx_18=0x1, fkc_idx_17=0x1, fkc_idx_16=0x1,
                                               fkc_idx_31=0x1, fkc_idx_30=0x1, fkc_idx_29=0x1, fkc_idx_28=0x1,
                                               fkc_idx_27=0x1, fkc_idx_26=0x1, fkc_idx_25=0x1, fkc_idx_24=0x1,
                                               fkc_idx_39=0x1, fkc_idx_38=0x1, fkc_idx_37=0x1, fkc_idx_36=0x1,
                                               fkc_idx_35=0x1, fkc_idx_34=0x1, fkc_idx_33=0x1, fkc_idx_32=0x1,
                                               fkc_idx_47=0x1, fkc_idx_46=0x1, fkc_idx_45=0x1, fkc_idx_44=0x1,
                                               fkc_idx_43=0x1, fkc_idx_42=0x1, fkc_idx_41=0x1, fkc_idx_40=0x1,
                                               fkc_idx_55=0x1, fkc_idx_54=0x1, fkc_idx_53=0x1, fkc_idx_52=0x1,
                                               fkc_idx_51=0x1, fkc_idx_50=0x1, fkc_idx_49=0x1, fkc_idx_48=0x1,
                                               fkc_idx_63=0x1, fkc_idx_62=0x1, fkc_idx_61=0x1, fkc_idx_60=0x1,
                                               fkc_idx_59=0x1, fkc_idx_58=0x1, fkc_idx_57=0x1, fkc_idx_56=0x1,
                                               fkc_idx_71=0x1, fkc_idx_70=0x1, fkc_idx_69=0x1, fkc_idx_68=0x1,
                                               fkc_idx_67=0x1, fkc_idx_66=0x1, fkc_idx_65=0x1, fkc_idx_64=0x1,
                                               fkc_idx_79=0x1, fkc_idx_78=0x1, fkc_idx_77=0x1, fkc_idx_76=0x1,
                                               fkc_idx_75=0x1, fkc_idx_74=0x1, fkc_idx_73=0x1, fkc_idx_72=0x1,
                                               fkc_idx_87=0x1, fkc_idx_86=0x1, fkc_idx_85=0x1, fkc_idx_84=0x1,
                                               fkc_idx_83=0x1, fkc_idx_82=0x1, fkc_idx_81=0x1, fkc_idx_80=0x1,
                                               fkc_idx_95=0x1, fkc_idx_94=0x1, fkc_idx_93=0x1, fkc_idx_92=0x1,
                                               fkc_idx_91=0x1, fkc_idx_90=0x1, fkc_idx_89=0x1, fkc_idx_88=0x1,
                                               fkc_idx_103=0x1, fkc_idx_102=0x1, fkc_idx_101=0x1, fkc_idx_100=0x1,
                                               fkc_idx_99=0x1, fkc_idx_98=0x1, fkc_idx_97=0x1, fkc_idx_96=0x1,
                                               fkc_idx_111=0x1, fkc_idx_110=0x1, fkc_idx_109=0x1, fkc_idx_108=0x1,
                                               fkc_idx_107=0x1, fkc_idx_106=0x1, fkc_idx_105=0x1, fkc_idx_104=0x1,
                                               fkc_idx_119=0x1, fkc_idx_118=0x1, fkc_idx_117=0x1, fkc_idx_116=0x1,
                                               fkc_idx_115=0x1, fkc_idx_114=0x1, fkc_idx_113=0x1, fkc_idx_112=0x1,
                                               fkc_idx_127=0x1, fkc_idx_126=0x1, fkc_idx_125=0x1, fkc_idx_124=0x1,
                                               fkc_idx_123=0x1, fkc_idx_122=0x1, fkc_idx_121=0x1, fkc_idx_120=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_fn_layer_trigger_as_bitmap_event

    @staticmethod
    def test_gshift_layer_trigger_as_list_event():
        """
        Test ``GShiftLayerTriggerAsListEvent`` class instantiation
        """
        my_class = GShiftLayerTriggerAsListEvent(device_index=0, feature_index=0,
                                                 key_trigger_0=0, key_trigger_1=0, key_trigger_2=0, key_trigger_3=0,
                                                 key_trigger_4=0, key_trigger_5=0, key_trigger_6=0, key_trigger_7=0,
                                                 key_trigger_8=0, key_trigger_9=0, key_trigger_10=0, key_trigger_11=0,
                                                 key_trigger_12=0, key_trigger_13=0, key_trigger_14=0, key_trigger_15=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GShiftLayerTriggerAsListEvent(device_index=0xFF, feature_index=0xFF,
                                                 key_trigger_0=0xFF, key_trigger_1=0xFF, key_trigger_2=0xFF,
                                                 key_trigger_3=0xFF, key_trigger_4=0xFF, key_trigger_5=0xFF,
                                                 key_trigger_6=0xFF, key_trigger_7=0xFF, key_trigger_8=0xFF,
                                                 key_trigger_9=0xFF, key_trigger_10=0xFF, key_trigger_11=0xFF,
                                                 key_trigger_12=0xFF, key_trigger_13=0xFF, key_trigger_14=0xFF,
                                                 key_trigger_15=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_gshift_layer_trigger_as_list_event

    @staticmethod
    def test_gshift_layer_trigger_as_bitmap_event():
        """
        Test ``GShiftLayerTriggerAsBitmapEvent`` class instantiation
        """
        my_class = GShiftLayerTriggerAsBitmapEvent(device_index=0, feature_index=0,
                                                   fkc_idx_7=0, fkc_idx_6=0, fkc_idx_5=0, fkc_idx_4=0,
                                                   fkc_idx_3=0, fkc_idx_2=0, fkc_idx_1=0, fkc_idx_0=0,
                                                   fkc_idx_15=0, fkc_idx_14=0, fkc_idx_13=0, fkc_idx_12=0,
                                                   fkc_idx_11=0, fkc_idx_10=0, fkc_idx_9=0, fkc_idx_8=0,
                                                   fkc_idx_23=0, fkc_idx_22=0, fkc_idx_21=0, fkc_idx_20=0,
                                                   fkc_idx_19=0, fkc_idx_18=0, fkc_idx_17=0, fkc_idx_16=0,
                                                   fkc_idx_31=0, fkc_idx_30=0, fkc_idx_29=0, fkc_idx_28=0,
                                                   fkc_idx_27=0, fkc_idx_26=0, fkc_idx_25=0, fkc_idx_24=0,
                                                   fkc_idx_39=0, fkc_idx_38=0, fkc_idx_37=0, fkc_idx_36=0,
                                                   fkc_idx_35=0, fkc_idx_34=0, fkc_idx_33=0, fkc_idx_32=0,
                                                   fkc_idx_47=0, fkc_idx_46=0, fkc_idx_45=0, fkc_idx_44=0,
                                                   fkc_idx_43=0, fkc_idx_42=0, fkc_idx_41=0, fkc_idx_40=0,
                                                   fkc_idx_55=0, fkc_idx_54=0, fkc_idx_53=0, fkc_idx_52=0,
                                                   fkc_idx_51=0, fkc_idx_50=0, fkc_idx_49=0, fkc_idx_48=0,
                                                   fkc_idx_63=0, fkc_idx_62=0, fkc_idx_61=0, fkc_idx_60=0,
                                                   fkc_idx_59=0, fkc_idx_58=0, fkc_idx_57=0, fkc_idx_56=0,
                                                   fkc_idx_71=0, fkc_idx_70=0, fkc_idx_69=0, fkc_idx_68=0,
                                                   fkc_idx_67=0, fkc_idx_66=0, fkc_idx_65=0, fkc_idx_64=0,
                                                   fkc_idx_79=0, fkc_idx_78=0, fkc_idx_77=0, fkc_idx_76=0,
                                                   fkc_idx_75=0, fkc_idx_74=0, fkc_idx_73=0, fkc_idx_72=0,
                                                   fkc_idx_87=0, fkc_idx_86=0, fkc_idx_85=0, fkc_idx_84=0,
                                                   fkc_idx_83=0, fkc_idx_82=0, fkc_idx_81=0, fkc_idx_80=0,
                                                   fkc_idx_95=0, fkc_idx_94=0, fkc_idx_93=0, fkc_idx_92=0,
                                                   fkc_idx_91=0, fkc_idx_90=0, fkc_idx_89=0, fkc_idx_88=0,
                                                   fkc_idx_103=0, fkc_idx_102=0, fkc_idx_101=0, fkc_idx_100=0,
                                                   fkc_idx_99=0, fkc_idx_98=0, fkc_idx_97=0, fkc_idx_96=0,
                                                   fkc_idx_111=0, fkc_idx_110=0, fkc_idx_109=0, fkc_idx_108=0,
                                                   fkc_idx_107=0, fkc_idx_106=0, fkc_idx_105=0, fkc_idx_104=0,
                                                   fkc_idx_119=0, fkc_idx_118=0, fkc_idx_117=0, fkc_idx_116=0,
                                                   fkc_idx_115=0, fkc_idx_114=0, fkc_idx_113=0, fkc_idx_112=0,
                                                   fkc_idx_127=0, fkc_idx_126=0, fkc_idx_125=0, fkc_idx_124=0,
                                                   fkc_idx_123=0, fkc_idx_122=0, fkc_idx_121=0, fkc_idx_120=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GShiftLayerTriggerAsBitmapEvent(device_index=0xFF, feature_index=0xFF,
                                                   fkc_idx_7=0x1, fkc_idx_6=0x1, fkc_idx_5=0x1, fkc_idx_4=0x1,
                                                   fkc_idx_3=0x1, fkc_idx_2=0x1, fkc_idx_1=0x1, fkc_idx_0=0x1,
                                                   fkc_idx_15=0x1, fkc_idx_14=0x1, fkc_idx_13=0x1, fkc_idx_12=0x1,
                                                   fkc_idx_11=0x1, fkc_idx_10=0x1, fkc_idx_9=0x1, fkc_idx_8=0x1,
                                                   fkc_idx_23=0x1, fkc_idx_22=0x1, fkc_idx_21=0x1, fkc_idx_20=0x1,
                                                   fkc_idx_19=0x1, fkc_idx_18=0x1, fkc_idx_17=0x1, fkc_idx_16=0x1,
                                                   fkc_idx_31=0x1, fkc_idx_30=0x1, fkc_idx_29=0x1, fkc_idx_28=0x1,
                                                   fkc_idx_27=0x1, fkc_idx_26=0x1, fkc_idx_25=0x1, fkc_idx_24=0x1,
                                                   fkc_idx_39=0x1, fkc_idx_38=0x1, fkc_idx_37=0x1, fkc_idx_36=0x1,
                                                   fkc_idx_35=0x1, fkc_idx_34=0x1, fkc_idx_33=0x1, fkc_idx_32=0x1,
                                                   fkc_idx_47=0x1, fkc_idx_46=0x1, fkc_idx_45=0x1, fkc_idx_44=0x1,
                                                   fkc_idx_43=0x1, fkc_idx_42=0x1, fkc_idx_41=0x1, fkc_idx_40=0x1,
                                                   fkc_idx_55=0x1, fkc_idx_54=0x1, fkc_idx_53=0x1, fkc_idx_52=0x1,
                                                   fkc_idx_51=0x1, fkc_idx_50=0x1, fkc_idx_49=0x1, fkc_idx_48=0x1,
                                                   fkc_idx_63=0x1, fkc_idx_62=0x1, fkc_idx_61=0x1, fkc_idx_60=0x1,
                                                   fkc_idx_59=0x1, fkc_idx_58=0x1, fkc_idx_57=0x1, fkc_idx_56=0x1,
                                                   fkc_idx_71=0x1, fkc_idx_70=0x1, fkc_idx_69=0x1, fkc_idx_68=0x1,
                                                   fkc_idx_67=0x1, fkc_idx_66=0x1, fkc_idx_65=0x1, fkc_idx_64=0x1,
                                                   fkc_idx_79=0x1, fkc_idx_78=0x1, fkc_idx_77=0x1, fkc_idx_76=0x1,
                                                   fkc_idx_75=0x1, fkc_idx_74=0x1, fkc_idx_73=0x1, fkc_idx_72=0x1,
                                                   fkc_idx_87=0x1, fkc_idx_86=0x1, fkc_idx_85=0x1, fkc_idx_84=0x1,
                                                   fkc_idx_83=0x1, fkc_idx_82=0x1, fkc_idx_81=0x1, fkc_idx_80=0x1,
                                                   fkc_idx_95=0x1, fkc_idx_94=0x1, fkc_idx_93=0x1, fkc_idx_92=0x1,
                                                   fkc_idx_91=0x1, fkc_idx_90=0x1, fkc_idx_89=0x1, fkc_idx_88=0x1,
                                                   fkc_idx_103=0x1, fkc_idx_102=0x1, fkc_idx_101=0x1, fkc_idx_100=0x1,
                                                   fkc_idx_99=0x1, fkc_idx_98=0x1, fkc_idx_97=0x1, fkc_idx_96=0x1,
                                                   fkc_idx_111=0x1, fkc_idx_110=0x1, fkc_idx_109=0x1, fkc_idx_108=0x1,
                                                   fkc_idx_107=0x1, fkc_idx_106=0x1, fkc_idx_105=0x1, fkc_idx_104=0x1,
                                                   fkc_idx_119=0x1, fkc_idx_118=0x1, fkc_idx_117=0x1, fkc_idx_116=0x1,
                                                   fkc_idx_115=0x1, fkc_idx_114=0x1, fkc_idx_113=0x1, fkc_idx_112=0x1,
                                                   fkc_idx_127=0x1, fkc_idx_126=0x1, fkc_idx_125=0x1, fkc_idx_124=0x1,
                                                   fkc_idx_123=0x1, fkc_idx_122=0x1, fkc_idx_121=0x1, fkc_idx_120=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_gshift_layer_trigger_as_bitmap_event

    @staticmethod
    def test_enable_disable_event():
        """
        Test ``EnableDisableEvent`` class instantiation
        """
        my_class = EnableDisableEvent(device_index=0, feature_index=0, failure=0, enabled=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = EnableDisableEvent(device_index=0xFF, feature_index=0xFF, failure=0x1, enabled=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_enable_disable_event
# end class FullKeyCustomizationInstantiationTestCase


class FullKeyCustomizationTestCase(TestCase):
    """
    Test ``FullKeyCustomization`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            FullKeyCustomizationV0.VERSION: {
                "cls": FullKeyCustomizationV0,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilitiesV0ToV1,
                    "get_capabilities_response_cls": GetCapabilitiesResponseV0,
                    "get_set_power_on_params_cls": GetSetPowerOnParams,
                    "get_set_power_on_params_response_cls": GetSetPowerOnParamsResponse,
                    "get_toggle_key_list_cls": GetToggleKeyList,
                    "get_toggle_key_list_response_cls": GetToggleKeyListResponse,
                    "get_set_enabled_cls": GetSetEnabled,
                    "get_set_enabled_response_cls": GetSetEnabledResponse,
                    "base_layer_trigger_as_list_event_cls": BaseLayerTriggerAsListEvent,
                    "base_layer_trigger_as_bitmap_event_cls": BaseLayerTriggerAsBitmapEvent,
                    "fn_layer_trigger_as_list_event_cls": FNLayerTriggerAsListEvent,
                    "fn_layer_trigger_as_bitmap_event_cls": FNLayerTriggerAsBitmapEvent,
                    "gshift_layer_trigger_as_list_event_cls": GShiftLayerTriggerAsListEvent,
                    "gshift_layer_trigger_as_bitmap_event_cls": GShiftLayerTriggerAsBitmapEvent,
                    "enable_disable_event_cls": EnableDisableEvent,
                },
                "max_function_index": 3
            },
            FullKeyCustomizationV1.VERSION: {
                "cls": FullKeyCustomizationV1,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilitiesV0ToV1,
                    "get_capabilities_response_cls": GetCapabilitiesResponseV1,
                    "get_set_power_on_params_cls": GetSetPowerOnParams,
                    "get_set_power_on_params_response_cls": GetSetPowerOnParamsResponse,
                    "get_toggle_key_list_cls": GetToggleKeyList,
                    "get_toggle_key_list_response_cls": GetToggleKeyListResponse,
                    "get_set_enabled_cls": GetSetEnabled,
                    "get_set_enabled_response_cls": GetSetEnabledResponse,
                    "get_set_sw_configuration_cookie_cls": GetSetSWConfigurationCookieV1,
                    "get_set_sw_configuration_cookie_response_cls": GetSetSWConfigurationCookieResponseV1,
                    "base_layer_trigger_as_list_event_cls": BaseLayerTriggerAsListEvent,
                    "base_layer_trigger_as_bitmap_event_cls": BaseLayerTriggerAsBitmapEvent,
                    "fn_layer_trigger_as_list_event_cls": FNLayerTriggerAsListEvent,
                    "fn_layer_trigger_as_bitmap_event_cls": FNLayerTriggerAsBitmapEvent,
                    "gshift_layer_trigger_as_list_event_cls": GShiftLayerTriggerAsListEvent,
                    "gshift_layer_trigger_as_bitmap_event_cls": GShiftLayerTriggerAsBitmapEvent,
                    "enable_disable_event_cls": EnableDisableEvent,
                },
                "max_function_index": 4
            },
        }
        cls.max_version = 1
    # end def setUpClass

    def test_factory(self):
        """
        Test ``FullKeyCustomizationFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(FullKeyCustomizationFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``FullKeyCustomizationFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                FullKeyCustomizationFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``FullKeyCustomizationFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = FullKeyCustomizationFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(obj, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(obj, interface)
                    # end with
                # end if
            # end for
        # end for
    # end def test_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check ``get_max_function_index`` returns correct value at each version

        :raise ``AssertionError``: Assert max_function_index that raise an exception
        """
        for version, expected in self.expected.items():
            obj = FullKeyCustomizationFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class FullKeyCustomizationTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
