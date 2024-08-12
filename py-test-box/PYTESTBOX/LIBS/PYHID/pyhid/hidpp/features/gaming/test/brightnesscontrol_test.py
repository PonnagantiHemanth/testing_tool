#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.gaming.test.brightnesscontrol_test
:brief: HID++ 2.0 ``BrightnessControl`` test module
:author: YY Liu <yliu5@logitech.com>
:date: 2023/08/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.gaming.brightnesscontrol import BrightnessChangeEvent
from pyhid.hidpp.features.gaming.brightnesscontrol import BrightnessControl
from pyhid.hidpp.features.gaming.brightnesscontrol import BrightnessControlFactory
from pyhid.hidpp.features.gaming.brightnesscontrol import BrightnessControlV0
from pyhid.hidpp.features.gaming.brightnesscontrol import BrightnessControlV1
from pyhid.hidpp.features.gaming.brightnesscontrol import GetBrightness
from pyhid.hidpp.features.gaming.brightnesscontrol import GetBrightnessResponse
from pyhid.hidpp.features.gaming.brightnesscontrol import GetIllumination
from pyhid.hidpp.features.gaming.brightnesscontrol import GetIlluminationResponse
from pyhid.hidpp.features.gaming.brightnesscontrol import GetInfo
from pyhid.hidpp.features.gaming.brightnesscontrol import GetInfoResponseV0
from pyhid.hidpp.features.gaming.brightnesscontrol import GetInfoResponseV1
from pyhid.hidpp.features.gaming.brightnesscontrol import IlluminationChangeEvent
from pyhid.hidpp.features.gaming.brightnesscontrol import SetBrightness
from pyhid.hidpp.features.gaming.brightnesscontrol import SetBrightnessResponse
from pyhid.hidpp.features.gaming.brightnesscontrol import SetIllumination
from pyhid.hidpp.features.gaming.brightnesscontrol import SetIlluminationResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BrightnessControlInstantiationTestCase(TestCase):
    """
    Test ``BrightnessControl`` testing classes instantiations
    """

    @staticmethod
    def test_brightness_control():
        """
        Test ``BrightnessControl`` class instantiation
        """
        my_class = BrightnessControl(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = BrightnessControl(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_brightness_control

    @staticmethod
    def test_get_info():
        """
        Test ``GetInfo`` class instantiation
        """
        my_class = GetInfo(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetInfo(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_info

    @staticmethod
    def test_get_brightness():
        """
        Test ``GetBrightness`` class instantiation
        """
        my_class = GetBrightness(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetBrightness(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_brightness

    @staticmethod
    def test_set_brightness():
        """
        Test ``SetBrightness`` class instantiation
        """
        my_class = SetBrightness(device_index=0, feature_index=0,
                                 brightness=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetBrightness(device_index=0xFF, feature_index=0xFF,
                                 brightness=HexList("FF" * (SetBrightness.LEN.BRIGHTNESS // 8)))

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_brightness

    @staticmethod
    def test_get_illumination():
        """
        Test ``GetIllumination`` class instantiation
        """
        my_class = GetIllumination(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetIllumination(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_illumination

    @staticmethod
    def test_set_illumination():
        """
        Test ``SetIllumination`` class instantiation
        """
        my_class = SetIllumination(device_index=0, feature_index=0,
                                   state=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetIllumination(device_index=0xFF, feature_index=0xFF,
                                   state=0x1)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_illumination

    @staticmethod
    def test_get_info_response_v0():
        """
        Test ``GetInfoResponseV0`` class instantiation
        """
        my_class = GetInfoResponseV0(device_index=0, feature_index=0,
                                     max_brightness=0,
                                     steps=0,
                                     events=0,
                                     hw_brightness=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetInfoResponseV0(device_index=0xFF, feature_index=0xFF,
                                     max_brightness=HexList("FF" * (GetInfoResponseV0.LEN.MAX_BRIGHTNESS // 8)),
                                     steps=0xFF,
                                     events=0x1,
                                     hw_brightness=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_info_response_v0

    @staticmethod
    def test_get_info_response_v1():
        """
        Test ``GetInfoResponseV1`` class instantiation
        """
        my_class = GetInfoResponseV1(device_index=0, feature_index=0,
                                     max_brightness=0,
                                     steps_lsb=0,
                                     transient=0,
                                     hw_on_off=0,
                                     illumination=0,
                                     events=0,
                                     hw_brightness=0,
                                     min_brightness=0,
                                     steps_msb=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetInfoResponseV1(device_index=0xFF, feature_index=0xFF,
                                     max_brightness=HexList("FF" * (GetInfoResponseV1.LEN.MAX_BRIGHTNESS // 8)),
                                     steps_lsb=0xFF,
                                     transient=0x1,
                                     hw_on_off=0x1,
                                     illumination=0x1,
                                     events=0x1,
                                     hw_brightness=0x1,
                                     min_brightness=HexList("FF" * (GetInfoResponseV1.LEN.MIN_BRIGHTNESS // 8)),
                                     steps_msb=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_info_response_v1

    @staticmethod
    def test_get_brightness_response():
        """
        Test ``GetBrightnessResponse`` class instantiation
        """
        my_class = GetBrightnessResponse(device_index=0, feature_index=0,
                                         brightness=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetBrightnessResponse(device_index=0xFF, feature_index=0xFF,
                                         brightness=HexList("FF" * (GetBrightnessResponse.LEN.BRIGHTNESS // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_brightness_response

    @staticmethod
    def test_set_brightness_response():
        """
        Test ``SetBrightnessResponse`` class instantiation
        """
        my_class = SetBrightnessResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetBrightnessResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_brightness_response

    @staticmethod
    def test_get_illumination_response():
        """
        Test ``GetIlluminationResponse`` class instantiation
        """
        my_class = GetIlluminationResponse(device_index=0, feature_index=0,
                                           state=0x0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetIlluminationResponse(device_index=0xFF, feature_index=0xFF,
                                           state=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_illumination_response

    @staticmethod
    def test_set_illumination_response():
        """
        Test ``SetIlluminationResponse`` class instantiation
        """
        my_class = SetIlluminationResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetIlluminationResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_illumination_response

    @staticmethod
    def test_brightness_change_event():
        """
        Test ``BrightnessChangeEvent`` class instantiation
        """
        my_class = BrightnessChangeEvent(device_index=0, feature_index=0,
                                         brightness=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = BrightnessChangeEvent(device_index=0xFF, feature_index=0xFF,
                                         brightness=HexList("FF" * (BrightnessChangeEvent.LEN.BRIGHTNESS // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_brightness_change_event

    @staticmethod
    def test_illumination_change_event():
        """
        Test ``IlluminationChangeEvent`` class instantiation
        """
        my_class = IlluminationChangeEvent(device_index=0, feature_index=0,
                                           state=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = IlluminationChangeEvent(device_index=0xFF, feature_index=0xFF,
                                           state=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_illumination_change_event
# end class BrightnessControlInstantiationTestCase


class BrightnessControlTestCase(TestCase):
    """
    Test ``BrightnessControl`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            BrightnessControlV0.VERSION: {
                "cls": BrightnessControlV0,
                "interfaces": {
                    "get_info_cls": GetInfo,
                    "get_info_response_cls": GetInfoResponseV0,
                    "get_brightness_cls": GetBrightness,
                    "get_brightness_response_cls": GetBrightnessResponse,
                    "set_brightness_cls": SetBrightness,
                    "set_brightness_response_cls": SetBrightnessResponse,
                    "brightness_change_event_cls": BrightnessChangeEvent,
                },
                "max_function_index": 2
            },
            BrightnessControlV1.VERSION: {
                "cls": BrightnessControlV1,
                "interfaces": {
                    "get_info_cls": GetInfo,
                    "get_info_response_cls": GetInfoResponseV1,
                    "get_brightness_cls": GetBrightness,
                    "get_brightness_response_cls": GetBrightnessResponse,
                    "set_brightness_cls": SetBrightness,
                    "set_brightness_response_cls": SetBrightnessResponse,
                    "get_illumination_cls": GetIllumination,
                    "get_illumination_response_cls": GetIlluminationResponse,
                    "set_illumination_cls": SetIllumination,
                    "set_illumination_response_cls": SetIlluminationResponse,
                    "brightness_change_event_cls": BrightnessChangeEvent,
                    "illumination_change_event_cls": IlluminationChangeEvent,
                },
                "max_function_index": 4
            },
        }
        cls.max_version = 1
    # end def setUpClass

    def test_factory(self):
        """
        Test ``BrightnessControlFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(BrightnessControlFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``BrightnessControlFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                BrightnessControlFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``BrightnessControlFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = BrightnessControlFactory.create(version)
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
            obj = BrightnessControlFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class BrightnessControlTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
