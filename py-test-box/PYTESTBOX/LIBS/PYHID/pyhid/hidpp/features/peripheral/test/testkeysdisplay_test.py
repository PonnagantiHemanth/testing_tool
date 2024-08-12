#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.peripheral.test.testkeysdisplay_test
:brief: HID++ 2.0 ``TestKeysDisplay`` test module
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.peripheral.testkeysdisplay import GetCapabilities
from pyhid.hidpp.features.peripheral.testkeysdisplay import GetCapabilitiesResponse
from pyhid.hidpp.features.peripheral.testkeysdisplay import KeyPressEvent
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetBacklightPWMDutyCycle
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetBacklightPWMDutyCycleResponse
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetDisplayAgeingModeState
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetDisplayAgeingModeStateResponse
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetDisplayPowerState
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetDisplayPowerStateResponse
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetDisplayRGBValue
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetDisplayRGBValueResponse
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetKeyCalibrationOffset
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetKeyCalibrationOffsetInFlash
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetKeyCalibrationOffsetInFlashResponse
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetKeyCalibrationOffsetResponse
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetKeyIcon
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetKeyIconResponse
from pyhid.hidpp.features.peripheral.testkeysdisplay import TestKeysDisplay
from pyhid.hidpp.features.peripheral.testkeysdisplay import TestKeysDisplayFactory
from pyhid.hidpp.features.peripheral.testkeysdisplay import TestKeysDisplayV0
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TestKeysDisplayInstantiationTestCase(TestCase):
    """
    Test ``TestKeysDisplay`` testing classes instantiations
    """

    @staticmethod
    def test_test_keys_display():
        """
        Test ``TestKeysDisplay`` class instantiation
        """
        my_class = TestKeysDisplay(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = TestKeysDisplay(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_test_keys_display

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
    def test_set_backlight_pwm_duty_cycle():
        """
        Test ``SetBacklightPWMDutyCycle`` class instantiation
        """
        my_class = SetBacklightPWMDutyCycle(device_index=0, feature_index=0,
                                            duty_pwm=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetBacklightPWMDutyCycle(device_index=0xFF, feature_index=0xFF,
                                            duty_pwm=0xFFFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_backlight_pwm_duty_cycle

    @staticmethod
    def test_set_display_rgb_value():
        """
        Test ``SetDisplayRGBValue`` class instantiation
        """
        my_class = SetDisplayRGBValue(device_index=0, feature_index=0,
                                      rgb_value=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetDisplayRGBValue(device_index=0xFF, feature_index=0xFF,
                                      rgb_value=0xFFFFFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_display_rgb_value

    @staticmethod
    def test_set_display_power_state():
        """
        Test ``SetDisplayPowerState`` class instantiation
        """
        my_class = SetDisplayPowerState(device_index=0, feature_index=0,
                                        power_state=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetDisplayPowerState(device_index=0xFF, feature_index=0xFF,
                                        power_state=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_display_power_state

    @staticmethod
    def test_set_key_icon():
        """
        Test ``SetKeyIcon`` class instantiation
        """
        my_class = SetKeyIcon(device_index=0, feature_index=0,
                              key_column=0,
                              key_row=0,
                              icon_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetKeyIcon(device_index=0xFF, feature_index=0xFF,
                              key_column=0xFF,
                              key_row=0xFF,
                              icon_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_key_icon

    @staticmethod
    def test_set_key_calibration_offset():
        """
        Test ``SetKeyCalibrationOffset`` class instantiation
        """
        my_class = SetKeyCalibrationOffset(device_index=0, feature_index=0,
                                           key_column=0,
                                           key_row=0,
                                           x_offset=0,
                                           y_offset=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetKeyCalibrationOffset(device_index=0xFF, feature_index=0xFF,
                                           key_column=0xFF,
                                           key_row=0xFF,
                                           x_offset=0xFF,
                                           y_offset=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_key_calibration_offset

    @staticmethod
    def test_set_key_calibration_offset_in_flash():
        """
        Test ``SetKeyCalibrationOffsetInFlash`` class instantiation
        """
        my_class = SetKeyCalibrationOffsetInFlash(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetKeyCalibrationOffsetInFlash(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_key_calibration_offset_in_flash

    @staticmethod
    def test_set_display_ageing_mode_state():
        """
        Test ``SetDisplayAgeingModeState`` class instantiation
        """
        my_class = SetDisplayAgeingModeState(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetDisplayAgeingModeState(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_display_ageing_mode_state

    @staticmethod
    def test_get_capabilities_response():
        """
        Test ``GetCapabilitiesResponse`` class instantiation
        """
        my_class = GetCapabilitiesResponse(device_index=0, feature_index=0,
                                           capabilities=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponse(device_index=0xFF, feature_index=0xFF,
                                           capabilities=HexList("FF" * (GetCapabilitiesResponse.LEN.CAPABILITIES // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response

    @staticmethod
    def test_set_backlight_pwm_duty_cycle_response():
        """
        Test ``SetBacklightPWMDutyCycleResponse`` class instantiation
        """
        my_class = SetBacklightPWMDutyCycleResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetBacklightPWMDutyCycleResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_backlight_pwm_duty_cycle_response

    @staticmethod
    def test_set_display_rgb_value_response():
        """
        Test ``SetDisplayRGBValueResponse`` class instantiation
        """
        my_class = SetDisplayRGBValueResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetDisplayRGBValueResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_display_rgb_value_response

    @staticmethod
    def test_set_display_power_state_response():
        """
        Test ``SetDisplayPowerStateResponse`` class instantiation
        """
        my_class = SetDisplayPowerStateResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetDisplayPowerStateResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_display_power_state_response

    @staticmethod
    def test_set_key_icon_response():
        """
        Test ``SetKeyIconResponse`` class instantiation
        """
        my_class = SetKeyIconResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetKeyIconResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_key_icon_response

    @staticmethod
    def test_set_key_calibration_offset_response():
        """
        Test ``SetKeyCalibrationOffsetResponse`` class instantiation
        """
        my_class = SetKeyCalibrationOffsetResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetKeyCalibrationOffsetResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_key_calibration_offset_response

    @staticmethod
    def test_set_key_calibration_offset_in_flash_response():
        """
        Test ``SetKeyCalibrationOffsetInFlashResponse`` class instantiation
        """
        my_class = SetKeyCalibrationOffsetInFlashResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetKeyCalibrationOffsetInFlashResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_key_calibration_offset_in_flash_response

    @staticmethod
    def test_set_display_ageing_mode_state_response():
        """
        Test ``SetDisplayAgeingModeStateResponse`` class instantiation
        """
        my_class = SetDisplayAgeingModeStateResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetDisplayAgeingModeStateResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_display_ageing_mode_state_response

    @staticmethod
    def test_key_press_event():
        """
        Test ``KeyPressEvent`` class instantiation
        """
        my_class = KeyPressEvent(device_index=0, feature_index=0,
                                 btn7=False,
                                 btn6=False,
                                 btn5=False,
                                 btn4=False,
                                 btn3=False,
                                 btn2=False,
                                 btn1=False,
                                 btn0=False,
                                 btn15=False,
                                 btn14=False,
                                 btn13=False,
                                 btn12=False,
                                 btn11=False,
                                 btn10=False,
                                 btn9=False,
                                 btn8=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = KeyPressEvent(device_index=0xFF, feature_index=0xFF,
                                 btn7=True,
                                 btn6=True,
                                 btn5=True,
                                 btn4=True,
                                 btn3=True,
                                 btn2=True,
                                 btn1=True,
                                 btn0=True,
                                 btn15=True,
                                 btn14=True,
                                 btn13=True,
                                 btn12=True,
                                 btn11=True,
                                 btn10=True,
                                 btn9=True,
                                 btn8=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_key_press_event
# end class TestKeysDisplayInstantiationTestCase


class TestKeysDisplayTestCase(TestCase):
    """
    Test ``TestKeysDisplay`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            TestKeysDisplayV0.VERSION: {
                "cls": TestKeysDisplayV0,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilities,
                    "get_capabilities_response_cls": GetCapabilitiesResponse,
                    "set_backlight_pwm_duty_cycle_cls": SetBacklightPWMDutyCycle,
                    "set_backlight_pwm_duty_cycle_response_cls": SetBacklightPWMDutyCycleResponse,
                    "set_display_rgb_value_cls": SetDisplayRGBValue,
                    "set_display_rgb_value_response_cls": SetDisplayRGBValueResponse,
                    "set_display_power_state_cls": SetDisplayPowerState,
                    "set_display_power_state_response_cls": SetDisplayPowerStateResponse,
                    "set_key_icon_cls": SetKeyIcon,
                    "set_key_icon_response_cls": SetKeyIconResponse,
                    "set_key_calibration_offset_cls": SetKeyCalibrationOffset,
                    "set_key_calibration_offset_response_cls": SetKeyCalibrationOffsetResponse,
                    "set_key_calibration_offset_in_flash_cls": SetKeyCalibrationOffsetInFlash,
                    "set_key_calibration_offset_in_flash_response_cls": SetKeyCalibrationOffsetInFlashResponse,
                    "set_display_ageing_mode_state_cls": SetDisplayAgeingModeState,
                    "set_display_ageing_mode_state_response_cls": SetDisplayAgeingModeStateResponse,
                    "key_press_event_cls": KeyPressEvent,
                },
                "max_function_index": 7
            },
        }
        cls.max_version = 0
    # end def setUpClass

    def test_factory(self):
        """
        Test ``TestKeysDisplayFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(TestKeysDisplayFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``TestKeysDisplayFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                TestKeysDisplayFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``TestKeysDisplayFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = TestKeysDisplayFactory.create(version)
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
            obj = TestKeysDisplayFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class TestKeysDisplayTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
