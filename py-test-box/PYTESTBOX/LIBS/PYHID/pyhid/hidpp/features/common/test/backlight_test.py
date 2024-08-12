#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.common.test.backlight_test
:brief: HID++ 2.0 ``Backlight`` test module
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/09/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.backlight import Backlight
from pyhid.hidpp.features.common.backlight import BacklightFactory
from pyhid.hidpp.features.common.backlight import BacklightInfoEventV1
from pyhid.hidpp.features.common.backlight import BacklightInfoEventV2ToV4
from pyhid.hidpp.features.common.backlight import BacklightV1
from pyhid.hidpp.features.common.backlight import BacklightV2
from pyhid.hidpp.features.common.backlight import BacklightV3
from pyhid.hidpp.features.common.backlight import BacklightV4
from pyhid.hidpp.features.common.backlight import GetBacklightConfig
from pyhid.hidpp.features.common.backlight import GetBacklightConfigResponseV1
from pyhid.hidpp.features.common.backlight import GetBacklightConfigResponseV2
from pyhid.hidpp.features.common.backlight import GetBacklightConfigResponseV3
from pyhid.hidpp.features.common.backlight import GetBacklightConfigResponseV4
from pyhid.hidpp.features.common.backlight import GetBacklightInfo
from pyhid.hidpp.features.common.backlight import GetBacklightInfoResponseV1
from pyhid.hidpp.features.common.backlight import GetBacklightInfoResponseV2
from pyhid.hidpp.features.common.backlight import GetBacklightInfoResponseV3
from pyhid.hidpp.features.common.backlight import GetBacklightInfoResponseV4
from pyhid.hidpp.features.common.backlight import SetBacklightConfigResponse
from pyhid.hidpp.features.common.backlight import SetBacklightConfigV1
from pyhid.hidpp.features.common.backlight import SetBacklightConfigV2
from pyhid.hidpp.features.common.backlight import SetBacklightConfigV3
from pyhid.hidpp.features.common.backlight import SetBacklightConfigV4
from pyhid.hidpp.features.common.backlight import SetBacklightEffect
from pyhid.hidpp.features.common.backlight import SetBacklightEffectResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BacklightInstantiationTestCase(TestCase):
    """
    Test ``Backlight`` testing classes instantiations
    """

    @staticmethod
    def test_backlight():
        """
        Test ``Backlight`` class instantiation
        """
        my_class = Backlight(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = Backlight(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_backlight

    @staticmethod
    def test_get_backlight_config():
        """
        Test ``GetBacklightConfig`` class instantiation
        """
        my_class = GetBacklightConfig(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetBacklightConfig(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_backlight_config

    @staticmethod
    def test_get_backlight_config_response_v1():
        """
        Test ``GetBacklightConfigResponseV1`` class instantiation
        """
        my_class = GetBacklightConfigResponseV1(device_index=0, feature_index=0, configuration=0, supported_options=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetBacklightConfigResponseV1(device_index=0xff, feature_index=0xff, configuration=0xff,
                                                supported_options=0xffff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_backlight_config_response

    @staticmethod
    def test_get_backlight_config_response_v2():
        """
        Test ``GetBacklightConfigResponseV2`` class instantiation
        """
        my_class = GetBacklightConfigResponseV2(device_index=0, feature_index=0,
                                                configuration=0,
                                                supported_options=0,
                                                backlight_effect_list=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetBacklightConfigResponseV2(device_index=0xff, feature_index=0xff,
                                                configuration=0xff,
                                                supported_options=0xffff,
                                                backlight_effect_list=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_backlight_config_response_v2

    @staticmethod
    def test_get_backlight_config_response_v3():
        """
        Test ``GetBacklightConfigResponseV3`` class instantiation
        """
        my_class = GetBacklightConfigResponseV3(device_index=0, feature_index=0, configuration=0, supported_options=0,
                                                backlight_effect_list=0, current_backlight_level=0,
                                                curr_duration_hands_out=0, curr_duration_hands_in=0,
                                                curr_duration_powered=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetBacklightConfigResponseV3(device_index=0xff, feature_index=0xff, configuration=0xff,
                                                supported_options=0xffff, backlight_effect_list=0xffff,
                                                current_backlight_level=0xff, curr_duration_hands_out=0xffff,
                                                curr_duration_hands_in=0xffff, curr_duration_powered=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_backlight_config_response_v3

    @staticmethod
    def test_get_backlight_config_response_v4():
        """
        Test ``GetBacklightConfigResponseV4`` class instantiation
        """
        my_class = GetBacklightConfigResponseV4(device_index=0, feature_index=0, configuration=0, supported_options=0,
                                                backlight_effect_list=0, current_backlight_level=0,
                                                curr_duration_hands_out=0, curr_duration_hands_in=0,
                                                curr_duration_powered=0, curr_duration_not_powered=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetBacklightConfigResponseV4(device_index=0xff, feature_index=0xff, configuration=0xff,
                                                supported_options=0xffff, backlight_effect_list=0xffff,
                                                current_backlight_level=0xff, curr_duration_hands_out=0xffff,
                                                curr_duration_hands_in=0xffff, curr_duration_powered=0xffff,
                                                curr_duration_not_powered=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_backlight_config_response_v4

    @staticmethod
    def test_set_backlight_config_v1():
        """
        Test ``SetBacklightConfigV1`` class instantiation
        """
        my_class = SetBacklightConfigV1(device_index=0, feature_index=0, configuration=0, options=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetBacklightConfigV1(device_index=0xff, feature_index=0xff, configuration=0xff, options=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_backlight_config_v1

    @staticmethod
    def test_set_backlight_config_v2():
        """
        Test ``SetBacklightConfigV2`` class instantiation
        """
        my_class = SetBacklightConfigV2(device_index=0, feature_index=0,
                                        configuration=0,
                                        options=0,
                                        backlight_effect=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetBacklightConfigV2(device_index=0xff, feature_index=0xff,
                                        configuration=0xff,
                                        options=0xff,
                                        backlight_effect=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_backlight_config_v2

    @staticmethod
    def test_set_backlight_config_v3():
        """
        Test ``SetBacklightConfigV3`` class instantiation
        """
        my_class = SetBacklightConfigV3(device_index=0, feature_index=0, configuration=0, options=0, backlight_effect=0,
                                        current_backlight_level=0, curr_duration_hands_out=0, curr_duration_hands_in=0,
                                        curr_duration_powered=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetBacklightConfigV3(device_index=0xff, feature_index=0xff, configuration=0xff, options=0xff,
                                        backlight_effect=0xff, current_backlight_level=0xff,
                                        curr_duration_hands_out=0xffff, curr_duration_hands_in=0xffff,
                                        curr_duration_powered=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_backlight_config_v3

    @staticmethod
    def test_set_backlight_config_v4():
        """
        Test ``SetBacklightConfigV4`` class instantiation
        """
        my_class = SetBacklightConfigV4(device_index=0, feature_index=0, configuration=0, options=0, backlight_effect=0,
                                        current_backlight_level=0, curr_duration_hands_out=0, curr_duration_hands_in=0,
                                        curr_duration_powered=0, curr_duration_not_powered=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetBacklightConfigV4(device_index=0xff, feature_index=0xff, configuration=0xff, options=0xff,
                                        backlight_effect=0xff, current_backlight_level=0xff,
                                        curr_duration_hands_out=0xffff, curr_duration_hands_in=0xffff,
                                        curr_duration_powered=0xffff, curr_duration_not_powered=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_backlight_config_v4

    @staticmethod
    def test_set_backlight_config_response():
        """
        Test ``SetBacklightConfigResponse`` class instantiation
        """
        my_class = SetBacklightConfigResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetBacklightConfigResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_backlight_config_response

    @staticmethod
    def test_get_backlight_info():
        """
        Test ``GetBacklightInfo`` class instantiation
        """
        my_class = GetBacklightInfo(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetBacklightInfo(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_backlight_info

    @staticmethod
    def test_get_backlight_info_response_v1():
        """
        Test ``GetBacklightInfoResponseV1`` class instantiation
        """
        my_class = GetBacklightInfoResponseV1(device_index=0, feature_index=0, number_of_level=0, current_level=0,
                                              backlight_status=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetBacklightInfoResponseV1(device_index=0xff, feature_index=0xff, number_of_level=0xff,
                                              current_level=0xff, backlight_status=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_backlight_info_response_v1

    @staticmethod
    def test_get_backlight_info_response_v2():
        """
        Test ``GetBacklightInfoResponseV2`` class instantiation
        """
        my_class = GetBacklightInfoResponseV2(device_index=0, feature_index=0,
                                              number_of_level=0,
                                              current_level=0,
                                              backlight_status=0,
                                              backlight_effect=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetBacklightInfoResponseV2(device_index=0xff, feature_index=0xff,
                                              number_of_level=0xff,
                                              current_level=0xff,
                                              backlight_status=0xff,
                                              backlight_effect=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_backlight_info_response_v2

    @staticmethod
    def test_get_backlight_info_response_v3():
        """
        Test ``GetBacklightInfoResponseV3`` class instantiation
        """
        my_class = GetBacklightInfoResponseV3(device_index=0, feature_index=0, number_of_level=0, current_level=0,
                                              backlight_status=0, backlight_effect=0, oob_duration_hands_out=0,
                                              oob_duration_hands_in=0, oob_duration_powered=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetBacklightInfoResponseV3(device_index=0xff, feature_index=0xff, number_of_level=0xff,
                                              current_level=0xff, backlight_status=0xff, backlight_effect=0xff,
                                              oob_duration_hands_out=0xffff, oob_duration_hands_in=0xffff,
                                              oob_duration_powered=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_backlight_info_response_v3

    @staticmethod
    def test_get_backlight_info_response_v4():
        """
        Test ``GetBacklightInfoResponseV4`` class instantiation
        """
        my_class = GetBacklightInfoResponseV4(device_index=0, feature_index=0, number_of_level=0, current_level=0,
                                              backlight_status=0, backlight_effect=0, oob_duration_hands_out=0,
                                              oob_duration_hands_in=0, oob_duration_powered=0,
                                              oob_duration_not_powered=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetBacklightInfoResponseV4(device_index=0xff, feature_index=0xff, number_of_level=0xff,
                                              current_level=0xff, backlight_status=0xff, backlight_effect=0xff,
                                              oob_duration_hands_out=0xffff, oob_duration_hands_in=0xffff,
                                              oob_duration_powered=0xffff, oob_duration_not_powered=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_backlight_info_response_v4

    @staticmethod
    def test_set_backlight_effect():
        """
        Test ``SetBacklightEffect`` class instantiation
        """
        my_class = SetBacklightEffect(device_index=0, feature_index=0,
                                      backlight_effect=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetBacklightEffect(device_index=0xff, feature_index=0xff,
                                      backlight_effect=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_backlight_effect

    @staticmethod
    def test_set_backlight_effect_response():
        """
        Test ``SetBacklightEffectResponse`` class instantiation
        """
        my_class = SetBacklightEffectResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetBacklightEffectResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_backlight_effect_response

    @staticmethod
    def test_backlight_info_event_v1():
        """
        Test ``BacklightInfoEventV1`` class instantiation
        """
        my_class = BacklightInfoEventV1(device_index=0, feature_index=0, number_of_level=0, current_level=0,
                                        backlight_status=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = BacklightInfoEventV1(device_index=0xff, feature_index=0xff, number_of_level=0xff, current_level=0xff,
                                        backlight_status=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_backlight_info_event_v1

    @staticmethod
    def test_backlight_info_event_v2_to_v4():
        """
        Test ``BacklightInfoEventV2ToV4`` class instantiation
        """
        my_class = BacklightInfoEventV2ToV4(device_index=0, feature_index=0,
                                            number_of_level=0,
                                            current_level=0,
                                            backlight_status=0,
                                            backlight_effect=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = BacklightInfoEventV2ToV4(device_index=0xff, feature_index=0xff,
                                            number_of_level=HexList('FF' * (BacklightInfoEventV2ToV4.LEN.NUMBER_OF_LEVEL // 8)),
                                            current_level=HexList('FF' * (BacklightInfoEventV2ToV4.LEN.CURRENT_LEVEL // 8)),
                                            backlight_status=HexList('FF' * (BacklightInfoEventV2ToV4.LEN.BACKLIGHT_STATUS // 8)),
                                            backlight_effect=HexList('FF' * (BacklightInfoEventV2ToV4.LEN.BACKLIGHT_EFFECT // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_backlight_info_event_v2_to_v4
# end class BacklightInstantiationTestCase


class BacklightTestCase(TestCase):
    """
    Test ``Backlight`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            BacklightV1.VERSION: {
                "cls": BacklightV1,
                "interfaces": {
                    "get_backlight_config_cls": GetBacklightConfig,
                    "get_backlight_config_response_cls": GetBacklightConfigResponseV1,
                    "set_backlight_config_cls": SetBacklightConfigV1,
                    "set_backlight_config_response_cls": SetBacklightConfigResponse,
                    "get_backlight_info_cls": GetBacklightInfo,
                    "get_backlight_info_response_cls": GetBacklightInfoResponseV1,
                    "backlight_info_event_cls": BacklightInfoEventV1,
                },
                "max_function_index": 2
            },
            BacklightV2.VERSION: {
                "cls": BacklightV2,
                "interfaces": {
                    "get_backlight_config_cls": GetBacklightConfig,
                    "get_backlight_config_response_cls": GetBacklightConfigResponseV2,
                    "set_backlight_config_cls": SetBacklightConfigV2,
                    "set_backlight_config_response_cls": SetBacklightConfigResponse,
                    "get_backlight_info_cls": GetBacklightInfo,
                    "get_backlight_info_response_cls": GetBacklightInfoResponseV2,
                    "set_backlight_effect_cls": SetBacklightEffect,
                    "set_backlight_effect_response_cls": SetBacklightEffectResponse,
                    "backlight_info_event_cls": BacklightInfoEventV2ToV4,
                },
                "max_function_index": 3
            },
            BacklightV3.VERSION: {
                "cls": BacklightV3,
                "interfaces": {
                    "get_backlight_config_cls": GetBacklightConfig,
                    "get_backlight_config_response_cls": GetBacklightConfigResponseV3,
                    "set_backlight_config_cls": SetBacklightConfigV3,
                    "set_backlight_config_response_cls": SetBacklightConfigResponse,
                    "get_backlight_info_cls": GetBacklightInfo,
                    "get_backlight_info_response_cls": GetBacklightInfoResponseV3,
                    "set_backlight_effect_cls": SetBacklightEffect,
                    "set_backlight_effect_response_cls": SetBacklightEffectResponse,
                    "backlight_info_event_cls": BacklightInfoEventV2ToV4,
                },
                "max_function_index": 3
            },
            BacklightV4.VERSION: {
                "cls": BacklightV4,
                "interfaces": {
                    "get_backlight_config_cls": GetBacklightConfig,
                    "get_backlight_config_response_cls": GetBacklightConfigResponseV4,
                    "set_backlight_config_cls": SetBacklightConfigV4,
                    "set_backlight_config_response_cls": SetBacklightConfigResponse,
                    "get_backlight_info_cls": GetBacklightInfo,
                    "get_backlight_info_response_cls": GetBacklightInfoResponseV4,
                    "set_backlight_effect_cls": SetBacklightEffect,
                    "set_backlight_effect_response_cls": SetBacklightEffectResponse,
                    "backlight_info_event_cls": BacklightInfoEventV2ToV4,
                },
                "max_function_index": 3
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``BacklightFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(BacklightFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``BacklightFactory`` using out of range versions
        """
        for version in [5, 6]:
            with self.assertRaises(KeyError):
                BacklightFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``BacklightFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = BacklightFactory.create(version)
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
        """
        for version, expected in self.expected.items():
            obj = BacklightFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class BacklightTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
