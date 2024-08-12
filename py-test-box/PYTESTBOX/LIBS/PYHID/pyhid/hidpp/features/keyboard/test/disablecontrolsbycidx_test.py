#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.keyboard.test.disablecontrolsbycidx_test
:brief: HID++ 2.0 ``DisableControlsByCIDX`` test module
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/03/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import DisableControlsByCIDX
from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import DisableControlsByCIDXFactory
from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import DisableControlsByCIDXV0
from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import DisableControlsByCIDXV1
from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import GameModeEvent
from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import GetCapabilities
from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import GetCapabilitiesResponse
from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import GetGameMode
from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import GetGameModeResponse
from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import GetSetPowerOnParams
from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import GetSetPowerOnParamsResponse
from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import SetDisabledControls
from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import SetDisabledControlsResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DisableControlsByCIDXInstantiationTestCase(TestCase):
    """
    Test ``DisableControlsByCIDX`` testing classes instantiations
    """

    @staticmethod
    def test_disable_controls_by_cidx():
        """
        Test ``DisableControlsByCIDX`` class instantiation
        """
        my_class = DisableControlsByCIDX(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = DisableControlsByCIDX(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_disable_controls_by_cidx

    @staticmethod
    def test_set_disabled_controls():
        """
        Test ``SetDisabledControls`` class instantiation
        """
        my_class = SetDisabledControls(device_index=0, feature_index=0, cidx_7=0, cidx_6=0, cidx_5=0,
                                       cidx_4=0, cidx_3=0, cidx_2=0, cidx_1=0, cidx_0=0, cidx_15=0,
                                       cidx_14=0, cidx_13=0, cidx_12=0, cidx_11=0, cidx_10=0, cidx_9=0,
                                       cidx_8=0, cidx_23=0, cidx_22=0, cidx_21=0, cidx_20=0, cidx_19=0,
                                       cidx_18=0, cidx_17=0, cidx_16=0, cidx_31=0, cidx_30=0, cidx_29=0,
                                       cidx_28=0, cidx_27=0, cidx_26=0, cidx_25=0, cidx_24=0, cidx_39=0,
                                       cidx_38=0, cidx_37=0, cidx_36=0, cidx_35=0, cidx_34=0, cidx_33=0,
                                       cidx_32=0, cidx_47=0, cidx_46=0, cidx_45=0, cidx_44=0, cidx_43=0,
                                       cidx_42=0, cidx_41=0, cidx_40=0, cidx_55=0, cidx_54=0, cidx_53=0,
                                       cidx_52=0, cidx_51=0, cidx_50=0, cidx_49=0, cidx_48=0, cidx_63=0,
                                       cidx_62=0, cidx_61=0, cidx_60=0, cidx_59=0, cidx_58=0, cidx_57=0,
                                       cidx_56=0, cidx_71=0, cidx_70=0, cidx_69=0, cidx_68=0, cidx_67=0,
                                       cidx_66=0, cidx_65=0, cidx_64=0, cidx_79=0, cidx_78=0, cidx_77=0,
                                       cidx_76=0, cidx_75=0, cidx_74=0, cidx_73=0, cidx_72=0, cidx_87=0,
                                       cidx_86=0, cidx_85=0, cidx_84=0, cidx_83=0, cidx_82=0, cidx_81=0,
                                       cidx_80=0, cidx_95=0, cidx_94=0, cidx_93=0, cidx_92=0, cidx_91=0,
                                       cidx_90=0, cidx_89=0, cidx_88=0, cidx_103=0, cidx_102=0, cidx_101=0,
                                       cidx_100=0, cidx_99=0, cidx_98=0, cidx_97=0, cidx_96=0, cidx_111=0,
                                       cidx_110=0, cidx_109=0, cidx_108=0, cidx_107=0, cidx_106=0, cidx_105=0,
                                       cidx_104=0, cidx_119=0, cidx_118=0, cidx_117=0, cidx_116=0, cidx_115=0,
                                       cidx_114=0, cidx_113=0, cidx_112=0, cidx_127=0, cidx_126=0, cidx_125=0,
                                       cidx_124=0, cidx_123=0, cidx_122=0, cidx_121=0, cidx_120=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetDisabledControls(device_index=0xff, feature_index=0xff,
                                       cidx_7=0x1, cidx_6=0x1, cidx_5=0x1, cidx_4=0x1, cidx_3=0x1, cidx_2=0x1,
                                       cidx_1=0x1, cidx_0=0x1, cidx_15=0x1, cidx_14=0x1, cidx_13=0x1, cidx_12=0x1,
                                       cidx_11=0x1, cidx_10=0x1, cidx_9=0x1, cidx_8=0x1, cidx_23=0x1, cidx_22=0x1,
                                       cidx_21=0x1, cidx_20=0x1, cidx_19=0x1, cidx_18=0x1, cidx_17=0x1, cidx_16=0x1,
                                       cidx_31=0x1, cidx_30=0x1, cidx_29=0x1, cidx_28=0x1, cidx_27=0x1, cidx_26=0x1,
                                       cidx_25=0x1, cidx_24=0x1, cidx_39=0x1, cidx_38=0x1, cidx_37=0x1, cidx_36=0x1,
                                       cidx_35=0x1, cidx_34=0x1, cidx_33=0x1, cidx_32=0x1, cidx_47=0x1, cidx_46=0x1,
                                       cidx_45=0x1, cidx_44=0x1, cidx_43=0x1, cidx_42=0x1, cidx_41=0x1, cidx_40=0x1,
                                       cidx_55=0x1, cidx_54=0x1, cidx_53=0x1, cidx_52=0x1, cidx_51=0x1, cidx_50=0x1,
                                       cidx_49=0x1, cidx_48=0x1, cidx_63=0x1, cidx_62=0x1, cidx_61=0x1, cidx_60=0x1,
                                       cidx_59=0x1, cidx_58=0x1, cidx_57=0x1, cidx_56=0x1, cidx_71=0x1, cidx_70=0x1,
                                       cidx_69=0x1, cidx_68=0x1, cidx_67=0x1, cidx_66=0x1, cidx_65=0x1, cidx_64=0x1,
                                       cidx_79=0x1, cidx_78=0x1, cidx_77=0x1, cidx_76=0x1, cidx_75=0x1, cidx_74=0x1,
                                       cidx_73=0x1, cidx_72=0x1, cidx_87=0x1, cidx_86=0x1, cidx_85=0x1, cidx_84=0x1,
                                       cidx_83=0x1, cidx_82=0x1, cidx_81=0x1, cidx_80=0x1, cidx_95=0x1, cidx_94=0x1,
                                       cidx_93=0x1, cidx_92=0x1, cidx_91=0x1, cidx_90=0x1, cidx_89=0x1, cidx_88=0x1,
                                       cidx_103=0x1, cidx_102=0x1, cidx_101=0x1, cidx_100=0x1, cidx_99=0x1, cidx_98=0x1,
                                       cidx_97=0x1, cidx_96=0x1, cidx_111=0x1, cidx_110=0x1, cidx_109=0x1, cidx_108=0x1,
                                       cidx_107=0x1, cidx_106=0x1, cidx_105=0x1, cidx_104=0x1, cidx_119=0x1,
                                       cidx_118=0x1, cidx_117=0x1, cidx_116=0x1, cidx_115=0x1, cidx_114=0x1,
                                       cidx_113=0x1, cidx_112=0x1, cidx_127=0x1, cidx_126=0x1, cidx_125=0x1,
                                       cidx_124=0x1, cidx_123=0x1, cidx_122=0x1, cidx_121=0x1, cidx_120=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_disabled_controls

    @staticmethod
    def test_set_disabled_controls_response():
        """
        Test ``SetDisabledControlsResponse`` class instantiation
        """
        my_class = SetDisabledControlsResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetDisabledControlsResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_disabled_controls_response

    @staticmethod
    def test_get_game_mode():
        """
        Test ``GetGameMode`` class instantiation
        """
        my_class = GetGameMode(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetGameMode(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_game_mode

    @staticmethod
    def test_get_game_mode_response():
        """
        Test ``GetGameModeResponse`` class instantiation
        """
        my_class = GetGameModeResponse(device_index=0, feature_index=0,
                                       lock_supported=0,
                                       supported=0,
                                       locked=0,
                                       enabled=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetGameModeResponse(device_index=0xff, feature_index=0xff,
                                       lock_supported=0x1,
                                       supported=0x1,
                                       locked=0x1,
                                       enabled=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_game_mode_response

    @staticmethod
    def test_get_set_power_on_params():
        """
        Test ``GetSetPowerOnParams`` class instantiation
        """
        my_class = GetSetPowerOnParams(device_index=0, feature_index=0,
                                       poweron_game_mode_lock_valid=0,
                                       poweron_game_mode_valid=0,
                                       poweron_game_mode_lock=0,
                                       poweron_game_mode=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetSetPowerOnParams(device_index=0xFF, feature_index=0xFF,
                                       poweron_game_mode_lock_valid=0x1,
                                       poweron_game_mode_valid=0x1,
                                       poweron_game_mode_lock=0x1,
                                       poweron_game_mode=0x1)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_set_power_on_params

    @staticmethod
    def test_get_set_power_on_params_response():
        """
        Test ``GetSetPowerOnParamsResponse`` class instantiation
        """
        my_class = GetSetPowerOnParamsResponse(device_index=0, feature_index=0,
                                               poweron_game_mode_lock=0,
                                               poweron_game_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetSetPowerOnParamsResponse(device_index=0xFF, feature_index=0xFF,
                                               poweron_game_mode_lock=0x1,
                                               poweron_game_mode=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_set_power_on_params_response

    @staticmethod
    def test_get_capabilities():
        """
        Test ``GetCapabilities`` class instantiation
        """
        my_class = GetCapabilities(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetCapabilities(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_capabilities

    @staticmethod
    def test_get_capabilities_response():
        """
        Test ``GetCapabilitiesResponse`` class instantiation
        """
        my_class = GetCapabilitiesResponse(device_index=0, feature_index=0,
                                           poweron_game_mode_lock=0,
                                           poweron_game_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponse(device_index=0xFF, feature_index=0xFF,
                                           poweron_game_mode_lock=0x1,
                                           poweron_game_mode=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response

    @staticmethod
    def test_game_mode_event():
        """
        Test ``GameModeEvent`` class instantiation
        """
        my_class = GameModeEvent(device_index=0, feature_index=0,
                                 locked=0,
                                 enabled=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GameModeEvent(device_index=0xff, feature_index=0xff,
                                 locked=0x1,
                                 enabled=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_game_mode_event
# end class DisableControlsByCIDXInstantiationTestCase


class DisableControlsByCIDXTestCase(TestCase):
    """
    Test ``DisableControlsByCIDX`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            DisableControlsByCIDXV0.VERSION: {
                "cls": DisableControlsByCIDXV0,
                "interfaces": {
                    "set_disabled_controls_cls": SetDisabledControls,
                    "set_disabled_controls_response_cls": SetDisabledControlsResponse,
                    "get_game_mode_cls": GetGameMode,
                    "get_game_mode_response_cls": GetGameModeResponse,
                    "game_mode_event_cls": GameModeEvent,
                },
                "max_function_index": 1
            },
            DisableControlsByCIDXV1.VERSION: {
                "cls": DisableControlsByCIDXV1,
                "interfaces": {
                    "set_disabled_controls_cls": SetDisabledControls,
                    "set_disabled_controls_response_cls": SetDisabledControlsResponse,
                    "get_game_mode_cls": GetGameMode,
                    "get_game_mode_response_cls": GetGameModeResponse,
                    "get_set_power_on_params_cls": GetSetPowerOnParams,
                    "get_set_power_on_params_response_cls": GetSetPowerOnParamsResponse,
                    "get_capabilities_cls": GetCapabilities,
                    "get_capabilities_response_cls": GetCapabilitiesResponse,
                    "game_mode_event_cls": GameModeEvent,
                },
                "max_function_index": 3
            },
        }
        cls.max_version = 1
    # end def setUpClass

    def test_factory(self):
        """
        Test ``DisableControlsByCIDXFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(DisableControlsByCIDXFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``DisableControlsByCIDXFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [2, 3]:
            with self.assertRaises(KeyError):
                DisableControlsByCIDXFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``DisableControlsByCIDXFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = DisableControlsByCIDXFactory.create(version)
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
            obj = DisableControlsByCIDXFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class DisableControlsByCIDXTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
